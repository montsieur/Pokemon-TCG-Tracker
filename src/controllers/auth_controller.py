from flask import Blueprint, request
from datetime import timedelta
from init import db, bcrypt
from models.user import User
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Validate required fields
        if not data or not username or not email or not password:
            return {"message": "Missing required fields."}, 400

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return {"message": "Email already registered."}, 409

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully."}, 201
    
    except IntegrityError as e:
        db.session.rollback()
        if e.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email or username already registered."}, 409
        return {"error": "An unexpected integrity error occurred."}, 500

@auth_blueprint.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Validate input
        if not email or not password:
            return {"error": "Email and password are required."}, 400

        # Retrieve user and check credentials
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200
        else:
            return {"error": "Invalid email or password."}, 401

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}, 500
