from flask import request, jsonify, send_from_directory
from ..services.document_service import DocumentService
from ..services.vector_store_service import VectorStoreService
from ..config.config import Config
import logging

document_service = DocumentService(
    {
        "pdf": Config.PDF_DIR,
        "docx": Config.DOCX_DIR,
        "csv": Config.CSV_DIR,
        "xlsx": Config.XLSX_DIR,
    }
)
vector_store_service = VectorStoreService(Config.DB_FOLDER, Config.CHUNK_SIZE, Config.CHUNK_OVERLAP)

def init_app(api_bp):
    @api_bp.route("/documentManagement")
    def document_management():
        try:
            pdf_files = document_service.list_documents("pdf")
            docx_files = document_service.list_documents("docx")
            csv_files = document_service.list_documents("csv")
            xlsx_files = document_service.list_documents("xlsx")
            document_count = vector_store_service.get_document_count()
            return jsonify({
                "pdf_count": len(pdf_files),
                "docx_count": len(docx_files),
                "csv_count": len(csv_files),
                "xlsx_count": len(xlsx_files),
                "doc_count": document_count,
            })
        except Exception as e:
            logging.error(f"Error in document_management: {e}")
            return jsonify({"error": str(e)}), 500

    @api_bp.route("/list_documents", methods=["GET"])
    def list_all_documents():
        try:
            document_details = document_service.list_document_details()
            return jsonify({
                "pdf_files": [d for d in document_details if d['type'] == 'pdf'],
                "docx_files": [d for d in document_details if d['type'] == 'docx'],
                "csv_files": [d for d in document_details if d['type'] == 'csv'],
                "xlsx_files": [d for d in document_details if d['type'] == 'xlsx'],
                "doc_files": [d for d in document_details if d['type'] == 'doc'], # Assuming you might have .doc files
            })
        except Exception as e:
            logging.error(f"Error listing document details: {e}")
            return jsonify({"error": str(e)}), 500

    @api_bp.route("/upload_document", methods=["POST"])
    def upload_document():
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request", "status": "failed"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file", "status": "failed"}), 400

        try:
            response = document_service.upload_document(file)
            vector_store_service.add_documents(response['chunks'], response['filename'])
            response["status"] = "success"
            return jsonify(response)
        except ValueError as ve:
            return jsonify({"error": str(ve), "status": "failed"}), 400
        except Exception as e:
            logging.error(f"Error uploading document: {e}")
            return jsonify({"error": str(e), "status": "failed"}), 500

    @api_bp.route("/delete_document", methods=["POST"])
    def delete_single_document():
        json_content = request.json
        file_name = json_content.get("file_name")
        file_type = json_content.get("file_type")

        if not file_name or not file_type:
            return jsonify({"error": "Both 'file_name' and 'file_type' are required in the JSON request"}), 400

        try:
            document_service.delete_document(file_name, file_type)
            vector_store_service.delete_documents_by_source(file_name)
            return jsonify({"status": "success"})
        except FileNotFoundError:
            return jsonify({"error": "File not found"}), 404
        except Exception as e:
            logging.error(f"Error deleting document: {e}")
            return jsonify({"error": str(e)}), 500

    @api_bp.route('/documents/<file_type>/<path:filename>')
    def serve_document(file_type, filename):
        file_dir = document_service.get_document_dir(file_type)
        if file_dir:
            return send_from_directory(file_dir, filename)
        else:
            return jsonify({"error": "Invalid file type"}), 400

    @api_bp.route("/delete_index_document", methods=["POST"])
    def delete_index_document():
        json_content = request.json
        doc_id = json_content.get("doc_id")

        if not doc_id:
            return jsonify({"error": "No 'doc_id' found in JSON request"}), 400

        try:
            vector_store_service.delete_document_by_id(doc_id)
            return jsonify({"status": "Document index deleted successfully"})
        except Exception as e:
            logging.error(f"Error deleting document index: {e}")
            return jsonify({"error": str(e)}), 500