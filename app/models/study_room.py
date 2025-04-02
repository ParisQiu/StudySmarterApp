# app/models/study_room.py

from datetime import datetime
from app import db

class StudyRoom(db.Model):
    __tablename__ = 'study_rooms'

    room_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    capacity = db.Column(db.Integer, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationship with posts in the study room
    posts = db.relationship('Post', backref='study_room', lazy=True)

    def __init__(self, name, capacity, creator_id, description=None):
        self.name = name
        self.capacity = capacity
        self.creator_id = creator_id
        self.description = description

    def __repr__(self):
        return f'<StudyRoom {self.name}>'
        