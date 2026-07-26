"""SQLAlchemy ORM models."""

from datetime import date, datetime
from enum import Enum

from sqlalchemy import (
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AttackLabel(str, Enum):
    """Supported event and alert classification labels."""

    NORMAL = "Normal"
    BRUTE_FORCE = "BruteForce"
    CREDENTIAL_STUFFING = "CredentialStuffing"
    IMPOSSIBLE_TRAVEL = "ImpossibleTravel"
    DEVICE_SPOOFING = "DeviceSpoofing"
    LATERAL_MOVEMENT = "LateralMovement"
    LOW_SLOW_EXFILTRATION = "LowSlowExfiltration"
    INSIDER_DRIFT = "InsiderDrift"


class User(Base):
    """Enterprise user profile."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    joining_date: Mapped[date] = mapped_column(Date, nullable=False)

    devices: Mapped[list["Device"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    events: Mapped[list["Event"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    alerts: Mapped[list["Alert"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Device(Base):
    """Known user device."""

    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    device_name: Mapped[str] = mapped_column(String(255), nullable=False)
    device_type: Mapped[str] = mapped_column(String(100), nullable=False)
    operating_system: Mapped[str] = mapped_column(String(100), nullable=False)
    browser: Mapped[str] = mapped_column(String(100), nullable=False)
    fingerprint: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    user: Mapped["User"] = relationship(back_populates="devices")
    events: Mapped[list["Event"]] = relationship(back_populates="device")


class Event(Base):
    """Security activity log entry."""

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)
    device_id: Mapped[int] = mapped_column(
        ForeignKey("devices.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    resource: Mapped[str] = mapped_column(String(255), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    authentication_method: Mapped[str] = mapped_column(String(100), nullable=False)
    session_duration: Mapped[int] = mapped_column(Integer, nullable=False)
    login_status: Mapped[str] = mapped_column(String(50), nullable=False)
    failed_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    bytes_transferred: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    command_sequence: Mapped[str | None] = mapped_column(Text, nullable=True)
    label: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    user: Mapped["User"] = relationship(back_populates="events")
    device: Mapped["Device | None"] = relationship(back_populates="events")


class Alert(Base):
    """Suspicious activity alert."""

    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    attack_type: Mapped[str] = mapped_column(String(50), nullable=False)
    prediction: Mapped[str] = mapped_column(String(50), nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    user: Mapped["User"] = relationship(back_populates="alerts")
