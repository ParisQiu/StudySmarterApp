#!/bin/bash

echo ">>> Setting environment..."
export FLASK_APP=app.py
export FLASK_ENV=production

echo ">>> Running migration with Python..."
python -c "from app import db; from flask_migrate import upgrade; upgrade()"

echo ">>> Starting Gunicorn..."
exec gunicorn app:app
