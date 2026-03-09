# RiskRadar CMPS 357 Instructions

---

## Project Proposal Stages and Steps Outline

This document defines the required staged extension work for the CMPS 357 RiskRadar final project.

The extension should:

- Build a distinct web-facing experience from the original mobile surface.
- Reuse and extend the existing backend and data-ingestion foundation.
- Add meaningful technical complexity beyond basic CRUD functionality.

---

## Stage 1: Web-App Extension

In this stage, the team builds a **web-app extension** of the RiskRadar mobile app with a unique interface and shared backend integration.

### Required Steps

1. Create a web application that connects to the existing RiskRadar backend APIs.
2. Design and implement a unique frontend interface using **PHP** scripts.
3. Provide access to core data/features already available in RiskRadar.
4. Ensure the web app is functional, usable, and consistent in user experience.

---

## Stage 2: Environmental Risk Assessment and Alert Prioritization Extensions

In this stage, the team adds intelligence layers that improve interpretation of environmental conditions for individual users.

### Step 1: Personal Risk Scoring Engine

1. Create a personalized environmental risk score based on:
	- User location
	- Health sensitivities
	- Current environmental data
2. Store and handle user data securely with privacy-aware design.
3. Integrate risk scoring into backend services and API access.
4. Add web/mobile UI views that present score and context clearly.

### Step 2: Smart Alert Prioritization System

Extend alerts into a prioritized ranking pipeline using factors such as:

- Risk score
- Distance from user
- Severity
- User sensitivity

---

## Stage 3: Data Visualization and User Experience Extensions

### Step 1: Interactive Risk Map (UI Extension)

1. Add a map visualization to mobile/web surfaces using Plotly.
2. Make the map interactive (zoom, pan, click for detailed risk data).
3. Ensure responsive behavior across screen sizes.
4. Integrate map rendering with live backend environmental/risk data.

---

## Stage 4: Predictive Analytics and AI-Driven Insights Extensions

### Step 1: Predictive Environmental Risk (AI/Data Extension)

1. Predict environmental risk **24-48 hours** ahead using scraper-derived patterns.
2. Create visualizations of predicted risk and trend behavior over time.
3. Present forecast output in a way that supports user planning decisions.

### Step 2: RiskRadar AI Assistant

1. Integrate an AI assistant/guide into the application.
2. Provide user-facing interpretation of environmental conditions, alerts, and travel risk context.
