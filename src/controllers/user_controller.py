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
    user = User.query.get(id)
    if not user:
        return {"message": f"User with ID {id} does not exist."}, 404
    user_schema = UserSchema()
    return user_schema.dump(user), 200

# Update a user by ID
@user_blueprint.route('/<int:user_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return {"message": "User not found."}, 404

        # Allow only the user themselves or an admin to update the profile
        if current_user_id != user_id and not User.query.get(current_user_id).is_admin:
            return {"message": "You do not have permission to update this user."}, 403

        data = request.get_json()

        # Update user fields if provided
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            if User.query.filter_by(email=data['email']).first():
                return {"message": "Email already in use by another user."}, 409
            user.email = data['email']
        if 'password' in data:
            user.set_password(data['password'])

        db.session.commit()
        return {"message": "User updated successfully."}, 200

    except Exception as e:
        db.session.rollback()
        return {"message": f"An error occurred: {str(e)}"}, 500

# Grant admin access to a user (admin access only)
@user_blueprint.route('/<int:user_id>/grant-admin', methods=['PUT'])
@jwt_required()
@auth_as_admin_decorator
def grant_admin(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"message": "User not found."}, 404

    # Check if the user is already an admin
    if user.is_admin:
        return {"message": "User is already an admin."}, 400

    user.is_admin = True
    db.session.commit()

    return {"message": f"User {user.username} is now an admin."}, 200

# Remove admin access from a user (admin access only)
@user_blueprint.route('/<int:user_id>/remove-admin', methods=['PUT'])
@jwt_required()
@auth_as_admin_decorator
def remove_admin(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"message": "User not found."}, 404

    # Check if the user is already not an admin
    if not user.is_admin:
        return {"message": f"User {user.username} is not an admin."}, 400

    user.is_admin = False
    db.session.commit()

    return {"message": f"Admin access removed from user {user.username}."}, 200

# Delete a user by ID
@user_blueprint.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return {"message": "User not found."}, 404

        # Allow only the user themselves or an admin to delete the profile
        if current_user_id != user_id and not User.query.get(current_user_id).is_admin:
            return {"message": "You do not have permission to delete this user."}, 403

        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully."}, 200

    except Exception as e:
        db.session.rollback()
        return {"message": f"An error occurred: {str(e)}"}, 500
