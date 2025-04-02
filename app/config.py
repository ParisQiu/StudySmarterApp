import os
from dotenv import load_dotenv

# Load environment variables from a .env file in the project root
load_dotenv()

class Config:
    # Flask configuration
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1", "t"]
    SECRET_KEY = os.getenv("SECRET_KEY") or os.urandom(24).hex()

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or os.urandom(24).hex()
    