from src import db, ma
from marshmallow import fields

class Trade(db.Model):
    __tablename__ = 'trades'

    id = db.Column(db.Integer, primary_key=True)
    offering_userID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiving_userID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    offering_cardID = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)
    receiving_cardID = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)
    offering_quantity = db.Column(db.Integer, default=1)
    receiving_quantity = db.Column(db.Integer, default=1)
    statusID = db.Column(db.Integer, db.ForeignKey('statuses.id'))

    # Relationships
    offering_user = db.relationship('User', foreign_keys=[offering_userID], back_populates='trades_offered')
    receiving_user = db.relationship('User', foreign_keys=[receiving_userID], back_populates='trades_received')
    offering_card = db.relationship('Card', foreign_keys=[offering_cardID], back_populates='trades_offered')
    receiving_card = db.relationship('Card', foreign_keys=[receiving_cardID], back_populates='trades_received')
    status = db.relationship('Status', back_populates='trades')

    def __repr__(self):
        return f'<Trading {self.id}>'

class TradingSchema(ma.Schema):
    offering_user = fields.Nested('UserSchema', exclude=["trades_offered"])
    receiving_user = fields.Nested('UserSchema', exclude=["trades_received"])
    offering_card = fields.Nested('CardSchema')
    receiving_card = fields.Nested('CardSchema')
    status = fields.Nested('CardStatusSchema')

class Meta:
        fields = ("id", "offering_user", "receiving_user", "offering_card", "receiving_card", "offering_quantity", "receiving_quantity", "status")
