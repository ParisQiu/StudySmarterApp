# app/models/media.py

from datetime import datetime
from app import db

class Media(db.Model):
    __tablename__ = 'media'

    media_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, type, file_path, post_id=None):
        self.type = type.strip()
        self.file_path = file_path.strip()
        self.post_id = post_id

    def __repr__(self):
        return f'<Media {self.media_id}>'
        