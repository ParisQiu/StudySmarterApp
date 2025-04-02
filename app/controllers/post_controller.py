# app/controllers/post_controller.py
from flask import request, jsonify
from app.models import Post
from app import db
from app.models.user import User
from app.models.study_room import StudyRoom  # Import StudyRoom to validate room existence

def create_post():
    """
    Endpoint for creating a new post.
Expects JSON with 'content' and 'creator_id'.
Optionally accepts 'room_id'. If provided, the study room must exist.

Enhancements:
- Validates that 'content' is not empty.
- Checks that 'creator_id' is an integer and that the user exists.
- Checks that 'room_id' is an integer (if provided) and that the study room exists.
- Returns detailed error messages.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Request data cannot be empty'}), 400

        # Check required fields
        required_fields = ['content', 'creator_id']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'message': 'Missing required fields',
                'required': required_fields,
                'missing': missing_fields
            }), 400

        # Validate and sanitize 'content'
        content = data.get('content', '').strip()
        if not content:
            return jsonify({'message': 'Content cannot be empty'}), 400

        # Validate creator_id
        try:
            creator_id = int(data.get('creator_id'))
        except (ValueError, TypeError):
            return jsonify({
                'message': 'Invalid creator_id. It must be an integer.'
            }), 400

        # Verify that the creator exists
        user = User.query.get(creator_id)
        if not user:
            return jsonify({'message': 'Creator (user) not found'}), 404

        # Validate room_id if provided and ensure the study room exists
        room_id = None
        if 'room_id' in data and data['room_id'] is not None:
            try:
                room_id = int(data.get('room_id'))
            except (ValueError, TypeError):
                return jsonify({
                    'message': 'Invalid room_id. It must be an integer if provided.'
                }), 400

            study_room = StudyRoom.query.get(room_id)
            if not study_room:
                return jsonify({'message': f'Study room with id {room_id} not found.'}), 404

        # Create and commit the new post
        new_post = Post(content=content, creator_id=creator_id, room_id=room_id)
        db.session.add(new_post)
        db.session.commit()

        return jsonify({
            'message': 'Post created successfully',
            'post_id': new_post.post_id,
            'content': new_post.content,
            'creator_id': new_post.creator_id,
            'room_id': new_post.room_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Failed to create post',
            'error': str(e)
        }), 500
        