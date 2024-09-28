# src/models/set.py

from src import db, ma
from marshmallow import fields

class Set(db.Model):
    __tablename__ = 'sets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    # Relationships
    cards = db.relationship("Card", back_populates="set")

    def __repr__(self):
        return f'<Set {self.name}>'


class SetSchema(ma.Schema):
    cards = fields.List(fields.Nested('CardSchema'))

    class Meta:
        fields = ("id", "name", "release_date", "cards")
