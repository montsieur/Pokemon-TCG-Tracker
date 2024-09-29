from init import db, ma
from marshmallow import fields

from models.status import StatusSchema

class Trade(db.Model):
    __tablename__ = 'trades'

    id = db.Column(db.Integer, primary_key=True)
    offering_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiving_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    offering_card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)
    receiving_card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)
    offering_quantity = db.Column(db.Integer, default=1)
    receiving_quantity = db.Column(db.Integer, default=1)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'))

    # Relationships
    offering_user = db.relationship('User', foreign_keys=[offering_user_id], back_populates='trades_offered')
    receiving_user = db.relationship('User', foreign_keys=[receiving_user_id], back_populates='trades_received')
    offering_card = db.relationship('Card', foreign_keys=[offering_card_id], back_populates='trades_offered')
    receiving_card = db.relationship('Card', foreign_keys=[receiving_card_id], back_populates='trades_received')
    status = db.relationship('Status', back_populates='trades')

    def __repr__(self):
        return f'<Trade id={self.id}>'

class TradingSchema(ma.Schema):
    id = fields.Int()
    offering_quantity = fields.Int()
    receiving_quantity = fields.Int()
    status = fields.Nested('StatusSchema', only=("id", "status_name"))
    
    # Nested relationships to get more details for offering and receiving users/cards
    offering_user = fields.Nested('UserSchema', only=("id", "username"))
    receiving_user = fields.Nested('UserSchema', only=("id", "username"))
    offering_card = fields.Nested('CardSchema', only=("id", "name", "card_type"))
    receiving_card = fields.Nested('CardSchema', only=("id", "name", "card_type"))

    class Meta:
        fields = (
            "id", "offering_user", "receiving_user", "offering_card", 
            "receiving_card", "offering_quantity", "receiving_quantity", "status"
        )

# To handle a single Trade object
trade_schema = TradingSchema()

# To handle a list of Trade objects
trades_schema = TradingSchema(many=True)
