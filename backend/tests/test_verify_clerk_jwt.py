import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from middleware.verify_clerk_jwt import VerifyClerkJWTMiddleware

# Test app setup
app = FastAPI()
app.add_middleware(VerifyClerkJWTMiddleware)

@app.get("/api/protected/test")
async def protected_route():
    return {"message": "Access granted"}

@app.get("/api/public/test")
async def public_route():
    return {"message": "Public access"}

client = TestClient(app)

# Mock JWKS data
MOCK_JWKS = {
    "keys": [{
        "kid": "test-key-id",
        "kty": "RSA",
        "alg": "RS256",
        "n": "test-key",
        "e": "AQAB"
    }]
}

# Mock valid token data
VALID_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6InRlc3Qta2V5LWlkIn0.eyJzdWIiOiJ1c2VyLTEyMyIsImVtYWlsIjoidGVzdEB0ZXN0LmNvbSJ9.signature"

@pytest.fixture
def mock_jwks():
    with patch("middleware.verify_clerk_jwt.get_clerk_jwks") as mock:
        mock.return_value = MOCK_JWKS
        yield mock

@pytest.fixture
def mock_jwt_decode():
    with patch("middleware.verify_clerk_jwt.jwt.decode") as mock:
        mock.return_value = {
            "sub": "user-123",
            "email": "test@test.com"
        }
        yield mock

def test_public_route_no_token():
    """Test that public routes work without a token"""
    response = client.get("/api/public/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Public access"}

def test_protected_route_no_token():
    """Test that protected routes require a token"""
    response = client.get("/api/protected/test")
    assert response.status_code == 401
    assert "Missing or invalid Authorization header" in response.json()["detail"]

def test_protected_route_invalid_auth_header():
    """Test invalid authorization header format"""
    response = client.get("/api/protected/test", headers={"Authorization": "Invalid"})
    assert response.status_code == 401
    assert "Missing or invalid Authorization header" in response.json()["detail"]

def test_protected_route_valid_token(mock_jwks, mock_jwt_decode):
    """Test successful authentication with valid token"""
    response = client.get(
        "/api/protected/test",
        headers={"Authorization": f"Bearer {VALID_TOKEN}"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Access granted"}

def test_protected_route_jwks_fetch_error(mock_jwks):
    """Test handling of JWKS fetch error"""
    mock_jwks.side_effect = Exception("JWKS fetch failed")
    response = client.get(
        "/api/protected/test",
        headers={"Authorization": f"Bearer {VALID_TOKEN}"}
    )
    assert response.status_code == 500
    assert "Internal authentication error" in response.json()["detail"]

def test_protected_route_invalid_token_payload(mock_jwks, mock_jwt_decode):
    """Test handling of invalid token payload"""
    mock_jwt_decode.return_value = {"invalid": "payload"}
    response = client.get(
        "/api/protected/test",
        headers={"Authorization": f"Bearer {VALID_TOKEN}"}
    )
    assert response.status_code == 401
    assert "Invalid token payload" in response.json()["detail"]

def test_protected_route_jwt_decode_error(mock_jwks, mock_jwt_decode):
    """Test handling of JWT decode error"""
    mock_jwt_decode.side_effect = Exception("Invalid token")
    response = client.get(
        "/api/protected/test",
        headers={"Authorization": f"Bearer {VALID_TOKEN}"}
    )
    assert response.status_code == 500
    assert "Internal authentication error" in response.json()["detail"] 