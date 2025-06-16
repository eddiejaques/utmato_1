# Utmato

A SaaS tool for marketing teams to plan, create, and track marketing campaigns with advanced targeting and UTM link management.

## Monorepo Structure
- frontend: Next.js (React)
- backend: FastAPI (Python)
- docs: Documentation
- scripts: Utility scripts

See .taskmaster/tasks/task_001.txt for setup details. 

---

## Testing the Initial Project Setup

Follow these steps to verify your development environment is working correctly:

### 1. Test the Frontend (Next.js)
- Install dependencies:
  ```sh
  cd frontend
  npm install
  ```
- Start the development server:
  ```sh
  npm run dev
  ```
- Open your browser at [http://localhost:3000](http://localhost:3000) and verify the Next.js welcome page appears.
- Lint and type-check:
  ```sh
  npm run lint
  npm run type-check
  ```

### 2. Test the Backend (FastAPI)
- Create and activate the Python virtual environment:
  ```sh
  cd ../backend
  source venv/bin/activate
  ```
- Install dependencies:
  ```sh
  pip install -r requirements.txt
  ```
- Start the FastAPI server:
  ```sh
  uvicorn main:app --reload
  ```
- Open your browser at [http://localhost:8000/health](http://localhost:8000/health) and verify you see `{ "status": "ok" }`.

### 3. Test Docker Compose (Optional)
- From the project root, run:
  ```sh
  docker-compose up --build
  ```
- Visit [http://localhost:3000](http://localhost:3000) (frontend) and [http://localhost:8000/health](http://localhost:8000/health) (backend) to verify both are running.

### 4. Verify Documentation and Environment Files
- Ensure the following files exist and are populated:
  - `README.md`
  - `frontend/.env.example`
  - `backend/.env.example`
  - `docs/README.md`, `docs/api.md`, `docs/setup.md`, `docs/architecture.md`
  - `.vscode/extensions.json`

### 5. Test Git Repository
- Run:
  ```sh
  git status
  ```
- Ensure the repository is initialized and clean (no uncommitted changes after setup).

### 6. Security and Dependency Audit
- **Frontend:**
  ```sh
  cd frontend
  npm audit
  ```
- **Backend:**
  ```sh
  cd ../backend
  source venv/bin/activate
  pip list --outdated
  deactivate
  ``` 

---

## Testing and Managing SQL Schema Changes

### 1. Apply SQL Schema Changes
- The main schema is defined in `scripts/schema.sql` (extracted from the PRD).
- To apply the schema to your database, run the SQL file using your preferred SQL client or the Supabase SQL editor:
  ```sh
  psql "$DATABASE_URL" -f scripts/schema.sql
  # or use the Supabase web SQL editor and paste the contents
  ```

### 2. Verify Schema with the Check Script
- Use the provided script to verify that all required tables and columns exist:
  ```sh
  # Set your environment variables (see below)
  python scripts/check_schema.py
  ```
- The script will print a summary indicating if the schema matches the expected structure.

### 3. Configuring the .env File for Different Environments
- The schema check script and your backend use environment variables to connect to the database.
- Create a `.env` file in the project root or backend directory (never commit real credentials to version control).
- Example `.env` file:
  ```env
  # Local development
  DB_HOST=localhost
  DB_PORT=5432
  DB_NAME=utmato
  DB_USER=postgres
  DB_PASSWORD=your_local_password

  # Staging (override as needed)
  # DB_HOST=staging-db-host
  # DB_PORT=5432
  # DB_NAME=utmato_stage
  # DB_USER=staging_user
  # DB_PASSWORD=staging_password

  # Production (override as needed)
  # DB_HOST=prod-db-host
  # DB_PORT=5432
  # DB_NAME=utmato_prod
  # DB_USER=prod_user
  # DB_PASSWORD=prod_password
  ```
- To switch environments, comment/uncomment the relevant section or use environment variable overrides in your deployment pipeline.
- **Best Practices:**
  - Use `.env.example` to document required variables for each environment.
  - Never commit real secrets to git.
  - Use secret managers or CI/CD environment variable settings for production.

--- 