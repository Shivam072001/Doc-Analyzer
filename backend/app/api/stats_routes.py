from flask import jsonify
from ..services.prompt_service import PromptService
from ..services.stats_service import StatsService
import logging

prompt_service = PromptService()
stats_service = StatsService()

def init_app(api_bp):
    @api_bp.route('/prompts', methods=['GET'])
    def get_prompts():
        try:
            serializable_prompts = prompt_service.get_serializable_prompts()
            return jsonify(serializable_prompts)
        except Exception as e:
            logging.error(f"Error getting prompts: {e}")
            return jsonify({"error": str(e)}), 500

    @api_bp.route("/document_usage", methods=["GET"])
    def get_document_usage():
        try:
            pdf_influence = stats_service.get_document_usage_percentage()
            return jsonify({"document_usage": pdf_influence})
        except Exception as e:
            logging.error(f"Error getting PDF usage: {e}")
            return jsonify({"error": str(e)}), 500