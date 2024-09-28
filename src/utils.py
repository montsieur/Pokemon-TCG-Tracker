from flask_jwt_extended import get_jwt_identity
import functools
from init import db
from models.user import User

def auth_as_admin_decorator(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        # Get the user's id from get_jwt_identity
        user_id = get_jwt_identity()
        if user_id is None:
            return {"error": "Authentication required"}, 401

        # Fetch the user from the db
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)

        # Check if user is admin
        if user and user.is_admin:
            # Allow the decorator function to execute
            return fn(*args, **kwargs)
        else:
            # Return error for unauthorized access
            return {"error": "Only admin can perform this action"}, 403

    return wrapper
