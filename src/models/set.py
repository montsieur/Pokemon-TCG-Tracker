from init import db, ma
from marshmallow import fields

class Set(db.Model):
    __tablename__ = 'sets'

    id = db.Column(db.Integer, primary_key=True)
    set_name = db.Column(db.String(120), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    # Relationships
    cards = db.relationship("Card", back_populates="set")

    def __repr__(self):
        return f'<Set {self.set_name}>'

class SetSchema(ma.Schema):
    id = fields.Int()
    set_name = fields.Str()
    release_date = fields.Date()
    cards = fields.List(fields.Nested('CardSchema', only=("id", "name")))

    class Meta:
        fields = (
            "id", "set_name", "release_date", "cards"
        )

# To handle a single Set object
set_schema = SetSchema()

# To handle a list of Set objects
sets_schema = SetSchema(many=True)