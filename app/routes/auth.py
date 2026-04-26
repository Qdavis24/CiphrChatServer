from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import User, db
from .helpers import make_token

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"message": "username, password, and public_key are required"}), 400

    try:
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username already taken"}), 409
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"message": "Failed to create account, please try again"}), 500

    return jsonify({"message": "Registration successful", "token": make_token(user)}), 200


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"message": "username and password are required"}), 400

    try:
        user = User.query.filter_by(username=username).first()
    except SQLAlchemyError:
        return jsonify({"message": "An error occurred, please try again"}), 500

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful", "token": make_token(user)}), 200
