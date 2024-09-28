from flask import Blueprint, request
from init import db
from models.trading import Trade, TradingSchema
from models.user import User
from models.card import Card
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import auth_as_admin_decorator

trading_blueprint = Blueprint('trade', __name__, url_prefix='/trades')

# Get all trades (Admin access required)
@trading_blueprint.route('/', methods=['GET'])
@jwt_required()
@auth_as_admin_decorator
def get_all_trades():
    trades = Trade.query.all()
    trading_schema = TradingSchema(many=True)
    return trading_schema.dump(trades), 200

# Get details of a specific trade
@trading_blueprint.route('/<int:trade_id>', methods=['GET'])
@jwt_required()
def get_trade(trade_id):
    trade = Trade.query.get(trade_id)
    if not trade:
        return {"error": f"Trade with ID {trade_id} does not exist"}, 404

    trading_schema = TradingSchema()
    return trading_schema.dump(trade), 200

# Create a new trade offer
@trading_blueprint.route('/', methods=['POST'])
@jwt_required()
def create_trade():
    data = request.get_json()
    offering_user_id = get_jwt_identity()

    # Validate the receiving user
    receiving_user = User.query.get(data['receiving_userID'])
    if not receiving_user:
        return {"error": "Receiving user does not exist"}, 404

    # Validate the cards involved in the trade
    offering_card = Card.query.get(data['offering_cardID'])
    receiving_card = Card.query.get(data['receiving_cardID'])
    if not offering_card or not receiving_card:
        return {"error": "One or both cards involved in the trade do not exist"}, 404

    # Ensure quantities are valid
    if data['offering_quantity'] <= 0 or data['receiving_quantity'] <= 0:
        return {"error": "Quantities must be greater than zero"}, 400

    # Create the new trade offer
    new_trade = Trade(
        offering_user_id=offering_user_id,
        receiving_user_id=data['receiving_user_id'],
        offering_card_id=data['offering_card_id'],
        receiving_card_id=data['receiving_card_id'],
        offering_quantity=data['offering_quantity'],
        receiving_quantity=data['receiving_quantity'],
        statusID=data['statusID']
    )
    db.session.add(new_trade)
    db.session.commit()
    return {"message": "Trade created successfully"}, 201

# Update trade status (accept, decline)
@trading_blueprint.route('/<int:trade_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_trade_status(trade_id):
    user_id = get_jwt_identity()
    trade = Trade.query.get(trade_id)

    if not trade:
        return {"error": f"Trade with ID {trade_id} does not exist"}, 404

    # Only involved users or admin can update the trade status
    if user_id != trade.offering_userID and user_id != trade.receiving_userID:
        current_user = User.query.get(user_id)
        if not current_user or not current_user.is_admin:
            return {"error": "You do not have permission to update this trade"}, 403

    data = request.get_json()
    trade.statusID = data['statusID']
    db.session.commit()
    return {"message": "Trade status updated successfully"}, 200

# Delete a trade (Admin access required)
@trading_blueprint.route('/<int:trade_id>', methods=['DELETE'])
@jwt_required()
@auth_as_admin_decorator
def delete_trade(trade_id):
    trade = Trade.query.get(trade_id)

    if not trade:
        return {"error": f"Trade with ID {trade_id} does not exist"}, 404

    db.session.delete(trade)
    db.session.commit()
    return {"message": "Trade deleted successfully"}, 200
