from init import db, ma
from marshmallow import fields

class Rarity(db.Model):
    __tablename__ = 'rarities'

    id = db.Column(db.Integer, primary_key=True)
    rarity_name = db.Column(db.String(50), unique=True, nullable=False)

    # Relationships
    cards = db.relationship("Card", back_populates="rarity")

    def __repr__(self):
        return f'<Rarity {self.rarity_name}>'

class RaritySchema(ma.Schema):
    id = fields.Int()
    rarity_name = fields.Str()

    class Meta:
        fields = ("id", "rarity_name")

# To handle a single Rarity object
rarity_schema = RaritySchema()

# To handle a list of Rarity objects
rarities_schema = RaritySchema(many=True)
