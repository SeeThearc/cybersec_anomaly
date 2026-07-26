"""Database connectivity and CRUD verification script."""

from sqlalchemy import text

from app.database import SessionLocal, check_db_connection, engine, init_db
from app import crud, schemas
from app.seed import seed_sample_data


def test_database_crud() -> None:
    print("Checking database connection...")
    if not check_db_connection():
        raise RuntimeError(
            "Could not connect to PostgreSQL. "
            "Ensure PostgreSQL is running and backend/.env is configured."
        )
    print("Connection successful.")

    print("Creating tables...")
    init_db()
    print("Tables created.")

    db = SessionLocal()
    try:
        print("Clearing existing test data...")
        for table_name in ("alerts", "events", "devices", "users"):
            db.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"))
        db.commit()

        print("Seeding sample records...")
        seeded_ids = seed_sample_data(db)
        print(f"Seeded records: {seeded_ids}")

        user = crud.get_user_with_relations(db, seeded_ids["user_id"])
        assert user is not None, "User should exist"
        assert len(user.devices) == 1, "User should have one device"
        assert len(user.events) == 1, "User should have one event"
        assert len(user.alerts) == 1, "User should have one alert"
        assert user.devices[0].user.id == user.id, "Device relationship should resolve"
        assert user.events[0].device.id == user.devices[0].id, "Event device relationship should resolve"
        print("Relationships verified.")

        updated_user = crud.update_user(
            db,
            user.id,
            schemas.UserUpdate(role="Senior Software Engineer"),
        )
        assert updated_user is not None
        assert updated_user.role == "Senior Software Engineer"
        print("Update operation verified.")

        assert crud.delete_alert(db, seeded_ids["alert_id"]) is True
        assert crud.get_alert(db, seeded_ids["alert_id"]) is None
        print("Delete operation verified.")

        remaining_alerts = crud.get_alerts(db)
        assert len(remaining_alerts) == 0
        print("CRUD operations verified.")
    finally:
        db.close()

    print("All database tests passed.")


if __name__ == "__main__":
    test_database_crud()
