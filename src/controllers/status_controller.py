from flask import Blueprint, request
from init import db
from models.status import Status, StatusSchema
from flask_jwt_extended import jwt_required
from utils import auth_as_admin_decorator

status_blueprint = Blueprint('status', __name__, url_prefix='/statuses')

# Get all statuses
@status_blueprint.route('/', methods=['GET'])
def get_all_statuses():
    statuses = Status.query.all()
    status_schema = StatusSchema(many=True)
    return status_schema.dump(statuses), 200

# Get a specific status by ID
@status_blueprint.route('/<int:id>', methods=['GET'])
def get_status(id):
    status = Status.query.get(id)
    if not status:
        return {"error": f"Status with ID {id} does not exist"}, 404

    status_schema = StatusSchema()
    return status_schema.dump(status), 200

# Add a new status (Admin access required)
@status_blueprint.route('/', methods=['POST'])
@jwt_required()
@auth_as_admin_decorator
def add_status():
    data = request.get_json()

    # Check if status already exists
    existing_status = Status.query.filter_by(status_name=data['status_name']).first()
    if existing_status:
        return {"error": "Status with this name already exists"}, 400

    new_status = Status(status_name=data['status_name'])
    db.session.add(new_status)
    db.session.commit()
    return {"message": "Status added successfully"}, 201

# Delete a status (Admin access required)
@status_blueprint.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@auth_as_admin_decorator
def delete_status(id):
    status = Status.query.get(id)
    if not status:
        return {"error": f"Status with ID {id} does not exist"}, 404

    db.session.delete(status)
    db.session.commit()
    return {"message": "Status deleted successfully"}, 200
