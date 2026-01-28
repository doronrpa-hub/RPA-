"""
RPA-PORT Customs AI - Tests
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "RPA-PORT Customs AI"
    assert data["status"] == "running"


def test_health():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_agreements():
    """Test trade agreements endpoint"""
    response = client.get("/api/agreements")
    assert response.status_code == 200
    data = response.json()
    assert "agreements" in data
    assert len(data["agreements"]) > 0
    
    # Check first agreement structure
    agreement = data["agreements"][0]
    assert "code" in agreement
    assert "name" in agreement
    assert "year" in agreement


def test_chat_no_api_key():
    """Test chat endpoint without API key returns error"""
    response = client.post(
        "/api/chat",
        json={"message": "test"}
    )
    # Should fail without API key
    assert response.status_code == 500


def test_classify_no_api_key():
    """Test classify endpoint without API key returns error"""
    response = client.post(
        "/api/classify",
        json={"description": "test product"}
    )
    # Should fail without API key
    assert response.status_code == 500
