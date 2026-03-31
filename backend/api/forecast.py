from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Alert
from datetime import datetime, timedelta
from schemas.risk_score import MapRiskZone, MapRiskOverlayOut
from typing import Optional

router = APIRouter(prefix="/forecast", tags=["Forecast"])

@router.get("", response_model=MapRiskOverlayOut)
def get_forecast(
    lat: Optional[float] = Query(None, description="Latitude for location-based forecast"),
    lon: Optional[float] = Query(None, description="Longitude for location-based forecast"),
    location: Optional[str] = Query(None, description="Location string (ZIP or City, State)"),
    hours: int = Query(48, ge=1, le=72, description="Forecast window in hours (default 48)"),
    db: Session = Depends(get_db),
):
    """
    Returns a risk forecast for the next 24-48 hours for a given location (lat/lon or location string).
    """
    # For MVP: Use alerts as risk proxies for the forecast window
    now = datetime.utcnow()
    window_end = now + timedelta(hours=hours)
    q = db.query(Alert)
    # Filter by time window
    q = q.filter(Alert.event_start <= window_end.isoformat(), Alert.event_end >= now.isoformat())
    # Filter by location if provided
    if lat is not None and lon is not None:
        # Simple radius filter (MVP: bounding box)
        lat_min, lat_max = lat - 1.0, lat + 1.0
        lon_min, lon_max = lon - 1.0, lon + 1.0
        q = q.filter(Alert.latitude >= lat_min, Alert.latitude <= lat_max,
                     Alert.longitude >= lon_min, Alert.longitude <= lon_max)
    elif location:
        # MVP: naive substring match on location_name
        q = q.filter(Alert.location_name.ilike(f"%{location}%"))
    alerts = q.all()
    risk_zones = []
    for alert in alerts:
        centroid = {"lat": alert.latitude, "lon": alert.longitude}
        sev = (alert.severity or "").lower()
        if sev in ("high", "critical"): rl = "high"
        elif sev == "moderate": rl = "moderate"
        else: rl = "low"
        risk_zones.append(MapRiskZone(centroid=centroid, risk_level=rl, risk_score=None))
    region_val = location or (f"{lat},{lon}" if lat and lon else "all")
    return MapRiskOverlayOut(
        risk_zones=risk_zones,
        region=region_val,
        generated_at=now.isoformat() + "Z",
    )
