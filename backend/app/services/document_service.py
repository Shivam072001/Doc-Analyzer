import os
import shutil
import hashlib
from ..core.interfaces import DocumentServiceInterface
from ..core.models.document import Document
from ..utils.file_utils import file_exists, compute_file_hash, clear_directory
from ..utils.text_processing import preprocess_text
from langchain_community.document_loaders import PDFPlumberLoader
import logging
from ..config.config import Config

class DocumentService(DocumentServiceInterface):
    def __init__(self, pdf_dir):
        self.pdf_dir = pdf_dir
        os.makedirs(self.pdf_dir, exist_ok=True)

    def list_pdfs(self) -> list[str]:
        return [f for f in os.listdir(self.pdf_dir) if f.endswith('.pdf')]

    def upload_pdf(self, file) -> dict:
        file_name = file.filename
        save_file = os.path.join(self.pdf_dir, file_name)

        if file_exists(save_file):
            raise ValueError("File already exists.")

        try:
            file_hash = compute_file_hash(file)
        except Exception as e:
            raise Exception(f"Error computing file hash: {e}") from e

        existing_files = self.list_pdfs()
        for existing_file in existing_files:
            existing_file_path = os.path.join(self.pdf_dir, existing_file)
            try:
                if compute_file_hash(open(existing_file_path, 'rb')) == file_hash:
                    raise ValueError("File with identical content already exists.")
            except Exception as e:
                raise Exception(f"Error checking existing files: {e}") from e

        try:
            file.save(save_file)
        except Exception as e:
            raise Exception(f"Error saving file: {e}") from e

        try:
            loader = PDFPlumberLoader(save_file)
            docs = loader.load_and_split()
            is_structured = True
        except Exception as e:
            logging.warning(f"Error loading structured text: {e}")
            docs = []
            is_structured = False

        if not docs:
            try:
                logging.info("Performing OCR (placeholder)")
                # Replace this with actual OCR implementation if needed
                text = "OCR processed text from PDF"
                docs = [Document(page_content=preprocess_text(text), metadata={"source": file_name})]
                is_structured = False
            except Exception as e:
                raise Exception(f"Error during OCR processing: {e}") from e
        else:
            docs = [Document(page_content=preprocess_text(doc.page_content), metadata={"source": file_name}) for doc in docs]

        # Assuming vector store service handles chunking
        return {
            "filename": file_name,
            "doc_len": len(docs),
            "chunks": docs, # Pass the preprocessed documents for chunking in the vector store service
            "is_structured": is_structured
        }

    def delete_pdf(self, file_name: str) -> None:
        file_path = os.path.join(self.pdf_dir, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info(f"Successfully deleted file: {file_path}")
        else:
            logging.warning(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

    def clear_pdf_directory(self) -> None:
        clear_directory(self.pdf_dir)