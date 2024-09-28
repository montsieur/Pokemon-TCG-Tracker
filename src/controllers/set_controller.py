from flask import Blueprint, request
from init import db
from models.set import Set, SetSchema
from flask_jwt_extended import jwt_required
from utils import auth_as_admin_decorator
from datetime import datetime

set_blueprint = Blueprint('set', __name__, url_prefix='/sets')

# Get all sets
@set_blueprint.route('/', methods=['GET'])
def get_all_sets():
    sets = Set.query.all()
    set_schema = SetSchema(many=True)
    return set_schema.dump(sets), 200

# Get a specific set by ID
@set_blueprint.route('/<int:id>', methods=['GET'])
def get_set(id):
    set_ = Set.query.get(id)
    if not set_:
        return {"error": f"Set with ID {id} does not exist"}, 404
    set_schema = SetSchema()
    return set_schema.dump(set_), 200

# Add a new set (Admin access required)
@set_blueprint.route('/', methods=['POST'])
@jwt_required()
@auth_as_admin_decorator
def add_set():
    data = request.get_json()
    try:
        release_date = datetime.strptime(data['release_date'], '%Y-%m-%d').date()
    except ValueError:
        return {"error": "Invalid date format. Please use YYYY-MM-DD."}, 400
    
    new_set = Set(set_name=data['set_name'], release_date=release_date)
    db.session.add(new_set)
    db.session.commit()
    return {"message": "Set added successfully"}, 201

# Update set details (Admin access required)
@set_blueprint.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@auth_as_admin_decorator
def update_set(id):
    set_ = Set.query.get(id)
    if not set_:
        return {"error": f"Set with ID {id} does not exist"}, 404

    data = request.get_json()
    
    # Update set fields if provided
    if 'set_name' in data:
        set_.set_name = data['set_name']
    
    if 'release_date' in data:
        try:
            set_.release_date = datetime.strptime(data['release_date'], '%Y-%m-%d').date()
        except ValueError:
            return {"error": "Invalid date format. Please use YYYY-MM-DD."}, 400

    db.session.commit()
    set_schema = SetSchema()
    return {
        "message": f"Set '{set_.set_name}' updated successfully",
        "set": set_schema.dump(set_)
    }, 200

# Delete a set by ID (Admin access required)
@set_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@auth_as_admin_decorator
def delete_set(id):
    set_ = Set.query.get(id)
    if not set_:
        return {"error": f"Set with ID {id} does not exist"}, 404
    db.session.delete(set_)
    db.session.commit()
    return {"message": "Set deleted successfully"}, 200
