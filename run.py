# run.py
import os
from app import create_app
from database import init_db

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    # Initialize the database before starting the server
    if init_db():
        print("Database initialized successfully")
    else:
        print("Failed to initialize database")

    # Get the port from environment variables or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    