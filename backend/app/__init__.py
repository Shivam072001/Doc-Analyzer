from flask import Flask, g
from flask_cors import CORS
from .api import api_bp
from .api import auth_bp
from .config.config import Config
import logging
from .utils.logging_config import setup_logging
from pymongo import MongoClient

def get_db():
    if 'db' not in g:
        client = MongoClient(current_app.config['MONGO_URI'])
        g.db = client.get_default_database()  # Or specify your database name here
    return g.db

def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(Config.get_config(environment))

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})  # Configure CORS for /api/*

    setup_logging(app)
    logging.info(f"Application started in {environment} environment.")

    app.before_request(connect_db)
    app.teardown_request(close_db)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

def connect_db():
    g.db = get_db()

def close_db(error):
    if 'db' in g:
        # MongoClient objects are designed to be long-lived,
        # so we don't explicitly close the client here in a simple setup.
        pass

from flask import current_app