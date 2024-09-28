from flask import Blueprint, request
from init import db
from models.user_card import UserCard, UserCardSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import auth_as_admin_decorator

user_card_blueprint = Blueprint('user_card', __name__, url_prefix='/user-cards')

# Get all cards owned by the current user
@user_card_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_user_cards():
    user_id = get_jwt_identity()
    user_cards = UserCard.query.filter_by(user_id=user_id).all()
    user_card_schema = UserCardSchema(many=True)
    return user_card_schema.dump(user_cards), 200

# Get all cards owned by a specific user (Admin access required)
@user_card_blueprint.route('/<int:user_id>', methods=['GET'])
@jwt_required()
@auth_as_admin_decorator
def get_specific_user_cards(user_id):
    user_cards = UserCard.query.filter_by(user_id=user_id).all()
    user_card_schema = UserCardSchema(many=True)
    return user_card_schema.dump(user_cards), 200

# Add a new card to the user's collection
@user_card_blueprint.route('/', methods=['POST'])
@jwt_required()
def add_user_card():
    user_id = get_jwt_identity()
    data = request.get_json()

    new_user_card = UserCard(
        user_id=user_id,
        card_id=data['card_id'],
        condition_id=data['condition_id']
    )
    db.session.add(new_user_card)
    db.session.commit()
    return {"message": "Card added to user's collection successfully"}, 201

# Update a user's card details (Admin or the owner of the card)
@user_card_blueprint.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_user_card(id):
    user_id = get_jwt_identity()
    user_card = UserCard.query.get(id)

    if not user_card:
        return {"error": f"UserCard with ID {id} does not exist"}, 404

    # Only admin or the owner can update the card details
    if user_card.user_id != user_id:
        current_user = db.session.get(UserCard, user_id)
        if not current_user or not current_user.is_admin:
            return {"error": "You do not have permission to update this item"}, 403

    data = request.get_json()

    # Update the condition if provided
    if 'condition_id' in data:
        user_card.condition_id = data['condition_id']

    db.session.commit()
    user_card_schema = UserCardSchema()
    return {
        "message": "User card updated successfully",
        "user_card": user_card_schema.dump(user_card)
    }, 200

# Delete a card from the user's collection (Admin or the owner of the card)
@user_card_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user_card(id):
    user_id = get_jwt_identity()
    user_card = UserCard.query.get(id)

    if not user_card:
        return {"error": f"UserCard with ID {id} does not exist"}, 404

    # Only admin or the owner can delete the card
    if user_card.user_id != user_id:
        current_user = db.session.get(UserCard, user_id)
        if not current_user or not current_user.is_admin:
            return {"error": "You do not have permission to delete this item"}, 403

    db.session.delete(user_card)
    db.session.commit()
    return {"message": "User card deleted successfully"}, 200
