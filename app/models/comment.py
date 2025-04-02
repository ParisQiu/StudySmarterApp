# app/models/comment.py

from datetime import datetime
from app import db

class Comment(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, post_id, creator_id, content):
        self.post_id = post_id
        self.creator_id = creator_id
        self.content = content.strip()  # Remove extra whitespace

    def __repr__(self):
        return f'<Comment {self.comment_id}>'
        