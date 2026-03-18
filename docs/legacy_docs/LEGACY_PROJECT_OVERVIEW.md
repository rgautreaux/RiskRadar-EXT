# RiskRadar — Legacy Project Overview (INFX 490 / CMPS 490)

> **Source:** CMPS490_contents/CMPS490_README.md, CMPS490_docs/INFX490_PROJECT_DESCRIPTION.md,
> CMPS490_docs/TARGET_AUDIENCE.md, CMPS490_docs/AUTHORS.md, CMPS490_docs/UNORGANIZED_PROJECT_NOTES.md

---

## Course Assignment Context

RiskRadar was originally developed as the capstone project for **INFX 490 / CMPS 490 — Senior Project**. The assignment required teams to design, develop, and present a data-driven solution addressing a real-world issue using publicly available datasets, AI/ML tools, and modern application development practices.

**Problem domain:** Environmental Issues (EPA, NOAA, NASA Earth Data)

**Key deliverables per the assignment:**
1. Project Proposal & Implementation Strategy — defined problem, target audience, scope, and MVP
2. Data Analysis & AI/ML Integration — data exploration, preprocessing, modeling, use of AI/ML frameworks
3. Functional Prototype — web/mobile application with modern UI/UX, adherence to data privacy and security standards
4. Collaboration & Facilitation — evidence of stakeholder collaboration
5. Final Presentation — executive-level presentation, business objective, methodology, MVP demo, recommendations

---

## Project Description

RiskRadar is an environmental alert monitoring and AI-powered summarization platform designed to help users identify and manage potential environmental conditions and risks they may encounter while traveling or during day-to-day activities.

**Core features:**
- Real-time alerts aggregated from government APIs (weather, air quality, pollution, wildfire, earthquakes)
- AI-generated 5-minute human-readable summaries (digests) of recent alerts
- Location-based filtering by ZIP code
- User-configurable alert type and severity preferences
- Mobile push notification delivery

The app scrapes real-time data from government APIs and websites, stores alerts in a local database, and uses LLMs to generate daily digests.

---

## Target Audience

### Primary Audiences

**Travelers**
- Individuals planning trips who need consolidated risk and weather information for their destinations
- Needs: weather forecasts, travel advisories, natural disaster alerts for specific regions
- Value: aggregated, AI-summarized risk data saves time versus checking multiple sources manually

**Truckers & Transportation Professionals**
- Commercial drivers and logistics operators who depend on weather and road conditions for safe, efficient routing
- Needs: real-time weather alerts along routes, severe weather warnings, regional risk summaries
- Value: timely, location-aware notifications help avoid hazardous conditions and plan alternate routes

**Industry & Construction Owners**
- Business owners and project managers whose operations are affected by environmental conditions
- Needs: weather forecasts for project sites, risk assessments for outdoor operations, historical trend data
- Value: data-driven scheduling and risk mitigation reduces weather-related delays and costs

### Secondary Audience

**General Public** — everyday users who want quick, reliable risk and weather information for their area. Expanding fully to serve the general public significantly increases scope; the MVP was scoped to one or two primary audiences first.

### Audience-Driven Design Decisions

| Decision | Rationale |
|---|---|
| Location by ZIP code only | Minimizes personal data collection while enabling regional alerts |
| Configurable alert types | Different audiences care about different risk categories |
| Quiet hours for notifications | Professionals need control over when they receive alerts |
| AI-generated summaries | All audiences benefit from concise, actionable insights over raw data |
| Mobile push notifications | Truckers and travelers need alerts while on the move |

---

## Team Members

| Name | ULID | Role | Email |
|---|---|---|---|
| Qui Huynh | C00405970 | Backend Developer | — |
| Noah Benoit | C00397372 | Security Lead | njbenoit1@gmail.com |
| Ben Manuel | C00477234 | Frontend Developer | — |
| Max Compeaux | C00513380 | AI Backend Developer | maxcompeaux@gmail.com |
| Rebecca Gautreaux | C00460817 | Database Administrator | rebecca.gautreaux@gmail.com |
| Celeste George | C00465845 | Frontend Developer | Celeste12204@gmail.com |

---

## Early Planning Notes

The following were the unresolved questions and action items from initial project scoping:

**Open questions at project start:**

1. **User Privacy** — Only ask users for ZIP/area code. No cookies for tracking. No user accounts (this changed; accounts were added for preferences/notifications).
2. **Self-Sustainability** — One-time payment vs. subscription model considered but not decided. Both require some form of user record-keeping.
3. **Target Audience** — Narrowed to travelers, truckers, and industry owners; general public acknowledged as too broad for MVP.

**Initial action items:**
1. Narrow scope, write user stories
2. Define system architecture and best practices
3. Complete Security Questionnaire
4. Research AI tools (work trees)
5. Identify security best practices

---

## Potential Data Sources Researched

### Global & Intergovernmental
- World Bank Open Data — climate, energy, and environmental indicators
- UN Environment Programme — global environmental reports
- Global Carbon Project — CO₂ and greenhouse gas emissions

### Climate & Atmosphere
- Berkeley Earth — global temperature records
- Copernicus Climate Change Service — European climate monitoring
- CO₂.Earth — real-time atmospheric CO₂ tracking

### Land, Oceans & Biodiversity
- Global Forest Watch — deforestation and forest cover data
- GBIF (Global Biodiversity Information Facility) — species occurrence
- Ocean Health Index — marine ecosystem health metrics

### Air & Water Quality
- OpenAQ — open-source, real-time global air quality data (API-ready)
- World Resources Institute: Aqueduct — global water risk and stress data

> The final implemented data sources are: NOAA/NWS, AirNow, EPA, USGS, and Firecrawl. See [LEGACY_ARCHITECTURE_TECH_STACK.md](LEGACY_ARCHITECTURE_TECH_STACK.md) for details.
