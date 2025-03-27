#!/bin/bash

echo "Setting Flask app context..."
export FLASK_APP=app.py
export FLASK_RUN_FROM_CLI=true

echo "Upgrading database..."
flask db upgrade

echo "Starting gunicorn..."
exec gunicorn app:app
