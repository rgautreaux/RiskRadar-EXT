# RiskRadar Architecture

---

## System Overview

RiskRadar follows a three-tier architecture:

```
┌──────────────┐     ┌──────────────────────────────────────┐     ┌────────────┐
│              │     │           Back End (Python)          │     │            │
│  Front End   │────>│                                      │────>│  MariaDB   │
│   (React)    │<────│  ┌────────────┐   ┌───────────────┐  │<────│  Database  │
│              │     │  │ Firecrawl  │   │  OpenAI API   │  │     │            │
└──────────────┘     │  │ (Scraping) │   │  (Summaries)  │  │     └────────────┘
                     │  └────────────┘   └───────────────┘  │
                     │         │                            │
                     │         ▼                            │
                     │    ┌──────────┐                      │
                     │    │ RabbitMQ │                      │
                     │    │ (Queue)  │                      │
                     │    └──────────┘                      │
                     └──────────────────────────────────────┘
                                    │
                                    ▼ 
                            ┌────────────────┐
                            │   Antimatter   │
                            │ (Data Security │
                            │   & Access)    │
                            └────────────────┘
```

### Data Flow

1. **Scraping**: The Python back end uses **Firecrawl** to crawl configured sources on a schedule, producing raw articles and alerts.
2. **Queuing**: Scrape jobs and AI processing tasks are dispatched via **RabbitMQ**, decoupling ingestion from analysis.
3. **Analysis**: The **OpenAI API** generates summaries and extracts risk insights from collected articles and alerts.
4. **Storage**: Processed data is persisted in **MariaDB** (`riskradar_db`).
5. **Security**: **Antimatter** enforces access policies and encryption on stored and transmitted data.
6. **Presentation**: The **React** front end fetches data from the Python API and renders the dashboard.

### Deployment

All services are containerized with **Docker** and orchestrated via Docker Compose. During local development, **Apache** (via XAMPP) serves as the web server with **phpMyAdmin** for database administration.

---

## Database Architecture

RiskRadar uses a MariaDB 10.4 relational database (`riskradar_db`) consisting of 13 tables organized into four functional groups: **Content**, **Users**, **Alerts & AI**, and **Operations**.

For full schema documentation including table definitions, entity relationships, normalization analysis, and known issues, see [DATA_MODEL.md](DATA_MODEL.md).
