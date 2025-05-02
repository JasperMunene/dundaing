from . import db
from sqlalchemy_serializer import SerializerMixin


class Ticket(db.Model, SerializerMixin):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Buyer
    ticket_type_id = db.Column(db.Integer, db.ForeignKey('ticket_types.id'), nullable=False)
    ticket_code = db.Column(db.String(64), unique=True, nullable=False)  # Unique QR code hash
    status = db.Column(db.String(20), default='valid')  # e.g., valid, used, refunded
    purchased_at = db.Column(db.DateTime, server_default=db.func.now())