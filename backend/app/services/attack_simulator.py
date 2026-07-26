"""Cyber attack simulation engine.

Generates realistic attack events that follow recognisable threat
signatures.  Each attack type produces a coherent incident — not random
anomalies — so the ML pipeline can learn distinguishing patterns.

Attack distribution targets (% of total dataset):
    Normal                90 %
    BruteForce             2 %
    CredentialStuffing     2 %
    ImpossibleTravel       1 %
    DeviceSpoofing         1 %
    LateralMovement        1 %
    LowSlowExfiltration    2 %
    InsiderDrift           1 %
"""

import random
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.models import AttackLabel, Device, Event, User
from app.utils import generate_ip

# ── Attack distribution (fraction of total events) ───────────────────

ATTACK_DISTRIBUTION: dict[AttackLabel, float] = {
    AttackLabel.BRUTE_FORCE: 0.02,
    AttackLabel.CREDENTIAL_STUFFING: 0.02,
    AttackLabel.IMPOSSIBLE_TRAVEL: 0.01,
    AttackLabel.DEVICE_SPOOFING: 0.01,
    AttackLabel.LATERAL_MOVEMENT: 0.01,
    AttackLabel.LOW_SLOW_EXFILTRATION: 0.02,
    AttackLabel.INSIDER_DRIFT: 0.01,
}

# Average events per incident — used to estimate how many incidents are
# needed to hit the target event count for each attack type.
_AVG_EVENTS: dict[AttackLabel, int] = {
    AttackLabel.BRUTE_FORCE: 8,
    AttackLabel.CREDENTIAL_STUFFING: 12,
    AttackLabel.IMPOSSIBLE_TRAVEL: 5,
    AttackLabel.DEVICE_SPOOFING: 5,
    AttackLabel.LATERAL_MOVEMENT: 8,
    AttackLabel.LOW_SLOW_EXFILTRATION: 15,
    AttackLabel.INSIDER_DRIFT: 22,
}

# ── Geography ────────────────────────────────────────────────────────

COUNTRIES: list[str] = [
    "India", "USA", "UK", "Germany",
    "Australia", "Canada", "Singapore", "Japan",
]

# ── Lateral-movement traversal paths ─────────────────────────────────

LATERAL_SEQUENCES: list[list[str]] = [
    ["Email", "HR Portal", "Payroll", "Database", "Admin Console"],
    ["Intranet", "Server Dashboard", "Active Directory",
     "Firewall Console", "Database"],
    ["Email", "Finance Portal", "Payroll", "SAP", "Admin Console"],
    ["Ticketing System", "Server Dashboard", "Network Monitor",
     "Admin Console", "Database"],
    ["Email", "Confluence", "GitHub", "Jenkins",
     "AWS Console", "Admin Console"],
]

# ── Resources targeted during exfiltration ───────────────────────────

EXFIL_RESOURCES: list[str] = [
    "Database", "SharePoint", "Finance Portal",
    "HR Portal", "Client Portal", "Payroll", "SAP",
]

# ── Sensitive resources for device-spoofing post-login ───────────────

SENSITIVE_RESOURCES: list[str] = [
    "Payroll", "Admin Console", "Database",
    "HR Portal", "Security Console", "Active Directory",
]

# Batch size for bulk DB inserts
_BATCH_SIZE: int = 500


# =====================================================================
#  Individual attack simulators
# =====================================================================


def _simulate_brute_force(
    user: User,
    profile: dict[str, Any],
    devices: list[Device],
    day: datetime,
) -> list[Event]:
    """Rapid failed-login burst followed by a successful login.

    Signature: high failure count, same IP, short time gaps.
    """
    events: list[Event] = []
    # Attacks typically happen outside working hours
    hour = random.choice([0, 1, 2, 3, 4, 22, 23])
    ts = day.replace(hour=hour, minute=random.randint(0, 30),
                     second=random.randint(0, 59), microsecond=0)

    attacker_ip = generate_ip()
    device = random.choice(devices)
    label = AttackLabel.BRUTE_FORCE.value
    num_failures = random.randint(5, 15)

    # Failed login attempts in rapid succession
    for attempt in range(num_failures):
        events.append(Event(
            user_id=user.id, timestamp=ts, country=profile["base_country"],
            ip_address=attacker_ip, device_id=device.id,
            resource="Authentication", action="Login",
            authentication_method="Password",
            session_duration=0, login_status="failure",
            failed_attempts=attempt + 1, bytes_transferred=0,
            command_sequence=None, label=label,
        ))
        ts += timedelta(milliseconds=random.randint(100, 1500))

    # Eventual success
    events.append(Event(
        user_id=user.id, timestamp=ts, country=profile["base_country"],
        ip_address=attacker_ip, device_id=device.id,
        resource="Authentication", action="Login",
        authentication_method="Password",
        session_duration=random.randint(60, 600),
        login_status="success", failed_attempts=num_failures,
        bytes_transferred=0, command_sequence=None, label=label,
    ))

    sequence = " > ".join(["Failed Login"] * num_failures + ["Login Success"])
    for ev in events:
        ev.command_sequence = sequence

    return events


def _simulate_impossible_travel(
    user: User,
    profile: dict[str, Any],
    devices: list[Device],
    day: datetime,
) -> list[Event]:
    """Two logins from distant countries within an impossibly short window.

    Signature: geo change, short time delta, large distance.
    """
    events: list[Event] = []
    device = random.choice(devices)
    label = AttackLabel.IMPOSSIBLE_TRAVEL.value
    home = profile["base_country"]

    # First login from home country
    ts1 = day.replace(hour=random.randint(8, 14), minute=random.randint(0, 59),
                      second=0, microsecond=0)

    events.append(Event(
        user_id=user.id, timestamp=ts1, country=home,
        ip_address=profile["base_ip"], device_id=device.id,
        resource="Authentication", action="Login",
        authentication_method=profile["auth_method"],
        session_duration=random.randint(300, 1800),
        login_status="success", failed_attempts=0,
        bytes_transferred=0, command_sequence=None, label=label,
    ))

    # Brief activity at home
    ts1 += timedelta(minutes=random.randint(2, 10))
    events.append(Event(
        user_id=user.id, timestamp=ts1, country=home,
        ip_address=profile["base_ip"], device_id=device.id,
        resource=random.choice(profile["preferred_resources"]),
        action="Access", authentication_method=profile["auth_method"],
        session_duration=random.randint(300, 1800),
        login_status="success", failed_attempts=0,
        bytes_transferred=random.randint(100, 5000),
        command_sequence=None, label=label,
    ))

    # Second login from a *different* country 15–45 min later
    foreign = random.choice([c for c in COUNTRIES if c != home])
    ts2 = ts1 + timedelta(minutes=random.randint(15, 45))

    events.append(Event(
        user_id=user.id, timestamp=ts2, country=foreign,
        ip_address=generate_ip(), device_id=device.id,
        resource="Authentication", action="Login",
        authentication_method=profile["auth_method"],
        session_duration=random.randint(300, 1800),
        login_status="success", failed_attempts=0,
        bytes_transferred=0, command_sequence=None, label=label,
    ))

    # Activity from foreign location
    ts2 += timedelta(minutes=random.randint(2, 10))
    events.append(Event(
        user_id=user.id, timestamp=ts2, country=foreign,
        ip_address=events[-1].ip_address, device_id=device.id,
        resource=random.choice(SENSITIVE_RESOURCES),
        action="Access", authentication_method=profile["auth_method"],
        session_duration=random.randint(300, 1800),
        login_status="success", failed_attempts=0,
        bytes_transferred=random.randint(100, 5000),
        command_sequence=None, label=label,
    ))

    seq = f"Login({home}) > Access > Login({foreign}) > Access"
    for ev in events:
        ev.command_sequence = seq

    return events


def _simulate_credential_stuffing(
    users: list[User],
    profiles: dict[int, dict[str, Any]],
    device_map: dict[int, list[Device]],
    day: datetime,
) -> list[Event]:
    """One attacker IP tries credentials against many users.

    Signature: same IP, multiple user IDs, high failure rate.
    """
    events: list[Event] = []
    label = AttackLabel.CREDENTIAL_STUFFING.value

    num_targets = random.randint(5, 12)
    targets = random.sample(users, min(num_targets, len(users)))
    attacker_ip = generate_ip()
    # Attacker's apparent country
    attacker_country = random.choice(COUNTRIES)

    hour = random.choice([1, 2, 3, 4, 5])
    ts = day.replace(hour=hour, minute=random.randint(0, 30),
                     second=0, microsecond=0)

    for target in targets:
        devices = device_map.get(target.id, [])
        device_id = devices[0].id if devices else None
        attempts = random.randint(2, 5)

        for i in range(attempts):
            events.append(Event(
                user_id=target.id, timestamp=ts,
                country=attacker_country,
                ip_address=attacker_ip, device_id=device_id,
                resource="Authentication", action="Login",
                authentication_method="Password",
                session_duration=0, login_status="failure",
                failed_attempts=i + 1, bytes_transferred=0,
                command_sequence=None, label=label,
            ))
            ts += timedelta(milliseconds=random.randint(50, 800))

    usernames = ", ".join(t.name.split()[0] for t in targets[:5])
    seq = f"Stuffing({usernames}...)"
    for ev in events:
        ev.command_sequence = seq

    return events


def _simulate_device_spoofing(
    user: User,
    profile: dict[str, Any],
    devices: list[Device],
    day: datetime,
) -> list[Event]:
    """Login from a completely unknown device and fingerprint.

    Signature: new OS, new browser, different fingerprint, no prior history
    for this device.
    """
    events: list[Event] = []
    label = AttackLabel.DEVICE_SPOOFING.value

    hour = random.choice([0, 1, 2, 3, 22, 23])
    ts = day.replace(hour=hour, minute=random.randint(0, 59),
                     second=0, microsecond=0)

    spoofed_ip = generate_ip()

    # Login with unknown device (device_id = None)
    events.append(Event(
        user_id=user.id, timestamp=ts, country=profile["base_country"],
        ip_address=spoofed_ip, device_id=None,
        resource="Authentication", action="Login",
        authentication_method="Password",
        session_duration=random.randint(120, 900),
        login_status="success", failed_attempts=random.randint(0, 2),
        bytes_transferred=0, command_sequence=None, label=label,
    ))

    # Immediately access sensitive resources
    num_accesses = random.randint(2, 5)
    accessed: list[str] = []
    for _ in range(num_accesses):
        ts += timedelta(minutes=random.randint(1, 8))
        resource = random.choice(SENSITIVE_RESOURCES)
        accessed.append(resource)
        events.append(Event(
            user_id=user.id, timestamp=ts, country=profile["base_country"],
            ip_address=spoofed_ip, device_id=None,
            resource=resource,
            action=random.choice(["Access", "Read", "Download"]),
            authentication_method="Password",
            session_duration=random.randint(120, 900),
            login_status="success", failed_attempts=0,
            bytes_transferred=random.randint(1024, 1024 * 1024),
            command_sequence=None, label=label,
        ))

    sequence = " > ".join(["Login(Unknown Device)"] + accessed)
    for ev in events:
        ev.command_sequence = sequence

    return events


def _simulate_lateral_movement(
    user: User,
    profile: dict[str, Any],
    devices: list[Device],
    day: datetime,
) -> list[Event]:
    """Traversal across escalating resources toward sensitive systems.

    Signature: sequential resource hops, privilege escalation pattern.
    """
    events: list[Event] = []
    device = random.choice(devices)
    label = AttackLabel.LATERAL_MOVEMENT.value

    ts = day.replace(hour=random.randint(10, 16), minute=random.randint(0, 59),
                     second=0, microsecond=0)

    # Login
    events.append(Event(
        user_id=user.id, timestamp=ts, country=profile["base_country"],
        ip_address=profile["base_ip"], device_id=device.id,
        resource="Authentication", action="Login",
        authentication_method=profile["auth_method"],
        session_duration=random.randint(600, 3600),
        login_status="success", failed_attempts=0,
        bytes_transferred=0, command_sequence=None, label=label,
    ))

    # Traverse a lateral-movement path
    path = random.choice(LATERAL_SEQUENCES)
    accessed: list[str] = []
    for resource in path:
        ts += timedelta(minutes=random.randint(2, 15))
        accessed.append(resource)
        events.append(Event(
            user_id=user.id, timestamp=ts, country=profile["base_country"],
            ip_address=profile["base_ip"], device_id=device.id,
            resource=resource,
            action=random.choice(["Access", "Read", "Download"]),
            authentication_method=profile["auth_method"],
            session_duration=random.randint(600, 3600),
            login_status="success", failed_attempts=0,
            bytes_transferred=random.randint(512, 512 * 1024),
            command_sequence=None, label=label,
        ))

    # Logout
    ts += timedelta(minutes=random.randint(1, 5))
    events.append(Event(
        user_id=user.id, timestamp=ts, country=profile["base_country"],
        ip_address=profile["base_ip"], device_id=device.id,
        resource="Authentication", action="Logout",
        authentication_method=profile["auth_method"],
        session_duration=random.randint(600, 3600),
        login_status="success", failed_attempts=0,
        bytes_transferred=0, command_sequence=None, label=label,
    ))

    sequence = " > ".join(["Login"] + accessed + ["Logout"])
    for ev in events:
        ev.command_sequence = sequence

    return events


def _simulate_low_slow_exfiltration(
    user: User,
    profile: dict[str, Any],
    devices: list[Device],
    base_day: datetime,
) -> list[Event]:
    """Gradually increasing data downloads over many days.

    Signature: small daily transfers that grow over time, consistent
    resource targeting, after-hours activity.
    """
    events: list[Event] = []
    device = random.choice(devices)
    label = AttackLabel.LOW_SLOW_EXFILTRATION.value

    num_days = random.randint(5, 10)
    # Start small (3–8 MB) and grow
    base_bytes = random.randint(3, 8) * 1024 * 1024
    target_resource = random.choice(EXFIL_RESOURCES)

    for d in range(num_days):
        current_day = base_day + timedelta(days=d)
        if current_day.weekday() >= 5:
            continue  # skip weekends

        # After-hours download sessions
        hour = random.randint(18, 22)
        ts = current_day.replace(hour=hour, minute=random.randint(0, 59),
                                 second=0, microsecond=0)

        # Gradual growth: 15–35 % increase per day
        growth = 1 + d * random.uniform(0.15, 0.35)
        transfer = int(base_bytes * growth)

        # Login
        events.append(Event(
            user_id=user.id, timestamp=ts, country=profile["base_country"],
            ip_address=profile["base_ip"], device_id=device.id,
            resource="Authentication", action="Login",
            authentication_method=profile["auth_method"],
            session_duration=random.randint(300, 1200),
            login_status="success", failed_attempts=0,
            bytes_transferred=0, command_sequence=None, label=label,
        ))

        # Access resource
        ts += timedelta(minutes=random.randint(3, 15))
        events.append(Event(
            user_id=user.id, timestamp=ts, country=profile["base_country"],
            ip_address=profile["base_ip"], device_id=device.id,
            resource=target_resource, action="Access",
            authentication_method=profile["auth_method"],
            session_duration=random.randint(300, 1200),
            login_status="success", failed_attempts=0,
            bytes_transferred=random.randint(100, 5000),
            command_sequence=None, label=label,
        ))

        # Download
        ts += timedelta(minutes=random.randint(2, 10))
        events.append(Event(
            user_id=user.id, timestamp=ts, country=profile["base_country"],
            ip_address=profile["base_ip"], device_id=device.id,
            resource=target_resource, action="Download",
            authentication_method=profile["auth_method"],
            session_duration=random.randint(300, 1200),
            login_status="success", failed_attempts=0,
            bytes_transferred=transfer, command_sequence=None, label=label,
        ))

        # Logout
        ts += timedelta(minutes=random.randint(1, 5))
        events.append(Event(
            user_id=user.id, timestamp=ts, country=profile["base_country"],
            ip_address=profile["base_ip"], device_id=device.id,
            resource="Authentication", action="Logout",
            authentication_method=profile["auth_method"],
            session_duration=random.randint(300, 1200),
            login_status="success", failed_attempts=0,
            bytes_transferred=0, command_sequence=None, label=label,
        ))

    seq = f"Login > {target_resource} > Download({num_days} days) > Logout"
    for ev in events:
        ev.command_sequence = seq

    return events


def _simulate_insider_drift(
    user: User,
    profile: dict[str, Any],
    devices: list[Device],
    base_day: datetime,
) -> list[Event]:
    """Gradually expanding resource access over weeks.

    Signature: normal resources initially, then progressive access to
    sensitive / out-of-role resources.
    """
    events: list[Event] = []
    device = random.choice(devices)
    label = AttackLabel.INSIDER_DRIFT.value

    # Start with 2 normal resources, add a new sensitive one each week
    base_resources = random.sample(
        profile["preferred_resources"],
        min(2, len(profile["preferred_resources"])),
    )
    drift_additions = random.sample(
        SENSITIVE_RESOURCES,
        min(4, len(SENSITIVE_RESOURCES)),
    )

    num_weeks = random.randint(3, 4)
    current_resources = list(base_resources)

    for week in range(num_weeks):
        # Each week, add a new sensitive resource
        if week > 0 and drift_additions:
            current_resources.append(drift_additions.pop(0))

        # 2–4 sessions per week
        sessions = random.randint(2, 4)
        for s in range(sessions):
            day_offset = week * 7 + s
            current_day = base_day + timedelta(days=day_offset)
            if current_day.weekday() >= 5:
                continue

            ts = current_day.replace(
                hour=random.randint(8, 17),
                minute=random.randint(0, 59),
                second=0, microsecond=0,
            )

            # Login
            events.append(Event(
                user_id=user.id, timestamp=ts,
                country=profile["base_country"],
                ip_address=profile["base_ip"], device_id=device.id,
                resource="Authentication", action="Login",
                authentication_method=profile["auth_method"],
                session_duration=random.randint(600, 3600),
                login_status="success", failed_attempts=0,
                bytes_transferred=0, command_sequence=None, label=label,
            ))

            # Access current resource set
            accessed: list[str] = []
            num_access = min(random.randint(2, 4), len(current_resources))
            for resource in random.sample(current_resources, num_access):
                ts += timedelta(minutes=random.randint(5, 25))
                accessed.append(resource)
                events.append(Event(
                    user_id=user.id, timestamp=ts,
                    country=profile["base_country"],
                    ip_address=profile["base_ip"], device_id=device.id,
                    resource=resource,
                    action=random.choice(["Access", "Read", "Download"]),
                    authentication_method=profile["auth_method"],
                    session_duration=random.randint(600, 3600),
                    login_status="success", failed_attempts=0,
                    bytes_transferred=random.randint(256, 256 * 1024),
                    command_sequence=None, label=label,
                ))

            # Logout
            ts += timedelta(minutes=random.randint(1, 10))
            events.append(Event(
                user_id=user.id, timestamp=ts,
                country=profile["base_country"],
                ip_address=profile["base_ip"], device_id=device.id,
                resource="Authentication", action="Logout",
                authentication_method=profile["auth_method"],
                session_duration=random.randint(600, 3600),
                login_status="success", failed_attempts=0,
                bytes_transferred=0, command_sequence=None, label=label,
            ))

            seq = " > ".join(["Login"] + accessed + ["Logout"])
            # Only tag the current session's events
            session_start = len(events) - len(accessed) - 2
            for ev in events[session_start:]:
                ev.command_sequence = seq

    return events


# =====================================================================
#  Orchestration
# =====================================================================


def run_attack_simulation(
    db: Session,
    users: list[User],
    device_map: dict[int, list[Device]],
    profiles: dict[int, dict[str, Any]],
    normal_count: int,
    seed: int = 43,
) -> dict[str, int]:
    """Generate attack events maintaining the target class distribution.

    The number of incidents per attack type is derived from *normal_count*
    so that the final dataset has approximately 90 % normal events and
    10 % attacks split across the seven types.
    """
    random.seed(seed)

    total_target = int(normal_count / 0.90)
    base_date = datetime.now(timezone.utc) - timedelta(days=30)
    generation_days = 30

    results: dict[str, int] = {}
    all_events: list[Event] = []

    for attack_label, pct in ATTACK_DISTRIBUTION.items():
        target_events = int(total_target * pct)
        avg_per_incident = _AVG_EVENTS[attack_label]
        num_incidents = max(1, target_events // avg_per_incident)

        incident_events: list[Event] = []

        for _ in range(num_incidents):
            day = base_date + timedelta(
                days=random.randint(0, generation_days - 1),
            )

            if attack_label == AttackLabel.BRUTE_FORCE:
                user = random.choice(users)
                evts = _simulate_brute_force(
                    user, profiles[user.id],
                    device_map[user.id], day,
                )

            elif attack_label == AttackLabel.IMPOSSIBLE_TRAVEL:
                user = random.choice(users)
                evts = _simulate_impossible_travel(
                    user, profiles[user.id],
                    device_map[user.id], day,
                )

            elif attack_label == AttackLabel.CREDENTIAL_STUFFING:
                evts = _simulate_credential_stuffing(
                    users, profiles, device_map, day,
                )

            elif attack_label == AttackLabel.DEVICE_SPOOFING:
                user = random.choice(users)
                evts = _simulate_device_spoofing(
                    user, profiles[user.id],
                    device_map[user.id], day,
                )

            elif attack_label == AttackLabel.LATERAL_MOVEMENT:
                user = random.choice(users)
                evts = _simulate_lateral_movement(
                    user, profiles[user.id],
                    device_map[user.id], day,
                )

            elif attack_label == AttackLabel.LOW_SLOW_EXFILTRATION:
                user = random.choice(users)
                # Start early enough that multi-day exfil fits the window
                start_day = base_date + timedelta(
                    days=random.randint(0, max(0, generation_days - 12)),
                )
                evts = _simulate_low_slow_exfiltration(
                    user, profiles[user.id],
                    device_map[user.id], start_day,
                )

            elif attack_label == AttackLabel.INSIDER_DRIFT:
                user = random.choice(users)
                # Start early enough for multi-week drift
                start_day = base_date + timedelta(
                    days=random.randint(0, max(0, generation_days - 28)),
                )
                evts = _simulate_insider_drift(
                    user, profiles[user.id],
                    device_map[user.id], start_day,
                )
            else:
                evts = []

            incident_events.extend(evts)

        results[attack_label.value] = len(incident_events)
        all_events.extend(incident_events)

    # Bulk insert in batches
    for i in range(0, len(all_events), _BATCH_SIZE):
        batch = all_events[i : i + _BATCH_SIZE]
        db.add_all(batch)
        db.flush()

    db.commit()
    return results
