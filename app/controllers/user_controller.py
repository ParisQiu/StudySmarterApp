# app/controllers/user_controller.py
from flask import jsonify
from app.models import User

def get_users():
    """
Endpoint to fetch all users.
Returns a list of users with their id, username, and email.
    """
    try:
        users = User.query.all()
        if not users:
            return jsonify({'message': 'No users found'}), 404

        users_data = [{
            'id': user.id,
            'username': user.username,
            'email': user.email
        } for user in users]

        return jsonify(users_data), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching users', 'error': str(e)}), 500
        