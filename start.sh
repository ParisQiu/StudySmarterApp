#!/bin/bash

export FLASK_APP=app.py
export FLASK_ENV=production

flask db upgrade
gunicorn app:app
