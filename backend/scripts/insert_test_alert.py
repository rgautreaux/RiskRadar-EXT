
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from db.models import Alert
from db.database import SessionLocal

# Insert a single test alert into the alerts table

def insert_test_alert():
    session = SessionLocal()
    try:
        alert = Alert(
            source="test_source",
            source_id="test_001",
            alert_type="test_type",
            severity="info",
            title="Test Alert Title",
            description="This is a test alert inserted for verification.",
            raw_data="{}",
            latitude=0.0,
            longitude=0.0,
            location_name="Test Location",
            event_start=datetime.now(timezone.utc).isoformat(),
            event_end=None,
            fetched_at=datetime.now(timezone.utc).isoformat(),
            created_at=datetime.now(timezone.utc).isoformat(),
            updated_at=datetime.now(timezone.utc).isoformat(),
        )
        session.add(alert)
        session.commit()
        print("✓ Test alert inserted successfully.")
    except Exception as e:
        print(f"Error inserting test alert: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    insert_test_alert()
