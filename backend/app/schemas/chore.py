from datetime import datetime, date
from pydantic import BaseModel


class ChoreCreate(BaseModel):
    title: str
    description: str | None = None
    assignee: str | None = None
    due_date: date | None = None
    category_id: int | None = None


class ChoreUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    assignee: str | None = None
    due_date: date | None = None
    completed: bool | None = None
    category_id: int | None = None


class ChoreRead(BaseModel):
    id: int
    title: str
    description: str | None
    assignee: str | None
    due_date: date | None
    completed: bool
    completed_at: datetime | None
    category_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
