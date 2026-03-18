# PROJECT PROPOSAL

## Project Premise
RiskRadar is an environmental risk awareness platform originally developed as a CMPS 490 mobile project. The CMPS 357 final project extends RiskRadar into a broader full-stack system by introducing a **distinct web-facing experience** while reusing the existing backend, database, and scraper ecosystem.

The premise is to solve a practical usability problem: environmental risk information is often scattered across multiple agencies and presented in ways that are difficult to interpret quickly. By aggregating and interpreting these data sources in one platform, RiskRadar helps users make safer day-to-day and travel decisions.

---

## Project Objectives
1. **Build a unique web-app extension**
   - Implement a web interface that is independent from the original mobile UI.
   - Connect the web frontend to existing backend APIs for alerts, summaries, and user data.

2. **Reuse and extend the current RiskRadar foundation**
   - Leverage existing scrapers, API routes, and database models.
   - Expand capabilities with new analytics and decision-support features.

3. **Deliver meaningful technical complexity beyond CRUD**
   - Add staged intelligence features including risk scoring, prioritization, visualization, and predictive insights.

4. **Improve clarity and accessibility of environmental information**
   - Transform technical environmental data into user-friendly summaries and actionable guidance.

---

## Project Goals (Staged)
### Stage 1: Web-App Extension (Completed)
- Deliver a functional PHP-based web interface with backend integration.
- Provide core RiskRadar features (alerts, summaries, user-facing data) in a usable and consistent web experience.

### Stage 2: Risk Assessment and Alert Prioritization
- Implement a **personal risk scoring engine** based on user location, sensitivities, and environmental conditions.
- Implement **smart alert prioritization** using risk score, distance, severity, and user sensitivity.

### Stage 3: Data Visualization and UX Extension
- Add an **interactive Plotly-based risk map** with zoom, pan, and click-to-detail interactions.
- Improve spatial understanding of environmental conditions across web/mobile surfaces.

### Stage 4: Predictive Analytics and AI-Driven Insights
- Add **24-48 hour predictive environmental risk forecasting** from scraper-derived historical patterns.
- Integrate a **RiskRadar AI Assistant** to interpret conditions, alerts, and travel-risk context in user-friendly language.

---

## Intended Outcomes
- Centralize fragmented environmental information into one decision-support platform.
- Help users act earlier through clearer risk interpretation and near-term forecasting.
- Improve personalization through user-specific scoring and prioritized alerts.
- Establish a scalable architecture that supports continued enhancements across backend intelligence and frontend usability.
