"""Synthetic enterprise data generation.

Generates realistic users, devices, and normal-behavior events for the
UEBA platform.  Attack simulation is handled separately in Milestone 4.
"""

import random
import uuid
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from faker import Faker
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import AttackLabel, Device, Event, User
from app.utils import generate_ip

# ── Faker instance ───────────────────────────────────────────────────

fake = Faker()

# ── Department Behavioral Profiles ───────────────────────────────────
# Each department defines the resources employees typically access,
# their working-hour range, average session length, preferred auth
# methods, and typical data-transfer volumes.

DEPARTMENT_PROFILES: dict[str, dict[str, Any]] = {
    "Engineering": {
        "roles": [
            "Software Engineer", "Senior Engineer", "Tech Lead",
            "DevOps Engineer", "QA Engineer",
        ],
        "resources": [
            "GitHub", "Jira", "Confluence", "Jenkins",
            "AWS Console", "VS Code Server", "Docker Hub",
        ],
        "work_start": (8, 10),
        "work_end": (17, 19),
        "session_minutes": (30, 120),
        "auth_methods": ["SSO", "MFA"],
        "download_mb": (5, 50),
        "upload_mb": (2, 30),
    },
    "Finance": {
        "roles": [
            "Financial Analyst", "Accountant", "Finance Manager",
            "Auditor", "Treasury Analyst",
        ],
        "resources": [
            "Payroll", "Finance Portal", "SAP",
            "Excel Online", "Expense System", "Tax Portal",
        ],
        "work_start": (8, 9),
        "work_end": (17, 18),
        "session_minutes": (20, 90),
        "auth_methods": ["MFA", "SSO"],
        "download_mb": (2, 20),
        "upload_mb": (1, 10),
    },
    "HR": {
        "roles": [
            "HR Manager", "Recruiter", "HR Analyst",
            "Benefits Coordinator", "Training Specialist",
        ],
        "resources": [
            "HR Portal", "Recruitment System", "Benefits Portal",
            "Training Platform", "Employee Directory",
        ],
        "work_start": (8, 10),
        "work_end": (17, 18),
        "session_minutes": (15, 60),
        "auth_methods": ["SSO", "Password"],
        "download_mb": (1, 15),
        "upload_mb": (1, 10),
    },
    "Sales": {
        "roles": [
            "Sales Representative", "Account Manager",
            "Sales Director", "Business Development", "Sales Analyst",
        ],
        "resources": [
            "Salesforce", "CRM Portal", "LinkedIn Sales",
            "Proposal System", "Client Portal",
        ],
        "work_start": (7, 10),
        "work_end": (17, 20),
        "session_minutes": (10, 60),
        "auth_methods": ["SSO", "Password"],
        "download_mb": (1, 10),
        "upload_mb": (1, 5),
    },
    "IT": {
        "roles": [
            "System Administrator", "Network Engineer",
            "IT Support", "Cloud Engineer", "DBA",
        ],
        "resources": [
            "Admin Console", "Network Monitor", "Ticketing System",
            "Server Dashboard", "Active Directory", "Firewall Console",
        ],
        "work_start": (7, 10),
        "work_end": (17, 20),
        "session_minutes": (30, 120),
        "auth_methods": ["MFA", "Certificate"],
        "download_mb": (5, 40),
        "upload_mb": (3, 25),
    },
    "Security": {
        "roles": [
            "Security Engineer", "SOC Analyst", "Incident Responder",
            "Threat Hunter", "Security Architect",
        ],
        "resources": [
            "SIEM Dashboard", "Threat Intel", "Forensics Tool",
            "Vulnerability Scanner", "Security Console", "Endpoint Protection",
        ],
        "work_start": (6, 10),
        "work_end": (18, 22),
        "session_minutes": (30, 180),
        "auth_methods": ["MFA", "Certificate"],
        "download_mb": (5, 60),
        "upload_mb": (2, 30),
    },
}

# Weighted distribution mirrors a typical enterprise headcount.
DEPARTMENT_WEIGHTS: dict[str, float] = {
    "Engineering": 0.30,
    "Sales": 0.20,
    "Finance": 0.15,
    "HR": 0.15,
    "IT": 0.10,
    "Security": 0.10,
}

# ── Geography ────────────────────────────────────────────────────────

COUNTRIES: list[str] = [
    "India", "USA", "UK", "Germany",
    "Australia", "Canada", "Singapore", "Japan",
]
COUNTRY_WEIGHTS: list[float] = [
    0.30, 0.25, 0.15, 0.10,
    0.05, 0.05, 0.05, 0.05,
]

# ── Device Catalogue ─────────────────────────────────────────────────

DEVICE_TYPES: dict[str, dict[str, list[str]]] = {
    "Laptop": {
        "os": ["Windows 11", "macOS Sonoma", "Ubuntu 22.04"],
        "browsers": ["Chrome", "Firefox", "Edge", "Safari"],
    },
    "Desktop": {
        "os": ["Windows 11", "Windows 10", "Ubuntu 22.04"],
        "browsers": ["Chrome", "Firefox", "Edge"],
    },
    "Mobile": {
        "os": ["iOS 17", "Android 14"],
        "browsers": ["Safari", "Chrome"],
    },
}

# ── Shared / Cross-department Resources ──────────────────────────────

SHARED_RESOURCES: list[str] = [
    "Email", "Slack", "Teams", "Zoom", "SharePoint", "Intranet",
]

# ── Access Action Probabilities ──────────────────────────────────────

ACCESS_ACTIONS: list[str] = ["Access", "Read", "Download", "Upload"]
ACCESS_ACTION_WEIGHTS: list[float] = [0.40, 0.30, 0.15, 0.15]

# Batch size for bulk DB inserts
_BATCH_SIZE: int = 500

# ── User Generation ─────────────────────────────────────────────────


def generate_users(db: Session, count: int = 1000) -> list[User]:
    """Create *count* enterprise users with department-weighted distribution."""
    departments = list(DEPARTMENT_WEIGHTS.keys())
    weights = list(DEPARTMENT_WEIGHTS.values())
    today = date.today()

    users: list[User] = []
    for _ in range(count):
        dept = random.choices(departments, weights=weights, k=1)[0]
        profile = DEPARTMENT_PROFILES[dept]
        role = random.choice(profile["roles"])
        country = random.choices(COUNTRIES, weights=COUNTRY_WEIGHTS, k=1)[0]
        joining = today - timedelta(days=random.randint(30, 5 * 365))

        users.append(User(
            name=fake.name(),
            department=dept,
            role=role,
            country=country,
            joining_date=joining,
        ))

    db.add_all(users)
    db.flush()  # IDs populated via RETURNING
    return users


# ── Behavioral Profile Builder ───────────────────────────────────────


def _build_user_profile(user: User) -> dict[str, Any]:
    """Derive a per-user behavioral profile used during event generation.

    This is **not** persisted — it drives how realistic events are created.
    """
    dp = DEPARTMENT_PROFILES[user.department]

    avg_login = random.randint(*dp["work_start"])
    avg_logout = random.randint(*dp["work_end"])
    # Ensure logout is after login
    if avg_logout <= avg_login:
        avg_logout = avg_login + 8

    return {
        "avg_login_hour": avg_login,
        "avg_logout_hour": avg_logout,
        "avg_session_minutes": random.randint(*dp["session_minutes"]),
        "preferred_resources": dp["resources"],
        "auth_method": random.choice(dp["auth_methods"]),
        "avg_downloads_mb": random.randint(*dp["download_mb"]),
        "avg_uploads_mb": random.randint(*dp["upload_mb"]),
        "base_country": user.country,
        "base_ip": generate_ip(),
        # Most employees log in once per day; some log in twice.
        "sessions_per_day": random.choices([1, 2], weights=[0.7, 0.3], k=1)[0],
    }


# ── Device Generation ────────────────────────────────────────────────


def generate_devices(
    db: Session, users: list[User],
) -> dict[int, list[Device]]:
    """Create 1–3 devices per user with realistic specs."""
    device_type_names = list(DEVICE_TYPES.keys())
    all_devices: list[Device] = []
    device_map: dict[int, list[Device]] = {}

    for user in users:
        num = random.choices([1, 2, 3], weights=[0.3, 0.5, 0.2], k=1)[0]
        first_name = user.name.split()[0]

        # First device is always a laptop
        chosen = ["Laptop"]
        if num >= 2:
            chosen.append(random.choice(["Desktop", "Mobile"]))
        if num >= 3:
            remaining = [t for t in device_type_names if t not in chosen]
            chosen.append(random.choice(remaining) if remaining else "Mobile")

        user_devices: list[Device] = []
        for dtype in chosen:
            spec = DEVICE_TYPES[dtype]
            device = Device(
                user_id=user.id,
                device_name=f"{first_name}-{dtype}",
                device_type=dtype,
                operating_system=random.choice(spec["os"]),
                browser=random.choice(spec["browsers"]),
                fingerprint=str(uuid.uuid4()),
            )
            user_devices.append(device)
            all_devices.append(device)

        device_map[user.id] = user_devices

    db.add_all(all_devices)
    db.flush()
    return device_map


# ── Event Generation ─────────────────────────────────────────────────


def generate_events(
    db: Session,
    users: list[User],
    device_map: dict[int, list[Device]],
    profiles: dict[int, dict[str, Any]],
    days: int = 30,
) -> int:
    """Generate 50–200 normal-behaviour events per user over *days* days."""
    base_date = datetime.now(timezone.utc) - timedelta(days=days)
    total: int = 0
    batch: list[Event] = []

    for user in users:
        profile = profiles[user.id]
        devices = device_map[user.id]
        target = random.randint(50, 200)
        user_events: list[Event] = []

        for day_offset in range(days):
            if len(user_events) >= target:
                break

            current_day = base_date + timedelta(days=day_offset)

            # Skip weekends 90 % of the time
            if current_day.weekday() >= 5 and random.random() < 0.9:
                continue

            for sess_idx in range(profile["sessions_per_day"]):
                if len(user_events) >= target:
                    break

                session = _generate_session(
                    user, profile, devices, current_day, sess_idx,
                )
                user_events.extend(session)

        # Trim to target so no user exceeds their cap
        user_events = user_events[:target]
        batch.extend(user_events)

        # Flush in batches to keep memory low
        if len(batch) >= _BATCH_SIZE:
            valid = _validate_events(batch)
            db.add_all(valid)
            db.flush()
            total += len(valid)
            batch = []

    # Remaining records
    if batch:
        valid = _validate_events(batch)
        db.add_all(valid)
        db.flush()
        total += len(valid)

    return total


def _generate_session(
    user: User,
    profile: dict[str, Any],
    devices: list[Device],
    session_date: datetime,
    session_idx: int,
) -> list[Event]:
    """Build one work session: Login → resource accesses → Logout."""
    events: list[Event] = []
    device = random.choice(devices)

    # Compute login time with jitter
    login_hour = profile["avg_login_hour"] + session_idx * 3
    login_hour = max(0, min(23, login_hour + random.choice([-1, 0, 0, 0, 1])))
    login_minute = random.randint(0, 59)

    ts = session_date.replace(
        hour=login_hour, minute=login_minute,
        second=random.randint(0, 59), microsecond=0,
    )

    session_secs = max(
        600,
        int(profile["avg_session_minutes"] * 60 * random.uniform(0.7, 1.3)),
    )

    # 5 % chance of a mistyped-password before success
    failed = 1 if random.random() < 0.05 else 0

    country = profile["base_country"]
    ip = profile["base_ip"]
    auth = profile["auth_method"]
    label = AttackLabel.NORMAL.value

    # ── Login ────────────────────────────────────────────────────
    events.append(Event(
        user_id=user.id, timestamp=ts, country=country,
        ip_address=ip, device_id=device.id,
        resource="Authentication", action="Login",
        authentication_method=auth, session_duration=session_secs,
        login_status="success", failed_attempts=failed,
        bytes_transferred=0, command_sequence=None, label=label,
    ))

    # ── Resource accesses (2–6) ──────────────────────────────────
    num_accesses = random.randint(2, 6)
    accessed: list[str] = []

    for _ in range(num_accesses):
        # 80 % department resource, 20 % shared resource
        if random.random() < 0.8:
            resource = random.choice(profile["preferred_resources"])
        else:
            resource = random.choice(SHARED_RESOURCES)

        accessed.append(resource)
        ts = ts + timedelta(minutes=random.randint(2, 30))

        action = random.choices(
            ACCESS_ACTIONS, weights=ACCESS_ACTION_WEIGHTS, k=1,
        )[0]

        if action == "Download":
            bytes_t = random.randint(
                1024, max(2048, profile["avg_downloads_mb"] * 512 * 1024),
            )
        elif action == "Upload":
            bytes_t = random.randint(
                512, max(1024, profile["avg_uploads_mb"] * 512 * 1024),
            )
        else:
            bytes_t = random.randint(64, 10240)

        events.append(Event(
            user_id=user.id, timestamp=ts, country=country,
            ip_address=ip, device_id=device.id,
            resource=resource, action=action,
            authentication_method=auth, session_duration=session_secs,
            login_status="success", failed_attempts=0,
            bytes_transferred=bytes_t, command_sequence=None, label=label,
        ))

    # ── Logout ───────────────────────────────────────────────────
    ts = ts + timedelta(minutes=random.randint(1, 10))
    events.append(Event(
        user_id=user.id, timestamp=ts, country=country,
        ip_address=ip, device_id=device.id,
        resource="Authentication", action="Logout",
        authentication_method=auth, session_duration=session_secs,
        login_status="success", failed_attempts=0,
        bytes_transferred=0, command_sequence=None, label=label,
    ))

    # Write the full action trail into every event of this session
    sequence = " > ".join(["Login"] + accessed + ["Logout"])
    for ev in events:
        ev.command_sequence = sequence

    return events


# ── Validation ───────────────────────────────────────────────────────

_VALID_COUNTRIES = set(COUNTRIES)
_VALID_LABELS = {label.value for label in AttackLabel}


def _validate_events(events: list[Event]) -> list[Event]:
    """Filter out any events with invalid or missing fields."""
    valid: list[Event] = []
    for e in events:
        if e.timestamp is None:
            continue
        if e.country not in _VALID_COUNTRIES:
            continue
        if e.session_duration is None or e.session_duration <= 0:
            continue
        if e.login_status not in ("success", "failure"):
            continue
        if e.label not in _VALID_LABELS:
            continue
        valid.append(e)
    return valid


# ── Helpers ──────────────────────────────────────────────────────────

# generate_ip() is imported from app.utils (shared with attack_simulator)


# ── CSV Export ───────────────────────────────────────────────────────


def export_datasets(
    db: Session,
    data_dir: Path,
) -> dict[str, int]:
    """Export events (joined with user info) as train / validation / test CSVs.

    Split ratio: 70 / 15 / 15.
    """
    data_dir.mkdir(parents=True, exist_ok=True)

    query = text("""
        SELECT
            e.id        AS event_id,
            e.user_id,
            u.name      AS user_name,
            u.department AS user_department,
            u.role      AS user_role,
            u.country   AS user_country,
            e.timestamp,
            e.country,
            e.ip_address,
            e.device_id,
            e.resource,
            e.action,
            e.authentication_method,
            e.session_duration,
            e.login_status,
            e.failed_attempts,
            e.bytes_transferred,
            e.command_sequence,
            e.label
        FROM events e
        JOIN users u ON e.user_id = u.id
        ORDER BY e.timestamp
    """)

    result = db.execute(query)
    columns = list(result.keys())
    rows = result.fetchall()

    if not rows:
        return {"train": 0, "validation": 0, "test": 0}

    df = pd.DataFrame(rows, columns=columns)

    # Shuffle then split 70 / 15 / 15
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    n = len(df)
    train_end = int(n * 0.70)
    val_end = int(n * 0.85)

    splits = {
        "train": df.iloc[:train_end],
        "validation": df.iloc[train_end:val_end],
        "test": df.iloc[val_end:],
    }

    counts: dict[str, int] = {}
    for name, part in splits.items():
        path = data_dir / f"{name}.csv"
        part.to_csv(path, index=False)
        counts[name] = len(part)

    return counts


# ── Orchestration ────────────────────────────────────────────────────


def run_generation(
    db: Session,
    user_count: int = 1000,
    seed: int = 42,
) -> dict[str, Any]:
    """End-to-end data generation pipeline.

    1. Clear existing data
    2. Generate users
    3. Generate devices
    4. Generate normal-behaviour events
    5. Simulate cyber attacks
    6. Export train / validation / test CSVs
    """
    import time

    random.seed(seed)
    np.random.seed(seed)
    Faker.seed(seed)

    start = time.time()

    # ── Clear existing data ──────────────────────────────────────
    print("Clearing existing data...")
    for table in ("alerts", "events", "devices", "users"):
        db.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))
    db.commit()

    # ── Users ────────────────────────────────────────────────────
    print(f"Generating {user_count} users...")
    users = generate_users(db, user_count)
    db.commit()
    print(f"  ✓ {len(users)} users created")

    # ── Behavioral profiles (in-memory only) ─────────────────────
    profiles: dict[int, dict[str, Any]] = {}
    for user in users:
        profiles[user.id] = _build_user_profile(user)

    # ── Devices ──────────────────────────────────────────────────
    print("Generating devices...")
    device_map = generate_devices(db, users)
    device_count = sum(len(devs) for devs in device_map.values())
    db.commit()
    print(f"  ✓ {device_count} devices created")

    # ── Normal events ────────────────────────────────────────────
    print("Generating normal-behaviour events...")
    normal_count = generate_events(db, users, device_map, profiles)
    db.commit()
    print(f"  ✓ {normal_count} normal events created")

    # ── Attack simulation ────────────────────────────────────────
    from app.services.attack_simulator import run_attack_simulation

    print("Simulating cyber attacks...")
    attack_results = run_attack_simulation(
        db, users, device_map, profiles, normal_count, seed=seed + 1,
    )
    attack_count = sum(attack_results.values())
    for attack_type, count in attack_results.items():
        print(f"    {attack_type}: {count:,} events")
    print(f"  ✓ {attack_count:,} attack events created")

    event_count = normal_count + attack_count

    # ── CSV export ───────────────────────────────────────────────
    print("Exporting datasets...")
    data_dir = Path(__file__).resolve().parent.parent.parent / "data"
    splits = export_datasets(db, data_dir)
    print(f"  ✓ train.csv:      {splits['train']:,} rows")
    print(f"  ✓ validation.csv: {splits['validation']:,} rows")
    print(f"  ✓ test.csv:       {splits['test']:,} rows")

    elapsed = round(time.time() - start, 1)
    print(f"Generation completed in {elapsed}s.")

    return {
        "users": len(users),
        "devices": device_count,
        "events": event_count,
        "splits": splits,
        "elapsed_seconds": elapsed,
    }
