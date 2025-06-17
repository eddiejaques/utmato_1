# Utmato

A SaaS tool for marketing teams to plan, create, and track marketing campaigns with advanced targeting and UTM link management.

## Project Overview

### Repository Structure (Task 001)
- `/frontend`: Next.js (React) application
- `/backend`: FastAPI (Python) server
- `/docs`: Project documentation
- `/scripts`: Utility scripts

## 1. Initial Project Setup (Task 001)

### Frontend Setup (Next.js)
```sh
cd frontend
npm install
npm run dev
```
- Visit [http://localhost:3000](http://localhost:3000)
- Run checks:
  ```sh
  npm run lint
  npm run type-check
  ```

### Backend Setup (FastAPI)
```sh
cd backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
- Visit [http://localhost:8000/health](http://localhost:8000/health)

### Docker Setup (Optional)
```sh
docker-compose up --build
```
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:8000/health](http://localhost:8000/health)

### Development Environment
- Required files:
  - `frontend/.env.example`
  - `backend/.env.example`
  - `docs/README.md`, `docs/api.md`, `docs/setup.md`, `docs/architecture.md`
  - `.vscode/extensions.json`

### Security Audit
```sh
# Frontend
cd frontend
npm audit

# Backend
cd backend
source venv/bin/activate
pip list --outdated
```

## 2. Database Setup (Task 002)

### Supabase Configuration
- Create a new Supabase project
- Configure project settings:
  - Region selection
  - Database password
  - API access

### Database Schema
- Main tables:
  - organizations
  - users
  - campaigns
  - links
  - invitations

### Schema Management
```sh
# Apply schema
psql "$DATABASE_URL" -f scripts/schema.sql

# Verify schema
python scripts/check_schema.py
```

### Environment Configuration
Create `.env` file with appropriate credentials:
```env
# Development
DB_HOST=localhost
DB_PORT=5432
DB_NAME=utmato
DB_USER=postgres
DB_PASSWORD=your_password

# Staging/Production settings in deployment
```

## 3. Database Migrations (Task 003)

### Migration Setup
```sh
# Install Alembic
pip install alembic

# Initialize
alembic init migrations

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Migration Testing
- Test migrations on development database
- Verify rollback functionality
- Check data integrity
- Test against production-like data in staging

## 4. Authentication System (Task 004)

### Clerk Setup
1. Create Clerk account and project at https://clerk.com/
2. Enable authentication methods:
   - Google OAuth
   - Email/Password

### Frontend Integration
1. Environment setup:
```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
```

2. Test Clerk integration:
```sh
cd frontend
npm run dev
# Visit http://localhost:3000/clerk-test
```

3. Run authentication tests:
```sh
npx jest app/clerk-test/page.test.tsx
```

### Backend JWT Verification
1. Environment setup:
```env
CLERK_SECRET_KEY=your_clerk_secret_key
CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
```

2. Run middleware tests:
```sh
cd backend
pytest tests/middleware/test_verify_clerk_jwt.py -v
```

### Protected Routes Testing
```sh
# Frontend tests
cd frontend
npm test -- --testPathPattern=protected-routes

# Backend tests
cd backend
pytest tests/routes/test_protected_routes.py -v
```

### Session Management Testing
```sh
# Frontend
cd frontend
npm test -- --testPathPattern=session-management

# Backend
cd backend
pytest tests/test_session_management.py -v
```

### Integration Testing
```sh
# Frontend
cd frontend
npm run test:auth

# Backend
cd backend
pytest tests/auth/ -v
```

### Troubleshooting
For authentication issues:
1. Verify environment variables
2. Check JWT middleware configuration
3. Review Clerk dashboard settings
4. Verify CORS configuration
5. Check browser console
6. Review backend logs

For detailed troubleshooting, see `docs/auth-troubleshooting.md`. 