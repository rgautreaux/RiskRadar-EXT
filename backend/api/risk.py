
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from ..db.database import get_db
from ..db.models import Alert, User
from ..schemas.risk_score import RiskScoreOut, MapRiskOverlayOut, MapRiskZone
from ..scoring import compute_risk_score
from ..scrapers.registry import load_all_scrapers

router = APIRouter(prefix="/risk", tags=["Risk Scoring"])

# Stage 3: Map Risk Overlay Endpoint
@router.get("/map", response_model=MapRiskOverlayOut)
def map_risk_overlay(
    region: str | None = None,
    bbox: str | None = None,
    # Removed unused argument 'risk_level'
    db: Session = Depends(get_db),
):
    # Overlay integration: fetch all overlays from registry
    overlays: list[MapRiskZone] = []
    for entry in load_all_scrapers():  # type: ignore
        scraper = entry["scraper"]  # type: ignore
        # Only process overlays (not all scrapers)
        if getattr(scraper, "alert_type", None) in {"air_quality", "wildfire", "weather", "pollution"}:
            # Fetch latest alerts for this overlay type
            q = db.query(Alert).filter(Alert.alert_type == scraper.alert_type)  # type: ignore
            if region and region.lower() != "all":
                q = q.filter(Alert.location_name.ilike(f"%{region}%"))
            if bbox:
                try:
                    minlon, minlat, maxlon, maxlat = map(float, bbox.split(","))
                    q = q.filter(
                        Alert.latitude >= minlat,
                        Alert.latitude <= maxlat,
                        Alert.longitude >= minlon,
                        Alert.longitude <= maxlon,
                    )
                except ValueError:
                    pass
            alerts = q.all()
            for alert in alerts:
                lat = float(alert.latitude) if alert.latitude is not None else None
                lon = float(alert.longitude) if alert.longitude is not None else None
                if lat is None or lon is None:
                    continue
                centroid = {"lat": lat, "lon": lon}
                sev = (alert.severity or "").lower()
                if sev in ("high", "critical"):
                    rl = "high"
                elif sev == "moderate":
                    rl = "moderate"
                else:
                    rl = "low"
                poly = [
                    {"lat": lat + 0.05, "lon": lon - 0.05},
                    {"lat": lat + 0.05, "lon": lon + 0.05},
                    {"lat": lat - 0.05, "lon": lon + 0.05},
                    {"lat": lat - 0.05, "lon": lon - 0.05},
                    {"lat": lat + 0.05, "lon": lon - 0.05},
                ]
                overlays.append(MapRiskZone(centroid=centroid, risk_level=rl, risk_score=None, polygon=poly))  # type: ignore
    region_val = region or "all"
    return MapRiskOverlayOut(
        risk_zones=overlays,  # type: ignore
        region=region_val,
        generated_at=datetime.now(timezone.utc).isoformat() + "Z",
    )


# New: Personalized Map Risk Overlay Endpoint
@router.get("/map/personalized/{user_id}", response_model=MapRiskOverlayOut)
def personalized_map_risk_overlay(
    user_id: int,
    region: str | None = None,
    # Removed unused argument 'bbox'
    db: Session = Depends(get_db),
):
    """Return a map overlay with user-personalized risk scores for each alert location."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    alerts = db.query(Alert).filter(Alert.latitude.isnot(None), Alert.longitude.isnot(None)).all()
    risk_zones: list[MapRiskZone] = []
    for alert in alerts:
        lat = float(alert.latitude) if alert.latitude is not None else None
        lon = float(alert.longitude) if alert.longitude is not None else None
        if lat is None or lon is None:
            continue
        centroid = {"lat": lat, "lon": lon}
        # Compute personalized risk score for this alert location
        # Temporarily override user location to alert location for scoring
        orig_lat, orig_lon = user.latitude, user.longitude
        user.latitude, user.longitude = lat, lon
        risk_score_result = compute_risk_score(user, db)
        user.latitude, user.longitude = orig_lat, orig_lon
        risk_score = risk_score_result.overall_score
        risk_level = risk_score_result.risk_level
        # Example: add a simple square polygon around the centroid (0.1 deg offset)
        poly = [
            {"lat": lat + 0.05, "lon": lon - 0.05},
            {"lat": lat + 0.05, "lon": lon + 0.05},
            {"lat": lat - 0.05, "lon": lon + 0.05},
            {"lat": lat - 0.05, "lon": lon - 0.05},
            {"lat": lat + 0.05, "lon": lon - 0.05},
        ]
        risk_zones.append(MapRiskZone(centroid=centroid, risk_level=risk_level, risk_score=risk_score, polygon=poly))
    region_val = region or "all"
    return MapRiskOverlayOut(
        risk_zones=risk_zones,
        region=region_val,
        generated_at=datetime.now(timezone.utc).isoformat() + "Z",
    )


@router.get("/score/{user_id}", response_model=RiskScoreOut)
def get_risk_score(
    user_id: int,
    radius_km: float = Query(default=150.0, ge=1.0, le=500.0),
    db: Session = Depends(get_db),
):
    """Compute a personalized environmental risk score for the user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return compute_risk_score(user, db, radius_km=radius_km)
