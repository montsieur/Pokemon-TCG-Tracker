from init import db, ma
from marshmallow import fields

class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    card_type = db.Column(db.String(100))
    rarity_id = db.Column(db.Integer, db.ForeignKey('rarities.id'))
    set_id = db.Column(db.Integer, db.ForeignKey('sets.id'))

    # Relationships
    user_cards = db.relationship('UserCard', back_populates='card')
    trades_offered = db.relationship('Trade', foreign_keys='Trade.offering_card_id', back_populates='offering_card')
    trades_received = db.relationship('Trade', foreign_keys='Trade.receiving_card_id', back_populates='receiving_card')
    rarity = db.relationship('Rarity', back_populates='cards')
    set = db.relationship('Set', back_populates='cards')

    def __repr__(self):
        return f'<Card {self.name}>'

class CardSchema(ma.Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    card_type = fields.Str()
    rarity = fields.Nested('RaritySchema')
    set = fields.Nested('SetSchema', only=("set_name", "release_date"))

    class Meta:
        fields = ("id", "name", "card_type", "rarity", "set")

# To handle a single Card object
card_schema = CardSchema()

# To handle a list of Card objects
cards_schema = CardSchema(many=True)