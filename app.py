from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from datetime import datetime, timezone
import re
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import secrets
import os
from flask_jwt_extended import get_jwt
from flask_cors import CORS
from flask_migrate import Migrate
from connect_db import connect_db 
from dotenv import load_dotenv

load_dotenv()


# Create a Flask application instance
app = Flask(__name__)



@app.route('/')
def home():
    return jsonify({"message": "Welcome to Study Smarter API!"})

# Configure CORS to allow specified source access
CORS(app, resources={r"/*": {"origins": "https://your-frontend-url.com"}})


# Load database configuration from config.py
app.config.from_object(Config)
print(app.config['SQLALCHEMY_DATABASE_URI'])
# Ensure to include a secure JWT Secret Key
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))  # Generates a secure random secret key

# Initialize SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-JWT-Extended
jwt = JWTManager(app)

# Define User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now(timezone.utc))

    study_rooms = db.relationship('StudyRoom', backref='creator', lazy=True)
    posts = db.relationship('Post', backref='creator', lazy=True)
    comments = db.relationship('Comment', backref='creator', lazy=True)

    # Explicitly define __init__ to prevent Pylance errors
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

# Define StudyRoom model
class StudyRoom(db.Model):
    __tablename__ = 'study_rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    capacity = db.Column(db.Integer, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now(timezone.utc))

    posts = db.relationship('Post', backref='study_room', lazy=True)


    # Explicitly define __init__ to prevent Pylance errors
    def __init__(self, name, description, capacity, creator_id):
        self.name = name
        self.description = description
        self.capacity = capacity
        self.creator_id = creator_id


# Define Post model
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('study_rooms.id'), nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now(timezone.utc))

    comments = db.relationship('Comment', backref='post', lazy=True)
    media = db.relationship('Media', backref='post', lazy=True)

   
    def __init__(self, content, creator_id, room_id=None):
        self.content = content
        self.creator_id = creator_id
        self.room_id = room_id

# Define Comment model
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now(timezone.utc))

    
    def __init__(self, post_id, creator_id, content):
        self.post_id = post_id
        self.creator_id = creator_id
        self.content = content





# Define Media model
class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # e.g., 'photo' or 'video'
    file_path = db.Column(db.String(255), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now(timezone.utc))

    # Explicitly define __init__ to avoid Pylance errors
    def __init__(self, type, file_path, post_id=None):
        self.type = type
        self.file_path = file_path
        self.post_id = post_id




# Route to test database connection
@app.route('/test_db')
def test_db():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users') 
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows), 200
    else:
        return jsonify({"message": "Failed to connect to the database"}), 500





@app.route('/signup', methods=['POST'])
def signup():
    try:  # Error handling block
        data = request.json

        # Request validation: Check for required fields
        if not data or not all(key in data for key in ['username', 'email', 'password']):
            return jsonify({'message': 'Missing username, email, or password'}), 400

        # Input sanitization: Strip any spaces and validate formats
        username = data['username'].strip()
        email = data['email'].strip()
        password = data['password'].strip()

        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first() # type: ignore
        if existing_user:
            return jsonify({'message': 'Username or Email already taken'}), 409  # HTTP 409: Conflict

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({'message': 'Invalid email format'}), 400

        # Validate password length
        if len(password) < 8:
            return jsonify({'message': 'Password must be at least 8 characters long'}), 400

        # Hash the password before saving
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Signup successful', 'user_id': new_user.id}), 201

    except Exception as e:
        db.session.rollback()  # Gracefully handle database errors
        return jsonify({'error': str(e), 'message': 'Failed to register user'}), 500


    
# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing credentials'}), 400
    
    try:
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=str(user.id))

            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Login failed'}), 500


# Get user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


# Update user information
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid or missing JSON data'}), 400

       
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()

        if not username and not email:
            return jsonify({'message': 'At least one field (username or email) must be provided'}), 400

        if username:
            user.username = username
        if email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                return jsonify({'message': 'Invalid email format'}), 400
            user.email = email

        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500



# Logout endpoint
# Store revoked tokens
revoked_tokens = set()

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        jti = get_jwt()['jti']  # Get the token's unique identifier (jti)
        revoked_tokens.add(jti)  # Store it in the revoked list
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]  # Extract token ID
    return jti in revoked_tokens  # Return True if the token is revoked


    
# Protected Route
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()  # Get user identity from token
    user = User.query.get(user_id)  # Fetch user details
    if user:
        return jsonify({"msg": "Access granted", "user": {"id": user.id, "username": user.username, "email": user.email}}), 200
    return jsonify({'message': 'User not found'}), 404


# Create a new study room
@app.route('/study_rooms', methods=['POST'])
def create_study_room():
    try:
        data = request.get_json()  # Use get_json() to safely get data
        if not data:
            return jsonify({'message': 'Invalid or missing JSON body'}), 400  # Error handling

        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        capacity = data.get('capacity')
        creator_id = data.get('creator_id')  # Ensure creator_id is included

        if not name or not capacity or not creator_id:
            return jsonify({'message': 'Name, capacity, and creator_id are required'}), 400

        new_room = StudyRoom(name=name, description=description, capacity=capacity, creator_id=creator_id)
        db.session.add(new_room)
        db.session.commit()

        return jsonify({'message': 'Study room created successfully', 'room_id': new_room.id}), 201

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


# Get a specific study room by ID
@app.route('/study_rooms/<int:id>', methods=['GET'])
def get_study_room(id):
    try:
        study_room = StudyRoom.query.get(id)
        if not study_room:
            return jsonify({'message': 'Study room not found'}), 404

        return jsonify({
            'id': study_room.id,
            'name': study_room.name,
            'description': study_room.description,
            'capacity': study_room.capacity,
            'creator_id': study_room.creator_id
        }), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


# Get all study rooms
@app.route('/study_rooms', methods=['GET'])
def get_study_rooms():
    try:
        rooms = StudyRoom.query.all()
        return jsonify([{'id': room.id, 'name': room.name, 'capacity': room.capacity} for room in rooms]), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500
    

# ---------------------------------
# Post Endpoints
# ---------------------------------

# Create a new post
@app.route('/posts', methods=['POST'])
def create_post():
    try:
     
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid or missing JSON data'}), 400

        content = data.get('content', '').strip()
        creator_id = data.get('creator_id')
        room_id = data.get('room_id')

        if not content or not creator_id:
            return jsonify({'message': 'Content and creator_id are required'}), 400

      
        new_post = Post(content=content, creator_id=creator_id, room_id=room_id)
        db.session.add(new_post)
        db.session.commit()

        return jsonify({'message': 'Post created successfully', 'post_id': new_post.id}), 201

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500



# Get all posts
@app.route('/posts', methods=['GET'])
def get_posts():
    try:
        posts = Post.query.all()
        return jsonify([{'id': post.id, 'content': post.content, 'creator_id': post.creator_id, 'room_id': post.room_id} for post in posts]), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


# Get post by ID
@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    try:
        post = Post.query.get(id)
        if not post:
            return jsonify({'message': 'Post not found'}), 404

        return jsonify({'id': post.id, 'content': post.content, 'creator_id': post.creator_id, 'room_id': post.room_id}), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


# Update post
@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    try:
        post = Post.query.get(id)
        if not post:
            return jsonify({'message': 'Post not found'}), 404

        # Use request.get_json() to prevent None.get() errors
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid or missing JSON data'}), 400

        # Ensure data is a dictionary before accessing keys
        post.content = data.get('content', post.content).strip()

        db.session.commit()
        return jsonify({'message': 'Post updated successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500



# Delete post
@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    try:
        post = Post.query.get(id)
        if not post:
            return jsonify({'message': 'Post not found'}), 404

        db.session.delete(post)
        db.session.commit()

        return jsonify({'message': 'Post deleted successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

# ---------------------------------
# Comment Endpoints
# ---------------------------------

# Add a comment to a post
@app.route('/comments', methods=['POST'])
def add_comment():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid or missing JSON data'}), 400
        
        post_id = data.get('post_id')
        creator_id = data.get('creator_id')
        content = data.get('content', '').strip()

        if not post_id or not creator_id or not content:
            return jsonify({'message': 'post_id, creator_id, and content are required'}), 400

        
        new_comment = Comment(post_id=post_id, creator_id=creator_id, content=content)
        db.session.add(new_comment)
        db.session.commit()  

        return jsonify({'message': 'Comment added successfully', 'comment_id': new_comment.id}), 201

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500



# Get all comments for a post
@app.route('/comments/<int:post_id>', methods=['GET'])
def get_comments(post_id):
    try:
        comments = Comment.query.filter_by(post_id=post_id).all()
        return jsonify([{'id': comment.id, 'post_id': comment.post_id, 'creator_id': comment.creator_id, 'content': comment.content} for comment in comments]), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


# Delete a comment
@app.route('/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    try:
        comment = Comment.query.get(id)
        if not comment:
            return jsonify({'message': 'Comment not found'}), 404

        db.session.delete(comment)
        db.session.commit()

        return jsonify({'message': 'Comment deleted successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

# ---------------------------------
# Media Endpoints
# ---------------------------------

# Upload media file
@app.route('/media', methods=['POST'])
def upload_media():
    try:
        # Use request.get_json() to prevent None.get() errors
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid or missing JSON data'}), 400

        file_type = data.get('type', '').strip()
        file_path = data.get('file_path', '').strip()
        post_id = data.get('post_id')

        if not file_type or not file_path:
            return jsonify({'message': 'type and file_path are required'}), 400

        new_media = Media(type=file_type, file_path=file_path, post_id=post_id)
        db.session.add(new_media)
        db.session.commit()

        return jsonify({'message': 'Media uploaded successfully', 'media_id': new_media.id}), 201

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500



# Get media details
@app.route('/media/<int:id>', methods=['GET'])
def get_media(id):
    try:
        media = Media.query.get(id)
        if not media:
            return jsonify({'message': 'Media not found'}), 404

        return jsonify({'id': media.id, 'type': media.type, 'file_path': media.file_path, 'post_id': media.post_id}), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500




# Run the Flask application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables exist before running
    # Use gunicorn for deployment
    app.run(debug=True, host='0.0.0.0', port=10000)