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