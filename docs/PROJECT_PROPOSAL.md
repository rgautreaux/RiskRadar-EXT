CMPS 357 – Team 3 Final Project Proposal

1. Project Title and Project Information
Project Title:
RiskRadar Web: Personalized Environmental Risk Intelligence Platform
Group Members:
Rebecca Gautreaux
Max Compeaux
Repository URL:
https://github.com/School-of-Computing-and-Informatics/cmps-357-sp26-final-project-cmps357-team-3.git
GitHub Classroom Assignment:
https://classroom.github.com/a/oHRMfboi
The project repository will be managed through the GitHub Classroom assignment listed above. Rebecca Gautreaux created the Team 3 team through the assignment link and accepted the assignment. The Max then joined the team soon afterwards. All project code, documentation, and development progress will be maintained in this repository throughout the semester.

2. Project Overview
RiskRadar Web is a web-based analytical extension of the RiskRadar mobile application. The goal of the system is to help users better understand environmental hazards that may impact their health, daily activities, or travel plans. The existing RiskRadar mobile application aggregates environmental alerts and generates summarized reports from sources such as weather alerts, air quality monitoring systems, and pollution data services. While these alerts provide useful information, interpreting their personal relevance can be difficult for many users.  We chose to extend our Senior Project for our Final to ensure we had a strong foundation and improve our skills by implementing new features.
The proposed web platform expands upon the existing system by introducing advanced data interpretation and personalized risk analysis features. Specifically, RiskRadar Web will incorporate a Personalized Environmental Risk Scoring Engine and a Smart Alert Prioritization System. These systems will analyze environmental data such as air quality levels, weather alerts, wildfire smoke data, and pollution reports, then compute a personalized environmental risk score based on each user’s health sensitivities and environmental preferences.  Alerts will also be dynamically prioritized according to three primary factors: the user’s risk score, the geographic proximity of the hazard, and the severity of the alert. This allows users to quickly identify which environmental threats are most relevant to them. By transforming complex environmental data into personalized, actionable insights, RiskRadar Web helps users make safer decisions regarding outdoor activity, travel planning, and exposure to hazardous environmental conditions.

3. Project Goals

**Core Deliverables (Required - Target Completion: April 29, 2026):**
- Implement a web-based dashboard that displays environmental hazard data collected by the existing RiskRadar backend system.
- Develop a Personalized Environmental Risk Scoring Engine that calculates a dynamic risk score based on real-time environmental conditions and user-defined sensitivity preferences.
- Implement a Smart Alert Prioritization System that ranks environmental alerts based on risk contribution, geographic proximity to the user, and severity level.
- Provide a user profile system that allows individuals to define environmental sensitivities such as asthma, pollen sensitivity, or heat sensitivity.
- Display prioritized alerts along with clear explanations describing why certain alerts are considered more important than others.
- Integrate the web application with the existing RiskRadar backend APIs and data ingestion pipelines.
- Provide clear visual summaries and explanations that help users interpret environmental conditions and understand their personal risk level.

**Optional Stretch Goals (If Time Permits After April 29):**
- Interactive geographic risk map using Plotly visualization
- Predictive environmental risk forecasting (24-48 hours ahead)
- AI-based environmental assistant for interpreting environmental conditions and travel risk context

4. Key Features
4.1 Core System Features
Personalized Environmental Risk Scoring Engine
The Personalized Environmental Risk Scoring Engine converts raw environmental data into a user-specific environmental risk score that reflects the potential danger of current conditions for an individual.
Instead of simply presenting environmental alerts, the system answers the question: “How risky are the current environmental conditions for me?”
The system will compute a risk score ranging from 0 to 100, representing the overall environmental risk level based on several contributing environmental factors.
Example output:
User Location: Baton Rouge, LA
	Risk Score: 72 (High Risk)
Contributing Factors:
Air Quality Index: 145 (Unhealthy for Sensitive Groups)
Heat Index: 103°F
Wildfire Smoke: Moderate
Pollen Level: High
Recommendation:
Limit prolonged outdoor activity and consider wearing respiratory protection when outdoors.
Implementation Approach
Environmental data collected by existing RiskRadar scrapers will be aggregated and analyzed. The risk score will be calculated using a weighted scoring model that combines multiple environmental metrics:
Risk Score =
(AQI Weight × AQI Value)
(Heat Weight × Heat Index)
(Smoke Weight × Smoke Level)
(Pollen Weight × Pollen Level)
Environmental metrics will be normalized to a standardized scale before being combined in the weighted risk calculation.  User-defined health sensitivities will modify these weights to personalize the risk score.  
Technical Complexity
This component introduces:
algorithmic risk modeling
multi-source environmental data aggregation
personalized analytics based on user profiles
explainable scoring logic that communicates risk factors to users

Smart Alert Prioritization System
Environmental monitoring systems frequently produce numerous alerts, many of which may not directly impact an individual user. The Smart Alert Prioritization System will rank alerts according to their relevance and urgency.
Alerts will be evaluated based on three key factors:
Contribution to the user’s environmental risk score
Geographic distance between the user and the hazard
Severity level of the alert
Example ranked alert output:
Wildfire Smoke Alert – 5 miles away – Critical
Air Quality Warning – Citywide – High
Heat Advisory – Regional – Moderate
Implementation Approach
Each alert will be assigned a priority score using a weighted ranking model:
Alert Priority Score =
(Risk Score Contribution)
(Severity Weight)
(Proximity Weight)
Proximity weight will be calculated based on the geographic distance between the user’s location and the location associated with the environmental alert. Alerts returned by the system API will be automatically sorted based on this score before being displayed to the user.
Technical Complexity
This feature requires:
geospatial distance calculations
alert severity weighting
dynamic ranking algorithms
personalized filtering of environmental alerts

4.2 User Interface and Interaction
Web Dashboard
The RiskRadar Web interface will present environmental insights through a centralized dashboard that includes:
a personalized environmental risk score
ranked environmental alerts
explanations of contributing risk factors
summarized environmental data trends
The interface will be designed to prioritize clarity and usability so users can quickly interpret environmental conditions and understand potential risks.

4.3 Data Storage and Processing
The web application will integrate with the existing RiskRadar backend database while extending it with additional models for:
user environmental sensitivity profiles
calculated environmental risk scores
alert prioritization metrics
Environmental data will continue to be collected through existing automated scraper pipelines that retrieve information from external environmental data sources.

5. Technical Stack (Proposed)
Frontend
For this extension, we will be building a new web-app frontend using PHP scripts that will link to the existing RiskRadar backend that both of us were a part of constructing for the Senior Project. PHP provides a lightweight, server-side rendering approach for developing the web interface. The frontend will include:
- PHP server-side scripting for dynamic page rendering and backend API integration
- HTML and CSS for responsive UI design and consistent visual styling
- Service wrappers in PHP for communicating with backend REST API endpoints
- Dashboard components displaying risk scores, alert rankings, and environmental summaries

Backend
This extension will be built from the existing backend, created using Python with FastAPI. FastAPI provides high-performance REST API capabilities and integrates well with the existing RiskRadar backend infrastructure responsible for:
environmental data aggregation
risk score calculations
alert prioritization logic
API endpoints used by the web dashboard

Database
The system will use MySQL, which is already used by the existing RiskRadar backend infrastructure. Reusing the existing database ensures compatibility with the current data ingestion pipelines and scraper services that collect environmental data and store:
environmental hazard data collected from external sources
user profile and sensitivity preferences
calculated environmental risk scores
prioritized environmental alerts
Using the same database system as the existing RiskRadar mobile application simplifies integration and allows the web application to access the same environmental datasets without requiring database migration or schema restructuring.  MySQL supports geographic data types and distance calculations that can be used to determine the proximity of environmental hazards to the user.

External APIs and Data Sources
Environmental data will be collected from several external sources, including:
air quality monitoring services
weather alert systems
environmental pollution monitoring agencies
Existing RiskRadar scrapers already retrieve much of this data, which will be reused for the web platform.

AI Integration (Optional)
If time permits, lightweight AI APIs will be used to power an environmental assistant capable of answering user questions about environmental conditions and risk scores.

6. Architecture Overview
RiskRadar Web extends the existing RiskRadar system architecture by introducing an additional risk analysis layer between the environmental data storage layer and the application interface.
System Interaction
Environmental data is first collected through automated scraper processes that retrieve information from external environmental APIs. This data is stored in the system database and made available for analysis.
The Risk Scoring Engine processes environmental metrics and generates personalized risk scores for users. The Smart Alert Prioritization System then evaluates and ranks environmental alerts based on their impact on the user’s calculated risk level.
The web frontend communicates with the backend through REST API endpoints implemented with FastAPI. These endpoints provide access to processed environmental data, risk scores, user profiles, and ranked alerts. The frontend retrieves this information dynamically and updates the dashboard interface accordingly.
System Architecture Diagram
External Environmental APIs
↓
Data Scrapers
↓
Environmental Database
↓
Risk Scoring Engine
↓
Smart Alert Prioritization
↓
REST API Layer
↓
RiskRadar Web Dashboard
This layered architecture separates responsibilities between data collection, risk analysis, alert prioritization, and user presentation, improving maintainability and scalability.

7. Development Timeline
The project development timeline spans approximately seven weeks (March 16 – May 1).
Week 1 (March 16 – March 22)
Project setup and planning
Create project repository
Review the existing RiskRadar backend codebase
Design database schema extensions
Define API endpoints
Week 2 (March 23 – March 29)
Risk Engine development
Implement environmental data aggregation
Develop an initial risk scoring algorithm
Begin backend integration
Week 3 (March 30 – April 5)
Alert prioritization implementation
Implement the alert ranking algorithm
Integrate severity and proximity calculations
Develop backend API endpoints
Week 4 (April 6 – April 12) – Project Checkpoint
Web dashboard development
Create an initial React dashboard interface
Display environmental risk score
Display prioritized alerts
Demonstrable progress at checkpoint:
functioning backend Risk Scoring Engine
working web dashboard displaying environmental data
Week 5 (April 13 – April 19)
User personalization features
Implement user sensitivity profiles
integrate personalization into risk calculations
Add explanatory risk summaries
Week 6 (April 20 – April 26)
User interface improvements and testing
refine dashboard layout
implement data visualizations
perform system testing and debugging
Week 7 (April 27 – May 1)
Project finalization
documentation
bug fixes
deployment or local system preparation 
deployment or local system demonstration
final presentation

8. Stretch Goals
If core functionality is completed ahead of schedule, several additional features will be explored. The following Stretch Goals will only be implemented if core system functionality is completed successfully.
Predictive Environmental Risk (AI/Data Extension)
This feature will forecast environmental risk levels for the next 24–48 hours using historical environmental data collected by the system.
Potential model inputs include:
past air quality levels
temperature patterns
wind speed
pollution trends
Example forecast:
Tomorrow’s Environmental Risk Forecast
Morning: Moderate Risk
Afternoon: High Risk (predicted AQI spike)
This feature introduces time-series analysis and predictive modeling capabilities. This Predictive Feature and other Stretch Goals will only be implemented if core system functionality is completed successfully.

Interactive Risk Map
An interactive geographic map will display environmental hazards visually across regions. Users will be able to view:
air quality zones
wildfire smoke coverage
pollution alerts
weather warnings
The backend will generate visuals utilizing the skills we learned through the implementation of a Jupyter Notebook in the second Programming Assignment.  MySQL supports geographic data types and distance calculations that can be used to determine the proximity of environmental hazards to the user. These visualizations and other Stretch Goals will only be implemented if core system functionality is completed successfully.

AI Environmental Assistant
An integrated AI assistant will help users interpret environmental data and alerts. Users will be able to ask questions such as:
“Is it safe to exercise outdoors today?”
“Why is my environmental risk score high?”
“What precautions should I take during a wildfire smoke alert?”
The assistant will generate responses using environmental data, alerts, and risk scores as contextual input. The AI assistant and other Stretch Goals will only be implemented if core system functionality is completed successfully.

9. Why This Project Matters
This project demonstrates several important software engineering concepts, including full-stack web development, API design, data processing pipelines, and algorithmic decision systems. By extending an existing mobile application with an analytical web platform, the project highlights the ability to design scalable systems that transform raw environmental data into meaningful insights.  RiskRadar Web reflects modern development practices such as modular architecture, user-centered interface design, and the integration of AI-assisted technologies. The system combines environmental data aggregation, personalized analytics, and interactive visualization to address a real-world problem. The web platform is designed to provide a more detailed analytical interface than the mobile application, allowing users to explore environmental trends, detailed alert rankings, and personalized risk insights in a larger dashboard environment.
As environmental hazards become increasingly frequent and complex, tools that help individuals interpret environmental risks are becoming more valuable. RiskRadar Web illustrates how software systems can empower users to make safer decisions using real-time environmental data, making the project both technically meaningful and practically relevant.

Written with assistance from ChatGPT.
https://chatgpt.com/share/69b0315d-8724-8002-a602-de27293427b8