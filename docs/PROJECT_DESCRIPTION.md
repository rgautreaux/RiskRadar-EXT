# RiskRadar CMPS 357 Final Project Description

## Project Overview

This project is the CMPS 357 final-project extension of **RiskRadar**, an environmental risk awareness platform originally developed as a mobile-focused CMPS 490 senior project. The purpose of this extension is to transform RiskRadar into a broader, full-stack system by introducing a **unique web application interface** and adding advanced capabilities that go beyond standard data display or basic CRUD workflows.

RiskRadar is designed for residents and travelers who need timely, understandable information about environmental hazards that may impact daily activities, outdoor work, or travel planning. The system integrates real-world environmental data sources, processes this data through backend services, and presents actionable insights through user-facing interfaces.

---

## Core Problem the Project Addresses

Environmental risk information is often fragmented across multiple agencies and presented in formats that are difficult for everyday users to interpret quickly. People may need to check separate sites for air quality, weather advisories, wildfire conditions, and other health-related environmental indicators. This creates decision fatigue and increases the chance that critical information is missed.

RiskRadar addresses this gap by:

- Aggregating data from multiple environmental sources into one platform.
- Converting technical data into concise, user-friendly summaries.
- Supporting personalized and prioritized risk interpretation.
- Presenting conditions through interfaces that improve clarity and usability.

---

## What This CMPS 357 Extension Is

The CMPS 357 implementation extends the existing RiskRadar backend and dataset ecosystem into a **new web-app experience** while planning and staging additional intelligence and visualization modules. Rather than duplicating the mobile interface, the project emphasizes an independent frontend surface and expanded functionality tailored to web usage and course requirements.

The extension is structured around four staged development goals:

1. **Web-App Extension**  
	Build a distinct web frontend connected to existing backend APIs for alerts, summaries, and user data.

2. **Environmental Risk Assessment and Alert Prioritization**  
	Add a personalized risk scoring engine and smart alert ordering based on severity, proximity, and user sensitivity factors.

3. **Data Visualization and UX Extension**  
	Introduce an interactive risk map experience to help users interpret spatial environmental patterns more effectively.

4. **Predictive Analytics and AI-Driven Insights**  
	Add short-horizon forecasting (24-48 hours) and an assistant-style interpretation layer for contextual guidance.

---

## System Direction and Technical Approach

The project follows a layered architecture:

- **Data ingestion layer**: Scrapers collect environmental information from external APIs/sources.
- **Data management layer**: Structured models and database workflows store and organize incoming data.
- **Analysis layer**: Summarization and planned risk-scoring/forecasting modules transform data into insight.
- **API layer**: Backend routes expose alerts, summaries, users, and planned risk/prediction outputs.
- **Client layer**: Mobile and web interfaces present information in accessible, decision-support formats.

This approach demonstrates architectural thinking by separating data acquisition, processing, reasoning, and presentation concerns, allowing the platform to scale in capability without tightly coupling all logic into a single layer.

---

## Primary Goals and Intended Outcomes

The project seeks to achieve the following outcomes:

- **Accessibility of environmental intelligence**: Make complex risk data understandable for non-technical users.
- **Actionable decision support**: Help users decide when to modify plans, limit exposure, or take preventive steps.
- **Personalization**: Move from generic alerts toward user-specific risk interpretation.
- **Improved situational awareness**: Provide both textual and visual (map-based) understanding of conditions.
- **Proactive insight**: Support anticipation of near-term risk through predictive analytics.
- **Technical depth**: Deliver meaningful complexity through algorithmic scoring, data fusion, visualization, and AI-assisted interpretation.

---

## Scope Within Course Context

This final project is intentionally positioned as a meaningful extension of prior senior-project work while remaining independently valuable for CMPS 357 evaluation. It preserves continuity with the established RiskRadar backend ecosystem, yet introduces new implementation scope in frontend design, analytics, and user-facing intelligence features.

In course terms, the project demonstrates:

- Structured multi-stage planning and execution.
- Integration of multiple technical subsystems (scrapers, APIs, DB, UI, AI components).
- Practical software design decisions around reliability, usability, and maintainability.
- Clear progression from foundational data delivery to advanced interpretation features.

---

## Long-Term Vision

RiskRadar’s long-term vision is to become a reliable environmental risk companion that combines real-time awareness with personalized, explainable guidance. The CMPS 357 extension establishes the groundwork for that direction by broadening platform reach (web), improving insight quality (scoring and prioritization), and preparing for forward-looking support (forecasting and assistant capabilities).

By unifying environmental monitoring, interpretation, and communication, this project aims to help users make safer and more informed day-to-day and travel decisions.
