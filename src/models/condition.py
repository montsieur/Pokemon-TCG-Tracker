from src import db, ma

class Condition(db.Model):
    __tablename__ = 'conditions'

    id = db.Column(db.Integer, primary_key=True)
    condition_name = db.Column(db.String(50), unique=True, nullable=False)

    # Relationships
    user_cards = db.relationship('UserCard', back_populates='condition')

class ConditionSchema(ma.Schema):
    class Meta:
        fields = ("id", "condition_name")