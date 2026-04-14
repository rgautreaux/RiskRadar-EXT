# Demo Onboarding & Extension Guide

This guide explains how to modify, extend, or customize the RiskRadar demo for new features, additional scenarios, or team onboarding.

---

## Table of Contents

1. [Adding New Demo Users](#adding-new-demo-users)
2. [Generating Custom Alerts](#generating-custom-alerts)
3. [Modifying Demo Fixtures](#modifying-demo-fixtures)
4. [Extending Browser Automation](#extending-browser-automation)
5. [Creating Custom Demo Scenarios](#creating-custom-demo-scenarios)
6. [Troubleshooting Common Issues](#troubleshooting-common-issues)

---

## Adding New Demo Users

### Quick Method: Extend fixtures.json

If you want to add a 5th demo user with custom sensitivities:

1. **Edit `backend/demo/fixtures.json`**
   ```json
   {
     "id": 5,
     "display_name": "Demo User (Elderly)",
     "email": "demo_elderly@riskradar.local",
     "email_plaintext": "demo_elderly@riskradar.local",
     "password_plaintext": "DemoElderly456!",
     "zip_code": "91201",
     "latitude": 34.1580,
     "longitude": -118.2339,
     "is_admin": false,
     "health_conditions": {
       "asthma": 1,
       "copd": 0,
       "allergies": 0,
       "heart_disease": 3,
       "elderly": 5,
       "pregnant": 0,
       "children": 0,
       "immunocompromised": 2
     },
     "stage_category": "Stage 2 & 4",
     "presentation_notes": "Elderly user with heart disease; demonstrates age-specific risk personalization"
   }
   ```

2. **Reseed the database**
   ```bash
   npm run demo:reset
   ```

3. **Verify**
   ```bash
   npm run demo:info
   ```
   Look for User 5 in the output.

### Advanced Method: Script-Based User Creation

For automated user creation in tests or deployments:

```python
from backend.demo.seed_demo_data import seed_users, SessionLocal
from backend.auth.security import encrypt_email, hash_email, password_hash
from backend.db.models import User
from datetime import datetime, timezone

session = SessionLocal()

new_user = User(
    id=6,
    email=encrypt_email("custom@riskradar.local"),
    email_lookup_hash=hash_email("custom@riskradar.local"),
    password_hash=password_hash("CustomPass789!"),
    display_name="Custom Test User",
    zip_code="90002",
    latitude=34.0195,
    longitude=-118.2417,
    health_conditions={"asthma": 2, "allergies": 1},
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc),
)

session.add(new_user)
session.commit()
session.close()
```

---

## Generating Custom Alerts

### Generate Alerts On Demand

```bash
# Generate 30 air quality alerts in San Francisco
npm run demo:generate-alerts -- --count 30 --type air_quality --location san_francisco

# Generate balanced distribution across all types
npm run demo:generate-alerts -- --count 50 --distribution balanced

# Generate high-severity alerts
npm run demo:generate-alerts -- --count 20 --severity high
```

### Programmatic Alert Generation

```python
from backend.demo.mock_alert_generator import generate_alerts
import json

# Generate 50 wildfire alerts around Los Angeles
alerts = generate_alerts(
    count=50,
    alert_type="wildfire",
    location="los_angeles",
    severity="medium",
    distribution="balanced"
)

# Save to file for batch import
with open("custom_alerts.json", "w") as f:
    json.dump(alerts, f, indent=2)

# Then import into database via seed script
# (Future enhancement: bulk_add_alerts() function)
```

---

## Modifying Demo Fixtures

### Changing Alert Parameters

**Example 1: Update alert location**

```json
{
  "id": 102,
  "source": "epa",
  "source_id": "epa_20260410_002",
  "alert_type": "air_quality",
  "severity": "high",
  "title": "Unhealthy Air Quality Alert",
  "description": "...",
  "location_name": "San Diego, CA",  // ← Changed from LA
  "latitude": 32.7157,                 // ← Updated coords
  "longitude": -117.1611,
  ...
}
```

**Example 2: Adjust alert severity**

Change `"severity": "high"` to `"severity": "low"` to see impact on risk scoring.

**Example 3: Add time-based variation**

```json
{
  "event_start": "2026-04-11T06:00:00Z",  // ← Tomorrow morning
  "event_end": "2026-04-11T18:00:00Z",
  ...
}
```

Then reseed: `npm run demo:reset`

### Adding a New Summary

```json
{
  "id": 3,
  "title": "Wildfire Risk Assessment",
  "content": "# Wildfire Season Alert\n\nSatellite imagery shows...",
  "summary_type": "risk_alert",
  "region": "San Gabriel Valley, CA",
  "generated_at": "2026-04-10T18:00:00Z",
  "model_used": "mock-summarizer",
  "token_count": 200,
  "alert_ids": [103, 113],
  "stage_category": "Stage 3 & 4",
  "presentation_notes": "Highlights wildfire-related alerts and forecasting"
}
```

---

## Extending Browser Automation

### Placeholder: Playwright Integration

*Phase 3 will implement Playwright-based browser automation. For now, manual demo walkthrough is the primary flow.*

### Future: Adding New User Journey

Once Playwright is integrated, you can add custom journeys:

```javascript
// frontend/web/tests/demo/journeys/custom_journey.js (Future)
export async function runCustomJourney(browser, options = {}) {
  const page = await browser.newPage();
  
  // Navigation example
  await page.goto('http://localhost:8000/risk.php');
  await page.fill('input[name="user_id"]', '3');
  await page.fill('input[name="radius"]', '75');
  await page.click('button:has-text("Calculate")');
  
  // Wait and screenshot
  await page.waitForSelector('.risk-score-result');
  await page.screenshot({ path: 'demo_risk_custom.png' });
  
  await page.close();
}
```

---

## Creating Custom Demo Scenarios

### Scenario 1: "First-Time User" Flow

**Goal**: Demonstrate user onboarding from registration to first personalized alert.

**Steps**:
1. Go to `/register.php`
2. Register as "New Demo User" with asthma sensitivity
3. Navigate to `/alerts.php`
4. Filter by "air_quality"
5. Go to `/risk.php` with the new user ID
6. Show air quality alerts ranked higher due to asthma

**Notes**:
- Emphasize how personalization kicks in immediately after settings
- Compare risk score before/after sensitivity settings

### Scenario 2: "Emergency Response" Flow

**Goal**: Demonstrate how the system prioritizes during a crisis (high air quality event).

**Setup**: Manually add a high-severity pollution alert to fixtures:

```json
{
  "id": 200,
  "alert_type": "pollution",
  "severity": "high",
  "title": "HAZMAT INCIDENT - Downtown LA",
  "description": "Chemical spill detected near industrial area...",
  "latitude": 34.0501,
  "longitude": -118.2426,
  "event_start": "2026-04-10T15:00:00Z",
  "event_end": "2026-04-10T20:00:00Z",
  "raw_data": {"incident_type": "hazmat", "radius_km": 2, "evacuation_recommended": true}
}
```

**Demo Flow**:
1. Reset demo: `npm run demo:reset`
2. Go to `/smart_alerts.php` with user ID 2 (respiratory sensitivities)
3. Show incident alert ranked at the top due to high severity + sensitivity match
4. Go to `/map.php`, zoom to incident location, show personalized overlays highlighting the zone

### Scenario 3: "Data Scale" Flow

**Goal**: Show system performance with larger datasets.

**Setup**:
```bash
npm run demo:generate-alerts -- --count 500 --distribution balanced
```

**Demo Flow**:
1. Go to `/alerts.php`
2. Apply filters: severity=high, alert_type=air_quality
3. Show pagination or scrolling through large results
4. Open DevTools → Performance tab
5. Measure page load time, rendering time
6. Go to `/smart_alerts.php` with same filters
7. Compare prioritization performance on larger dataset

---

## Troubleshooting Common Issues

### Issue: `npm run demo:setup` fails with "Python not found"

**Cause**: Virtual environment not activated or Python path not in PATH.

**Solution**:
```bash
# Ensure .venv exists
python -m venv .venv

# Activate (Windows)
.venv\Scripts\Activate.ps1

# Or on Unix
source .venv/bin/activate

# Try again
npm run demo:setup
```

### Issue: Demo database is stale; features not responding

**Cause**: Schema changed but demo.db wasn't reset.

**Solution**:
```bash
npm run demo:clean
npm run demo:setup
npm run demo:verify
```

### Issue: `Demo user exists with ID already` error during seed

**Cause**: Multiple seed attempts without clean.

**Solution**:
```bash
npm run demo:reset  # Clears and reseeds
```

### Issue: Backend returns 404 for `/api/v1/alerts`

**Cause**: Backend API not running or wrong URL in PHP config.

**Solution**:
1. Verify backend running: `python backend/main.py` in separate terminal
2. Check [frontend/web/config/config.php](../frontend/web/config/config.php) for `API_BASE_URL`
3. Ensure it matches backend host/port (e.g., `http://localhost:8000`)

### Issue: Map doesn't load on `/map.php`

**Cause**: Plotly library missing or geospatial data malformed.

**Solution**:
1. Check browser console (F12) for JavaScript errors
2. Verify alerts have valid lat/lon in demo.db
3. Ensure `risk_map.js` is properly loaded: check `<script src="...risk_map.js">` in page HTML

### Issue: Assistant widget shows blank on `/assistant.php`

**Cause**: React component not compiled or API misconfiguration.

**Solution**:
1. Check browser console for errors
2. Verify React bundle exists: `ls frontend/public/Golby/`
3. Check backend `/api/v1/assistant/` endpoint is responding

---

## Adding Features to Demo Suite

### Before & After: Adding a New Risk Factor

**Scenario**: You want to add "Pollen Count" as a new risk factor in Stage 2.

**Steps**:

1. **Update models** (`backend/db/models.py`):
   ```python
   class Alert(Base):
       # ...
       pollen_count = Column(Integer, nullable=True)  # New field
   ```

2. **Update risk scoring** (`backend/services/risk_scoring.py`):
   ```python
   pollen_factor = (alert.pollen_count or 0) / 500.0  # Normalize 0-1
   base_score = (pollen_factor × 0.15) + (other_factors...)  # Adjust weights
   ```

3. **Update fixtures** (`backend/demo/fixtures.json`):
   ```json
   {
     "id": 116,
     "alert_type": "pollen",
     "title": "High Pollen Count",
     "raw_data": {"pollen_count": 450}
   }
   ```

4. **Reseed**:
   ```bash
   npm run demo:seed
   ```

5. **Update demo runbook** ([DEMO_RUNBOOK.md](./DEMO_RUNBOOK.md)):
   - Add pollen alerts to Step 3 narrative
   - Explain pollen weighting in risk score

6. **Update feature mapping** ([DEMO_FEATURES_BY_STAGE.md](./DEMO_FEATURES_BY_STAGE.md)):
   - Add row for pollen risk factor

---

## Testing Your Customizations

### Unit Test Template

```python
# backend/tests/test_demo_custom.py
import pytest
from backend.demo.seed_demo_data import load_fixtures
from backend.db.models import Alert

def test_custom_alert_loads():
    """Verify custom alert fixture loads correctly."""
    fixtures = load_fixtures()
    alert = next((a for a in fixtures['alerts'] if a['id'] == 200), None)
    assert alert is not None
    assert alert['severity'] == 'high'
    assert alert['latitude'] is not None
```

### Integration Test Template

```python
# Test that custom alerts influence risk scoring
def test_hazmat_alert_impacts_risk_score(db_session, api_client):
    """Hazmat incident should increase risk for nearby users."""
    user = db_session.query(User).filter_by(id=2).first()
    
    # Get baseline score
    response1 = api_client.get(f"/api/v1/risk/me?user_id={user.id}")
    baseline_score = response1.json()['risk_score']
    
    # Add hazmat alert near user
    # ... insert alert ...
    
    # Recalculate score
    response2 = api_client.get(f"/api/v1/risk/me?user_id={user.id}")
    new_score = response2.json()['risk_score']
    
    # Assert score increased
    assert new_score > baseline_score
```

---

## Documentation Maintenance

When you add or modify demo features, keep these documents in sync:

1. **[DEMO_RUNBOOK.md](./DEMO_RUNBOOK.md)** — Update narrative and step descriptions
2. **[DEMO_FEATURES_BY_STAGE.md](./DEMO_FEATURES_BY_STAGE.md)** — Add feature-to-code mapping
3. **[../README.md](../README.md)** — Update feature checklist if necessary
4. **Fixtures versioning** — Bump `_metadata.version` in [fixtures.json](../backend/demo/fixtures.json) if schema changes

---

## Best Practices

✅ **DO:**
- Keep fixtures deterministic (same inputs → same outputs) for reproducible demos
- Add `presentation_notes` to fixtures explaining what graders should notice
- Test custom scenarios before presenting to stakeholders
- Document why you modified demo data (e.g., "Added scenario for high-severity air quality event")

❌ **DON'T:**
- Manually edit demo.db with raw SQL (regenerate from fixtures instead)
- Hardcode test user IDs in custom scripts (use fixtures)
- Leave demo data in inconsistent state (always reseed before/after experiments)
- Skip running `npm run demo:verify` after modifications

---

## Next Steps

1. **For Graders**: Use [DEMO_RUNBOOK.md](./DEMO_RUNBOOK.md) to run the presentation
2. **For Team Members**: Modify fixtures and fixtures to add custom scenarios
3. **For Developers**: Extend mock_alert_generator.py to support new alert types
4. **For Maintenance**: Check this guide when adding new stages or features

---

**Questions?** Refer to the main [README.md](../README.md) or individual stage planning docs in [docs/PLANNING_DOCS/](../PLANNING_DOCS/).
