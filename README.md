# StudySmarter API

StudySmarter API is a RESTful backend built with Flask that serves as the core for a study-oriented application. It provides secure user authentication using JWT, and supports functionalities like managing study rooms, posts, comments, and media uploads. The project follows a modular MVC architecture to ensure clean separation of concerns and ease of maintenance.

## Features

- **User Authentication:**
  - User registration (signup)
  - User login with JWT token issuance
  - Token revocation (logout)

- **Study Rooms:**
  - Create and retrieve study rooms for collaborative study sessions

- **Posts & Comments:**
  - Users can create posts in study rooms
  - Users can comment on posts

- **Media Uploads:**
  - Upload media files associated with posts

## Folder Structure
```bash
/StudySmarterAPI
├── app
│   ├── __init__.py          # App factory & extension initialization
│   ├── config.py            # Application configuration (loads .env)
│   ├── models               # ORM models
│   │   ├── __init__.py      # Centralized model imports
│   │   ├── user.py          # User model
│   │   ├── study_room.py    # StudyRoom model
│   │   ├── post.py          # Post model
│   │   ├── comment.py       # Comment model
│   │   └── media.py         # Media model
│   ├── controllers          # Controllers for business logic
│   │   ├── __init__.py      # Package initialization for controllers
│   │   ├── auth_controller.py       # Signup, login, logout endpoints
│   │   ├── user_controller.py       # User-related endpoints
│   │   ├── study_room_controller.py # Study room endpoints
│   │   ├── post_controller.py       # Post endpoints
│   │   ├── comment_controller.py    # Comment endpoints
│   │   └── media_controller.py      # Media upload endpoints
│   ├── routes               # Registers API endpoints via blueprints
│   │   ├── __init__.py      # Package initialization for routes
│   │   └── api_routes.py    # Aggregated API endpoints from controllers
│   └── services             # Business logic and helper functions
│       └── auth_service.py  # Authentication related services
├── tests                    # Unit and integration tests
│   ├── __init__.py          # Package initialization for tests
│   ├── test_auth.py
│   ├── test_routes.py
│   └── test_db.py
├── generate_secret.py       # Utility for generating JWT secret keys
├── database.py              # Database initialization and migration commands
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── render.yaml              # Deployment configuration for Render
└── README.md                # Project overview and setup instructions
```


## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd StudySmarterAPI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a .env file in the project root with the following content (replace placeholder values with your actual configuration):

```bash
# Flask configuration
FLASK_DEBUG=True
SECRET_KEY=your_flask_secret_key_here

# Database configuration
DB_HOST=localhost
DB_NAME=studysmarter_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_PORT=5432

# Alternatively, you can set a full database URL:
# DATABASE_URL=postgresql://your_db_user:your_db_password@localhost/studysmarter_db

# JWT configuration
JWT_SECRET_KEY=your_jwt_secret_key_here

# Application port
PORT=5000

```

### 5. Initialize the Database
Make sure your PostgreSQL server is running and the database exists. Then run:

```bash
python run.py
```

## API Endpoints

Your API will be accessible at [http://localhost:5000](http://localhost:5000) (or the port specified in your `.env`).

The API endpoints are registered under the `/api` prefix:

### Authentication
- **POST /api/signup** – Register a new user.
- **POST /api/login** – Log in and receive a JWT token.
- **POST /api/logout** – Log out and revoke the JWT token.

### Users
- **GET /api/users** – Retrieve all users.

### Study Rooms
- **POST /api/study_rooms** – Create a new study room.
- **GET /api/study_rooms** – Retrieve all study rooms.
- **GET /api/study_rooms/<id>** – Retrieve a study room by ID.

### Posts
- **POST /api/posts** – Create a new post.

### Comments
- **POST /api/comments** – Create a new comment.

### Media
- **POST /api/media** – Upload media associated with a post.

## Testing

Unit and integration tests are available in the `tests` directory. To run the tests, execute:

```bash
pytest
```

## Deployment

The project can be deployed to cloud platforms like Render, Heroku, or AWS. A sample configuration for Render is provided in `render.yaml`.

## Generating a JWT Secret

If you need to generate a secure JWT secret key, run:

```bash
python generate_secret.py
```

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with Flask, SQLAlchemy, and Flask-JWT-Extended.
- Environment variable management with python-dotenv.
- Database connection via psycopg2.

