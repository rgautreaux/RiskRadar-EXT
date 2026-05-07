# Web Security and Privacy Predeploy Review

## Security Hardening Checklist
- Remove local debug error display in production entrypoints.
- Keep `.env` and `config.local.php` out of commits.
- Enforce strong `JWT_SECRET_KEY` and rotate per environment.
- Ensure CORS allowlist includes only approved origins in production.
- Use HTTPS-only deployment with secure cookie transport.
- Validate guest/anonymous rate limits and login lockout.
- Confirm CSRF validation on all state-changing form posts.

## Privacy Checklist
- Collect only minimum required personal data.
- Document optional notification channels as opt-in only.
- Add clear notice for feedback/analytics capture and purpose.
- Do not store plaintext secrets or sensitive tokens in frontend storage.

## Secret and Config Handling
- Store runtime secrets in hosting secret manager.
- Never embed API keys into frontend JS bundles.
- Validate required env vars at startup and fail closed when missing.

## Pen-test Light Pass (Web)
- Auth flow checks: session fixation, weak password rejection, login lockout behavior.
- Input checks: registration/profile fields, map/location query params.
- Access checks: guest cannot access admin analytics.
- Browser checks: verify no sensitive response data leaks in console/network.

## Evidence to Capture
- Screenshots/log snippets of secure cookie and CORS headers.
- Test results for `npm run backend:check`, `npm run web:test:e2e`, `npm run web:test:a11y`.
- Short sign-off note with date, branch, and reviewer name.
