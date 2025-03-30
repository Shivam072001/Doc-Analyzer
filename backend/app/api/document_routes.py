from flask import request, jsonify, send_from_directory, Blueprint
from ..services.document_service import DocumentService
from ..services.vector_store_service import VectorStoreService
from ..config.config import Config
import logging

document_service = DocumentService(Config.PDF_DIR)
vector_store_service = VectorStoreService(Config.DB_FOLDER, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP)

def init_app(api_bp):
    @api_bp.route("/pdfManagement")
    def pdf_management():
        try:
            pdf_files = document_service.list_pdfs()
            document_count = vector_store_service.get_document_count()
            return jsonify({"pdf_count": len(pdf_files), "doc_count": document_count})
        except Exception as e:
            logging.error(f"Error in pdf_management: {e}")
            return jsonify({"error": str(e)}), 500

    @api_bp.route("/list_pdfs", methods=["GET"])
    def list_pdfs():
        try:
            pdf_files = document_service.list_pdfs()
            return jsonify({"pdf_files": pdf_files})
        except Exception as e:
            logging.error(f"Error in list_pdfs: {e}")
            return jsonify({"error": str(e)}), 500

    @api_bp.route("/pdf", methods=["POST"])
    def upload_pdf():
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request", "status": "failed"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file", "status": "failed"}), 400

        try:
            response = document_service.upload_pdf(file)
            vector_store_service.add_documents(response['chunks'], response['filename'])
            response["status"] = "success"  # Add status to successful response
            return jsonify(response)
        except ValueError as ve:
            return jsonify({"error": str(ve), "status": "failed"}), 400
        except Exception as e:
            logging.error(f"Error uploading PDF: {e}")
            return jsonify({"error": str(e), "status": "failed"}), 500
        
    @api_bp.route("/list_documents", methods=["GET"])
    def list_documents():
        try:
            documents = vector_store_service.list_documents()
            return jsonify({"documents": documents}), 200
        except Exception as e:
            logging.error(f"Error listing documents: {e}")
            return jsonify({"error": "An error occurred while listing documents. Please try again later."}), 500

    @api_bp.route("/delete_pdf", methods=["POST"])
    def delete_pdf():
        json_content = request.json
        file_name = json_content.get("file_name")

        if not file_name:
            return jsonify({"error": "No 'file_name' found in JSON request"}), 400

        try:
            document_service.delete_pdf(file_name)
            vector_store_service.delete_documents_by_source(file_name)
            return jsonify({"status": "success"})
        except FileNotFoundError:
            return jsonify({"error": "File not found"}), 404
        except Exception as e:
            logging.error(f"Error deleting PDF: {e}")
            return jsonify({"error": str(e)}), 500

    @api_bp.route('/pdfs/<path:filename>')
    def serve_pdf(filename):
        return send_from_directory(Config.PDF_DIRECTORY, filename)

    @api_bp.route("/delete_document", methods=["POST"])
    def delete_document():
        json_content = request.json
        doc_id = json_content.get("doc_id")

        if not doc_id:
            return jsonify({"error": "No 'doc_id' found in JSON request"}), 400

        try:
            vector_store_service.delete_document_by_id(doc_id)
            return jsonify({"status": "Document deleted successfully"})
        except Exception as e:
            logging.error(f"Error deleting document: {e}")
            return jsonify({"error": str(e)}), 500