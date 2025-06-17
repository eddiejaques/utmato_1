# Backend Middleware Documentation

## Clerk JWT Verification Middleware

**File:** `backend/middleware/verify_clerk_jwt.py`

### Purpose
Protects FastAPI routes by verifying Clerk-issued JWTs. Attaches user info to `request.state.user` if valid.

### Usage
- Middleware is automatically applied to routes starting with `/api/protected`.
- Add your protected endpoints under this path.

### Environment Variables
- `CLERK_PUBLISHABLE_KEY`: Your Clerk publishable key
- `CLERK_SECRET_KEY`: Your Clerk secret key

### Example
```python
from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/api/protected/example")
async def protected_example(request: Request):
    user = request.state.user  # ClerkTokenPayload instance
    return {"user_id": user.sub, "email": user.email}
```

### Error Handling
- Returns 401 for missing/invalid/expired tokens
- Returns 500 for internal errors

### Testing
- See `backend/tests/middleware/test_verify_clerk_jwt.py` for test cases (to be implemented) 