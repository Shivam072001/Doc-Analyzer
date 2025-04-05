from flask import Flask, request, jsonify
from ..core.models.ai_models import DocumentClassifier
from ..core.enums import AvailableModels  # Import the enum

app = Flask(__name__)
document_classifier_instance = None

def init_app(api_bp):
    @app.route('/set_model', methods=['POST'])
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

    @app.route('/classify', methods=['POST'])
    def classify_document():
        if document_classifier_instance is None:
            return jsonify({"error": "No model has been set. Please call /set_model first."}), 400

        data = request.get_json()
        if not data or 'document_text' not in data:
            return jsonify({"error": "Missing 'document_text' in request body"}), 400

        document_text = data['document_text']
        prediction = document_classifier_instance.predict(document_text)

        if prediction:
            return jsonify(prediction), 200
        else:
            return jsonify({"message": "Could not classify the document or an error occurred."}), 200

    @app.route('/available_models', methods=['GET'])
    def get_available_models():
        """
        Returns a list of predefined Hugging Face models from the enum.
        """
        models = [model.to_dict() for model in AvailableModels]
        return jsonify({"models": models}), 200

    if __name__ == '__main__':
        app.run(debug=True)