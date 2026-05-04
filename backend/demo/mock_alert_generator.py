#!/usr/bin/env python3
"""
RiskRadar Mock Alert Generator

Generates additional environmental alerts on-demand for demonstration,
stress-testing, or custom showcase scenarios.

Usage:
    python mock_alert_generator.py --count 20 --alert-type air_quality
    python mock_alert_generator.py --count 50 --location "san_francisco"
    python mock_alert_generator.py --count 100 --severity high --distribution balanced
"""

import argparse
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List

# Alert type definitions
ALERT_TYPES = ["weather", "air_quality", "wildfire", "earthquake", "pollution"]

# Severity distribution
SEVERITY_LEVELS = ["low", "medium", "high"]

# Weather alert templates
WEATHER_ALERTS = [
    {"title": "Heat Advisory", "description": "Excessive heat expected. Drink fluids and stay indoors during peak hours."},
    {"title": "Cold Warning", "description": "Dangerous cold expected. Limit outdoor exposure."},
    {"title": "Wind Advisory", "description": "Strong winds expected. Secure loose objects."},
    {"title": "Flood Warning", "description": "Flash flooding possible. Avoid flood-prone areas."},
    {"title": "Tornado Watch", "description": "Tornado conditions possible. Stay alert."},
    {"title": "Dense Fog Advisory", "description": "Visibility severely reduced. Drive carefully."},
    {"title": "Winter Storm Warning", "description": "Heavy snow and ice expected."},
    {"title": "Thunderstorm Warning", "description": "Severe thunderstorms expected."},
]

# Air quality alert templates
AIR_QUALITY_ALERTS = [
    {"title": "Air Quality Alert", "description": "Unhealthy air quality. Sensitive groups should avoid outdoor activities."},
    {"title": "Ozone Alert", "description": "High ozone levels. Reduce strenuous outdoor activity."},
    {"title": "Particulate Matter Alert", "description": "High PM2.5 levels. Use air filtration."},
    {"title": "AQI Unhealthy for Sensitive Groups", "description": "Air quality concerns for respiratory conditions."},
]

# Wildfire alert templates
WILDFIRE_ALERTS = [
    {"title": "Wildfire Activity Detected", "description": "Thermal anomaly detected. Under monitoring."},
    {"title": "Active Wildfire", "description": "Wildfire currently burning. Evacuation possible."},
    {"title": "Wildfire Smoke Advisory", "description": "Heavy smoke affecting air quality."},
]

# Earthquake definitions
EARTHQUAKE_ALERTS = [
    {"title": "Minor Earthquake", "magnitude": "2.5", "description": "Minor earthquake detected. No damage expected."},
    {"title": "Small Earthquake", "magnitude": "3.5", "description": "Small earthquake detected. Minor damage possible."},
    {"title": "Moderate Earthquake", "magnitude": "4.5", "description": "Moderate earthquake detected. Damage possible in affected areas."},
    {"title": "Strong Earthquake", "magnitude": "5.5", "description": "Strong earthquake detected. Significant damage possible."},
]

# Pollution alert templates
POLLUTION_ALERTS = [
    {"title": "Industrial Emissions Alert", "description": "Industrial pollution levels elevated. Limit exposure."},
    {"title": "Vehicle Emission Alert", "description": "Traffic pollution high. Consider alternative transportation."},
    {"title": "Hazardous Waste Advisory", "description": "Potential hazardous material release. Follow local guidance."},
]

# Location presets with lat/lon ranges
LOCATIONS = {
    "los_angeles": {
        "center_lat": 34.0522,
        "center_lon": -118.2437,
        "lat_range": 0.5,
        "lon_range": 0.5,
        "region": "Los Angeles, CA",
    },
    "san_francisco": {
        "center_lat": 37.7749,
        "center_lon": -122.4194,
        "lat_range": 0.3,
        "lon_range": 0.3,
        "region": "San Francisco, CA",
    },
    "san_diego": {
        "center_lat": 32.7157,
        "center_lon": -117.1611,
        "lat_range": 0.3,
        "lon_range": 0.3,
        "region": "San Diego, CA",
    },
    "seattle": {
        "center_lat": 47.6062,
        "center_lon": -122.3321,
        "lat_range": 0.3,
        "lon_range": 0.3,
        "region": "Seattle, WA",
    },
    "denver": {
        "center_lat": 39.7392,
        "center_lon": -104.9903,
        "lat_range": 0.4,
        "lon_range": 0.4,
        "region": "Denver, CO",
    },
}


def generate_alert_id(base_id: int) -> int:
    """Generate unique alert ID based on base."""
    return 200 + base_id  # Start at 200 to avoid fixture conflicts


def generate_random_location(location: str = "los_angeles") -> tuple:
    """Generate random coordinates within location bounds."""
    loc = LOCATIONS.get(location.lower(), LOCATIONS["los_angeles"])
    lat = loc["center_lat"] + random.uniform(-loc["lat_range"], loc["lat_range"])
    lon = loc["center_lon"] + random.uniform(-loc["lon_range"], loc["lon_range"])
    return lat, lon, loc["region"]


def generate_weather_alert(alert_id: int, severity: str, location: str) -> dict:
    """Generate weather alert."""
    template = random.choice(WEATHER_ALERTS)
    lat, lon, region = generate_random_location(location)
    
    event_start = datetime.now(timezone.utc)
    event_end = event_start + timedelta(hours=random.randint(4, 48))
    
    return {
        "id": alert_id,
        "source": "nws",
        "source_id": f"nws_generated_{alert_id}",
        "alert_type": "weather",
        "severity": severity,
        "title": template["title"],
        "description": template["description"],
        "location_name": region,
        "latitude": round(lat, 4),
        "longitude": round(lon, 4),
        "event_start": event_start.isoformat(),
        "event_end": event_end.isoformat(),
        "raw_data": {"region": region, "generated": True},
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def generate_air_quality_alert(alert_id: int, severity: str, location: str) -> dict:
    """Generate air quality alert."""
    template = random.choice(AIR_QUALITY_ALERTS)
    lat, lon, region = generate_random_location(location)
    
    aqi_map = {"low": random.randint(50, 100), "medium": random.randint(101, 200), "high": random.randint(201, 500)}
    aqi = aqi_map[severity]
    
    event_start = datetime.now(timezone.utc)
    event_end = event_start + timedelta(hours=random.randint(4, 12))
    
    return {
        "id": alert_id,
        "source": "epa",
        "source_id": f"epa_generated_{alert_id}",
        "alert_type": "air_quality",
        "severity": severity,
        "title": template["title"],
        "description": template["description"],
        "location_name": region,
        "latitude": round(lat, 4),
        "longitude": round(lon, 4),
        "event_start": event_start.isoformat(),
        "event_end": event_end.isoformat(),
        "raw_data": {"aqi": aqi, "pm2_5": round(random.uniform(10, 300), 1), "region": region, "generated": True},
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def generate_wildfire_alert(alert_id: int, severity: str, location: str) -> dict:
    """Generate wildfire alert."""
    template = random.choice(WILDFIRE_ALERTS)
    lat, lon, region = generate_random_location(location)
    
    event_start = datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 72))
    
    return {
        "id": alert_id,
        "source": "firms",
        "source_id": f"firms_generated_{alert_id}",
        "alert_type": "wildfire",
        "severity": severity,
        "title": template["title"],
        "description": template["description"],
        "location_name": region,
        "latitude": round(lat, 4),
        "longitude": round(lon, 4),
        "event_start": event_start.isoformat(),
        "event_end": None,
        "raw_data": {
            "satellite": random.choice(["NOAA-20", "VIIRS"]),
            "confidence": round(random.uniform(0.7, 0.99), 2),
            "region": region,
            "generated": True,
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def generate_earthquake_alert(alert_id: int, severity: str, location: str) -> dict:
    """Generate earthquake alert."""
    template = random.choice(EARTHQUAKE_ALERTS)
    lat, lon, region = generate_random_location(location)
    
    event_time = datetime.now(timezone.utc) - timedelta(hours=random.randint(0, 24))
    
    return {
        "id": alert_id,
        "source": "usgs",
        "source_id": f"usgs_generated_{alert_id}",
        "alert_type": "earthquake",
        "severity": severity,
        "title": template["title"],
        "description": template["description"],
        "location_name": region,
        "latitude": round(lat, 4),
        "longitude": round(lon, 4),
        "event_start": event_time.isoformat(),
        "event_end": event_time.isoformat(),
        "raw_data": {
            "magnitude": float(template["magnitude"]),
            "depth_km": round(random.uniform(5, 200), 1),
            "region": region,
            "generated": True,
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def generate_pollution_alert(alert_id: int, severity: str, location: str) -> dict:
    """Generate pollution alert."""
    template = random.choice(POLLUTION_ALERTS)
    lat, lon, region = generate_random_location(location)
    
    event_start = datetime.now(timezone.utc)
    event_end = event_start + timedelta(hours=random.randint(2, 8))
    
    return {
        "id": alert_id,
        "source": "epa",
        "source_id": f"epa_pollution_generated_{alert_id}",
        "alert_type": "pollution",
        "severity": severity,
        "title": template["title"],
        "description": template["description"],
        "location_name": region,
        "latitude": round(lat, 4),
        "longitude": round(lon, 4),
        "event_start": event_start.isoformat(),
        "event_end": event_end.isoformat(),
        "raw_data": {"pollutants": random.sample(["NO2", "CO", "SO2", "PM10"], 2), "region": region, "generated": True},
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def generate_alerts(
    count: int = 20,
    alert_type: str = None,
    location: str = "los_angeles",
    severity: str = None,
    distribution: str = "random",
) -> List[dict]:
    """Generate mock alerts based on parameters."""
    alerts = []
    
    # Determine alert types
    types_to_use = [alert_type] if alert_type else ALERT_TYPES
    
    # Determine severities
    severities_to_use = [severity] if severity else SEVERITY_LEVELS
    
    # Distribution logic
    if distribution == "balanced":
        # Distribute evenly across types and severities
        per_combination = max(1, count // (len(types_to_use) * len(severities_to_use)))
        for alert_t in types_to_use:
            for sev in severities_to_use:
                for _ in range(per_combination):
                    if len(alerts) < count:
                        alerts.append((alert_t, sev))
    else:
        # Random distribution
        for _ in range(count):
            alert_t = random.choice(types_to_use)
            sev = random.choice(severities_to_use)
            alerts.append((alert_t, sev))
    
    # Generate alert dictionaries
    generated_alerts = []
    alert_id_counter = 200
    
    generators = {
        "weather": generate_weather_alert,
        "air_quality": generate_air_quality_alert,
        "wildfire": generate_wildfire_alert,
        "earthquake": generate_earthquake_alert,
        "pollution": generate_pollution_alert,
    }
    
    for alert_type, severity in alerts[:count]:
        generator = generators[alert_type]
        alert = generator(alert_id_counter, severity, location)
        generated_alerts.append(alert)
        alert_id_counter += 1
    
    return generated_alerts


def main():
    parser = argparse.ArgumentParser(description="Generate mock environmental alerts")
    parser.add_argument("--count", type=int, default=20, help="Number of alerts to generate")
    parser.add_argument(
        "--alert-type",
        choices=ALERT_TYPES,
        help="Specific alert type (weather, air_quality, wildfire, earthquake, pollution)",
    )
    parser.add_argument(
        "--location",
        choices=list(LOCATIONS.keys()),
        default="los_angeles",
        help="Geographic location for alerts",
    )
    parser.add_argument("--severity", choices=SEVERITY_LEVELS, help="Specific severity level")
    parser.add_argument(
        "--distribution",
        choices=["random", "balanced"],
        default="random",
        help="Distribution strategy across types/severities",
    )
    parser.add_argument("--output-file", help="Save alerts to JSON file")
    parser.add_argument("--format", choices=["json", "sql"], default="json", help="Output format")
    
    args = parser.parse_args()
    
    print("\n📊 RiskRadar Mock Alert Generator")
    print(f"Generating {args.count} alerts...")
    print(f"  Location: {args.location}")
    if args.alert_type:
        print(f"  Alert Type: {args.alert_type}")
    if args.severity:
        print(f"  Severity: {args.severity}")
    print(f"  Distribution: {args.distribution}")
    print("-" * 60)
    
    alerts = generate_alerts(args.count, args.alert_type, args.location, args.severity, args.distribution)
    
    print(f"✓ Generated {len(alerts)} alerts\n")
    
    if args.output_file:
        output_path = Path(args.output_file)
        with open(output_path, "w") as f:
            json.dump(alerts, f, indent=2)
        print(f"✓ Saved to {output_path}")
    else:
        # Print summary
        type_counts = {}
        severity_counts = {}
        for alert in alerts:
            alert_type = alert["alert_type"]
            severity = alert["severity"]
            type_counts[alert_type] = type_counts.get(alert_type, 0) + 1
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        print("Alert Type Distribution:")
        for alert_type, count in sorted(type_counts.items()):
            print(f"  {alert_type}: {count}")
        
        print("\nSeverity Distribution:")
        for severity, count in sorted(severity_counts.items()):
            print(f"  {severity}: {count}")
        
        print("\nOutput (first 3 alerts):")
        print(json.dumps(alerts[:3], indent=2))


if __name__ == "__main__":
    main()
