# RiskRadar Web-App Security Questionnaire

This questionnaire is designed to assess the security posture of the RiskRadar Web Application. It is mapped to OWASP Top 10, NIST, and GDPR requirements.

## 1. Input Validation & Output Escaping
- Are all user inputs validated and sanitized on the server side? (OWASP A1, NIST SI-10)
- Are allowlists used for form/query parameters where possible?
- Is output escaping applied to all dynamic content in templates? (OWASP A7)

## 2. Authentication & Session Management
- Is authentication required for sensitive actions? (OWASP A2, NIST IA-2)
- Are passwords stored using a slow hash (bcrypt/Argon2) with salt? (OWASP A2, NIST IA-5)
- Are session tokens random, unique, and securely stored? (OWASP A2)
- Is session timeout enforced?

## 3. Access Control
- Are authorization checks enforced on all endpoints? (OWASP A5, NIST AC-3)
- Are sensitive resources protected from direct object reference attacks?

## 4. CSRF & CORS
- Is CSRF protection implemented for all state-changing requests? (OWASP A8)
- Is CORS configured to allow only trusted origins? (OWASP A8)

## 5. Error Handling & Logging
- Are error messages generic and free of sensitive information? (OWASP A6)
- Are security-relevant events logged and monitored? (NIST AU-2, AU-6)

## 6. Secure Configuration
- Are secrets (API keys, DB credentials) stored outside source code? (OWASP A6, NIST CM-6)
- Are default credentials removed/changed?
- Is HTTPS enforced in production?

## 7. Rate Limiting & Abuse Prevention
- Is rate limiting applied to authentication and sensitive endpoints? (OWASP A4)
- Are automated abuse and brute-force attacks detected and mitigated?

## 8. Privacy & Compliance
- Is user data collection minimized and documented? (GDPR Art. 5)
- Are users informed about data usage and consent obtained? (GDPR Art. 7, 13)
- Can users request data deletion or export? (GDPR Art. 15, 17)

## 9. Dependency & Vulnerability Management
- Are dependencies regularly updated and scanned for vulnerabilities? (OWASP A9)
- Is an SBOM maintained for the web-app?

## 10. Threat Modeling & Review
- Has a threat model been created and reviewed for the web-app?
- Are security docs and controls reviewed periodically?

---

**Instructions:**
- For each item, provide evidence or a link to the relevant code, configuration, or documentation.
- Mark N/A if not applicable, and explain why.
