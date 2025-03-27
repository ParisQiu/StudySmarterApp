#!/bin/bash

export FLASK_APP=app.py
export FLASK_ENV=production

echo ">>> Setting environment..."
echo ">>> Running migration with Python..."


python3 -c "
from app import app, db
from flask_migrate import upgrade
with app.app_context():
    upgrade()
"

echo ">>> Starting Gunicorn..."

gunicorn app:app
