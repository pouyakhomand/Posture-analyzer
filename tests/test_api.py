import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Posture Extractor Microservice"
    assert data["status"] == "running"


def test_analyze_endpoint_no_files():
    """Test analyze endpoint with no files."""
    response = client.post("/api/v1/analyze")
    assert response.status_code == 422  # Validation error


def test_analyze_endpoint_invalid_angle():
    """Test analyze endpoint with invalid angle."""
    # This would need a mock file for proper testing
    # For now, just test the validation logic
    pass


def test_docs_endpoint():
    """Test that docs endpoint is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_endpoint():
    """Test that redoc endpoint is accessible."""
    response = client.get("/redoc")
    assert response.status_code == 200 