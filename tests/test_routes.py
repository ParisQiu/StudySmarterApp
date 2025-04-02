# tests/test_routes.py
import pytest
from app import create_app, db

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

def test_home_route(client):
    # Test the root route defined in the application (likely in app.py)
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert "StudySmarter API is running" in data

def test_get_users_empty(client):
    # Test GET /api/users when no users are present
    response = client.get("/api/users")
    # Depending on your controller implementation, this might return 404 or an empty list.
    if response.status_code == 200:
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0
    else:
        assert response.status_code == 404
        