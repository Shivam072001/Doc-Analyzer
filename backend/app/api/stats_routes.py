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

    @api_bp.route("/pdf_usage", methods=["GET"])
    def get_pdf_usage():
        try:
            pdf_influence = stats_service.get_pdf_usage_percentage()
            return jsonify({"pdf_usage": pdf_influence})
        except Exception as e:
            logging.error(f"Error getting PDF usage: {e}")
            return jsonify({"error": str(e)}), 500