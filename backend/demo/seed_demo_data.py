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
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Add backend directory to path for package imports (auth, db, etc.)
sys.path.insert(0, str(Path(__file__).parent.parent))

from ..auth.security import create_session_token, encrypt_email, hash_email, password_hash
from ..db.models import Alert, Base, Summary, User
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker


def build_demo_session_factory(db_path: str):
    """Create an isolated SQLAlchemy engine/session factory for the demo DB path."""
    resolved = Path(db_path).resolve()
    database_url = f"sqlite:///{resolved}"
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    session_factory = sessionmaker(bind=engine)
    return engine, session_factory


def load_fixtures() -> dict[str, Any]:
    """Load fixtures.json from the demo directory."""
    fixtures_path = Path(__file__).parent / "fixtures.json"
    if not fixtures_path.exists():
        raise FileNotFoundError(f"Fixtures file not found: {fixtures_path}")
    
    with open(fixtures_path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_demo_db(engine, db_path: str = "demo.db") -> str:
    """Create a fresh demo database."""
    db_path = Path(db_path).resolve()
    if db_path.exists():
        db_path.unlink()
        print(f"✓ Removed existing demo database: {db_path}")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print(f"✓ Created fresh demo database: {db_path}")
    return str(db_path)


def seed_users(session, fixtures: dict[str, Any]) -> dict[str, Any]:
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
            alert_types=json.dumps(user_data.get("alert_types", [])),
            notify_severity=user_data.get("notify_severity", "medium"),
            health_conditions=json.dumps(user_data.get("health_conditions", {})),
            created_at=datetime.now(timezone.utc).isoformat(),
            updated_at=datetime.now(timezone.utc).isoformat(),
        )
        session.add(user)
        session.flush()  # Ensure ID is assigned
        
        # Generate session token
        token, expires_at = create_session_token(user.id)
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


def seed_alerts(session, fixtures: dict[str, Any]) -> dict[int, dict[str, Any]]:
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
            event_start=event_start.isoformat(),
            event_end=event_end.isoformat() if event_end else None,
            raw_data=json.dumps(alert_data.get("raw_data", {})),
            fetched_at=datetime.now(timezone.utc).isoformat(),
            created_at=datetime.now(timezone.utc).isoformat(),
            updated_at=datetime.now(timezone.utc).isoformat(),
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


def seed_summaries(session, fixtures: dict[str, Any]) -> dict[int, dict[str, Any]]:
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
            generated_at=generated_at.isoformat(),
            model_used=summary_data.get("model_used", "mock-summarizer"),
            token_count=summary_data.get("token_count", 0),
            alert_ids=json.dumps(summary_data.get("alert_ids", [])),
            created_at=datetime.now(timezone.utc).isoformat(),
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


def save_metadata(metadata: dict[str, Any], db_path: str = "demo.db") -> None:
    """Save seeding metadata to JSON file for reference."""
    metadata_path = Path(db_path).parent / "seed_metadata.json"
    metadata["db_path"] = str(Path(db_path).resolve())
    metadata["seed_timestamp"] = datetime.now(timezone.utc).isoformat()
    metadata["fixtures_version"] = "1.0"
    
    with open(metadata_path, "w", encoding="utf-8") as f:
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
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify demo.db schema and seed data completeness (don't modify DB)",
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Print seed_metadata.json (user IDs, tokens, alert counts)",
    )
    parser.add_argument(
        "--clean-only",
        action="store_true",
        help="Remove demo.db and seed_metadata.json without reseeding",
    )
    args = parser.parse_args()
    
    try:
        print("\n🌍 RiskRadar Demo Data Seeding Script")
        print(f"Mode: {args.mode} | Database: {args.db_path}")
        print("-" * 60)
        
        # Handle info/verify/clean operations
        if args.info:
            metadata_path = Path(args.db_path).parent / "seed_metadata.json"
            if metadata_path.exists():
                with open(metadata_path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                print("\n📋 Seed Metadata:")
                print(json.dumps(metadata, indent=2))
                return 0
            else:
                print(f"❌ No seed metadata found at {metadata_path}")
                return 1
        
        if args.verify:
            db_path = Path(args.db_path)
            if not db_path.exists():
                print(f"❌ Database not found at {db_path}")
                return 1
            
            print(f"\n📊 Verifying demo database: {db_path}")
            _, session_factory = build_demo_session_factory(str(db_path))
            session = session_factory()
            
            # Count records
            user_count = session.query(User).count()
            alert_count = session.query(Alert).count()
            summary_count = session.query(Summary).count()
            
            print(f"  ✓ Users: {user_count}")
            print(f"  ✓ Alerts: {alert_count}")
            print(f"  ✓ Summaries: {summary_count}")
            
            session.close()
            
            # Expected counts
            expected_users = 4
            expected_alerts = 15
            expected_summaries = 2
            
            all_good = (
                user_count >= expected_users
                and alert_count >= expected_alerts
                and summary_count >= expected_summaries
            )
            
            if all_good:
                print("\n✅ Demo database verification passed!")
                return 0
            else:
                print(
                    f"\n⚠️  Warning: Expected at least {expected_users} users, "
                    f"{expected_alerts} alerts, {expected_summaries} summaries"
                )
                return 1
        
        if args.clean_only:
            db_path = Path(args.db_path)
            metadata_path = db_path.parent / "seed_metadata.json"
            
            if db_path.exists():
                db_path.unlink()
                print(f"✓ Removed {db_path}")
            
            if metadata_path.exists():
                metadata_path.unlink()
                print(f"✓ Removed {metadata_path}")
            
            print("\n✅ Demo database and metadata cleaned!")
            return 0
        
        # Load fixtures
        fixtures = load_fixtures()
        print(f"✓ Loaded fixtures from {Path(__file__).parent}/fixtures.json")
        print(f"  - {len(fixtures['users'])} users")
        print(f"  - {len(fixtures['alerts'])} alerts")
        print(f"  - {len(fixtures['summaries'])} summaries")
        
        # Build isolated demo engine/session for this run
        engine, session_factory = build_demo_session_factory(args.db_path)

        # Handle database setup
        if args.mode == "fresh":
            db_path = create_demo_db(engine, args.db_path)

        # Ensure schema exists for seed/reset modes when DB already exists.
        Base.metadata.create_all(bind=engine)
        
        # Create session
        session = session_factory()
        
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
    
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user.", file=sys.stderr)
        return 130
    except (OSError, ValueError, RuntimeError) as e:
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
