# RiskRadar Specification

---

## Project Overview

RiskRadar is an AI-driven data analytics platform that aggregates, analyzes, and presents risk-related information from publicly available data sources. It addresses the challenge of extracting actionable insights from complex, scattered datasets by combining automated web scraping, AI-powered summarization, and a user-friendly dashboard.

**Domain**: Environmental Issues / Public Health (weather-related risk data)

---

## Functional Requirements

### FR-1: Data Ingestion

- **FR-1.1**: The system shall scrape configured external sources on a recurring schedule using Firecrawl.
- **FR-1.2**: The system shall store raw and processed article content in the database.
- **FR-1.3**: The system shall log each scrape run with status, duration, and article/alert counts.
- **FR-1.4**: The system shall support adding, removing, and deactivating sources without code changes.

### FR-2: Alert Management

- **FR-2.1**: The system shall generate alerts from scraped data, classified by type and severity.
- **FR-2.2**: The system shall associate alerts with geographic locations (latitude/longitude and location name).
- **FR-2.3**: The system shall link alerts to their source articles.

### FR-3: AI-Powered Analysis

- **FR-3.1**: The system shall generate summaries of alerts and articles using the OpenAI API.
- **FR-3.2**: The system shall track which AI model was used and token consumption for each summary.
- **FR-3.3**: The system shall support regional summary generation aggregating multiple alerts.

### FR-4: User Management

- **FR-4.1**: The system shall support user registration with email and password.
- **FR-4.2**: The system shall allow users to set location preferences via zip code.
- **FR-4.3**: The system shall allow users to select preferred alert types and categories.
- **FR-4.4**: The system shall track user reading history and progress per article.

### FR-5: Notifications

- **FR-5.1**: The system shall support push notifications via device tokens (iOS and Android).
- **FR-5.2**: The system shall allow users to configure notification preferences (enable/disable, daily digest, quiet hours).
- **FR-5.3**: The system shall filter notifications by severity based on user preferences.

### FR-6: Front-End Dashboard

- **FR-6.1**: The system shall display alerts and articles in an interactive React-based dashboard.
- **FR-6.2**: The system shall support categorization and tagging for filtering content.
- **FR-6.3**: The system shall present AI-generated summaries alongside source data.

---

## Non-Functional Requirements

### NFR-1: Security

- **NFR-1.1**: User passwords shall be stored as hashes, never in plaintext.
- **NFR-1.2**: Data access policies shall be enforced via Antimatter, independent of storage infrastructure.
- **NFR-1.3**: The system shall not use tracking cookies or collect data without user consent.

### NFR-2: Performance

- **NFR-2.1**: Scrape jobs and AI processing shall run asynchronously via RabbitMQ to avoid blocking the main application thread.
- **NFR-2.2**: The database shall use appropriate indexes for frequently queried columns.

### NFR-3: Portability & Deployment

- **NFR-3.1**: All services shall be containerized with Docker for consistent cross-platform deployment.
- **NFR-3.2**: The system shall support local development via XAMPP (Apache + phpMyAdmin).

### NFR-4: Data Privacy

- **NFR-4.1**: The system shall collect only the minimum user data required (zip/area code for location).
- **NFR-4.2**: The system shall comply with data privacy best practices as outlined in the project security questionnaire.

### NFR-5: Maintainability

- **NFR-5.1**: The codebase shall separate front-end (React), back-end (Python), and database concerns.
- **NFR-5.2**: External API integrations shall be modular and replaceable.

---

## MVP Scope

The minimum viable product includes:

1. Automated scraping of at least one configured source
2. Alert generation with type, severity, and location
3. AI-generated summaries of collected alerts
4. User registration with location-based preferences
5. React dashboard displaying alerts, articles, and summaries
6. Docker-based deployment

---

## Out of Scope (Future Considerations)

- Payment/subscription model (see [UNORGANIZED_PROJECT_NOTES.md](UNORGANIZED_PROJECT_NOTES.md))
- Real-time streaming alerts (current design is poll-based)
- Mobile-native applications (current front end is web-based React)