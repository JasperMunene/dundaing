from . import db
from sqlalchemy_serializer import SerializerMixin


class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    organizer_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))
    capacity = db.Column(db.Integer)
    status = db.Column(db.String(20), default='draft')  # e.g., draft, published, canceled
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationship to event images
    images = db.relationship(
        'EventImage',
        backref='event',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )