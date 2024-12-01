from flask import Blueprint, jsonify

api_bp = Blueprint("api", __name__)


@api_bp.route("/api")
def index():
    return jsonify({"message": "Hello, World!"})
