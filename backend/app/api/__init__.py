from flask import Blueprint
from . import document_routes, query_routes, stats_routes

api_bp = Blueprint('api', __name__)

document_routes.init_app(api_bp)
query_routes.init_app(api_bp)
stats_routes.init_app(api_bp)