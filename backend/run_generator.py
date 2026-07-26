"""Run the synthetic data generation pipeline."""

from dotenv import load_dotenv

load_dotenv()

from app.database import SessionLocal, init_db
from app.ml.data_generator import run_generation


def main() -> None:
    print("Initialising database tables...")
    init_db()

    db = SessionLocal()
    try:
        result = run_generation(db, user_count=1000)
        print("\n── Summary ──")
        print(f"  Users:    {result['users']:,}")
        print(f"  Devices:  {result['devices']:,}")
        print(f"  Events:   {result['events']:,}")
        print(f"  Time:     {result['elapsed_seconds']}s")
    finally:
        db.close()


if __name__ == "__main__":
    main()
