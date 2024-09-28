from init import db, ma
from marshmallow import fields

class UserCard(db.Model):
    __tablename__ = 'user_cards'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)
    condition_id = db.Column(db.Integer, db.ForeignKey('conditions.id'), nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="user_cards") # Link back to the User model
    card = db.relationship("Card", back_populates="user_cards")  # Link to the Card model
    condition = db.relationship("Condition", back_populates="user_cards")  # Link to the Condition model

    def __repr__(self):
        return f"<UserCard user_id={self.user_id}, card_id={self.card_id}, condition_id={self.condition_id}>"

class UserCardSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=("id", "username"))
    card = fields.Nested('CardSchema', only=("id", "name", "card_type"))
    condition = fields.Nested('ConditionSchema', only=("id", "condition_name"))

    class Meta:
        fields = ('id', 'user_id', 'card_id', 'condition_id', 'user', 'card')

# To handle a single UserCard object
user_card_schema = UserCardSchema()

# To handle a list of UserCard objects
user_cards_schema = UserCardSchema(many=True)