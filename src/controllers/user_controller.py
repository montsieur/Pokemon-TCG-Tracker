from flask import Blueprint, jsonify, request
from init import db
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required
from utils import auth_as_admin_decorator


user_blueprint = Blueprint('user', __name__, url_prefix='/users')

@user_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return jsonify(user_schema.dump(users)), 200

@user_blueprint.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = User.query.get_or_404(id)
    user_schema = UserSchema()
    return jsonify(user_schema.dump(user)), 200

@user_blueprint.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@auth_as_admin_decorator
def update_user(id):
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404
    
    if user.id != get_jwt_identity() and not user.is_admin:
        return "Unauthorized", 401

    data = request.get_json()

    # Update user fields if provided
   
    user.username = data['username'] or user.username
    user.email = data['email'] or user.email
    user.is_admin = data['is_admin'] or user.is_admin

    db.session.commit()

    user_schema = UserSchema()
    profile = user_schema.dump(user)
    message = f"User {user.username} updated successfully."
    return {"message": message, "user": profile}, 200

@user_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@auth_as_admin_decorator
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200
