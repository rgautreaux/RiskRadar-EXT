# RiskRadar Demo Runbook

**Purpose**: Step-by-step guide for presenting the RiskRadar Web-Extension across all 4 stages.  
**Audience**: Graders, professors, stakeholders.  
**Duration**: ~12–15 minutes for the full demonstration.

Latest verification snapshot (2026-04-14): connectivity preflight PASS, web build PASS, and demo journey PASS (6/6).

---

## Prerequisites

✅ Ensure all prerequisites are met before starting:

- [ ] Backend FastAPI server running on `http://127.0.0.1:8001`
- [ ] Web frontend accessible via PHP on `http://127.0.0.1:8080`
- [ ] Demo database populated (`npm run demo:setup`)
- [ ] Assistant assets built (`npm run build:web`)
- [ ] Connectivity preflight passes (`npm run verify:connectivity`)
- [ ] Connectivity preflight confirms readiness and map API wiring (includes guest-session bootstrap for login-gated map verification)
- [ ] `.env` file configured with API settings (see [PROGRAM_EXECUTION.md](./PROGRAM_EXECUTION.md))
- [ ] Modern web browser (Chrome, Firefox, Safari, Edge)
- [ ] ~15 minutes of uninterrupted time

### Quick Setup

```bash
# Terminal 1: Setup demo database
npm run demo:setup

# Terminal 2: Build frontend assistant assets
npm run build:web

# Terminal 3: Start backend API (canonical demo port)
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8001

# Terminal 4: Start PHP web server (from repository root)
php -S 127.0.0.1:8080 -t frontend/web/public

# Terminal 5: Run wiring preflight (fails fast if backend/frontend linkage is broken)
npm run verify:connectivity
```

Once all required services are running and preflight passes, navigate to **http://127.0.0.1:8080** in your browser.

---

## Demo Flow Overview

| Step | Duration | Feature | Demo URL | Key Points |
|------|----------|---------|----------|-----------|
| 1 | 2 min | Login Gate, Registration, and Guest Option | `/login.php` | Required entry point with sign in/register/guest choices |
| 2 | 1 min | Dashboard Overview | `/index.php` | Live data integration, summary display |
| 3 | 2 min | Personalized Risk Scoring | `/risk.php` | Enter user ID, view score breakdown |
| 4 | 2 min | Smart/Prioritized Alerts | `/smart_alerts.php` | Ranking based on risk factors |
| 5 | 3 min | Interactive Risk Map | `/map.php` | Overlays, personalization, accessibility |
| 6 | 2 min | Forecast & AI Assistant | `/forecast.php` + `/assistant.php` | 24–48 hour predictions, AI recommendations |

---

## Detailed Demo Steps

### **Step 1: Login Gate, Registration & Profile Setup** *(2 minutes)*

**Narrative:**  
*"The web app now starts at Login. From here, users can sign in, create an account, or continue as guest. For this demo, I'll create a new account to show how personalized profiles drive risk scoring."*

#### Actions

1. **Open Login Page (Required Entry)**
   - Navigate to **http://127.0.0.1:8080/login.php**
   - Confirm page offers **Sign in**, **Create one**, and **Continue as Guest**

2. **Open Registration Page from Login**
   - Click **Create one** (or navigate to `/register.php`)
   - Title should say "Create a RiskRadar account"

3. **Fill Registration Form**
   - Display Name: `Demo User - [Your Name]`
   - Email: `demo_test@riskradar.local`
   - Password: `DemoPass123!` (meets strength requirements: 8+ chars, mixed case, number, special char)
   - ZIP Code: `90001` (Los Angeles area)
   - Click **Register**

4. **Verify Success**
   - System redirect to login page with success message
   - Point out: *"The system validates password strength before storing. Passwords are hashed with pbkdf2_sha256, and emails are encrypted at rest."*

5. **Optional Guest Demo Path**
   - From login, click **Continue as Guest** to demonstrate no-account access to feature pages
   - Continue demo either as guest or signed-in user

6. **Open Profile/Preferences**
   - Navigate to **http://127.0.0.1:8080/profile.php**
   - Scroll to "Health Conditions" section
   - Set the following sensitivities:
     - **Asthma**: 4 (high)
     - **Allergies**: 2 (medium)
     - **Heart Disease**: 1 (low)
     - Leave others at 0
   - Scroll down to view current settings if available
   - Click **Save Preferences**

7. **Presenter Notes**
   - Highlight: *"These sensitivities are stored securely and will be used to personalize risk scoring, smart alert ranking, and forecast advice."*
   - Point out: *"This is Stage 2 personalization—the system now knows about this user's health profile."*

---

### **Step 2: Dashboard Overview** *(1 minute)*

**Narrative:**  
*"Now let's go to the dashboard to see a high-level overview of environmental conditions in the region."*

#### Actions

1. **Navigate to Dashboard**
   - Go to **http://127.0.0.1:8080/index.php**

2. **Review Dashboard Contents**
   - **Alert Count**: Should show "15 Active Alerts" (or similar)
   - **Highest Severity**: Likely "High" or "Medium"
   - **Most Common Type**: Probably "Air Quality" or "Weather"
   - **Top Alerts**: Should display cards for the top 3–5 alerts
   - **Latest Summary**: Should display one summary with title and snippet

3. **Presenter Notes**
   - *"The dashboard aggregates real-time data from our backend. These alerts are fetched from multiple sources: National Weather Service, EPA air quality, NASA satellite data for wildfires, USGS seismic data, and other environmental APIs."*
   - Point to one of the alerts: *"Each alert shows severity, location, and a summary. The data pipes through our backend processing before display, demonstrating Stage 1 integration."*
   - Highlight the summary box: *"Summaries are AI-generated digests of current conditions. We're using mock data for determinism, but in production these integrate with LLM services."*

---

### **Step 3: Personalized Risk Scoring** *(2 minutes)*

**Narrative:**  
*"Now let's look at personalized risk scoring. This is Stage 2 functionality—it combines the user's health profile with current environmental data to calculate a personalized risk score."*

#### Actions

1. **Navigate to Risk Scoring Page**
   - Go to **http://127.0.0.1:8080/risk.php**

2. **Enter Demo User ID**
   - User ID Input: Enter `2` (corresponds to Demo User - Medium Risk from fixtures)
   - Radius (km): `50` (shows relevant alerts within 50 km)
   - Click **Calculate Risk**

3. **Review Risk Score Output**
   - **Overall Risk Score**: Should display a number 0–100
   - **Risk Tier**: "Low", "Medium", or "High" label
   - **Score Breakdown** (if shown):
     - Air Quality Factor: %
     - Weather Factor: %
     - Wildfire Factor: %
     - Proximity Factor: %
     - Health Sensitivity Boost: %

4. **Presenter Notes**
   - *"The risk score combines multiple factors: current air quality, weather alerts, wildfire proximity, and the user's health sensitivities. The formula weights air quality at 35%, weather 20%, wildfire 25%, pollution 20%, plus a sensitivity boost."*
   - *"User 2 has asthma and allergies, so air quality alerts contribute more to their risk. A different user without those conditions would see the same alert data but calculate a lower score."*
   - *"This demonstrates algorithmic decision-making (Stage 2 requirement) and personalization (Stage 2 feature)."*

---

### **Step 4: Smart/Prioritized Alerts** *(2 minutes)*

**Narrative:**  
*"Beyond risk scoring, we also rank alerts by priority. This helps users focus on what's most relevant to them."*

#### Actions

1. **Navigate to Smart Alerts Page**
   - Go to **http://127.0.0.1:8080/smart_alerts.php**

2. **Enter Parameters**
   - User ID: `2` (same demo user)
   - Radius (km): `100`
   - Limit: `10` (show top 10 alerts)
   - Click **Get Prioritized Alerts**

3. **Review Results**
   - Alerts should display in descending priority order (highest priority first)
   - Each alert card should show:
     - Title
     - Severity badge (High/Medium/Low)
     - Distance from user location
     - Priority score or urgency label
   - Compare to /alerts.php to show the difference: *"Notice these are ranked differently! Air quality alerts rank higher for this user because of their asthma sensitivity."*

4. **Presenter Notes**
   - *"Prioritization uses a composite scoring formula: 45% risk contribution, 25% distance decay, 20% severity, 10% health sensitivity match."*
   - *"This is Stage 2 complexity—dynamic ranking based on user profile and data. The same alerts appear on the generic Alerts page in a different order."*

---

### **Step 5: Interactive Risk Map** *(3 minutes)*

**Narrative:**  
*"Stage 3 introduces geospatial visualization. The interactive map shows risk zones and environmental data on a geospatial backdrop."*

#### Actions

1. **Navigate to Map**
   - Go to **http://127.0.0.1:8080/map.php**
   - Wait for map to load (should show Los Angeles area by default)

2. **Demonstrate Basic Navigation**
   - Zoom in (scroll up or `+` button)
   - Zoom out (scroll down or `-` button)
   - Pan by dragging

3. **Enable Overlays**
   - Look for a legend or overlay toggles (left or right sidebar)
   - Enable the following overlays one by one:
     - **Alert Zones**: Should show markers/circles for alert locations
     - **Risk Zones**: Should show heat map or colored regions
     - **AQI Heatmap**: Air quality overlay
     - Optionally: Wildfire, Weather, Pollution overlays

4. **Click on a Marker/Zone**
   - Click on an alert marker
   - A popup or tooltip should show:
     - Alert title, severity, description
     - Distance from default location
     - Relevant metadata (e.g., temperature, AQI value)

5. **Enable Personalized View**
   - Find the "Personalized Risk Map" checkbox or toggle
   - Enter User ID: `3` (Demo User - High Risk, has multiple sensitivities)
   - Enable personalization
   - Overlay should update to show personalized risk zones (may highlight different areas based on health conditions)

6. **Test Accessibility**
   - Use **Tab key** to navigate through interactive elements
   - Verify keyboard focus is visible
   - Press **Enter** to activate overlay toggles or markers
   - Confirm screen reader-friendly labels (e.g., "Toggle Alerts Overlay, currently off")

7. **Presenter Notes**
   - *"This is Stage 3—data visualization with interactive controls. The map integrates live alert and risk data from the backend."*
   - *"Notice the responsive design—we're on desktop now, but the same interface works on tablets and phones by wrapping controls vertically and using touch-friendly buttons."*
   - *"Accessibility is built in. All overlays can be toggled via keyboard, and the map is screen-reader navigable. This ensures inclusive design."*
   - *"The personalized overlays show how spatial context combines with user profiles—User 3's high sensitivities highlight risks that might be lower for other users."*

---

### **Step 6: Forecast & AI Assistant** *(2 minutes)*

**Narrative:**  
*"Stage 4 is predictive analytics and AI-driven insights. Here, we show 24–48 hour forecasting and an AI assistant for contextual guidance."*

#### Actions

1. **Navigate to Forecast Page**
   - Go to **http://127.0.0.1:8080/forecast.php**

2. **Review Forecast Display**
   - Should show a timeline or chart spanning the next 24–48 hours
   - X-axis: Hours or times
   - Y-axis: Risk level (Low/Medium/High) or numerical scale
   - Look for:
     - **Confidence bands**: Shaded areas showing uncertainty ranges
     - **Risk peaks**: Times when risk is highest
     - **Risk type grouping**: Sections for Air Quality, Weather, Wildfire alerts

3. **Enter Location (if interactive)**
   - Try entering a ZIP code: `90028`
   - Or select a city/state: Example, "Los Angeles, CA"
   - Forecast should re-render for that location

4. **Review Personalized Advice**
   - Scroll down to see recommendations tailored to the user's profile
   - Examples:
     - *"Air quality expected to peak at 2–4 PM. Avoid outdoor exercise during this window if you have respiratory conditions."*
     - *"Heat index reaching 105°F. Elderly residents should stay in air-conditioned spaces."*

5. **Navigate to AI Assistant**
   - Go to **http://127.0.0.1:8080/assistant.php**

6. **View AI Assistant Widget**
   - Should see a chat-style interface (React component)
   - Look for:
     - **Chat input box** at the bottom
     - **Example prompts** or help text (e.g., "Ask about..." suggestions)
     - **Assistant persona** indicator (e.g., "Golby, your RiskRadar Assistant")

7. **Try an Example Query** (if the assistant accepts user input)
   - Type a question like: `"What should I do about the high air quality alert?"`
   - Assistant should respond with contextual guidance based on current alert data
   - Point out: *"The response integrates live data and user profile, demonstrating guardrailed AI."*

8. **Presenter Notes**
   - *"Forecasting combines historical patterns and current conditions to predict the next 1–2 days. In production, this integrates with LLM-based interpretation."*
   - *"The AI assistant uses guardrails to ensure safe, reliable responses. It has context on user health conditions and current alerts, allowing personalized guidance."*
   - *"This is Stage 4—predictive analytics and AI-driven decision support. The system moves beyond displaying data to helping users interpret and act on it."*

---

## Fallback Instructions (If Issues Arise)

### Map Page Won't Load
- **Cause**: Backend API unreachable or Plotly library issue
- **Workaround**: Skip to Step 6 (Forecast). Show a screenshot of the map from the evidence folder (docs/PLANNING_DOCS/STAGE3_DOCS/) if available

### Risk Score Returns Error
- **Cause**: User ID not in database
- **Workaround**: Use User ID `2` or `3` (from demo fixtures). Verify demo.db was created: `npm run demo:info`

### Assistant Page Shows Blank Widget
- **Cause**: React component not loaded or API misconfiguration
- **Workaround**: Open browser console (F12 → Console tab). Show the error message. Explain that in production, the widget integrates with LLM APIs.

### Air Quality Alert Not Showing
- **Cause**: EPA API key missing or mock data mode not active
- **Expected**: Demo mode has hardcoded fixtures, so this shouldn't happen. Verify `npm run demo:verify` passes.

---

## Q&A Reference

**Q: Why are user health sensitivities limited to 0–5?**  
A: Bounded scales prevent outlier effects and simplify user UX. Sensitivity × 0.08 multiplier ensures the boost doesn't overwhelm other factors.

**Q: How does the system ensure privacy?**  
A: User emails are encrypted at rest using Fernet (symmetric cipher). Passwords are hashed with pbkdf2_sha256. Session tokens expire after 24 hours.

**Q: Can the map show real-time updates?**  
A: Yes, in production. The demo uses static fixture data for reproducibility. With `--live` flag, scrapers fetch real data from EPA, NWS, NASA, etc.

**Q: Why mock the forecast instead of using live LLM APIs?**  
A: For grading reproducibility and determinism. With `--live` flag, the system calls the configured LLM provider (DeepSeek, OpenAI, Anthropic).

**Q: What's the difference between the web app and the mobile app?**  
A: The mobile app (Expo/React Native) is the original CMPS 490 project. The web app (PHP frontend) is the Stage 1 CMPS 357 extension. Both share the same backend API.

---

## Timing & Checkpoint Reminders

- **0–2 min**: Steps 1–2 (registration, dashboard)
- **2–4 min**: Step 3 (risk scoring)
- **4–6 min**: Step 4 (smart alerts)
- **6–9 min**: Step 5 (map—longest, most visual)
- **9–11 min**: Step 6 (forecast, assistant)
- **11–15 min**: Q&A and discussion

If running short on time:
- **Minimum demo**: Steps 2, 3, 5 (dashboard, risk score, map) = ~6 minutes
- **Extended demo**: All 6 steps + live alert generation = ~20 minutes

---

## Evidence & Grading Reference

For graders reviewing this demo:
- **Stage 1 Evidence**: Steps 2–4 (web app, alerts, summaries)
- **Stage 2 Evidence**: Step 3 (risk scoring), Step 4 (prioritization)
- **Stage 3 Evidence**: Step 5 (map visualization, responsive UX, accessibility)
- **Stage 4 Evidence**: Step 6 (forecast, AI assistant)

See [DEMO_FEATURES_BY_STAGE.md](./DEMO_FEATURES_BY_STAGE.md) for detailed feature-to-code mapping.

---

## Next Steps After This Demo

1. **Manual Testing**: Try the demo flow on different screen sizes (360px mobile, 768px tablet, 1280px desktop)
2. **Extended Data**: Use `npm run demo:generate-alerts --count 50` to show the system handling scale
3. **Error States**: Break things intentionally (unplug API, enter invalid user ID) to verify graceful error handling
4. **Code Review**: Walkthrough the implementation files linked in DEMO_FEATURES_BY_STAGE.md
5. **Performance**: Run backend tests: `npm run verify:backend`

---

**End of Runbook. Thank you for reviewing RiskRadar!**
