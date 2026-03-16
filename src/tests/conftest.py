"""
Test configuration and fixtures for FastAPI app tests.
"""
import pytest
from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def client():
    """Provide a TestClient instance for testing the FastAPI app."""
    return TestClient(app)
