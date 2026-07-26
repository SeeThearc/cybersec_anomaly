"""Pydantic schemas for database operations."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    department: str = Field(min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=100)
    country: str = Field(min_length=1, max_length=100)
    joining_date: date


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    department: str | None = Field(default=None, min_length=1, max_length=100)
    role: str | None = Field(default=None, min_length=1, max_length=100)
    country: str | None = Field(default=None, min_length=1, max_length=100)
    joining_date: date | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class DeviceBase(BaseModel):
    user_id: int
    device_name: str = Field(min_length=1, max_length=255)
    device_type: str = Field(min_length=1, max_length=100)
    operating_system: str = Field(min_length=1, max_length=100)
    browser: str = Field(min_length=1, max_length=100)
    fingerprint: str = Field(min_length=1, max_length=255)


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    device_name: str | None = Field(default=None, min_length=1, max_length=255)
    device_type: str | None = Field(default=None, min_length=1, max_length=100)
    operating_system: str | None = Field(default=None, min_length=1, max_length=100)
    browser: str | None = Field(default=None, min_length=1, max_length=100)
    fingerprint: str | None = Field(default=None, min_length=1, max_length=255)


class DeviceRead(DeviceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EventBase(BaseModel):
    user_id: int
    timestamp: datetime
    country: str = Field(min_length=1, max_length=100)
    ip_address: str = Field(min_length=1, max_length=45)
    device_id: int | None = None
    resource: str = Field(min_length=1, max_length=255)
    action: str = Field(min_length=1, max_length=100)
    authentication_method: str = Field(min_length=1, max_length=100)
    session_duration: int = Field(ge=0)
    login_status: str = Field(min_length=1, max_length=50)
    failed_attempts: int = Field(ge=0, default=0)
    bytes_transferred: int = Field(ge=0, default=0)
    command_sequence: str | None = None
    label: str = Field(min_length=1, max_length=50)


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    timestamp: datetime | None = None
    country: str | None = Field(default=None, min_length=1, max_length=100)
    ip_address: str | None = Field(default=None, min_length=1, max_length=45)
    device_id: int | None = None
    resource: str | None = Field(default=None, min_length=1, max_length=255)
    action: str | None = Field(default=None, min_length=1, max_length=100)
    authentication_method: str | None = Field(default=None, min_length=1, max_length=100)
    session_duration: int | None = Field(default=None, ge=0)
    login_status: str | None = Field(default=None, min_length=1, max_length=50)
    failed_attempts: int | None = Field(default=None, ge=0)
    bytes_transferred: int | None = Field(default=None, ge=0)
    command_sequence: str | None = None
    label: str | None = Field(default=None, min_length=1, max_length=50)


class EventRead(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class AlertBase(BaseModel):
    user_id: int
    risk_score: float = Field(ge=0, le=100)
    attack_type: str = Field(min_length=1, max_length=50)
    prediction: str = Field(min_length=1, max_length=50)
    explanation: str = Field(min_length=1)


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    risk_score: float | None = Field(default=None, ge=0, le=100)
    attack_type: str | None = Field(default=None, min_length=1, max_length=50)
    prediction: str | None = Field(default=None, min_length=1, max_length=50)
    explanation: str | None = Field(default=None, min_length=1)


class AlertRead(AlertBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class CopilotRequest(BaseModel):
    question: str


class PredictionRequest(BaseModel):
    event: dict


class StatisticsResponse(BaseModel):
    total_users: int
    total_events: int
    attack_counts: dict
    average_risk: float
    high_risk_users: int
    critical_alerts: int


class AnalyticsResponse(BaseModel):
    attack_distribution: dict
    department_distribution: dict
    risk_trend: list
    monthly_events: list
    top_resources: dict
    top_attack_types: dict
