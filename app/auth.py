from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from .extensions import db
from .models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"message": "Username already exists."}), 400

    user = User(username=username)
    user.password = password

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully."}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"message": "Username and password are required."}, 400

    user = User.query.filter_by(username=username).first()

    if user is None or not user.authenticate(password):
        return {"message": "Invalid username or password."}, 401

    access_token = create_access_token(identity=str(user.id))

    return {
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username
        }
    }, 200
