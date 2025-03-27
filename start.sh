#!/bin/bash

echo ">>> Setting environment..."
export FLASK_APP=app.py
export FLASK_ENV=production

echo ">>> Running migration upgrade..."
python3 -c "
from app import app, db
from flask_migrate import Migrate, upgrade

migrate = Migrate(app, db)  
with app.app_context():
    upgrade()
"

echo ">>> Starting Gunicorn..."
gunicorn app:app
