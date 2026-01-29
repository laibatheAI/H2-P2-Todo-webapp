import pytest
from fastapi.testclient import TestClient
from src.main import app
from sqlmodel import create_engine, Session, SQLModel
from unittest.mock import patch
from contextlib import contextmanager

# Create a test client
client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_auth_endpoints_exist():
    """Test that auth endpoints exist (even if they return 401/422 for invalid requests)"""
    # Test login endpoint exists
    response = client.post("/api/auth/login")
    # Should return 422 (validation error) or 401 (unauthorized) but not 404
    assert response.status_code in [401, 422]

    # Test register endpoint exists
    response = client.post("/api/auth/register")
    # Should return 422 (validation error) but not 404
    assert response.status_code == 422

def test_tasks_endpoints_exist():
    """Test that tasks endpoints exist (should require auth)"""
    # Test GET tasks endpoint exists
    response = client.get("/api/tasks")
    # Should return 401 (unauthorized) but not 404
    assert response.status_code == 401

    # Test POST tasks endpoint exists
    response = client.post("/api/tasks", json={"title": "test"})
    # Should return 401 (unauthorized) but not 404
    assert response.status_code == 401