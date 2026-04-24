# Proposal Repository Summary

## Project
- Repo: cmps-357-sp26-final-project-cmps357-team-3
- Description: Project Title: RiskRadar Web Personalized Environmental Risk Intelligence Platform

## Proposed Tech Stack / Architecture
- React
- Flask
- PostgreSQL

## Major Features Planned
- Build a web dashboard that aggregates weather, air-quality, and pollution inputs into a single personalized risk view.
- Implement an alert prioritization engine that ranks environmental hazards by user profile factors such as asthma sensitivity, pollen response, and heat risk.
- Show explainable scoring details so users can understand why each alert was ranked and what inputs drove the score.
- Add mapped and historical views of risk trends, with predictive forecasting as a stretch feature when core functionality is complete.


## Data Structures / Algorithms Proposed
- A user profile object and preference map store triggers like asthma, pollen sensitivity, and heat tolerance to parameterize risk calculations.
- Time-series arrays store hourly and daily environmental inputs so the system can compute trend-aware risk instead of one-point snapshots.
- A weighted scoring algorithm combines weather, air-quality, and pollution signals into a single personalized risk score.
- Priority sorting ranks alerts by score and recency so the most relevant hazards appear first on the dashboard.
- If forecasting is enabled, rolling-window smoothing is used to estimate near-future risk for map and trend views.

