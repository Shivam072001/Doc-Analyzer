import pytest
import os
from app.services.document_service import DocumentService
from werkzeug.datastructures import FileStorage

# Assuming 'test_pdf.pdf' exists in the 'tests/data' directory
TEST_PDF_PATH = os.path.join(os.path.dirname(__file__), 'data', 'test_pdf.pdf')
TEST_PDF_CONTENT = b'This is a test PDF file.'

@pytest.fixture
def document_service(tmp_path):
    pdf_dir = tmp_path / "pdf_test_dir"
    pdf_dir.mkdir()
    return DocumentService(str(pdf_dir))

@pytest.fixture
def test_pdf_file():
    with open(TEST_PDF_PATH, 'wb') as f:
        f.write(TEST_PDF_CONTENT)
    with open(TEST_PDF_PATH, 'rb') as f:
        yield f
    os.remove(TEST_PDF_PATH)

def test_list_pdfs_empty(document_service):
    assert document_service.list_pdfs() == []

def test_upload_pdf(document_service, test_pdf_file):
    file = FileStorage(stream=test_pdf_file, filename='test_pdf.pdf', content_type='application/pdf')
    response = document_service.upload_pdf(file)
    assert response['filename'] == 'test_pdf.pdf'
    assert os.path.exists(os.path.join(document_service.pdf_dir, 'test_pdf.pdf'))
    assert len(document_service.list_pdfs()) == 1

def test_upload_existing_pdf(document_service, test_pdf_file):
    file = FileStorage(stream=test_pdf_file, filename='test_pdf.pdf', content_type='application/pdf')
    document_service.upload_pdf(file)
    with pytest.raises(ValueError, match="File already exists."):
        document_service.upload_pdf(file)

def test_delete_pdf(document_service, test_pdf_file):
    file = FileStorage(stream=test_pdf_file, filename='test_pdf.pdf', content_type='application/pdf')
    document_service.upload_pdf(file)
    document_service.delete_pdf('test_pdf.pdf')
    assert not os.path.exists(os.path.join(document_service.pdf_dir, 'test_pdf.pdf'))
    assert document_service.list_pdfs() == []

def test_delete_nonexistent_pdf(document_service):
    with pytest.raises(FileNotFoundError, match="File not found"):
        document_service.delete_pdf('nonexistent.pdf')

def test_clear_pdf_directory(document_service, test_pdf_file):
    file = FileStorage(stream=test_pdf_file, filename='test_pdf.pdf', content_type='application/pdf')
    document_service.upload_pdf(file)
    assert len(document_service.list_pdfs()) == 1
    document_service.clear_pdf_directory()
    assert len(document_service.list_pdfs()) == 0