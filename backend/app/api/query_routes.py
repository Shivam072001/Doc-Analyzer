from flask import request, jsonify
from ..services.llm_service import LLMService
from ..services.vector_store_service import VectorStoreService
from ..services.prompt_service import PromptService
from ..services.stats_service import StatsService
from ..config.config import Config
from ..services.document_service import DocumentService
import logging

document_service = DocumentService(Config.PDF_DIR)
llm_service = LLMService(Config.OLLAMA_MODEL)
vector_store_service = VectorStoreService(Config.DB_FOLDER, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP, Config.SCORE_THRESHOLD, Config.SEARCH_K)
prompt_service = PromptService()
stats_service = StatsService()

def init_app(api_bp):
    @api_bp.route("/ai", methods=["POST"])
    def ask_ai():
        json_content = request.json
        query = json_content.get("query")

        if not query:
            return jsonify({"error": "No 'query' found in JSON request"}), 400

        try:
            response = llm_service.invoke(query)
            return jsonify({"answer": response})
        except Exception as e:
            logging.error(f"Error in /ai: {e}")
            return jsonify({"error": str(e)}), 500

    @api_bp.route("/ask_pdf", methods=["POST"])
    def ask_pdf():
        json_content = request.json
        query = json_content.get("query")
        prompt_type = json_content.get("promptType")

        if not query:
            return jsonify({"error": "No 'query' found in JSON request"}), 400

        prompt = prompt_service.get_prompt(prompt_type)
        if not prompt:
            return jsonify({"error": "Unknown prompt type"}), 400

        try:
            retrieval_result = vector_store_service.query_vector_store(query, prompt)
            answer = retrieval_result['answer']
            sources = stats_service.create_context_with_metadata(retrieval_result.get("context", []))

            stats_service.update_usage_counts(retrieval_result.get("context", []))
            pdf_usage = stats_service.get_pdf_usage_percentage()
            query_usage = stats_service.get_query_usage_percentage()
            stats_service.update_chat_history(query, answer)

            response_data = {
                "answer": answer if sources else f"No relevant documents found for the query: {query}. This answer is generated without any PDF context.",
                "sources": sources,
                "pdf_usage": pdf_usage,
                "query_usage": query_usage,
                "disclaimer": "This answer is not based on any available PDF documents." if not sources else None
            }
            return jsonify(response_data)
        except Exception as e:
            logging.error(f"Error in /ask_pdf: {e}")
            return jsonify({"error": str(e)}), 500

    @api_bp.route("/clear_chat_history", methods=["POST"])
    def clear_chat_history():
        stats_service.clear_chat_history()
        return jsonify({"status": "Chat history cleared successfully"})

    @api_bp.route("/clear_db", methods=["POST"])
    def clear_db():
        try:
            vector_store_service.clear_vector_store()
            document_service.clear_pdf_directory()
            return jsonify({"status": "Database and files cleared successfully"})
        except Exception as e:
            logging.error(f"Error clearing database: {e}")
            return jsonify({"error": str(e)}), 500