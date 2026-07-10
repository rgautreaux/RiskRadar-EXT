# Travel MVP Features Scaffolding

**Project:** RiskRadar CMPS 357 — Travel-Specific Enhancements  
**Features:** Saved locations, trip alerts, timezone support  
**Timeline:** 2–5 days per feature (backend + frontend + tests)

---

## Feature 1: Saved Locations

### Database Schema

```sql
CREATE TABLE user_locations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    name VARCHAR(255),          -- e.g., "Office", "Home", "Costa Rica Trip"
    latitude FLOAT,
    longitude FLOAT,
    zip_code VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
```

### Backend API

Add to `backend/api/users.py`:

```python
@router.post("/locations")
async def save_location(
    user_id: int, 
    name: str, 
    lat: float, 
    lon: float, 
    db: Session
):
    """Save a location for quick alert/risk lookups."""
    loc = UserLocation(
        user_id=user_id,
        name=name,
        latitude=lat,
        longitude=lon
    )
    db.add(loc)
    db.commit()
    return {"id": loc.id, "name": loc.name}

@router.get("/locations/{user_id}")
async def get_locations(user_id: int, db: Session):
    """List all saved locations for user."""
    return db.query(UserLocation).filter_by(user_id=user_id).all()

@router.delete("/locations/{location_id}")
async def delete_location(location_id: int, db: Session):
    """Remove saved location."""
    loc = db.query(UserLocation).get(location_id)
    if loc:
        db.delete(loc)
        db.commit()
    return {"status": "deleted"}
```

### Frontend UI

Add to `frontend/web/views/profile.php`:

```php
<h3>Saved Locations</h3>
<div id="locations-list"></div>

<h4>Add Location</h4>
<form id="add-location-form">
    <input type="text" name="location_name" placeholder="e.g., Costa Rica House" />
    <input type="text" name="zip_code" placeholder="ZIP/Postal Code" />
    <input type="number" name="latitude" placeholder="Latitude" step="0.0001" />
    <input type="number" name="longitude" placeholder="Longitude" step="0.0001" />
    <button type="submit">Save Location</button>
</form>

<script>
document.getElementById('add-location-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = new FormData(e.target);
    const response = await fetch(`/api/v1/users/${userId}/locations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(Object.fromEntries(data))
    });
    if (response.ok) {
        alert('Location saved!');
        loadLocations();
    }
});
</script>
```

---

## Feature 2: Trip Alerts (Smart Notifications for Trips)

### Database Schema

```sql
CREATE TABLE trips (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    name VARCHAR(255),          -- e.g., "Costa Rica 2026"
    start_date DATE,
    end_date DATE,
    primary_location_id INT,    -- Foreign key to user_locations
    alert_types VARCHAR(255),   -- JSON: ["wildfire", "air_quality"]
    notify_via VARCHAR(50),     -- "email", "sms", "push"
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (primary_location_id) REFERENCES user_locations(id)
);
```

### Backend API

Add to `backend/api/users.py`:

```python
@router.post("/trips")
async def create_trip(
    user_id: int,
    name: str,
    start_date: str,
    end_date: str,
    primary_location_id: int,
    alert_types: list[str],
    db: Session
):
    """Create a trip with specific alert rules."""
    trip = Trip(
        user_id=user_id,
        name=name,
        start_date=start_date,
        end_date=end_date,
        primary_location_id=primary_location_id,
        alert_types=json.dumps(alert_types)
    )
    db.add(trip)
    db.commit()
    return trip

@router.get("/trips/{user_id}")
async def get_trips(user_id: int, db: Session):
    """List active and past trips."""
    return db.query(Trip).filter_by(user_id=user_id).all()
```

### Trip-Aware Alert Filtering

Modify `backend/api/alerts.py` to filter by active trip:

```python
@router.get("/alerts/trip/{trip_id}")
async def get_trip_alerts(trip_id: int, db: Session):
    """Get alerts relevant to active trip."""
    trip = db.query(Trip).get(trip_id)
    if not trip:
        raise HTTPException(status_code=404)
    
    # Filter alerts by trip location and active period
    alerts = db.query(Alert).filter(
        Alert.created_at >= trip.start_date,
        Alert.created_at <= trip.end_date,
        # ... geospatial distance filter ...
    ).all()
    
    return alerts
```

---

## Feature 3: Timezone Support

### Backend Config

Add to `backend/config/settings.py`:

```python
from zoneinfo import ZoneInfo

class Settings:
    SUPPORTED_TIMEZONES = [
        "America/New_York",
        "America/Chicago", 
        "America/Denver",
        "America/Los_Angeles",
        "Europe/London",
        "Europe/Paris",
        "Asia/Tokyo",
        "Australia/Sydney",
        # Add more as needed
    ]
    DEFAULT_TIMEZONE = "America/New_York"
```

### User Timezone Preference

Update `User` model in `backend/db/models.py`:

```python
class User(Base):
    # ... existing fields ...
    timezone = Column(String(50), default="America/New_York")
    
    def get_local_time(self, utc_time):
        """Convert UTC time to user's timezone."""
        from datetime import datetime
        from zoneinfo import ZoneInfo
        
        tz = ZoneInfo(self.timezone or "America/New_York")
        return utc_time.replace(tzinfo=ZoneInfo("UTC")).astimezone(tz)
```

### Frontend Timezone Selector

Add to `frontend/web/views/profile.php`:

```php
<label for="timezone">Timezone</label>
<select name="timezone" id="timezone">
    <option value="America/New_York">Eastern Time</option>
    <option value="America/Chicago">Central Time</option>
    <option value="America/Denver">Mountain Time</option>
    <option value="America/Los_Angeles">Pacific Time</option>
    <option value="Europe/London">GMT</option>
    <option value="Europe/Paris">CET</option>
    <option value="Asia/Tokyo">JST</option>
    <option value="Australia/Sydney">AEDT</option>
</select>
```

---

## 4. Implementation Roadmap

| Feature | Backend | Frontend | Tests | Priority |
|---------|---------|----------|-------|----------|
| Saved Locations | 2h | 1h | 1h | High |
| Trip Alerts | 2h | 2h | 1h | High |
| Timezone Support | 1h | 1h | 0.5h | Medium |

**Total effort:** ~12 hours (phased rollout recommended)

---

## 5. Phase 1: Saved Locations (Quickest Win)

1. Add `user_locations` table migration
2. Implement `/locations` CRUD endpoints
3. Add profile UI for managing locations
4. Test end-to-end
5. Open PR: "feat: saved locations for quick lookups"

---

## 6. Phase 2: Trip Alerts (Medium Complexity)

1. Add `trips` table
2. Implement `/trips` CRUD endpoints
3. Modify alert query to support trip context
4. Add trip management UI
5. Add notification logic (wire to backend email/SMS if available)
6. Open PR: "feat: trip-aware alert notifications"

---

## 7. Phase 3: Timezone Support (Low Risk)

1. Add `timezone` column to `users` table
2. Add timezone selector to profile
3. Update all time displays to use user's timezone
4. Add helper function to convert times
5. Test alerts/forecasts display in correct timezone
6. Open PR: "feat: timezone support for global travelers"

---

## 8. Feature Flags

Wrap behind feature flags during rollout:

```python
# backend/config/settings.py
FEATURE_SAVED_LOCATIONS = getenv("FEATURE_SAVED_LOCATIONS") == "true"
FEATURE_TRIP_ALERTS = getenv("FEATURE_TRIP_ALERTS") == "true"
FEATURE_TIMEZONE = getenv("FEATURE_TIMEZONE") == "true"
```

```php
// frontend/web/components/features.php
$features = [
    'saved_locations' => getenv('FEATURE_SAVED_LOCATIONS') === 'true',
    'trip_alerts' => getenv('FEATURE_TRIP_ALERTS') === 'true',
    'timezone' => getenv('FEATURE_TIMEZONE') === 'true',
];
```

---

## 9. Testing Checklist

- [ ] Saved locations CRUD works end-to-end
- [ ] Trip creation and alert filtering work
- [ ] Timezone conversions are accurate
- [ ] No regressions in existing alerts/forecast/map flows
- [ ] Mobile responsive (360px–768px)
- [ ] Accessible (keyboard, screen reader)

---

## 10. Next Steps

1. Pick Phase 1 (saved locations) as first PR
2. Implement, test, gather feedback
3. Merge and move to Phase 2
4. Iterate until all phases complete

**Recommended sequence:** Locations → Trips → Timezone (each 1–2 PRs)
