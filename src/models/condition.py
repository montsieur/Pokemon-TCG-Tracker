from src import db, ma

class Condition(db.Model):
    __tablename__ = 'conditions'

    id = db.Column(db.Integer, primary_key=True)
    condition_name = db.Column(db.String(50), unique=True, nullable=False)

    # Relationships
    user_cards = db.relationship('UserCard', back_populates='condition')

    def __repr__(self):
        return f"<Condition name={self.condition_name}>"

class ConditionSchema(ma.Schema):
    id = fields.Int()
    condition_name = fields.Str()
    
    class Meta:
        fields = ("id", "condition_name")

# To handle a single Condition object
condition_schema = ConditionSchema()

# To handle a list of Condition objects
conditions_schema = ConditionSchema(many=True)