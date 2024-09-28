from init import db, ma
from marshmallow import fields

class Status(db.Model):
    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(50), unique=True, nullable=False)

    # Relationships
    trades = db.relationship('Trade', back_populates='status')

    def __repr__(self):
        return f'<CardStatus {self.status_name}>'

class StatusSchema(ma.Schema):
    id = fields.Int()
    status_name = fields.Str()

    class Meta:
        fields = ("id", "status_name")

# To handle a single Status object
status_schema = StatusSchema()

# To handle a list of Status objects
statuses_schema = StatusSchema(many=True)