from flask import Blueprint, request
from init import db
from models.wishlist import Wishlist, WishlistSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import auth_as_admin_decorator

wishlist_blueprint = Blueprint('wishlist', __name__, url_prefix='/wishlists')

# Get wishlists of all users (Admin access required)
@wishlist_blueprint.route('/', methods=['GET'])
@jwt_required()
@auth_as_admin_decorator
def get_all_wishlists():
    wishlists = Wishlist.query.all()
    wishlist_schema = WishlistSchema(many=True)
    return wishlist_schema.dump(wishlists), 200

# Get a specific user's wishlist
@wishlist_blueprint.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_wishlist(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        # Allow admin users to access any user's wishlist
        current_user = db.session.get(User, current_user_id)
        if not current_user or not current_user.is_admin:
            return {"error": "You do not have permission to view this wishlist"}, 403

    wishlists = Wishlist.query.filter_by(user_id=user_id).all()
    wishlist_schema = WishlistSchema(many=True)
    return wishlist_schema.dump(wishlists), 200

# Add a card to a user's wishlist
@wishlist_blueprint.route('/', methods=['POST'])
@jwt_required()
def add_to_wishlist():
    user_id = get_jwt_identity()
    data = request.get_json()

    new_wishlist_item = Wishlist(user_id=user_id, card_id=data['card_id'])
    db.session.add(new_wishlist_item)
    db.session.commit()
    return {"message": "Card added to wishlist"}, 201

# Remove a card from a wishlist by wishlist ID
@wishlist_blueprint.route('/<int:wishlist_id>', methods=['DELETE'])
@jwt_required()
def delete_wishlist_item(wishlist_id):
    user_id = get_jwt_identity()
    wishlist_item = Wishlist.query.get(wishlist_id)

    if not wishlist_item:
        return {"error": f"Wishlist item with ID {wishlist_id} does not exist"}, 404

    if wishlist_item.user_id != user_id:
        # Allow admin users to delete any user's wishlist item
        current_user = db.session.get(User, user_id)
        if not current_user or not current_user.is_admin:
            return {"error": "You do not have permission to delete this item"}, 403

    db.session.delete(wishlist_item)
    db.session.commit()
    return {"message": "Wishlist item deleted successfully"}, 200
