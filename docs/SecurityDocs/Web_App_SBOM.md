# RiskRadar Web-App Software Bill of Materials (SBOM)

This SBOM lists all major components, libraries, and dependencies used in the RiskRadar Web Application. It is intended to support vulnerability management, compliance, and supply chain transparency.

## Application Overview
- **Frontend:** PHP (custom), HTML, CSS, JavaScript
- **Backend API:** FastAPI (Python)
- **Database:** SQLite (dev), PostgreSQL (prod)
- **Other:** RabbitMQ (messaging), Docker (deployment)

## PHP Web Frontend
- PHP 8.x
- Composer (dependency manager)
- [List any PHP libraries or frameworks used, e.g., Slim, Laravel, etc.]
- Custom code: `frontend/web/`

## JavaScript (if used)
- [List any JS libraries, e.g., jQuery, Axios, etc.]

## Python Backend (API)
- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic
- slowapi (rate limiting)
- [Other libraries: see backend/requirements.txt]

## Infrastructure
- Docker
- RabbitMQ
- Nginx/Apache (if used)

## Security & Compliance
- All dependencies are tracked in `backend/requirements.txt` and `composer.json` (if used)
- Dependencies are updated regularly and scanned for vulnerabilities
- SBOM is reviewed and updated with each major release

---

**Instructions:**
- Update this SBOM whenever dependencies change.
- For a full list, see `backend/requirements.txt` and any PHP/JS package files.
- Consider using automated SBOM tools (e.g., CycloneDX, Syft) for future updates.
