# app/controllers/comment_controller.py
from flask import request, jsonify
from app.models import Comment, Post
from app import db

def create_comment():
    """
    Endpoint for creating a comment.
    Expects JSON with 'post_id', 'creator_id', and 'content'.

Enhancements:
- Validates that required fields are present.
- Ensures that 'post_id' and 'creator_id' are integers.
- Ensures that 'content' is a non-empty string.
- Checks that the referenced post exists.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        # Check for required fields
        required_fields = ['post_id', 'creator_id', 'content']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'message': 'Missing required fields',
                'required': required_fields,
                'missing': missing_fields
            }), 400

        # Validate and sanitize input values
        try:
            post_id = int(data['post_id'])
            creator_id = int(data['creator_id'])
            content = str(data['content']).strip()
        except (ValueError, TypeError) as e:
            return jsonify({
                'message': 'Invalid field types',
                'error': str(e),
                'expected': {
                    'post_id': 'integer',
                    'creator_id': 'integer',
                    'content': 'string'
                }
            }), 400

        if not content:
            return jsonify({'message': 'Comment content cannot be empty'}), 400

        # Verify that the referenced post exists
        post = Post.query.get(post_id)
        if not post:
            return jsonify({'message': f"Post with id {post_id} not found."}), 404

        # Create and commit the new comment
        new_comment = Comment(post_id=post_id, creator_id=creator_id, content=content)
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({
            'message': 'Comment created successfully',
            'comment_id': new_comment.comment_id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Failed to create comment',
            'error': str(e)
        }), 500
        