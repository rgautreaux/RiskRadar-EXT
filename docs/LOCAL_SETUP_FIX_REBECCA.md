# Rebecca's Local Environment — Complete Fix Guide
> Based on full analysis of: settings.py, users.py, database.py, insert_test_alert.py,
> the TRANSCRIPT.md history, and all provided screenshots.

---

## Summary of All Problems Found

| # | Problem | Root Cause | Status |
|---|---------|-----------|--------|
| 1 | Backend crashes on startup | `settings.py` IndentationError | **Fix provided** |
| 2 | Registration/Login fails | Backend not running (caused by #1) | Resolved by fixing #1 |
| 3 | `config.local.php` points to wrong port | Backend now runs on 8002, config says 8001 | **Fix provided** |
| 4 | Database is empty | Backend never ran, insert script couldn't run | Resolved by fixing #1 + #3 |
| 5 | Pylint E0401 import errors in VS Code | Pylint doesn't know `backend/` is the root | **Fix provided** |
| 6 | CSS 404s (tailwind.css, theme.css) | `UI_UX_STYLE_FILES` not in `frontend/web/public/` | **Fix provided** |
| 7 | Password "testpassword" rejected | Backend requires minimum 12 characters | **Documented** |

---

## FIX 1 — Replace `backend/config/settings.py`

The file had a duplicate `pythonpath` field with wrong indentation (8 spaces instead of 4),
which pushed `model_config` outside the class body entirely. This caused the
`IndentationError: unindent does not match any outer indentation level` crash
that prevented ALL backend startup attempts.

**Action:** Replace your `backend/config/settings.py` with the corrected version
already provided (settings.py in your outputs). The key changes are:
- Removed the duplicate over-indented `pythonpath` line (was at 8 spaces)
- Moved `model_config = SettingsConfigDict(extra="allow")` to be the FIRST line
  inside the `Settings` class (standard Pydantic v2 convention)
- Kept the single correct `pythonpath: str = ""` at 4-space indent

---

## FIX 2 — Update `frontend/web/config/config.local.php`

The transcript shows Copilot created `config.local.php` pointing to port `8001`,
but your backend is now running on port `8002`. This mismatch means the frontend
sends registration/login requests to a port with nothing listening — which is why
you see "Registration failed. Please verify the backend is running."

**Action:** Open `frontend/web/config/config.local.php` and make sure it says:

```php
<?php
return [
    'api' => [
        'base_url' => 'http://127.0.0.1:8002',
        'prefix' => '/api/v1',
        'timeout' => 5.0,
    ],
];
```

> NOTE: This file is in `.gitignore` — editing it will NOT affect your teammates.

---

## FIX 3 — Correct Startup Commands (run in this exact order)

Previous attempts used wrong commands (`uvicorn backend.main:app` from the project
root fails because Python can't resolve `config.settings` as an absolute import).

### Step 1: Start the backend
Open a terminal and run:
```powershell
cd path\to\your\project\backend
.\.venv\Scripts\activate
uvicorn main:app --host 127.0.0.1 --port 8002
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8002
INFO:     Application startup complete.
```

If you see a `pydantic_settings` validation error about `pythonpath`, it means
settings.py still has the old broken version — re-apply Fix 1.

### Step 2: Start the frontend (separate terminal)
```powershell
cd path\to\your\project
php -S 127.0.0.1:8002 -t frontend/web/public
```

Wait — the frontend is ALSO trying to use port 8002 in your screenshot (Image 5).
You need them on DIFFERENT ports. Use:
```powershell
php -S 127.0.0.1:8082 -t frontend/web/public
```

Then update `config.local.php` accordingly — the frontend port doesn't matter for
the config, only the BACKEND port does. Your config.local.php `base_url` always
points to the backend (8002), regardless of what port the frontend runs on.

Then open: **http://127.0.0.1:8082/register.php**

---

## FIX 4 — Populate the Database (after backend is running)

The `alerts` table is empty because the backend never ran successfully to seed it,
and the `insert_test_alert.py` script was also broken by the settings.py crash.

Once the backend is running (Fix 1 + 3 done), open a NEW terminal and run:

```powershell
cd path\to\your\project\backend
.\.venv\Scripts\activate
python scripts/insert_test_alert.py
```

You should see: `✓ Test alert inserted successfully.`

Then refresh phpMyAdmin and the `alerts` table will have a row.

**If you still get an error**, check your `backend/.env` file. It must contain:
```
DATABASE_URL=mysql+pymysql://root@127.0.0.1:3306/riskradarweb_db
```
(No password is correct if your MySQL root has no password locally, which the
transcript confirms is your setup.)

---

## FIX 5 — Fix Pylint E0401 Import Errors in VS Code

These are NOT real runtime errors — they are VS Code/Pylint false positives because
Pylint runs from the project root and doesn't know that `backend/` is the Python root.
They do NOT prevent the app from running.

**Action:** Create `.vscode/settings.json` in your project root (or add to it if it
already exists) with this content:

```json
{
    "python.analysis.extraPaths": ["./backend"],
    "pylint.args": [
        "--init-hook",
        "import sys; sys.path.insert(0, 'backend')"
    ]
}
```

> This file CAN be committed — it helps all teammates. But check with your team first
> in case they have their own `.vscode/settings.json`.

After saving, reload VS Code (`Ctrl+Shift+P` → "Developer: Reload Window") and the
red import errors should disappear.

---

## FIX 6 — CSS 404 Errors (tailwind.css, theme.css)

`app.css` imports:
```css
@import '../../../../../UI_UX_STYLE_FILES/styles/tailwind.css';
@import '../../../../../UI_UX_STYLE_FILES/styles/theme.css';
```

The PHP server serves files from `frontend/web/public/`, but the `UI_UX_STYLE_FILES/`
folder lives at the project root — the relative `../../../../../` path tries to go
5 levels up from the CSS file, which may or may not resolve correctly depending on
how PHP serves it.

**Check first:**
```powershell
ls UI_UX_STYLE_FILES\styles\
```

If `tailwind.css` and `theme.css` exist there, the path resolution is the issue.
The PHP built-in server resolves paths relative to the document root
(`frontend/web/public/`), so a request for `/UI_UX_STYLE_FILES/...` will 404.

**Fix option A (recommended, local only):** Symlink or copy the styles into the
public folder:
```powershell
# From the project root:
xcopy UI_UX_STYLE_FILES\styles frontend\web\public\UI_UX_STYLE_FILES\styles /E /I
```

**Fix option B:** Ask your teammate who owns `UI_UX_STYLE_FILES` if the CSS files
are committed. If they're in `.gitignore` or were never pushed, do a `git pull`
from their branch and check.

> Note: These 404s affect styling only — they do NOT block registration/login.

---

## FIX 7 — Password Requirements for Testing

The backend `settings.py` has `PASSWORD_MIN_LENGTH: int = 12`.

The `validate_password_strength` function in `auth/security.py` enforces this.

The test password "testpassword" is **exactly 12 characters** and may pass, but
previous curl tests were failing because PowerShell was mangling the JSON quotes.

When testing registration, use a password like: `TestPassword123!`

---

## Quick Verification Checklist

After applying all fixes, run through this in order:

- [ ] `backend/config/settings.py` — no indentation errors (use the provided file)
- [ ] `frontend/web/config/config.local.php` — `base_url` is `http://127.0.0.1:8002`
- [ ] Backend starts: `cd backend && uvicorn main:app --host 127.0.0.1 --port 8002`
- [ ] Browser: `http://127.0.0.1:8002/docs` shows FastAPI documentation
- [ ] Frontend starts: `php -S 127.0.0.1:8082 -t frontend/web/public`
- [ ] Browser: `http://127.0.0.1:8082/register.php` loads the registration page
- [ ] Register with password 12+ chars — success message appears
- [ ] `python scripts/insert_test_alert.py` runs without errors
- [ ] phpMyAdmin `alerts` table now has 1 row

---

## What NOT to Do (Lessons from the Transcript)

1. **Do NOT run `uvicorn backend.main:app` from the project root** — always `cd backend` first.
2. **Do NOT commit `config.local.php` or `.env`** — these are local-only files.
3. **Do NOT add error reporting (`ini_set`) to register.php permanently** — remove after debugging.
4. **Do NOT run the backend on the same port as the frontend** — they must be different.
5. **The Pylint E0401 errors are cosmetic** — ignore them until Fix 5 is applied; they never prevented the app from running.
