# app/models/post.py

from datetime import datetime
from app import db

class Post(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('study_rooms.room_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    comments = db.relationship('Comment', backref='post', lazy=True)
    media = db.relationship('Media', backref='post', lazy=True)

    def __init__(self, content, creator_id, room_id=None):
        self.content = content
        self.creator_id = creator_id
        self.room_id = room_id

    def __repr__(self):
        return f'<Post {self.post_id}>'
        