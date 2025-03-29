import psycopg2
import os

# database configuration
db_config = {
    "host": "study_smarter_db_user.db.onrender.com",
    "port": 5432,
    "database": "study_smarter_db",
    "user": "study_smarter_db_user",
    "password": "Fr3Hk3mPahxzduWA98Vn6r6n9r29hBW0",
}

# Connect to Database
def connect_db():
    try:
        conn = psycopg2.connect(
            host=db_config["host"],
            database=db_config["database"],
            user=db_config["user"],
            password=db_config["password"],
            port=db_config["port"]
        )
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None
