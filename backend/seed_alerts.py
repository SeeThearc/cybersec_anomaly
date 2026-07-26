import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from app.database import SessionLocal
from app import crud, schemas, models
from datetime import datetime, timedelta, date
import random

def seed_demo_data():
    db = SessionLocal()
    
    # 1. Ensure at least 5 users exist
    departments = ["Engineering", "HR", "Sales", "Finance", "Admin"]
    roles = ["Software Engineer", "HR Manager", "Account Executive", "Financial Analyst", "System Admin"]
    
    users = crud.get_users(db, limit=10)
    user_ids = [u.id for u in users]
    
    if len(user_ids) < 5:
        print("Creating dummy users for demonstration...")
        for i in range(len(user_ids) + 1, 6):
            new_user = models.User(
                name=f"Demo User {i}",
                department=departments[i % len(departments)],
                role=roles[i % len(roles)],
                country="USA",
                joining_date=date(2025, 1, 1)
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user_ids.append(new_user.id)
            print(f"Created User ID: {new_user.id}")

    # 2. Generate a variety of alerts across these 5 users
    print("Seeding alerts across users 1 to 5...")
    
    attack_types = ["BruteForce", "CredentialStuffing", "LateralMovement", "ImpossibleTravel", "InsiderDrift"]
    explanations = {
        "BruteForce": "Multiple failed login attempts detected in a short time window.",
        "CredentialStuffing": "Login attempts from multiple previously unseen foreign IP addresses.",
        "LateralMovement": "User attempted to access restricted resources outside their department.",
        "ImpossibleTravel": "Logins detected from two geographically distant locations within an impossible timeframe.",
        "InsiderDrift": "Significant deviation from historical baseline behavior, downloading unusual amounts of data."
    }

    # Clear old mock alerts to keep the dashboard clean (optional, but good for demo)
    db.query(models.Alert).delete()
    db.commit()

    # Generate 12 varied alerts
    for i in range(12):
        u_id = random.choice(user_ids[:5]) # Pick from first 5 users
        attack = random.choice(attack_types)
        risk = random.uniform(70.0, 99.0)
        
        # Stagger the timestamps to look realistic in the timeline
        created_at = datetime.utcnow() - timedelta(minutes=random.randint(1, 120))
        
        db_alert = models.Alert(
            user_id=u_id,
            risk_score=risk,
            attack_type=attack,
            prediction=attack,
            explanation=explanations[attack],
            created_at=created_at
        )
        db.add(db_alert)
    
    db.commit()
    print("Successfully seeded 12 diverse alerts across multiple users!")
    db.close()

if __name__ == "__main__":
    seed_demo_data()
