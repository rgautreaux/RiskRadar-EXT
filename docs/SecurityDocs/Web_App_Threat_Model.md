# RiskRadar Web-App Threat Model

This document identifies and analyzes security threats to the RiskRadar Web Application, and documents mitigations in place. It is aligned with OWASP Top 10, NIST, and GDPR requirements.

## 1. Assets
- User data (profile, preferences, risk scores)
- Alert and summary data
- Authentication/session tokens
- API keys and secrets

## 2. Entry Points
- Web forms (registration, profile, preferences)
- API endpoints (alerts, summaries, users)
- Static assets (JS, CSS, images)

## 3. Trust Boundaries
- Browser ↔ Web server
- Web server ↔ API backend
- API backend ↔ Database

## 4. Attacker Goals
- Steal or modify user data
- Gain unauthorized access (privilege escalation)
- Disrupt service (DoS)
- Abuse APIs (scraping, brute-force)
- Exfiltrate sensitive data (GDPR violation)

## 5. Threats & Mitigations (STRIDE)
| Threat | Example | Mitigation |
|--------|---------|------------|
| Spoofing | Fake login, session hijack | CSRF tokens, secure session cookies, authentication checks |
| Tampering | Malicious input, API abuse | Input validation, output escaping, allowlists |
| Repudiation | Deny actions | Audit logging, traceable user actions |
| Information Disclosure | Data leak, verbose errors | Output sanitization, generic error messages, access controls |
| Denial of Service | Flooding, abuse | Rate limiting, resource quotas, fallback handling |
| Elevation of Privilege | Bypass auth, direct object access | Authorization checks, least privilege, endpoint validation |

## 6. Compliance Risks
- GDPR: Data minimization, user consent, right to erasure/export
- NIST: Access control, audit, secure configuration
- OWASP: Top 10 risks addressed in code and docs

## 7. Open Issues / To-Do
- Migrate password hashing to bcrypt/Argon2
- Restrict CORS origins before production
- Implement rate limiting on sensitive endpoints
- Periodic review of dependencies and SBOM

---

**Instructions:**
- Update this threat model as the web-app evolves.
- Link to evidence in code/docs for each mitigation.
- Review at least once per major release.
