from src import db, ma
from marshmallow import fields

class Wishlist(db.Model):
    __tablename__ = 'wishlists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))

    # Relationships
    user = db.relationship('User', back_populates='wishlists')
    card = db.relationship('Card', back_populates='wishlist_entries')

    def __repr__(self):
        return f'<Wishlist id={self.id}>'


class WishlistSchema(ma.Schema):
    id = fields.Int()
    user_id = fields.Int()
    card_id = fields.Int()
    user = fields.Nested('UserSchema', exclude=["wishlists"])
    card = fields.Nested('CardSchema', exclude=["wishlist_entries"])

    class Meta:
        fields = ("id", "user_id", "card_id", "user", "card")

# To handle a single Wishlist object
wishlist_schema = WishlistSchema()

# To handle a list of Wishlist objects
wishlists_schema = WishlistSchema(many=True)