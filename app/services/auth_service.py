# app/services/auth_service.py

from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta

def register_user(username: str, email: str, password: str) -> User:
    """
Registers a new user.

Steps:
1. Checks if a user with the given email already exists.
2. If not, hashes the password.
3. Creates a new User record and commits it to the database.

Args:
username (str): The desired username.
email (str): The user's email address.
password (str): The user's plain-text password.

Returns:
User: The newly created User object if registration is successful,
or None if a user with the email already exists.
    """
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create a new user
    new_user = User(username=username, email=email, password=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        raise e

def login_user_service(email: str, password: str) -> dict:
    """
Authenticates a user and generates a JWT token if the credentials are valid.

Steps:
1. Retrieves the user by email.
2. Verifies the provided password against the hashed password.
3. If authentication is successful, generates an access token.

Args:
email (str): The user's email address.
password (str): The user's plain-text password.

Returns:
dict: A dictionary containing the access token and user information,
or None if authentication fails.
    """
    # Retrieve the user from the database
    user = User.query.filter_by(email=email).first()
    if not user:
        return None

    # Verify the password
    if not check_password_hash(user.password, password):
        return None

    # Generate an access token with an expiration of 1 hour
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
    return {
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }
    