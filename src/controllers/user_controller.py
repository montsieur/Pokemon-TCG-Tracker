from flask import Blueprint, request
from init import db
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import auth_as_admin_decorator

user_blueprint = Blueprint('user', __name__, url_prefix='/users')

# Get all users (admin access only)
@user_blueprint.route('/', methods=['GET'])
@jwt_required()
@auth_as_admin_decorator
def get_all_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return user_schema.dump(users), 200

# Get a user by ID (admin access only)
@user_blueprint.route('/<int:id>', methods=['GET'])
@jwt_required()
@auth_as_admin_decorator
def get_user(id):
    user = User.query.get_or_404(id)
    user_schema = UserSchema()
    return user_schema.dump(users), 200

# Update a user by ID (admin access only)
@user_blueprint.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@auth_as_admin_decorator
def update_user(id):
    user = User.query.get_or_404(id)

    data = request.get_json()

    # Update user fields if provided
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.is_admin = data.get('is_admin', user.is_admin)

    db.session.commit()

    user_schema = UserSchema()
    profile = user_schema.dump(user)
    message = f"User {user.username} updated successfully."
    return {"message": message, "user": profile}, 200

# Delete a user by ID (admin access only)
@user_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@auth_as_admin_decorator
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted successfully."}, 200