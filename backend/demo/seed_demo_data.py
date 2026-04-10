#!/usr/bin/env python3
"""
RiskRadar Demo Data Seeding Script

Loads fixture data and seeds a SQLite database for demonstration purposes.
Supports modes:
  - fresh: Create a new demo.db from scratch
  - seed: Add fixtures to existing SQLite database
  - reset: Clear all data and reseed existing SQLite database

Usage:
    python seed_demo_data.py --mode fresh
    python seed_demo_data.py --mode seed
    python seed_demo_data.py --mode reset
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from auth.security import encrypt_email, hash_email, password_hash, create_session_token
from db.database import SessionLocal, engine
from db.models import Base, Alert, Summary, User
from sqlalchemy import text


def load_fixtures() -> dict:
    """Load fixtures.json from the demo directory."""
    fixtures_path = Path(__file__).parent / "fixtures.json"
    if not fixtures_path.exists():
        raise FileNotFoundError(f"Fixtures file not found: {fixtures_path}")
    
    with open(fixtures_path, "r") as f:
        return json.load(f)


def create_demo_db(db_path: str = "demo.db") -> str:
    """Create a fresh demo database."""
    db_path = Path(db_path).resolve()
    if db_path.exists():
        db_path.unlink()
        print(f"✓ Removed existing demo database: {db_path}")
    
    # Create all tables
    Base.metadata.create_all(engine)
    print(f"✓ Created fresh demo database: {db_path}")
    return str(db_path)


def seed_users(session, fixtures: dict) -> dict:
    """Seed users from fixtures into database."""
    users_data = fixtures.get("users", [])
    created_users = {}
    session_tokens = {}
    
    for user_data in users_data:
        user = User(
            id=user_data["id"],
            email=encrypt_email(user_data["email_plaintext"]),
            email_lookup_hash=hash_email(user_data["email_plaintext"]),
            password_hash=password_hash(user_data["password_plaintext"]),
            display_name=user_data["display_name"],
            zip_code=user_data.get("zip_code"),
            latitude=user_data.get("latitude"),
            longitude=user_data.get("longitude"),
            is_admin=user_data.get("is_admin", False),
            alert_types=user_data.get("alert_types", []),
            notify_severity=user_data.get("notify_severity", "medium"),
            health_conditions=user_data.get("health_conditions", {}),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        session.add(user)
        session.flush()  # Ensure ID is assigned
        
        # Generate session token
        token, expires_at = create_session_token(user["id"])
        session_tokens[user_data["id"]] = {
            "token": token,
            "expires_at": expires_at.isoformat(),
            "user_id": user_data["id"],
            "email_plaintext": user_data["email_plaintext"],
        }
        
        created_users[user_data["id"]] = {
            "id": user_data["id"],
            "email": user_data["email_plaintext"],
            "display_name": user_data["display_name"],
            "health_conditions": user_data.get("health_conditions", {}),
        }
        
        print(f"  ✓ User {user_data['id']}: {user_data['display_name']}")
    
    session.commit()
    return {"users": created_users, "session_tokens": session_tokens}


def seed_alerts(session, fixtures: dict) -> dict:
    """Seed alerts from fixtures into database."""
    alerts_data = fixtures.get("alerts", [])
    created_alerts = {}
    
    for alert_data in alerts_data:
        # Parse event times
        event_start = datetime.fromisoformat(alert_data["event_start"].replace("Z", "+00:00"))
        event_end = None
        if alert_data.get("event_end"):
            event_end = datetime.fromisoformat(alert_data["event_end"].replace("Z", "+00:00"))
        
        alert = Alert(
            id=alert_data["id"],
            source=alert_data["source"],
            source_id=alert_data["source_id"],
            alert_type=alert_data["alert_type"],
            severity=alert_data["severity"],
            title=alert_data["title"],
            description=alert_data["description"],
            location_name=alert_data.get("location_name"),
            latitude=alert_data.get("latitude"),
            longitude=alert_data.get("longitude"),
            event_start=event_start,
            event_end=event_end,
            raw_data=alert_data.get("raw_data", {}),
            fetched_at=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        session.add(alert)
        
        created_alerts[alert_data["id"]] = {
            "id": alert_data["id"],
            "alert_type": alert_data["alert_type"],
            "severity": alert_data["severity"],
            "title": alert_data["title"],
            "location": alert_data.get("location_name"),
        }
    
    session.commit()
    print(f"  ✓ Created {len(alerts_data)} alerts")
    return created_alerts


def seed_summaries(session, fixtures: dict) -> dict:
    """Seed summaries from fixtures into database."""
    summaries_data = fixtures.get("summaries", [])
    created_summaries = {}
    
    for summary_data in summaries_data:
        generated_at = datetime.fromisoformat(summary_data["generated_at"].replace("Z", "+00:00"))
        
        summary = Summary(
            id=summary_data["id"],
            title=summary_data["title"],
            content=summary_data["content"],
            summary_type=summary_data.get("summary_type", "daily_digest"),
            region=summary_data.get("region"),
            generated_at=generated_at,
            model_used=summary_data.get("model_used", "mock-summarizer"),
            token_count=summary_data.get("token_count", 0),
            alert_ids=summary_data.get("alert_ids", []),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        session.add(summary)
        session.flush()
        
        created_summaries[summary_data["id"]] = {
            "id": summary_data["id"],
            "title": summary_data["title"],
            "summary_type": summary_data.get("summary_type", "daily_digest"),
            "alert_count": len(summary_data.get("alert_ids", [])),
        }
    
    session.commit()
    print(f"  ✓ Created {len(summaries_data)} summaries")
    return created_summaries


def clear_demo_data(session) -> None:
    """Clear existing demo data (alerts, summaries, users)."""
    print("Clearing existing demo data...")
    session.execute(text("DELETE FROM alerts;"))
    session.execute(text("DELETE FROM summaries;"))
    session.execute(text("DELETE FROM users;"))
    session.commit()
    print("✓ Cleared all demo data")


def save_metadata(metadata: dict, db_path: str = "demo.db") -> None:
    """Save seeding metadata to JSON file for reference."""
    metadata_path = Path(db_path).parent / "seed_metadata.json"
    metadata["db_path"] = str(Path(db_path).resolve())
    metadata["seed_timestamp"] = datetime.now(timezone.utc).isoformat()
    metadata["fixtures_version"] = "1.0"
    
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"✓ Saved metadata to {metadata_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Seed RiskRadar demo database with fixture data"
    )
    parser.add_argument(
        "--mode",
        choices=["fresh", "seed", "reset"],
        default="fresh",
        help="Seeding mode: fresh (create new), seed (add to existing), reset (clear and reseed)",
    )
    parser.add_argument(
        "--db-path",
        default="demo.db",
        help="Path to database file (default: demo.db in current directory)",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        default=False,
        help="Fetch real environmental data from scrapers (not yet implemented)",
    )
    args = parser.parse_args()
    
    try:
        print(f"\n🌍 RiskRadar Demo Data Seeding Script")
        print(f"Mode: {args.mode} | Database: {args.db_path}")
        print("-" * 60)
        
        # Load fixtures
        fixtures = load_fixtures()
        print(f"✓ Loaded fixtures from {Path(__file__).parent}/fixtures.json")
        print(f"  - {len(fixtures['users'])} users")
        print(f"  - {len(fixtures['alerts'])} alerts")
        print(f"  - {len(fixtures['summaries'])} summaries")
        
        # Handle database setup
        if args.mode == "fresh":
            db_path = create_demo_db(args.db_path)
            os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
        
        # Create session
        session = SessionLocal()
        
        # Seed data
        print("\nSeeding data...")
        
        if args.mode == "reset":
            clear_demo_data(session)
        
        print("  Loading users...")
        user_result = seed_users(session, fixtures)
        
        print("  Loading alerts...")
        alerts_result = seed_alerts(session, fixtures)
        
        print("  Loading summaries...")
        summaries_result = seed_summaries(session, fixtures)
        
        session.close()
        
        # Prepare output metadata
        metadata = {
            "status": "success",
            "mode": args.mode,
            "demo_users": user_result["users"],
            "session_tokens": user_result["session_tokens"],
            "alerts_created": len(alerts_result),
            "alert_ids": list(alerts_result.keys()),
            "summaries_created": len(summaries_result),
            "summary_ids": list(summaries_result.keys()),
        }
        
        # Save metadata
        save_metadata(metadata, args.db_path)
        
        # Output results
        print("\n" + "=" * 60)
        print("✅ Demo Data Seeding Complete!")
        print("=" * 60)
        print(json.dumps(metadata, indent=2))
        print("=" * 60)
        
        return 0
    
    except Exception as e:
        error_result = {
            "status": "error",
            "error_message": str(e),
            "error_type": type(e).__name__,
        }
        print(f"\n❌ Error: {e}", file=sys.stderr)
        print(json.dumps(error_result, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
