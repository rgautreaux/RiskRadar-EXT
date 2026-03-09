# CMPS 357 Final Project Transcript

This document serves as a transcript for all usage of AI tools within the CMPS 357 Final Project. It includes all interactions with AI tools, such as ChatGPT, along with the context of each interaction and any relevant files or links.


## Project Proposal Brainstorming Session

This brainstorming session was conducted on April 26, 2026, and involved a discussion between Rebecca and ChatGPT regarding potential extensions for the RiskRadar project. The goal was to identify an extension that would be effective, achievable, and fit well with the existing codebase of the RiskRadar mobile app.

https://chatgpt.com/share/69aef5cd-0b48-8002-a3a3-d71eaa97918d 

**Rebecca:** 

Attached File:
Team6Project-main.zip
Zip Archive


These are the requirements for my Final Project:
''' 
You must propose an original software project of your own design. The project may be:



A web application
Example: a browser-based task manager that allows users to create projects, assign deadlines, and track progress.


A mobile application
Example: a study planner that sends reminders, tracks completed study sessions, and visualizes progress over time.


A desktop application
Example: a local file organizer that categorizes documents, images, and media files based on user-defined rules.


A systems or tools-based project
Example: a command-line tool that analyzes log files and produces summaries or visual reports of system activity.


A data-driven or AI-enhanced application
Example: a program that analyzes user input data and generates recommendations or predictions using a lightweight model or API.


A game or interactive platform
Example: a small strategy or puzzle game with persistent player progress and scoring.


Another instructor-approved technical project
Example: a custom simulation, educational tool, or specialized application addressing a niche technical problem.


The project must include meaningful technical complexity beyond basic CRUD (Create, Read, Update, Delete) functionality. It should demonstrate architectural thinking, structured development, and thoughtful design decisions.
'''

My current idea for my Final Project is to create a meaningful extension of the content in the attached ZIP file. What kind of extension would be applied to this project that would be an achievable goal, fit the outlined requirements for a Final Project, and be useful to users of the Mobile App within the ZIP?

**ChatGPT:** I looked through the ZIP and README. Your project RiskRadar is already a fairly solid system:

Mobile app concept for environmental risk awareness

Python backend (likely FastAPI)

Scrapers pulling data from sources like EPA, NWS, AirNow

LLM summarization for “5-minute summaries”

Alerts + users + summaries APIs

Scheduler for data collection

So your base system already has:

data ingestion (scrapers)

backend APIs

database models

LLM summaries

alerts

Your final project extension should add a new layer of functionality, not just another endpoint or CRUD table.

Below are four extensions that fit your requirements, are achievable for one student, and demonstrate technical complexity.

1. Personal Risk Scoring Engine (Best Overall Option)
Concept:
Create a personalized environmental risk score for each user based on location, health sensitivities, and environmental data.

What it adds
Instead of just showing raw alerts, the app answers:

“How risky is the environment for me right now?”

Features
Users set preferences such as:

asthma / respiratory sensitivity

pollen sensitivity

heat sensitivity

outdoor activity level

travel plans

The backend then computes a Risk Score (0–100) using:

AQI (AirNow)

weather alerts (NWS)

pollution reports (EPA)

pollen or wildfire smoke data

heat index

Example output
Your Risk Score: 72 (High)

Reasons:
- AQI: 155 (Unhealthy)
- Heat Index: 103°F
- Pollen Level: High

Recommendation:
Avoid outdoor activity for long periods.
Technical complexity
You would implement:

risk scoring algorithm

weighted data aggregation

user preference model

recommendation generator

Architecture:

Scrapers → Database
        → Risk Engine
        → Personalized Score
        → API → Mobile App
Why professors like this
It shows:

algorithm design

backend architecture

decision logic

personalized data processing

2. Predictive Environmental Risk (AI/Data Extension)
Concept:
Predict environmental risk 24–48 hours ahead.

Features
Use historical data collected by your scrapers to:

forecast AQI

estimate risk trends

warn users early

Example:

Tomorrow Risk Forecast
Morning: Moderate
Afternoon: High (AQI spike predicted)
Implementation options
Simple and achievable:

time-series regression

moving averages

lightweight ML model (scikit-learn)

Example features:

previous AQI

weather patterns

wind speed

temperature

Technical complexity
Demonstrates:

data modeling

predictive analytics

feature engineering

3. Smart Alert Prioritization System
Right now alerts are likely simple triggers.

Extend this into a priority ranking system.

Idea
Not all alerts are equally important.

Your system ranks them by:

Risk Score
Distance from user
Severity
User sensitivity
Example
Instead of 10 alerts:

1. Wildfire Smoke Nearby (Critical)
2. AQI Unhealthy (High)
3. Heat Advisory (Moderate)
Architecture
Alerts → Scoring Engine → Ranked Alerts API
Technical complexity
scoring algorithms

geospatial logic

alert ranking system

4. Interactive Risk Map (Great UI Extension)
Add a map visualization to the mobile app.

Features
Users see a map showing:

AQI zones

wildfire smoke

pollution sites

weather alerts

Implementation
Backend:

geoJSON endpoints

aggregated environmental data

Frontend:

map framework (Leaflet / Mapbox / Google Maps)

Why it’s good
visual data interpretation

spatial data handling

API design

Best Choice for Your Situation
If you want highest chance of a strong final project grade, I recommend:

Personalized Risk Scoring Engine

Because it shows:

architecture

algorithms

user personalization

meaningful functionality

And it fits perfectly with RiskRadar.

Example Final Project Title
RiskRadar+: A Personalized Environmental Risk Prediction and Alert System

Example Feature List (Final Project Scope)
You could implement:

User environmental sensitivity profile

Risk scoring algorithm

Alert prioritization

Personalized recommendations

API endpoint for risk scores

Mobile UI risk dashboard

Example Architecture (Professors love this)
Environmental Data Sources
        ↓
Data Scrapers
        ↓
Database
        ↓
Risk Analysis Engine
        ↓
Recommendation Generator
        ↓
API Layer
        ↓
Mobile App Dashboard
💡 If you want, I can also help you:

Pick the best extension based on your codebase

Design the system architecture diagram

Write the Final Project proposal

Suggest specific files to add to this repository

Just tell me and I’ll break it down step-by-step.

---

**Rebecca:** Which of these extension ideas would be the most effective and achievable to implement based on the RiskRadar Codebase?  Provide a System Architecture Diagram for the ideal extension that includes the files that will need to be added to the RiskRadar Repository.

**ChatGPT:** After examining the repository structure, the most effective and achievable extension for your RiskRadar codebase is:

Personalized Environmental Risk Scoring Engine
This extension fits the project far better than the others because your codebase already contains the infrastructure needed:

Existing system components in your repo:

Scrapers (backend/scrapers/)

AirNow

EPA

NWS

FIRMS wildfire

Database models (backend/db/models.py)

LLM summarization pipeline (backend/llm/summarizer.py)

APIs

alerts.py

summaries.py

users.py

Scheduler

scrapers/scheduler.py

Mobile frontend

React Native (Expo)

Your system already collects environmental data.

What it does not yet do is:

transform that data into personalized insight.

That gap makes the Risk Scoring Engine the ideal extension.

Why This Extension Is the Best Fit
Compared to other options:

Extension	Difficulty	Fit with Existing Code
Predictive ML	Medium–High	Needs historical data training
Interactive Map	Medium	Mostly frontend work
Alert Ranking	Medium	Limited user personalization
Risk Scoring Engine	Medium	Uses existing scrapers + APIs perfectly
This extension:

Adds algorithmic logic

Uses existing data

Adds new API endpoints

Adds new database models

Adds new frontend UI

This clearly satisfies the requirement:

“meaningful technical complexity beyond basic CRUD”

What the Extension Will Do
The system will calculate a Personal Environmental Risk Score for each user.

Example:

Location: Atlanta, GA

Risk Score: 68 (High)

Factors:
AQI: 142 (Unhealthy for Sensitive Groups)
Heat Index: 101°F
Wildfire Smoke: Moderate
Pollen: High

Recommendation:
Avoid prolonged outdoor exercise today.
New System Components
You will add a Risk Analysis Layer between the database and API.

Current architecture:

Scrapers → Database → API → Mobile App
New architecture:

Scrapers → Database → Risk Engine → API → Mobile App
System Architecture Diagram (Ideal Extension)
                    +-----------------------+
                    |  External Data APIs   |
                    |  (AirNow, EPA, NWS)   |
                    +----------+------------+
                               |
                               v
                    +-----------------------+
                    |       Scrapers        |
                    | backend/scrapers/*    |
                    +----------+------------+
                               |
                               v
                    +-----------------------+
                    |        Database       |
                    | backend/db/models.py  |
                    +----------+------------+
                               |
                               v
                  +---------------------------+
                  |   NEW: Risk Scoring       |
                  |       Engine              |
                  | backend/risk_engine/      |
                  +-----------+---------------+
                              |
                              v
                     +--------------------+
                     |       APIs         |
                     | backend/api/*      |
                     +---------+----------+
                               |
                               v
                      +------------------+
                      |   Mobile App     |
                      | React Native UI  |
                      +------------------+
New Files to Add to the Repository
You will create a new module.

New Backend Directory
backend/risk_engine/
Files
1️⃣ Risk Score Calculator
backend/risk_engine/risk_calculator.py
Responsibilities:

combine environmental metrics

compute risk score

generate explanation

Example logic:

risk = (
    AQI_weight * aqi_score +
    heat_weight * heat_index +
    smoke_weight * smoke_level +
    pollen_weight * pollen_level
)
2️⃣ Recommendation Generator
backend/risk_engine/recommendations.py
Produces messages like:

"Limit outdoor exercise"
"Wear an N95 mask outdoors"
"Air quality safe for outdoor activity"
3️⃣ Risk Data Aggregator
backend/risk_engine/data_aggregator.py
Pulls latest metrics from DB:

AQI

wildfire smoke

weather alerts

heat index

4️⃣ Risk API Endpoint
backend/api/risk.py
Example endpoint:

GET /risk/{user_id}
Response:

{
  "risk_score": 68,
  "level": "High",
  "factors": {
    "aqi": 142,
    "heat_index": 101,
    "wildfire_smoke": "moderate"
  },
  "recommendation": "Avoid prolonged outdoor exercise."
}
Then register it in:

backend/api/router.py
5️⃣ User Sensitivity Model
Extend:

backend/db/models.py
Add:

UserSensitivity
Example fields:

asthma: bool
heat_sensitive: bool
pollen_sensitive: bool
outdoor_activity_level: int
6️⃣ Schema for API
Add:

backend/schemas/risk.py
Database Changes
Migration file:

backend/db/migrations/2026-04-risk-engine.sql
Adds:

user_sensitivity table
Mobile App Changes
Add a Risk Dashboard screen.

New file:

frontend/RiskRadar/app/(tabs)/risk.tsx
Displays:

risk score

factors

recommendations

Updated Repository Structure
Simplified:

backend
 ├ api
 │   ├ alerts.py
 │   ├ summaries.py
 │   ├ users.py
 │   └ risk.py   NEW
 │
 ├ risk_engine   NEW
 │   ├ risk_calculator.py
 │   ├ data_aggregator.py
 │   └ recommendations.py
 │
 ├ db
 │   └ models.py (updated)
 │
 └ schemas
     └ risk.py   NEW
Why This Will Impress Your Professor
This extension demonstrates:

Architectural Thinking
You introduce a new analysis layer.

Algorithm Design
Weighted environmental risk scoring.

Data Integration
Multiple environmental sources combined.

User Personalization
Risk varies per user.

API Expansion
New endpoints + schema.

Full-Stack Work
Backend + mobile UI.

Estimated Implementation Difficulty
Component	Difficulty
Risk scoring algorithm	Easy
Data aggregation	Easy
API endpoint	Easy
DB model	Easy
Frontend dashboard	Medium
Overall difficulty: Very manageable for a final project.

If you'd like, I can also show you:
The exact risk scoring algorithm to implement

The exact code skeleton for all new files

The API endpoint implementation

The UI mockup for the mobile app

Those would make the implementation almost plug-and-play for this repository.