from app import db, app
from sqlalchemy import text

with app.app_context():
    try:
        db.session.execute(text("SELECT 1"))
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")
