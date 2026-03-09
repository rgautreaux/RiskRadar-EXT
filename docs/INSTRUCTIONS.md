# INSTRUCTIONS for CMPS 357 Final Project Proposal



---

# Project Proposal Stages and Steps Outline

## Stage 1:  Web-App Extension
In this stage, we will create a *web-app extension* of our **RiskRadar mobile app**. This will involve developing a new frontend interface that is unique from the mobile app, while leveraging the same backend and data sources.

- Create a new web application that connects to the existing RiskRadar backend.
- Design and implement a unique frontend interface for the web app using **PHP** scripts that provide access to the same data and features as the mobile app.
- Ensure that the web app is fully functional and provides a seamless user experience.


## Stage 2: Environmental Risk Assessment and Alert Prioritization Extensions

In this stage, we will implement further extensions that enhance the environmental risk assessment and alert prioritization features of the RiskRadar application.

### Step 1: Personal Risk Scoring Engine
- Create a personalized environmental risk score for each user based on location, health sensitivities, and environmental data
- Make sure that all user data is securely stored and handled in compliance with privacy standards.
- Integrate the risk scoring engine into the existing backend and ensure that it can be accessed through the API for use in both the mobile and web applications.
- Design a user interface in both the web application to display the personalized risk scores to users in an intuitive and informative way.

### Step 2: Smart Alert Prioritization System
Extend alerts into a priority ranking system based on the Scoring Engine, considering factors such as:
- Risk Score
- Distance from user
- Severity
- User sensitivity


## Stage 3: Data Visualization and User Experience Extensions


### Step 1: Interactive Risk Map (UI Extension)
- Add a map visualization to the mobile/web app using Plotly
- Make the map interactive, allowing users to zoom, pan, and click on specific locations to view detailed environmental risk information.
- Ensure that the map is responsive and works well
- Integrate the map with the existing backend to display real-time environmental data and risk assessments based on the user's location and other relevant factors.

## Stage 4: Predictive Analytics and AI-Driven Insights Extensions

### Step 1: Predictive Environmental Risk (AI/Data Extension)
- Predict environmental risk 24–48 hours ahead by referencing the patterns from data obtained by scrapers
- Create visualizations to show predicted risks and trends over time, allowing users to make informed decisions about their activities and travel plans based on anticipated environmental conditions.

### Step2: RiskRadar AI Assistant
- AI assistant or guide integrated into the application that helps users interpret environmental conditions, alerts, or travel risks