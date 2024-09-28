from flask import Blueprint, request
from init import db
from models.condition import Condition, ConditionSchema
from flask_jwt_extended import jwt_required
from utils import auth_as_admin_decorator

condition_blueprint = Blueprint('condition', __name__, url_prefix='/conditions')

# Get all conditions
@condition_blueprint.route('/', methods=['GET'])
def get_all_conditions():
    conditions = Condition.query.all()
    condition_schema = ConditionSchema(many=True)
    return condition_schema.dump(conditions), 200

# Add a new condition (Admin access required)
@condition_blueprint.route('/', methods=['POST'])
@jwt_required()
@auth_as_admin_decorator
def add_condition():
    data = request.get_json()
    new_condition = Condition(condition_name=data['condition_name'])
    db.session.add(new_condition)
    db.session.commit()
    return {"message": "Condition added successfully"}, 201

# Delete a condition by ID (Admin access required)
@condition_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@auth_as_admin_decorator
def delete_condition(id):
    condition = Condition.query.get(id)
    if not condition:
        return {"error": f"Condition with ID {id} does not exist"}, 404

    db.session.delete(condition)
    db.session.commit()
    return {"message": "Condition deleted successfully"}, 200
