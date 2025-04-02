# app/controllers/media_controller.py
from flask import request, jsonify
from app.models import Media
from app import db
from app.models.post import Post  # Import Post model to validate post_id if provided

def upload_media():
    """
Endpoint for uploading media.
Expects JSON with 'type' and 'file_path'.
Optionally accepts 'post_id'.

Enhancements:
- Validates that 'type' and 'file_path' are not empty.
- Validates that 'type' is one of the allowed media types.
- Validates that 'post_id', if provided, is an integer and corresponds to an existing post.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        # Check required fields
        required_fields = ['type', 'file_path']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'message': 'Missing required fields',
                'required': required_fields,
                'missing': missing_fields
            }), 400

        # Validate and sanitize the media type and file path
        media_type = data.get('type', '').strip().lower()
        file_path = data.get('file_path', '').strip()

        if not media_type:
            return jsonify({'message': 'Media type cannot be empty'}), 400
        if not file_path:
            return jsonify({'message': 'File path cannot be empty'}), 400

        # Optionally check allowed media types
        allowed_types = ['image', 'video', 'audio']
        if media_type not in allowed_types:
            return jsonify({'message': f"Invalid media type. Allowed types: {', '.join(allowed_types)}"}), 400

        # Validate post_id if provided and verify that the post exists
        post_id = data.get('post_id')
        if post_id is not None:
            try:
                post_id = int(post_id)
            except (ValueError, TypeError):
                return jsonify({'message': 'Invalid post_id type. Must be an integer.'}), 400

            post = Post.query.get(post_id)
            if not post:
                return jsonify({'message': f"Post with id {post_id} not found."}), 404

        # Create and commit the new media entry
        new_media = Media(type=media_type, file_path=file_path, post_id=post_id)
        db.session.add(new_media)
        db.session.commit()

        return jsonify({
            'message': 'Media uploaded successfully',
            'media_id': new_media.media_id,
            'type': new_media.type,
            'file_path': new_media.file_path,
            'post_id': new_media.post_id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Media upload failed', 'error': str(e)}), 500
        