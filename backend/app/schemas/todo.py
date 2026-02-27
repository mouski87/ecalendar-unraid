from datetime import datetime
from pydantic import BaseModel


class TodoListCreate(BaseModel):
    title: str
    color: str | None = None
    category_id: int | None = None


class TodoListRead(BaseModel):
    id: int
    title: str
    color: str | None
    category_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TodoItemCreate(BaseModel):
    title: str
    sort_order: int = 0


class TodoItemUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None
    sort_order: int | None = None


class TodoItemRead(BaseModel):
    id: int
    list_id: int
    title: str
    completed: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
