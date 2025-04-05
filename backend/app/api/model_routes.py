from flask import Flask, request, jsonify
from ..core.models.ai_models import DocumentClassifier
from ..core.enums import AvailableModels  # Import the enum

document_classifier_instance = None

def init_app(api_bp):
    def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
        """Splits text into chunks of a specified size."""
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i + chunk_size])
        return chunks

    @api_bp.route('/set_model', methods=['POST'])
    def set_model():
        global document_classifier_instance
        data = request.get_json()
        if not data or 'model_name' not in data:
            return jsonify({"error": "Missing 'model_name' in request body"}), 400

        model_name = data['model_name']
        try:
            document_classifier_instance = DocumentClassifier(model_name=model_name)
            return jsonify({"message": f"Model '{model_name}' set successfully"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @api_bp.route('/classify', methods=['POST'])
    def classify_document():
        if document_classifier_instance is None:
            return jsonify({"error": "No model has been set. Please call /set_model first."}), 400

        data = request.get_json()
        if not data or 'document_text' not in data:
            return jsonify({"error": "Missing 'document_text' in request body"}), 400

        document_text = data['document_text']
        chunk_size = 500  # You can configure this value
        chunks = chunk_text(document_text, chunk_size)
        all_predictions = []

        for chunk in chunks:
            prediction = document_classifier_instance.predict(chunk)
            if prediction:
                all_predictions.append(prediction)
            else:
                all_predictions.append({"error": "Could not classify this chunk or an error occurred."})

        return jsonify({"predictions": all_predictions}), 200

    @api_bp.route('/available_models', methods=['GET'])
    def get_available_models():
        """
        Returns a list of predefined Hugging Face models from the enum.
        """
        models = [model.to_dict() for model in AvailableModels]
        return jsonify({"models": models}), 200