# Demo Evidence Report

Generated: 2026-04-13T04:18:06.094Z

## Run Summary

- Base URL: http://127.0.0.1:8080
- Started: 2026-04-13T04:17:51.478Z
- Finished: 2026-04-13T04:18:00.076Z
- Overall Status: passed
- Steps Executed: 6

## Step Results

| Step | Name | Status | Duration (ms) | URL | Error |
|---|---|---|---:|---|---|
| 1 | Dashboard Overview | passed | 1133 | http://127.0.0.1:8080/index.php |  |
| 2 | Personalized Risk Scoring | passed | 733 | http://127.0.0.1:8080/risk.php?user_id=2&radius_km=50 |  |
| 3 | Smart Alerts Prioritization | passed | 718 | http://127.0.0.1:8080/smart_alerts.php?user_id=2&radius_km=100&limit=10 |  |
| 4 | Interactive Risk Map | passed | 3646 | http://127.0.0.1:8080/map.php |  |
| 5 | Forecast View | passed | 707 | http://127.0.0.1:8080/forecast.php |  |
| 6 | AI Assistant View | passed | 1659 | http://127.0.0.1:8080/assistant.php |  |

## Captured Screenshots

- demo_01_dashboard.png: Dashboard Overview (static/evidence/demo_screenshots/demo_01_dashboard.png)
- demo_02_risk_scoring.png: Personalized Risk Scoring (static/evidence/demo_screenshots/demo_02_risk_scoring.png)
- demo_03_smart_alerts.png: Smart Alerts Prioritization (static/evidence/demo_screenshots/demo_03_smart_alerts.png)
- demo_04_map.png: Interactive Risk Map (static/evidence/demo_screenshots/demo_04_map.png)
- demo_05_forecast.png: Forecast View (static/evidence/demo_screenshots/demo_05_forecast.png)
- demo_06a_assistant_response.png: Assistant reply rendered after sending a prompt (static/evidence/demo_screenshots/demo_06a_assistant_response.png)
- demo_06b_assistant_feedback.png: Assistant feedback interaction complete (static/evidence/demo_screenshots/demo_06b_assistant_feedback.png)
- demo_06c_assistant_guardrail.png: Assistant guardrail response rendered (static/evidence/demo_screenshots/demo_06c_assistant_guardrail.png)
- demo_06_assistant.png: AI Assistant View (static/evidence/demo_screenshots/demo_06_assistant.png)

## Stage Coverage

- Stage 1: Dashboard and baseline web navigation
- Stage 2: Risk scoring and prioritized alerts
- Stage 3: Interactive map load and personalization toggle
- Stage 4: Forecast and assistant page flows

## Notes

Use this report with docs/DEMO_RUNBOOK.md and docs/DEMO_FEATURES_BY_STAGE.md for grading evidence.
