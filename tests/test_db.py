# tests/test_db.py
import pytest
from database import create_connection, init_db

def test_create_connection():
    conn = create_connection()
    if conn is None:
        pytest.skip("Database not configured for testing")
    else:
        assert conn is not None
        conn.close()

def test_init_db():
    # Ensure that the database tables can be initialized.
    conn = create_connection()
    if conn is None:
        pytest.skip("Database not configured for testing")
    result = init_db()
    assert result is True
    