# CMPS 357 - Final Project - Group 3

Due Date: May 6, 2026, 12:55 CST

This repository contains the code and documentation for Group 3's CMPS 357 final project. The primary objective is to build a meaningful extension of our CMPS 490 RiskRadar senior project with new web-facing capabilities and advanced decision-support features.

Our senior project focuses on developing **RiskRadar**, an environmental risk awareness platform that helps residents and travelers identify and manage potential environmental risks using data analytics.

Our goal for the CMPS 357 final project is to build a unique web-app extension with a distinct frontend interface while extending the platform with features such as personalized risk assessment, interactive mapping, and predictive/AI-supported insights.

---

# CMPS 357 Extension Project Proposal


## Initial Plan:

**Web-App Extension of our RiskRadar Mobile App**
Our initial idea was to create a web-app extension of our RiskRadar mobile app. This is because we thought a web extension would be a more straightforward extension of our mobile app, and would allow us to leverage the same backend we constructed and utilize the same data sources. 

However, our professor suggested we go the Web Extension route *only* if we do **NOT** pivot to a Web-app in CMPS490. If we *do* create a web app extension, then it was reccomended that we implement an entirely new and unique frontend than that of the Mobile App so that we do not have to worry about relying on our CMPS490 frontend and have to wait for them to complete their frontend work before we can start our work for this project.  This ensures a level of independence between the two projects and allows us to work on our project without having to worry about the progress of the CMPS490 frontend.

However, in case issues arise and we must pivot in CMPS490, we are discussing further extensions we can implement to further differenciate the two projects and ensure that we are not relying too heavily on the CMPS490 project for our work for this one.

## Further Extensions (if we pivot to Web-App in CMPS490):

### Environmental Risk Assessment and Alert Prioritization Extensions

**Personal Risk Scoring Engine (Best Overall Option)**: Create a personalized environmental risk score for each user based on location, health sensitivities, and environmental data

**Smart Alert Prioritization System (Potential Extension of Personal Risk Scoring Engine)**:  Extend alerts into a priority ranking system by:
- Risk Score
- Distance from user
- Severity
- User sensitivity

### Predictive Analytics and AI-Driven Insights Extensions
**Predictive Environmental Risk (AI/Data Extension)**: Predict environmental risk 24–48 hours ahead by referencing the patterns from data obtained by scrapers

**RiskRadar AI Assistant**- AI assistant or guide integrated into the application that helps users interpret environmental conditions, alerts, or travel risks


### Data Visualization and User Experience Extensions
**Interactive Risk Map (Great UI Extension)**- Add a map visualization to the mobile/web app , similar to PA2 as to make the data presented even more user-friendly and accessible

**RiskRadar AI Assistant**- AI assistant or guide integrated into the application that helps users interpret environmental conditions, alerts, or travel risks


## Project Purpose
The goal of this project is to transform RiskRadar into a broader full-stack system by introducing a web application experience that is distinct from the mobile app while reusing the existing backend and data-ingestion foundation. This extension improves how users interpret environmental conditions by combining real-time alerts, AI-generated summaries, staged personalization features, and planned interactive/predictive capabilities.

---

## Team Members, Roles, Responsibilities, and Contributions

| Max                           | (Contributions) |


| Rebecca                           |  (Contributions) |

---

# CMPS 490 Senior Project Contents

## Project Content

### CMPS 490 RiskRadar Mobile App

[RiskRadar Mobile App Repository](https://github.com/QuiHu/Team6Project.git)
[RiskRadar README](./CMPS490_README.md)

**RiskRadar** is a mobile app designed to help users identify and manage potential environmental conditions and risks they may encounter whilst traveling or their day-to-day activities. The app provides features such as real-time alerts, climate data statistics, and user-friendly 5-Minute Summaries.

As an extension of our RiskRadar mobile app, this respository contains code from this mobile app to provide a foundation for our web-app extension.

### RiskRadar Web-App Extension

### Additional Features and Extensions


---


## Project Progress

### Certification of Original Work
The required Certification of Original Work is included in the [CERTIFICATION.md](./CERTIFICATION.md) file.

### Stages and Steps

See the full staged implementation plan here: [Project Stages](./docs/STAGES.md)

### Current Stage Status

| Stage | Title | Status | Last Updated | Notes |
|---|---|---|---|---|
| 1 | Web-App Extension | In Progress | 2026-03-09 | Building unique PHP web interface connected to existing backend APIs. |
| 2 | Environmental Risk Assessment and Alert Prioritization Extensions | Not Started | 2026-03-09 | Planned: personal risk scoring engine and smart alert ranking. |
| 3 | Data Visualization and User Experience Extensions | Not Started | 2026-03-09 | Planned: interactive Plotly-based risk map for web/mobile surfaces. |
| 4 | Predictive Analytics and AI-Driven Insights Extensions | Not Started | 2026-03-09 | Planned: 24-48h forecasting and RiskRadar AI Assistant integration. |

**Status Legend**
- **Not Started**: Requirements are defined, but implementation has not begun.
- **In Progress**: Implementation is actively underway and may be partially complete.
- **Completed**: Implementation and verification are complete, with docs/tests updated as needed.
