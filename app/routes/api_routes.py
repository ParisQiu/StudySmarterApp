# app/routes/api_routes.py
from flask import Blueprint
from app.controllers.auth_controller import signup, login_user, logout_user
from app.controllers.user_controller import get_users
from app.controllers.study_room_controller import create_study_room, get_study_room, get_all_study_rooms
from app.controllers.post_controller import create_post
from app.controllers.comment_controller import create_comment
from app.controllers.media_controller import upload_media

# Create a blueprint for all API routes
api_bp = Blueprint('api', __name__)

# --------------------------
# Authentication Routes
# --------------------------
api_bp.route('/signup', methods=['POST'])(signup)
api_bp.route('/login', methods=['POST'])(login_user)
api_bp.route('/logout', methods=['POST'])(logout_user)

# --------------------------
# User Routes
# --------------------------
api_bp.route('/users', methods=['GET'])(get_users)

# --------------------------
# Study Room Routes
# --------------------------
api_bp.route('/study_rooms', methods=['POST'])(create_study_room)
api_bp.route('/study_rooms', methods=['GET'])(get_all_study_rooms)
api_bp.route('/study_rooms/<int:id>', methods=['GET'])(get_study_room)

# --------------------------
# Post Routes
# --------------------------
api_bp.route('/posts', methods=['POST'])(create_post)

# --------------------------
# Comment Routes
# --------------------------
api_bp.route('/comments', methods=['POST'])(create_comment)

# --------------------------
# Media Routes
# --------------------------
api_bp.route('/media', methods=['POST'])(upload_media)
