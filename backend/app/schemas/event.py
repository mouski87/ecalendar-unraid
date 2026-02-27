from datetime import datetime
from pydantic import BaseModel


class EventCreate(BaseModel):
    title: str
    description: str | None = None
    start: datetime
    end: datetime
    all_day: bool = False
    recurrence: str | None = None
    category_id: int | None = None


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start: datetime | None = None
    end: datetime | None = None
    all_day: bool | None = None
    recurrence: str | None = None
    category_id: int | None = None


class EventRead(BaseModel):
    id: int
    title: str
    description: str | None
    start: datetime
    end: datetime
    all_day: bool
    recurrence: str | None
    category_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
