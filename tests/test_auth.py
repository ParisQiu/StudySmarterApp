# tests/test_auth.py
import pytest
from app import create_app, db
from flask import json

@pytest.fixture
def app_instance():
    app = create_app()
    app.config["TESTING"] = True
    # Use an in-memory SQLite database for testing purposes
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app_instance):
    return app_instance.test_client()

def test_signup_missing_fields(client):
    # Test signup endpoint with missing data
    response = client.post("/api/signup", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing required fields" in data["message"]

def test_signup_success(client):
    # Test successful user registration
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/api/signup", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert "User registered successfully" in data["message"]
    assert "id" in data

def test_login_invalid_credentials(client):
    # Attempt to login with non-existent credentials
    payload = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/login", json=payload)
    assert response.status_code == 401
    data = response.get_json()
    assert "Invalid credentials" in data["message"]

def test_signup_and_login(client):
    # Register a new user
    signup_payload = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "securepassword"
    }
    signup_response = client.post("/api/signup", json=signup_payload)
    assert signup_response.status_code == 201

    # Login with the newly registered user's credentials
    login_payload = {
        "email": "newuser@example.com",
        "password": "securepassword"
    }
    login_response = client.post("/api/login", json=login_payload)
    assert login_response.status_code == 200
    login_data = login_response.get_json()
    assert "access_token" in login_data
    