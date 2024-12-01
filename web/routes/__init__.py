from .index import index_bp
from .api import api_bp


def init_app(app):
    app.register_blueprint(index_bp)
    app.register_blueprint(api_bp)
