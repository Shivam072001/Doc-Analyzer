import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '..', '..', 'data')
    DB_FOLDER = os.path.join(DATA_DIR, 'db')
    PDF_DIR = os.path.join(DATA_DIR, 'pdf')
    LOGS_DIR = os.path.join(BASE_DIR, '..', '..', 'logs')
    PDF_DIRECTORY = PDF_DIR  # For serving PDFs

    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3.1')
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 2048))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 100))
    SCORE_THRESHOLD = float(os.getenv('SCORE_THRESHOLD', 0.1))
    SEARCH_K = int(os.getenv('SEARCH_K', 20))
    
    MONGO_URI = os.getenv('MONGO_URI')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key') # Add a secret key

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