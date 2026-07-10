# Security & Privacy Review Hardening Checklist

**Project:** RiskRadar CMPS 357  
**Purpose:** Final hardening before production deployment  
**Audience:** Graders, team leads, security reviewers

---

## 1. Authentication & Authorization

- [ ] **Passwords hashed correctly**
  - Check: `backend/auth/security.py` uses `pbkdf2_sha256` or `bcrypt`
  - Test: Create user, verify DB stores hashed password (not plaintext)
  - Verify: Min 12-character requirement enforced

- [ ] **Session tokens secure**
  - Check: `JWT_SECRET_KEY` is strong (32+ chars, random)
  - Check: Tokens use `HS256` or `RS256` algorithm (not `none`)
  - Test: Expired tokens rejected; invalid signatures rejected

- [ ] **CSRF protection enabled**
  - Check: All POST forms include CSRF token
  - Check: Backend validates CSRF middleware is active
  - Test: POST without token fails with 403

- [ ] **Rate limiting active**
  - Check: `/api/v1/users/login` has 10-failure lockout (15 min)
  - Check: Assistant guest limit enforced (`GUEST_DAILY_LIMIT`)
  - Test: Exceed limits; verify lockout message shown

- [ ] **HttpOnly, Secure cookies**
  - Check: Session cookie has `HttpOnly`, `Secure`, `SameSite=Strict`
  - Verify: Cookie not accessible via JavaScript (prevents XSS theft)

---

## 2. Data Protection

- [ ] **Sensitive data encrypted at rest**
  - Check: Emails encrypted with Fernet key (`backend/auth/security.py`)
  - Check: API keys (LLM_API_KEY, FIRECRAWL_API_KEY) in `.env`, not committed
  - Test: Query email from DB; verify it's encrypted (not plaintext)

- [ ] **HTTPS enforced (production only)**
  - Check: `CORS_ALLOWED_ORIGINS` in production uses `https://`
  - Check: Redirect HTTP → HTTPS configured (reverse proxy or app)

- [ ] **Data minimization**
  - Check: Only collect data needed for functionality
  - Check: User can view/delete their data (GDPR)
  - Test: Request `/api/v1/users/{user_id}` returns user's data

- [ ] **Database access control**
  - Check: Non-root user for app DB connection (not `root:root`)
  - Check: DB backups encrypted or stored securely
  - Check: Automatic backups configured (recovery plan)

---

## 3. API Security

- [ ] **Input validation**
  - Check: All endpoints validate input (Pydantic models)
  - Check: No SQL injection (using SQLAlchemy ORM, parameterized queries)
  - Test: Send malicious SQL in query params; verify rejected

- [ ] **Output escaping**
  - Check: All user data displayed in HTML is escaped
  - Check: Frontend uses `htmlspecialchars()` in PHP
  - Test: Insert `<script>alert('xss')</script>` in alert name; verify escaped

- [ ] **CORS configured correctly**
  - Check: `CORS_ALLOWED_ORIGINS` lists only trusted domains
  - Check: `*` not used in production (test-only)
  - Test: Request from different origin fails (preflight denied)

- [ ] **API key rotation policy**
  - Check: Plan for rotating LLM_API_KEY, FIRECRAWL_API_KEY, JWT_SECRET_KEY
  - Document: How to safely rotate without downtime

- [ ] **Error messages don't leak info**
  - Check: 5xx errors don't expose stack traces to client
  - Check: Auth errors don't reveal if user exists
  - Test: Login with invalid email; message is generic

---

## 4. Frontend Security

- [ ] **No secrets in frontend code**
  - Check: No API keys, database URLs, passwords in JavaScript/CSS/HTML
  - Check: Config reads from `config.local.php` (server-side only)
  - Test: Inspect network requests; no credentials visible

- [ ] **Content Security Policy (CSP) optional but recommended**
  - Add header: `Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'`
  - Test: Inline `<script>` blocked if CSP is strict

- [ ] **X-Frame-Options prevents clickjacking**
  - Add header: `X-Frame-Options: DENY`
  - Test: Try to embed page in `<iframe>` from different origin; fails

- [ ] **X-Content-Type-Options prevents MIME sniffing**
  - Add header: `X-Content-Type-Options: nosniff`

---

## 5. File & Upload Handling

- [ ] **No arbitrary file uploads**
  - Check: App doesn't accept user file uploads (or has strict whitelist)
  - Check: Any allowed uploads are served as attachments, not executed
  - Check: File type validated (MIME type + magic bytes)

- [ ] **No sensitive files exposed**
  - Check: `.env` not in version control
  - Check: `backend/__pycache__`, `node_modules` not served
  - Check: Admin paths protected (e.g., `/admin` requires login)

---

## 6. Logging & Monitoring

- [ ] **Sensitive data not logged**
  - Check: Passwords, API keys, emails NOT logged in plaintext
  - Check: Failed login attempts logged (for audit)
  - Check: Log retention policy defined (e.g., 30 days)

- [ ] **Error reporting safe**
  - Check: Production errors logged to file/sentry (not displayed to user)
  - Check: Stack traces only visible to admins/developers

---

## 7. Dependency Security

- [ ] **Dependencies up-to-date**
  - Run: `pip check` (Python)
  - Run: `npm audit` (JavaScript)
  - Fix: Any high/critical vulnerabilities

- [ ] **Vulnerable package check**
  - Run: `safety check` (checks Python packages against known vulnerabilities)
  - Run: `npm audit fix` (updates vulnerable packages)

---

## 8. Deployment Secrets & Config

- [ ] **Environment variables set for production**
  - [ ] `DATABASE_URL` → production DB (not SQLite)
  - [ ] `JWT_SECRET_KEY` → strong random key (rotate from test key)
  - [ ] `EMAIL_ENCRYPTION_KEY` → securely generated Fernet key
  - [ ] `OPENROUTER_API_KEY` → use secrets manager, not hardcoded
  - [ ] `FIRECRAWL_API_KEY` → use secrets manager
  - [ ] `CORS_ALLOWED_ORIGINS` → production domain only
  - [ ] `SCHEMA_VALIDATION_STRICT` → set to `true` for production

- [ ] **Secrets manager integration**
  - Document: How to fetch secrets (AWS Secrets Manager, GitHub Secrets, etc.)
  - Document: Rotation process for expired secrets

- [ ] **Database migration safety**
  - Check: All migrations are idempotent (can run multiple times safely)
  - Check: Rollback plan documented (how to revert if migration fails)

---

## 9. Privacy & Compliance

- [ ] **Privacy policy exists**
  - Check: Document at `/privacy.md` or `/privacy.php`
  - Check: Covers data collection, retention, deletion, GDPR rights

- [ ] **GDPR compliance**
  - [ ] User can request data export (`/api/v1/users/{user_id}/export`)
  - [ ] User can request data deletion (`/api/v1/users/{user_id}/delete`)
  - [ ] Consent obtained for non-essential cookies/tracking
  - [ ] Data retention policy defined (e.g., delete inactive users after 1 year)

- [ ] **Accessibility (WCAG) & Privacy**
  - Check: No tracking pixels or analytics without consent
  - Check: Focus management doesn't leak user identity

---

## 10. Testing & Verification

### Run Security Tests

```bash
# Python dependency scan
safety check

# Node dependency audit
npm audit

# Linting for obvious issues
pylint backend --disable=all --enable=security
```

### Manual Checks

```bash
# 1. Check for hardcoded secrets
grep -r "password\|api_key\|secret" frontend/web --include="*.php" --include="*.js"

# 2. Verify .gitignore protects secrets
cat .gitignore | grep -E ".env|secrets|private"

# 3. Check database connection string
grep DATABASE_URL backend/.env

# 4. Verify CORS settings
grep CORS_ALLOWED backend/config/settings.py
```

### Security Checklist Commands

```bash
# Run full verification
npm run verify:backend

# Check no secrets committed
git log -p | grep -i "api_key\|password" | head -5

# Check file permissions (Linux/macOS)
ls -la backend/.env
```

---

## 11. Pre-Deployment Checklist

- [ ] All tests passing (`npm run backend:check`)
- [ ] No new security warnings in dependencies
- [ ] `.env` file generated locally; `.env.example` committed (no values)
- [ ] Database migrations tested on staging
- [ ] CORS origins verified for production domain
- [ ] Error handling tested (no stack traces leaked)
- [ ] Backup/recovery plan documented
- [ ] Rollback plan documented
- [ ] Team trained on how to rotate secrets
- [ ] Monitoring/alerting configured (alerts for failed logins, errors)

---

## 12. Post-Deployment

- [ ] Monitor logs for auth/API errors
- [ ] Set up alerts for suspicious activity (multiple failed logins, etc.)
- [ ] Schedule quarterly security reviews
- [ ] Plan for dependency updates (monthly)
- [ ] Collect user feedback on security features (UX of lockouts, warnings, etc.)

---

## 13. Known Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| API key exposed | Medium | High | Use secrets manager; rotate quarterly |
| SQL injection | Low | Critical | Use ORM (SQLAlchemy) + validate input |
| XSS via alert names | Low | Medium | Escape all user output in HTML |
| CSRF attacks | Low | Medium | Use CSRF tokens on all forms |
| Brute-force login | Low | Medium | Rate limiting + account lockout |
| Data breach | Low | Critical | Encrypt sensitive data; regular backups |

---

## 14. Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [CWE: Common Weakness Enumeration](https://cwe.mitre.org/)
- [Python Security Best Practices](https://www.python.org/dev/peps/pep-0476/)
- [Node.js Security Best Practices](https://nodejs.org/en/knowledge/file-system/security/introduction/)

---

## 15. Sign-Off

**Security Reviewer:** ________________  
**Date:** ________________  
**Approved for:** [ ] Testing  [ ] Production  

**Comments:**
```
_______________________________________________________
_______________________________________________________
```

---

**Estimated effort for hardening:** 4–8 hours (review + fixes)  
**Recommended:** Stagger over 2–3 days with team review
