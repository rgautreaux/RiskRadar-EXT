Playwright E2E tests

How to run the frontend E2E tests locally:

1. Start or build the frontend and backend so the site is reachable.

   - Backend (from project root):

```bash
cd backend
.venv\Scripts\activate   # Windows PowerShell; or `source .venv/bin/activate` on macOS/Linux
uvicorn main:app --host 127.0.0.1 --port 8001
```

   - Frontend (PHP built-in server) – run from project root:

```bash
php -S 127.0.0.1:8080 -t frontend/web/public
```

2. Install Playwright browsers (only once):

```bash
npm run playwright:install
```

3. Run the E2E tests (from project root):

```bash
npm run web:test:e2e
```

Notes:
- The tests use `RISKRADAR_WEB_BASE_URL` env var to override the default `http://127.0.0.1:8080`.
- Ensure `backend/.env` is populated so API calls from the frontend succeed during tests.
- For CI, consider adding a web-server startup step or use Playwright `webServer` option.
