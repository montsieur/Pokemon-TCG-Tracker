from flask import Blueprint, request
from init import db
from models.card import Card, CardSchema
from flask_jwt_extended import jwt_required
from utils import auth_as_admin_decorator

card_blueprint = Blueprint('card', __name__, url_prefix='/cards')

# Get all cards
@card_blueprint.route('/', methods=['GET'])
def get_all_cards():
    cards = Card.query.all()
    card_schema = CardSchema(many=True)
    return card_schema.dump(cards), 200

# Get a specific card by ID
@card_blueprint.route('/<int:card_id>', methods=['GET'])
def get_card(card_id):
    card = Card.query.get_or_404(card_id)
    card_schema = CardSchema()
    return card_schema.dump(card), 200

# Add a new card (Admin access required)
@card_blueprint.route('/', methods=['POST'])
@jwt_required()
@auth_as_admin_decorator
def add_card():
    data = request.get_json()
    new_card = Card(
        name=data['name'],
        type=data['type'],
        rarityID=data['rarityID'],
        setID=data['setID']
    )
    db.session.add(new_card)
    db.session.commit()
    return {"message": "Card added successfully"}, 201

# Update card details (Admin access required)
@card_blueprint.route('/<int:card_id>', methods=['PUT', 'PATCH'])
@jwt_required()
@auth_as_admin_decorator
def update_card(card_id):
    card = Card.query.get_or_404(card_id)
    data = request.get_json()

    # Update card fields if provided
    card.name = data.get('name', card.name)
    card.type = data.get('type', card.type)
    card.rarityID = data.get('rarityID', card.rarityID)
    card.setID = data.get('setID', card.setID)

    db.session.commit()
    card_schema = CardSchema()
    return {
        "message": f"Card '{card.name}' updated successfully",
        "card": card_schema.dump(card)
    }, 200

# Delete a card by ID (Admin access required)
@card_blueprint.route('/<int:card_id>', methods=['DELETE'])
@jwt_required()
@auth_as_admin_decorator
def delete_card(card_id):
    card = Card.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()
    return {"message": "Card deleted successfully"}, 200
