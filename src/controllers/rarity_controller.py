from flask import Blueprint, request
from init import db
from models.rarity import Rarity, RaritySchema
from flask_jwt_extended import jwt_required
from utils import auth_as_admin_decorator

rarity_blueprint = Blueprint('rarity', __name__, url_prefix='/rarities')

# Get all rarities
@rarity_blueprint.route('/', methods=['GET'])
def get_all_rarities():
    rarities = Rarity.query.all()
    rarity_schema = RaritySchema(many=True)
    return rarity_schema.dump(rarities), 200

# Get a specific rarity by ID
@rarity_blueprint.route('/<int:id>', methods=['GET'])
def get_rarity(id):
    rarity = Rarity.query.get_or_404(id)
    rarity_schema = RaritySchema()
    return rarity_schema.dump(rarity), 200

# Add a new rarity (Admin access required)
@rarity_blueprint.route('/', methods=['POST'])
@jwt_required()
@auth_as_admin_decorator
def add_rarity():
    data = request.get_json()
    new_rarity = Rarity(rarity_name=data['rarity_name'])
    db.session.add(new_rarity)
    db.session.commit()
    return {"message": "Rarity added successfully"}, 201

# Delete a rarity by ID (Admin access required)
@rarity_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@auth_as_admin_decorator
def delete_rarity(id):
    rarity = Rarity.query.get_or_404(id)
    db.session.delete(rarity)
    db.session.commit()
    return {"message": "Rarity deleted successfully"}, 200