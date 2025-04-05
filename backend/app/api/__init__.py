from flask import Blueprint
from . import document_routes, query_routes, stats_routes, auth_routes, model_routes

api_bp = Blueprint('api', __name__, url_prefix='/api')

document_routes.init_app(api_bp)
query_routes.init_app(api_bp)
stats_routes.init_app(api_bp)
model_routes.init_app(api_bp)

auth_bp = Blueprint('auth_api', __name__, url_prefix='/auth') # You can keep the original auth_bp registration

auth_routes.init_app(auth_bp)
api_bp.register_blueprint(auth_bp)
