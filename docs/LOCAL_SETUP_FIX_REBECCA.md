# Rebecca Local Setup Fix (Final)

This is the validated local fix path for the web app workflow.

## Known-good local topology
- Backend API: `http://127.0.0.1:8001`
- Web frontend: `http://127.0.0.1:8080`
- Keep backend and frontend on different ports.

## 1. Activate virtual environment
From repository root:

```powershell
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned)
.\.venv\Scripts\Activate.ps1
```

## 2. Validate backend env file
Ensure `backend/.env` includes at minimum:

```env
DATABASE_URL=sqlite:///./riskradar.db
JWT_SECRET_KEY=replace-with-strong-secret
EMAIL_ENCRYPTION_KEY=replace-with-fernet-key
CORS_ALLOWED_ORIGINS=http://127.0.0.1:8080,http://localhost:8080
```

## 3. Rebuild deterministic demo DB
From repository root:

```powershell
npm run demo:setup
```

## 4. Start backend (do not use `backend.main:app` from root)

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8001
```

Expected health checks:

```powershell
curl http://127.0.0.1:8001/
curl http://127.0.0.1:8001/api/v1/alerts?limit=1
```

## 5. Start frontend in a second terminal
From repository root:

```powershell
php -S 127.0.0.1:8080 -t frontend/web/public
```

Open `http://127.0.0.1:8080/login.php`.

## 6. Build/refresh frontend assets
From repository root:

```powershell
npm run build:web
```

For iterative work:

```powershell
npm run build:web:watch
```

## 7. Quick verification flow
1. Continue as guest.
2. Register a new account.
3. Log in with the new account.
4. Open Alerts, Map, Assistant, and Travel pages.

## 8. If registration/login fails
- Confirm backend is running on `8001`.
- Confirm frontend points to backend `8001` in config/environment.
- Confirm CORS includes `127.0.0.1:8080`.
- Re-run `npm run demo:setup` for schema/data reset.

## 9. If styles or widget do not load
- Run `npm run build:web`.
- Hard refresh browser cache.
- Verify files exist under `frontend/web/public/assets`.

## 10. Validation commands
From repository root:

```powershell
npm run verify:connectivity
npm run backend:check
npm run web:test:e2e
npm run web:test:a11y
```
