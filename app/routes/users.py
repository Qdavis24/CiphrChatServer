from flask import Blueprint, jsonify

from .helpers import connected_users

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.get("/connected")
def get_connected_users():
    print(connected_users)
    return jsonify({"connected_users": list(connected_users.keys())}), 200
