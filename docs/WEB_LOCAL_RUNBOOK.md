# Web Local Runbook (Backend + Frontend)

## Scope
This runbook covers the web application local startup flow only.

## 1. Prerequisites
- Python 3.10+
- Node.js 18+
- npm 9+
- PHP 8+
- Local `.venv` created at repository root

## 2. Environment Setup
Create or update `backend/.env` with local values:

```env
DATABASE_URL=sqlite:///./riskradar.db
JWT_SECRET_KEY=replace-with-strong-secret
EMAIL_ENCRYPTION_KEY=replace-with-fernet-key
CORS_ALLOWED_ORIGINS=http://127.0.0.1:8080,http://localhost:8080
GUEST_DAILY_LIMIT=10
```

Optional keys:

```env
LLM_API_KEY=your-openai-compatible-key
OPENROUTER_API_KEY=your-openrouter-key
FIRECRAWL_API_KEY=your-firecrawl-key
```

## 3. Install Dependencies
From repository root:

```powershell
npm install
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
```

## 4. Seed Demo Data
From repository root:

```powershell
npm run demo:setup
```

## 5. Start Backend (Terminal 1)

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8001
```

Health checks:

```powershell
curl http://127.0.0.1:8001/
curl http://127.0.0.1:8001/api/v1/alerts?limit=1
```

## 6. Build Web Assets
From repository root:

```powershell
npm run build:web
```

For active UI edits:

```powershell
npm run build:web:watch
```

## 7. Start Web Frontend (Terminal 2)
From repository root:

```powershell
php -S 127.0.0.1:8080 -t frontend/web/public
```

Open:
- `http://127.0.0.1:8080/login.php`

## 8. Verification Commands
From repository root:

```powershell
npm run verify:connectivity
npm run backend:check
npm run web:test:e2e
npm run web:test:a11y
```

## 9. Demo Journey Command
From repository root:

```powershell
npm run demo:run
```

## 10. Troubleshooting
- If API requests fail from web pages, confirm backend port is `8001` and CORS includes `127.0.0.1:8080`.
- If the assistant widget is missing, run `npm run build:web` again.
- If schema drift appears, reset demo DB: `npm run demo:setup`.
- If stale assets remain, clear browser cache and hard refresh.
