from . import db
from sqlalchemy_serializer import SerializerMixin


class TicketType(db.Model, SerializerMixin):
    __tablename__ = 'ticket_types'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)
    sale_start = db.Column(db.DateTime)
    sale_end = db.Column(db.DateTime)