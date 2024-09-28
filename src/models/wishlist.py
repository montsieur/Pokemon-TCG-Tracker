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
        return f'<Wishlist {self.id}>'


class WishlistSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude=["wishlists"])
    card = fields.Nested('CardSchema', exclude=["wishlist_entries"])

    class Meta:
        fields = ("id", "user_id", "card_id", "card")
