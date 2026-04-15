# RiskRadar — GDPR & CCPA Compliance Review

**Prepared by:** Noah Benoit (Security Lead)
**Date:** April 15, 2026
**Prior Review:** March 22, 2026 (`GDPR_CCPA_COMPLIANCE_REVIEW_3_22_26.md`)
**Scope:** User data collection, storage, processing, and rights obligations under GDPR and CCPA
**Codebase Branch:** Noah-Benoit-Work-Branch (includes PR #73 merge from main, April 15, 2026)

---

## Overview

This review updates the March 22, 2026 compliance assessment to reflect the current state of the codebase following the latest sprint merges. Since the prior review, the team has made meaningful progress: email encryption has been implemented using AES-CBC with HMAC-based uniqueness lookups, notification channels have been expanded, and input validation has been strengthened. However, several compliance gaps remain open, and the email encryption implementation has two cryptographic flaws that must be resolved before the protection is considered effective. Two new data concerns have also been identified.

---

## What Changed Since the March 22 Review

| Area | Change | Compliance Impact |
|---|---|---|
| Email storage | Encrypted with AES-CBC; HMAC used for lookups | GDPR Art. 32 — **partially resolved** (crypto issues remain — see below) |
| Notification channels | `notify_push`, `notify_email`, `notify_sms` columns added to `users` | New data categories added to inventory |
| Schema normalization | `Location`, `UserAlertTypePreference`, `SummaryAlert`, `AlertRawPayload` tables added | Data model complexity increased; deletion scope now wider |
| Notification dispatch logging | `NotificationDispatchLog` referenced — records who was notified and by whom | New PII processing; requires Privacy Policy disclosure |
| Registration UI | Terms of Service / Privacy Policy links visible in `registration.tsx` | Consent UI present but links are dead — content still absent |
| Input validation | Email regex and password minimum added to schemas | Minor improvement to data quality |
| CORS | Now configurable via `CORS_ALLOWED_ORIGINS` env var | Still defaults to `*` if not set — partially addressed |

---

## Updated Data Inventory

| Category | Data Points | Storage Location | Sensitivity | Change Since 3/22 |
|---|---|---|---|---|
| Account | Encrypted email (`email_encrypted`) | `users.email_encrypted` (AES-CBC) | HIGH — PII | **Updated** — no longer plaintext for new users |
| Account | Email HMAC for uniqueness lookup | `users.email_hmac` | MEDIUM — not reversible alone | **New** |
| Account | Legacy plaintext email (migration in progress) | `users.email` (nullable) | HIGH — PII | Deprecated; not removed yet |
| Account | Hashed password | `users.password_hash` (bcrypt) | MEDIUM — stored safely | Unchanged |
| Identity | Display name | `users.display_name` (plaintext) | LOW–MEDIUM | Unchanged |
| Location | ZIP code, latitude, longitude | `users.zip_code`, `users.latitude`, `users.longitude` | MEDIUM — PII when combined | Unchanged |
| Location | Normalized location records | `locations` table | MEDIUM | **New** |
| Device | Push notification token | `users.device_token` | MEDIUM — device identifier | Unchanged |
| Preferences | Alert type preferences (junction table) | `user_alert_type_preferences` | LOW | **New** — moved from JSON column |
| Preferences | Notification channel flags | `users.notify_push`, `users.notify_email`, `users.notify_sms` | LOW | **New** |
| Preferences | Severity filter | `users.notify_severity` | LOW | Unchanged |
| Operational | Notification dispatch records | `notification_dispatch_log` | MEDIUM — links users to alerts | **New** — see note below |
| Environmental | Alerts and AI summaries | `alerts`, `summaries` tables | LOW — public data | Unchanged |

> **Note on `notification_dispatch_log`:** This table records `initiated_by_user_id`, `provider`, `recipients_total`, `sent_count`, `failed_count`, and `status` for every notification dispatch. It establishes a linkage between users and alert events — which users were targeted, who triggered the notification, and via what channel. This constitutes behavioral/operational PII under GDPR and must be disclosed in the Privacy Policy and included in any erasure or export response.

---

## GDPR Analysis

### Lawful Basis for Processing (Article 6)

GDPR requires a documented lawful basis for each type of personal data processing.

**Current status:** The registration screen (`frontend/RiskRadar/app/auth/registration.tsx`) now renders "Terms of Service" and "Privacy Policy" as tappable link text in the registration flow. This is a positive step. However, the links are not connected to any actual documents — tapping them does nothing. No Terms of Service or Privacy Policy content exists in the repository.

**Remaining gap:** The consent mechanism is cosmetic. Users cannot read what they are agreeing to. Displaying non-functional privacy links may itself create legal exposure by implying consent that cannot be meaningfully given.

**Action required:**
- Draft a Privacy Policy that covers all data types in the updated inventory above (including `notification_dispatch_log` and encrypted email storage).
- Draft Terms of Service.
- Connect both links in `registration.tsx` to actual content (e.g., an in-app modal or hosted URL).
- Ensure the registration form requires affirmative acknowledgment (checkbox) before account creation, not just passive display.

---

### Data Minimization (Article 5(1)(c))

GDPR requires that only the minimum data necessary for the stated purpose is collected.

**Current status:** Data collection remains largely proportionate to the app's purpose. The new `notification_dispatch_log` table, however, stores `initiated_by_user_id` and `recipients_total` even when the notification provider is `noop` (i.e., no actual notification was sent). Logging operational data for non-events has a weak justification under data minimization.

**Potential gap:** The `notify_email` and `notify_sms` flags are stored on the User model, but neither email-based nor SMS-based notification delivery is currently implemented. Collecting consent-like flags for unimplemented features should be evaluated against Article 5(1)(c).

**Action required:** Document the business justification for `notification_dispatch_log` records in the Privacy Policy. Evaluate whether SMS/email notification fields should be omitted until those channels are actually built.

---

### Right to Erasure / Right to be Forgotten (Article 17)

Users have the right to request deletion of all their personal data.

**Current status:** There is still no `DELETE /users/me` endpoint in `backend/api/users.py`. This gap was identified in the March 22 review and **remains unresolved**.

**Scope has expanded:** Since March 22, deletion must now also cover:
- `users.email_encrypted` and `users.email_hmac`
- `user_alert_type_preferences` (linked by user FK)
- `notification_dispatch_log` records where `initiated_by_user_id` matches the user

**Action required (assigned to Qui):** Implement `DELETE /users/me` that either hard-deletes all PII or anonymizes it (nulling PII columns while retaining aggregate rows for operational logs). Ensure all tables in the expanded scope are included.

---

### Data Portability (Article 20)

Users have the right to receive a copy of their personal data in a portable format.

**Current status:** There is still no `GET /users/me/export` endpoint. This gap was identified in the March 22 review and **remains unresolved**. The expanded data model (preferences junction table, dispatch logs) means the export scope is wider than previously documented.

**Action required:** Implement a `GET /users/me/export` endpoint returning all user-linked data as JSON, including the decrypted email, preferences, notification settings, and a count of dispatch log entries.

---

### Security of Processing (Article 32)

GDPR requires that personal data be protected with appropriate technical measures.

**Current status — improvements:**
- Passwords: bcrypt hashing — **compliant**
- Email: AES-CBC encryption now implemented for new registrations — **improvement over plaintext**
- CORS: Now configurable via environment variable — **partial improvement**

**Current status — remaining issues:**

1. **Fixed AES initialization vector (CRITICAL):** The email encryption uses `_EMAIL_AES_IV = b"RiskRadarEmailIV"` — a static, hardcoded 16-byte IV. With AES-CBC, using the same IV for every encryption means two users with the same email address (or any re-encrypted email) produce identical ciphertexts. This leaks equality information and makes the encryption deterministic rather than semantically secure. The code comment acknowledges this is only appropriate for demo use. This must be fixed before encrypted emails can be considered protected under Article 32.

2. **JWT secret reused as AES encryption key source:** The AES key for email encryption is derived by computing `SHA-256(JWT_SECRET_KEY)`. This means a single compromised environment variable exposes both authentication token signing and email decryption. Key separation is a fundamental requirement under Article 32's principle of appropriate technical measures.

3. **Legacy plaintext email column still present:** `users.email` remains in the schema (nullable, marked deprecated). Until the migration completes and this column is dropped, the old plaintext email values remain accessible.

4. **JWT secret has hardcoded fallback default:** `JWT_SECRET_KEY` defaults to `"CHANGE-ME-set-a-real-secret-in-dotenv"` if `.env` is absent — a publicly known string that invalidates all token security.

5. **HTTP in production (frontend):** `API_BASE_URL` in the frontend uses `http://`, transmitting encrypted-at-rest data (including login credentials and tokens) in cleartext over the network.

**Action required:**
- Fix AES-CBC IV to use `os.urandom(16)` per encryption call (resolves GDPR Art. 32 gap on email encryption).
- Introduce a separate `EMAIL_ENCRYPTION_KEY` environment variable (resolves key-reuse issue).
- Complete the email migration and drop the plaintext `users.email` column.
- Remove the fallback default from `JWT_SECRET_KEY`.
- Enforce HTTPS in production (redirect HTTP → HTTPS).

---

### Data Breach Notification (Article 33)

In the event of a data breach, GDPR requires notification to the supervisory authority within 72 hours.

**Current status:** No breach response procedure has been drafted. The `KEY_MANAGEMENT_PLAN.md` covers key rotation procedures, which is the correct starting point, but a dedicated incident response plan has not been added to the repository.

**Changed risk profile:** With email addresses now stored encrypted, a database breach no longer exposes plaintext emails — provided the AES IV and key reuse issues are resolved first. If they are not resolved, a breach would expose all emails through the deterministic ciphertext. The JWT secret exposure via git history (see Security Report C-02) means an attacker with the codebase and database could currently decrypt all stored emails.

**Action required:** Draft a breach response procedure documenting notification contacts, the 72-hour GDPR timeline, affected data categories, and remediation steps. Reference `KEY_MANAGEMENT_PLAN.md` for the rotation component.

---

## CCPA Analysis

CCPA applies to for-profit businesses meeting certain size thresholds. As a student capstone project, RiskRadar does not currently meet those thresholds. Compliance is documented for production readiness.

### Key CCPA Rights — Updated Status

| Right | Prior Status (3/22) | Current Status (4/15) | Gap |
|---|---|---|---|
| Right to Know (what data is collected) | No Privacy Policy | Links present in UI but content absent | Draft and publish Privacy Policy |
| Right to Delete | No deletion endpoint | **Still no deletion endpoint** | Implement DELETE endpoint — priority unchanged |
| Right to Correct | Not assessed | No correction flow beyond full preference update | Consider PUT /users/me for basic corrections |
| Right to Opt-Out of Sale | N/A | N/A — RiskRadar does not sell user data | Document this explicitly in Privacy Policy |
| Right to Non-Discrimination | N/A | N/A — no tiered access model | No action needed |
| Right to Know (automated decisions) | Not assessed | AI summaries generated from user location data | Disclose LLM processing in Privacy Policy |

> **New CCPA consideration:** RiskRadar now uses an LLM to generate location-based summaries based on the user's zip code. CCPA requires disclosure of the categories of personal information used in automated processing and the business purpose for that processing. This should be added to the Privacy Policy.

---

## Compliance Gaps Summary

| Gap | Regulation | Severity | Status vs. 3/22 | Owner |
|---|---|---|---|---|
| No Privacy Policy content (UI links are dead) | GDPR Art. 6, CCPA | HIGH | **Unchanged** | Team; Noah to review |
| Fixed AES IV in email encryption | GDPR Art. 32 | HIGH | **New** | Qui, Noah |
| JWT secret reused as AES key source | GDPR Art. 32 | HIGH | **New** | Qui, Noah |
| No user deletion endpoint | GDPR Art. 17, CCPA | HIGH | **Unchanged** | Qui |
| JWT secret has hardcoded default fallback | GDPR Art. 32 | HIGH | Unchanged | Qui, Noah |
| Legacy plaintext `users.email` column not yet removed | GDPR Art. 32 | HIGH | **New** | Qui |
| No data export endpoint | GDPR Art. 20 | MEDIUM | Unchanged | Qui |
| CORS still defaults to wildcard | GDPR Art. 32 | MEDIUM | **Partially addressed** — env var added, default unchanged | Qui |
| HTTP used in frontend (no TLS) | GDPR Art. 32 | MEDIUM | Unchanged | Qui, Noah |
| No rate limiting on login | GDPR Art. 32 | MEDIUM | Unchanged | Qui |
| `notification_dispatch_log` not disclosed in Privacy Policy | GDPR Art. 5, CCPA | MEDIUM | **New** | Team; Noah to review |
| `notification_dispatch_log` not included in erasure scope | GDPR Art. 17 | MEDIUM | **New** | Qui |
| LLM processing of location data not disclosed | GDPR Art. 22, CCPA | MEDIUM | **New** | Team; Noah to review |
| No breach response procedure | GDPR Art. 33 | MEDIUM | Unchanged | Noah |
| `notify_email`/`notify_sms` flags collected for unbuilt features | GDPR Art. 5 | LOW | **New** | Team |

---

## Recommended Compliance Roadmap

**Immediate (before any public-facing deployment):**
1. Fix AES-CBC fixed IV → use `os.urandom(16)` per call
2. Introduce separate `EMAIL_ENCRYPTION_KEY` env var
3. Complete email encryption migration; drop `users.email` plaintext column
4. Remove hardcoded `JWT_SECRET_KEY` default
5. Implement `DELETE /users/me` endpoint (include all new tables in scope)

**Pre-launch (required for compliance):**
6. Draft and publish Privacy Policy — must cover: encrypted email, location data, notification dispatch log, LLM processing, data retention periods
7. Activate consent checkbox in registration UI (currently dead links)
8. Remove CORS `*` default; require explicit origins in `.env`
9. Enforce HTTPS/TLS in production environment

**Shortly after launch:**
10. Implement `GET /users/me/export` data portability endpoint
11. Add rate limiting on `/users/login` and `/users/register`
12. Draft breach response procedure and store in `docs/SecurityDocs/`
13. Evaluate whether `notify_email`/`notify_sms` fields should be deferred until those channels are built
14. Add LLM processing disclosure to Privacy Policy

---

## Items Resolved Since March 22

| Prior Gap | Resolution |
|---|---|
| Email stored in plaintext | AES-CBC encryption implemented for new registrations via `email_encrypted` + `email_hmac` columns. Crypto issues (IV, key reuse) remain — see GDPR Art. 32 section above. |

---

*This review was prepared as part of the RiskRadar User Security Plan. It reflects the state of the codebase as of April 15, 2026 (Noah-Benoit-Work-Branch, post PR #73 merge) and is intended as a planning document for the team — not legal advice.*
