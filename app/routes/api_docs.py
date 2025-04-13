# app/routes/api_docs.py
from flask import Blueprint
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/docs'
API_URL = '/static/openapi.yaml'  # This should match where your file is served

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "StudySmarterApp API"}
)

docs_bp = Blueprint('docs', __name__)
docs_bp.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
