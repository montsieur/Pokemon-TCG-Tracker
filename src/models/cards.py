from src import db, ma
from marshmallow import fields

class Card(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100))
    rarityID = db.Column(db.Integer, db.ForeignKey('rarities.id'))
    setID = db.Column(db.Integer, db.ForeignKey('sets.id'))

    # Relationships
    user_cards = db.relationship('UserCard', back_populates='card')
    wishlist_entries = db.relationship('Wishlist', back_populates='card')
    trades_offered = db.relationship('Trade', foreign_keys='Trade.offering_cardID', back_populates='offering_card')
    trades_received = db.relationship('Trade', foreign_keys='Trade.receiving_cardID', back_populates='receiving_card')
    rarity = db.relationship('Rarity', back_populates='cards')
    set = db.relationship('Set', back_populates='cards')

    def __repr__(self):
        return f'<Card {self.name}>'

class CardSchema(ma.Schema):
    rarity = fields.Nested('RaritySchema')
    status = fields.Nested('CardStatusSchema')

    class Meta:
        fields = ("id", "name", "rarity", "status")