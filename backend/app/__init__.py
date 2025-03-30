from flask import Flask
from flask_cors import CORS
from .api import api_bp
from .config.config import Config
import logging
from .utils.logging_config import setup_logging

def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(Config.get_config(environment))

    setup_logging(app)
    logging.info(f"Application started in {environment} environment.")

    CORS(app)  # Enable CORS for all routes

    app.register_blueprint(api_bp, url_prefix='/api')

    return app