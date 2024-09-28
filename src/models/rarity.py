from src import db, ma

class Rarity(db.Model):
    __tablename__ = 'rarities'

    id = db.Column(db.Integer, primary_key=True)
    rarity_name = db.Column(db.String(50), unique=True, nullable=False)

    # Relationships
    cards = db.relationship("Card", back_populates="rarity")

    def __repr__(self):
        return f'<Rarity {self.rarity_name}>'

class RaritySchema(ma.Schema):
    class Meta:
        fields = ("id", "rarity_name")
