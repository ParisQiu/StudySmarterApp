# app/controllers/auth_controller.py
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, create_access_token
from app import db
from app.services.auth_service import register_user, login_user_service
from app.models.user import User  # To check if a user already exists

def signup():
    """
    Endpoint for user registration.
    Expects JSON with 'username', 'email', and 'password'.
    If the email is already registered, returns "User already registered".
    On successful registration, returns a JWT token along with the user's ID.
    """
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ['username', 'email', 'password']):
            return jsonify({'message': 'Missing required fields'}), 400

        # Clean input values
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        # Validate that the values are not empty after stripping
        if not username or not email or not password:
            return jsonify({'message': 'Empty values are not allowed'}), 400

        # Check if a user with the provided email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'User already registered'}), 409

        # Create the new user using the service function
        new_user = register_user(username, email, password)
        if new_user:
            # Generate JWT token for the new user, ensuring identity is a string
            token = create_access_token(identity=str(new_user.id))
            return jsonify({
                'message': 'User registered successfully',
                'id': new_user.id,
                'access_token': token
            }), 201
        else:
            return jsonify({'message': 'User registration failed'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 500

def login_user():
    """
    Endpoint for user login.
    Expects JSON with 'email' and 'password'.
    On successful login, returns a JWT token and user information.
    """
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ['email', 'password']):
            return jsonify({'message': 'Missing credentials'}), 400

        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        # Ensure that credentials are not empty
        if not email or not password:
            return jsonify({'message': 'Email and password cannot be empty'}), 400

        result = login_user_service(email, password)
        if result:
            # Ensure identity is a string when creating the access token
            token = create_access_token(identity=str(result.get('id')))
            result['access_token'] = token
            return jsonify(result), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'message': 'Login failed', 'error': str(e)}), 500

@jwt_required()
def logout_user():
    """
    Endpoint for logging out the user.
    Revokes the JWT token by adding its unique identifier (jti) to a revocation list.
    """
    try:
        # Import the global revoked_tokens set defined in app/__init__.py
        from app import revoked_tokens
        token_data = get_jwt()
        if not token_data or 'jti' not in token_data:
            return jsonify({'message': 'Invalid token data'}), 400
        jti = token_data['jti']
        revoked_tokens.add(jti)
        return jsonify({'message': 'Successfully logged out'}), 200
    except Exception as e:
        return jsonify({'message': 'Logout failed', 'error': str(e)}), 500