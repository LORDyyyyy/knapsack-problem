from flask import Flask
from web.routes import init_app


def create_app() -> Flask:
    app = Flask(__name__)
    init_app(app)

    return app


def start(port: int = 5000):
    app = create_app()
    app.run(debug=True, port=port)
