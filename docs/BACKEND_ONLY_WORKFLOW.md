# Backend-Only Workflow (No Frontend Required)

Use this runbook when you want to work safely in backend-only mode and avoid frontend/mobile setup errors.

## Scope

- Supported: backend API development, backend tests, backend verification, backend demo-data setup/validation.
- Not required in this mode: web runtime server and mobile runtime commands.

## 1) Environment Setup (Windows PowerShell)

From repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r backend/requirements.txt
```

## 2) Start Backend API

```powershell
npm run backend:run
```

Quick health checks:

- API docs: http://localhost:8001/docs
- OpenAPI: http://localhost:8001/openapi.json

## 3) Backend Verification (Primary)

From repository root:

```powershell
npm run backend:test
npm run backend:check
npm run verify:backend
```

`npm run backend:test` is the fast local pytest command.

`npm run backend:check` runs a one-command validation gate (pytest + full backend verification workflow).

`npm run verify:backend` runs the full backend pytest path plus deterministic smoke verification.

## 4) Demo Data Commands (Backend-Only Safe)

From repository root:

```powershell
npm run demo:setup
npm run demo:verify
npm run demo:info
```

These are safe for backend-only workflows.

## 5) Commands To Skip In Backend-Only Mode

- `php -S 127.0.0.1:8080 -t frontend/web/public`
- `npm run demo:run`
- `npm run demo:report`
- `cd frontend/mobile/RiskRadar` + `npx expo start`

Reason: these commands require web/mobile frontend runtime assets that are intentionally out of scope for this workflow.

## 6) Optional: Hide Frontend Locally Without Deleting It

If you want a backend-focused local checkout while preserving repo history and avoiding destructive deletes:

```powershell
git sparse-checkout init --cone
git sparse-checkout set backend docs package.json README.md
```

To restore full checkout later:

```powershell
git sparse-checkout disable
```

## 7) Daily Backend-Only Loop

1. Activate venv.
2. Run `npm run backend:test` during development.
3. Start backend with `npm run backend:run` only when needed.
4. Run `npm run backend:check` before review/push.
5. Use `npm run demo:setup|verify|info` for deterministic demo-data checks.
6. Avoid frontend/mobile commands unless intentionally switching to UI validation.
