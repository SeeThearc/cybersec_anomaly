import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from app.database import SessionLocal
from app import crud, schemas, models
from datetime import datetime, timedelta

def seed_alerts():
    db = SessionLocal()
    
    # Check if we have users
    users = crud.get_users(db, limit=5)
    if not users:
        print("No users found. Run /generate-data first.")
        return
        
    user_id = users[0].id
    
    # Create some mock alerts
    alerts = [
        schemas.AlertCreate(
            user_id=user_id,
            risk_score=92.5,
            attack_type="CredentialStuffing",
            prediction="CredentialStuffing",
            explanation="Multiple failed login attempts from unknown foreign IPs followed by a sudden successful login."
        ),
        schemas.AlertCreate(
            user_id=user_id,
            risk_score=85.0,
            attack_type="LateralMovement",
            prediction="LateralMovement",
            explanation="Unusual access to Payroll DB by an Engineering user outside of standard business hours."
        )
    ]
    
    for alert in alerts:
        crud.create_alert(db, alert)
        
    print("Successfully seeded 2 mock alerts into the database.")
    db.close()

if __name__ == "__main__":
    seed_alerts()
