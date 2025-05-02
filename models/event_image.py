from . import db
from sqlalchemy_serializer import SerializerMixin


class EventImage(db.Model, SerializerMixin):
    __tablename__ = 'event_images'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(
        db.Integer,
        db.ForeignKey('events.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    url = db.Column(db.String(255), nullable=False, comment='Image URL')
    is_primary = db.Column(db.Boolean, default=False, nullable=False, comment='Flag the primary image')
    uploaded_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)