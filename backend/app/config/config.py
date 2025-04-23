import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '..', '..', 'data')
    DB_FOLDER = os.path.join(DATA_DIR, 'db')
    PDF_DIR = os.path.join(DATA_DIR, 'pdf')
    DOCX_DIR = os.path.join(DATA_DIR, 'docx')
    CSV_DIR = os.path.join(DATA_DIR, 'csv')
    XLSX_DIR = os.path.join(DATA_DIR, 'xlsx')
    LOGS_DIR = os.path.join(BASE_DIR, '..', '..', 'logs')
    PDF_DIRECTORY = PDF_DIR  # For serving PDFs
    DOCX_DIR = DOCX_DIR
    CSV_DIR = CSV_DIR
    XLSX_DIR = XLSX_DIR

    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.1')
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 2048))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 100))
    SCORE_THRESHOLD = float(os.getenv('SCORE_THRESHOLD', 0.1))
    SEARCH_K = int(os.getenv('SEARCH_K', 20))
    
    MONGO_URI = os.getenv('MONGO_URI')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'DocParser')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key') # Add a secret key

    UPLOADTHING_TOKEN=os.getenv('UPLOADTHING_TOKEN')
    UPLOADTHING_URL=os.getenv('UPLOADTHING_URL', 'https://uploadthing.com/api/v6/uploadFiles')
    UPLOADTHING_MULTIPART_URL=os.getenv('UPLOADTHING_MULTIPART_URL', 'https://uploadthing.com/api/v6/completeMultipart')

    @staticmethod
    def get_config(environment):
        if environment == 'development':
            return DevelopmentConfig
        elif environment == 'testing':
            return TestingConfig
        elif environment == 'production':
            return ProductionConfig
        else:
            raise ValueError(f"Unknown environment: {environment}")

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    # Add specific testing configurations if needed

class ProductionConfig(Config):
    DEBUG = False
    # Add specific production configurations if needed