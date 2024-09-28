from src import db, ma

class Status(db.Model):
    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(50), unique=True, nullable=False)

    # Relationships
    trades = db.relationship('Trade', back_populates='status', lazy=True)

    def __repr__(self):
        return f'<CardStatus {self.status}>'


class CardStatusSchema(ma.Schema):
    class Meta:
        fields = ("id", "status")
