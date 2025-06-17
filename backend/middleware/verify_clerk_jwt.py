import os
import json
import requests
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from pydantic import BaseModel, ValidationError
from jose import jwt, JWTError
from functools import lru_cache

CLERK_PUBLISHABLE_KEY = os.getenv("CLERK_PUBLISHABLE_KEY")
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
CLERK_JWT_ISSUER = f"https://clerk.{os.getenv('CLERK_FRONTEND_API')}.accounts.dev"

class ClerkTokenPayload(BaseModel):
    sub: str
    email: Optional[str] = None
    # Add more fields as needed

@lru_cache()
def get_clerk_jwks() -> Dict[str, Any]:
    """Fetch and cache Clerk's JWKS (JSON Web Key Set)"""
    response = requests.get(f"{CLERK_JWT_ISSUER}/.well-known/jwks.json")
    response.raise_for_status()
    return response.json()

class VerifyClerkJWTMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Only protect routes that start with /api/protected
        if not request.url.path.startswith("/api/protected"):
            return await call_next(request)

        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
        
        token = auth_header.split(" ", 1)[1]
        
        try:
            # Get the key set
            jwks = get_clerk_jwks()
            
            # Decode the token header to get the key ID
            header = jwt.get_unverified_header(token)
            if 'kid' not in header:
                raise JWTError("No 'kid' in token header")
            
            # Find the matching key in the JWKS
            key = None
            for jwk in jwks['keys']:
                if jwk['kid'] == header['kid']:
                    key = jwk
                    break
            
            if not key:
                raise JWTError("No matching key found in JWKS")
            
            # Verify the token
            payload = jwt.decode(
                token,
                key,
                algorithms=['RS256'],
                audience=CLERK_PUBLISHABLE_KEY,
                issuer=CLERK_JWT_ISSUER
            )
            
            # Validate payload with Pydantic
            user = ClerkTokenPayload(
                sub=payload.get('sub'),
                email=payload.get('email')
            )
            
            # Attach user info to request.state
            request.state.user = user
            
        except JWTError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
        except ValidationError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token payload: {str(e)}")
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch JWKS: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal authentication error")
        
        return await call_next(request) 