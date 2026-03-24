# RiskRadar Security Documentation

This directory contains security documentation for the RiskRadar Web Application. All documents are aligned with OWASP Top 10, NIST, and GDPR requirements.

## Contents
- **Web_App_Security_Questionnaire.md** — Checklist for web-app security controls and compliance
- **Web_App_SBOM.md** — Software Bill of Materials for the web-app
- **Web_App_Threat_Model.md** — Threat model and mitigations for the web-app
- [Other security docs as needed]

## How to Use
- Review the questionnaire to assess security posture and identify gaps
- Use the SBOM to track dependencies and support vulnerability management
- Reference the threat model to understand risks and implemented controls

## Update Policy
- Update these documents with each major release or when significant changes are made to the web-app
- Review for compliance with OWASP Top 10, NIST, and GDPR at least annually

## Related Files
- `frontend/web/README.md` — Web-app architecture and setup
- `backend/requirements.txt` — Backend dependencies
- `docs/PLANNING_DOCS/` — Planning and implementation details
- `README.md`, `STAGES.md` — Project-level documentation

## Web-App Security Controls Summary

The RiskRadar web-app implements robust security controls, including:
- Input validation and output escaping (PHP service and template layers)
- CSRF protection for all state-changing requests
- Allowlist-based query/form parameter validation
- Defensive error handling and fallback rendering
- Secure API integration with safe handling of timeouts, non-2xx, and malformed responses
- No secrets or credentials exposed in frontend code
- All controls and requirements are documented in planning and implementation docs

See also: frontend/web/README.md, api_client.php, docs/PLANNING_DOCS/PLANNING_STAGES.md, docs/STAGES.md
