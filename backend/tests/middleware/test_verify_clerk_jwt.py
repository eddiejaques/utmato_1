import os
import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from jose import jwt, JWTError
from middleware.verify_clerk_jwt import VerifyClerkJWTMiddleware, ClerkTokenPayload

# Test app setup
app = FastAPI()
app.add_middleware(VerifyClerkJWTMiddleware)

@app.get("/api/public")
async def public_route():
    return {"message": "public"}

@app.get("/api/protected/test")
async def protected_route(request: Request):
    user = request.state.user
    return {"user_id": user.sub, "email": user.email}

client = TestClient(app)

# Mock data
MOCK_VALID_TOKEN = "valid.jwt.token"
MOCK_EXPIRED_TOKEN = "expired.jwt.token"
MOCK_INVALID_TOKEN = "invalid.jwt.token"

MOCK_JWKS = {
    "keys": [{
        "kid": "test-key-1",
        "kty": "RSA",
        "alg": "RS256",
        "use": "sig",
        "n": "test-key",
        "e": "AQAB"
    }]
}

MOCK_TOKEN_HEADER = {
    "kid": "test-key-1",
    "alg": "RS256"
}

MOCK_TOKEN_PAYLOAD = {
    "sub": "user_123",
    "email": "test@example.com",
    "aud": "test_publishable_key",
    "iss": "https://clerk.test.accounts.dev"
}

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Set mock environment variables for testing"""
    with patch.dict(os.environ, {
        "CLERK_SECRET_KEY": "test_secret_key",
        "CLERK_PUBLISHABLE_KEY": "test_publishable_key",
        "CLERK_FRONTEND_API": "test"
    }):
        yield

@pytest.fixture
def mock_get_jwks():
    """Mock the JWKS endpoint response"""
    with patch("middleware.verify_clerk_jwt.get_clerk_jwks") as mock:
        mock.return_value = MOCK_JWKS
        yield mock

@pytest.fixture
def mock_jwt():
    """Mock JWT decode and header functions"""
    with patch("middleware.verify_clerk_jwt.jwt") as mock:
        mock.get_unverified_header.return_value = MOCK_TOKEN_HEADER
        mock.decode.return_value = MOCK_TOKEN_PAYLOAD
        yield mock

def test_public_route_access():
    """Test that public routes are accessible without authentication"""
    response = client.get("/api/public")
    assert response.status_code == 200
    assert response.json() == {"message": "public"}

def test_protected_route_no_auth_header():
    """Test that protected routes require authentication header"""
    response = client.get("/api/protected/test")
    assert response.status_code == 401
    assert "Missing or invalid Authorization header" in response.json()["detail"]

def test_protected_route_invalid_auth_format():
    """Test that auth header must be in Bearer format"""
    response = client.get("/api/protected/test", headers={"Authorization": "Invalid format"})
    assert response.status_code == 401
    assert "Missing or invalid Authorization header" in response.json()["detail"]

def test_protected_route_valid_token(mock_get_jwks, mock_jwt):
    """Test successful authentication with valid token"""
    response = client.get(
        "/api/protected/test",
        headers={"Authorization": f"Bearer {MOCK_VALID_TOKEN}"}
    )
    
    assert response.status_code == 200
    assert response.json() == {
        "user_id": MOCK_TOKEN_PAYLOAD["sub"],
        "email": MOCK_TOKEN_PAYLOAD["email"]
    }
    
    mock_jwt.get_unverified_header.assert_called_once_with(MOCK_VALID_TOKEN)
    mock_jwt.decode.assert_called_once_with(
        MOCK_VALID_TOKEN,
        MOCK_JWKS["keys"][0],
        algorithms=['RS256'],
        audience="test_publishable_key",
        issuer="https://clerk.test.accounts.dev"
    )

def test_protected_route_invalid_token(mock_get_jwks, mock_jwt):
    """Test handling of invalid tokens"""
    mock_jwt.decode.side_effect = JWTError("Invalid token")
    
    response = client.get(
        "/api/protected/test",
        headers={"Authorization": f"Bearer {MOCK_INVALID_TOKEN}"}
    )
    
    assert response.status_code == 401
    assert "Invalid token" in response.json()["detail"]

def test_protected_route_no_matching_key(mock_get_jwks, mock_jwt):
    """Test handling of tokens with no matching key in JWKS"""
    mock_jwt.get_unverified_header.return_value = {"kid": "non-existent-key"}
    
    response = client.get(
        "/api/protected/test",
        headers={"Authorization": f"Bearer {MOCK_VALID_TOKEN}"}
    )
    
    assert response.status_code == 401
    assert "No matching key found in JWKS" in response.json()["detail"]

def test_protected_route_jwks_fetch_error(mock_get_jwks):
    """Test handling of JWKS fetch errors"""
    mock_get_jwks.side_effect = Exception("Failed to fetch JWKS")
    
    response = client.get(
        "/api/protected/test",
        headers={"Authorization": f"Bearer {MOCK_VALID_TOKEN}"}
    )
    
    assert response.status_code == 500
    assert "Failed to fetch JWKS" in response.json()["detail"]

def test_protected_route_no_email(mock_get_jwks, mock_jwt):
    """Test handling of tokens without email"""
    payload_without_email = MOCK_TOKEN_PAYLOAD.copy()
    del payload_without_email["email"]
    mock_jwt.decode.return_value = payload_without_email
    
    response = client.get(
        "/api/protected/test",
        headers={"Authorization": f"Bearer {MOCK_VALID_TOKEN}"}
    )
    
    assert response.status_code == 200
    assert response.json() == {
        "user_id": MOCK_TOKEN_PAYLOAD["sub"],
        "email": None
    } 