"""Database CRUD operations."""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app import models, schemas


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.get(models.User, user_id)


def get_user_with_relations(db: Session, user_id: int) -> models.User | None:
    stmt = (
        select(models.User)
        .options(
            selectinload(models.User.devices),
            selectinload(models.User.events),
            selectinload(models.User.alerts),
        )
        .where(models.User.id == user_id)
    )
    return db.scalars(stmt).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    stmt = select(models.User).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def update_user(
    db: Session,
    user_id: int,
    user_update: schemas.UserUpdate,
) -> models.User | None:
    db_user = get_user(db, user_id)
    if db_user is None:
        return None

    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if db_user is None:
        return False

    db.delete(db_user)
    db.commit()
    return True


def create_device(db: Session, device: schemas.DeviceCreate) -> models.Device:
    db_device = models.Device(**device.model_dump())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def get_device(db: Session, device_id: int) -> models.Device | None:
    return db.get(models.Device, device_id)


def get_devices_by_user(db: Session, user_id: int) -> list[models.Device]:
    stmt = select(models.Device).where(models.Device.user_id == user_id)
    return list(db.scalars(stmt).all())


def get_devices(db: Session, skip: int = 0, limit: int = 100) -> list[models.Device]:
    stmt = select(models.Device).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def update_device(
    db: Session,
    device_id: int,
    device_update: schemas.DeviceUpdate,
) -> models.Device | None:
    db_device = get_device(db, device_id)
    if db_device is None:
        return None

    for field, value in device_update.model_dump(exclude_unset=True).items():
        setattr(db_device, field, value)

    db.commit()
    db.refresh(db_device)
    return db_device


def delete_device(db: Session, device_id: int) -> bool:
    db_device = get_device(db, device_id)
    if db_device is None:
        return False

    db.delete(db_device)
    db.commit()
    return True


def create_event(db: Session, event: schemas.EventCreate) -> models.Event:
    db_event = models.Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_event(db: Session, event_id: int) -> models.Event | None:
    return db.get(models.Event, event_id)


def get_events(db: Session, skip: int = 0, limit: int = 100) -> list[models.Event]:
    stmt = select(models.Event).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def get_events_by_user(db: Session, user_id: int) -> list[models.Event]:
    stmt = select(models.Event).where(models.Event.user_id == user_id)
    return list(db.scalars(stmt).all())


def update_event(
    db: Session,
    event_id: int,
    event_update: schemas.EventUpdate,
) -> models.Event | None:
    db_event = get_event(db, event_id)
    if db_event is None:
        return None

    for field, value in event_update.model_dump(exclude_unset=True).items():
        setattr(db_event, field, value)

    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int) -> bool:
    db_event = get_event(db, event_id)
    if db_event is None:
        return False

    db.delete(db_event)
    db.commit()
    return True


def create_alert(db: Session, alert: schemas.AlertCreate) -> models.Alert:
    db_alert = models.Alert(**alert.model_dump())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def get_alert(db: Session, alert_id: int) -> models.Alert | None:
    return db.get(models.Alert, alert_id)


def get_alerts(db: Session, skip: int = 0, limit: int = 100) -> list[models.Alert]:
    stmt = select(models.Alert).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


def get_alerts_by_user(db: Session, user_id: int) -> list[models.Alert]:
    stmt = select(models.Alert).where(models.Alert.user_id == user_id)
    return list(db.scalars(stmt).all())


def update_alert(
    db: Session,
    alert_id: int,
    alert_update: schemas.AlertUpdate,
) -> models.Alert | None:
    db_alert = get_alert(db, alert_id)
    if db_alert is None:
        return None

    for field, value in alert_update.model_dump(exclude_unset=True).items():
        setattr(db_alert, field, value)

    db.commit()
    db.refresh(db_alert)
    return db_alert


def delete_alert(db: Session, alert_id: int) -> bool:
    db_alert = get_alert(db, alert_id)
    if db_alert is None:
        return False

    db.delete(db_alert)
    db.commit()
    return True
