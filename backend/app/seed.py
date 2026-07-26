"""Sample database seed data for development and testing."""

from datetime import date, datetime, timezone

from sqlalchemy.orm import Session

from app import crud, models, schemas


def seed_sample_data(db: Session) -> dict[str, int]:
    """Insert representative records across all tables."""
    user = crud.create_user(
        db,
        schemas.UserCreate(
            name="Alice Johnson",
            department="Engineering",
            role="Software Engineer",
            country="India",
            joining_date=date(2022, 3, 15),
        ),
    )

    device = crud.create_device(
        db,
        schemas.DeviceCreate(
            user_id=user.id,
            device_name="Alice-Laptop",
            device_type="Laptop",
            operating_system="Windows",
            browser="Chrome",
            fingerprint="fp-alice-laptop-001",
        ),
    )

    event = crud.create_event(
        db,
        schemas.EventCreate(
            user_id=user.id,
            timestamp=datetime(2026, 7, 25, 9, 10, tzinfo=timezone.utc),
            country="India",
            ip_address="192.168.1.10",
            device_id=device.id,
            resource="GitHub",
            action="Access",
            authentication_method="SSO",
            session_duration=3600,
            login_status="success",
            failed_attempts=0,
            bytes_transferred=0,
            command_sequence="Login > Email > GitHub > Logout",
            label=models.AttackLabel.NORMAL.value,
        ),
    )

    alert = crud.create_alert(
        db,
        schemas.AlertCreate(
            user_id=user.id,
            risk_score=72.5,
            attack_type=models.AttackLabel.IMPOSSIBLE_TRAVEL.value,
            prediction=models.AttackLabel.IMPOSSIBLE_TRAVEL.value,
            explanation="Login detected from a new country shortly after a previous session.",
        ),
    )

    return {
        "user_id": user.id,
        "device_id": device.id,
        "event_id": event.id,
        "alert_id": alert.id,
    }
