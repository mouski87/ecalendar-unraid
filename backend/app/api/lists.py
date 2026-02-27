from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..db import get_db
from ..models import TodoList, TodoItem
from ..schemas import (
    TodoListCreate,
    TodoListRead,
    TodoItemCreate,
    TodoItemUpdate,
    TodoItemRead,
)

router = APIRouter(prefix="/api/lists", tags=["lists"])


@router.get("", response_model=list[TodoListRead])
async def list_todo_lists(db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(TodoList).order_by(TodoList.created_at))
    return [TodoListRead.model_validate(t) for t in r.scalars().all()]


@router.post("", response_model=TodoListRead, status_code=201)
async def create_todo_list(schema: TodoListCreate, db: AsyncSession = Depends(get_db)):
    lst = TodoList(**schema.model_dump())
    db.add(lst)
    await db.flush()
    await db.refresh(lst)
    return TodoListRead.model_validate(lst)


@router.get("/{list_id}", response_model=TodoListRead)
async def get_todo_list(list_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(TodoList).where(TodoList.id == list_id))
    lst = r.scalar_one_or_none()
    if not lst:
        raise HTTPException(404, "List not found")
    return TodoListRead.model_validate(lst)


@router.delete("/{list_id}", status_code=204)
async def delete_todo_list(list_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(TodoList).where(TodoList.id == list_id))
    lst = r.scalar_one_or_none()
    if not lst:
        raise HTTPException(404, "List not found")
    await db.execute(TodoItem.__table__.delete().where(TodoItem.list_id == list_id))
    await db.delete(lst)
    return None


@router.get("/{list_id}/items", response_model=list[TodoItemRead])
async def list_items(list_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(
        select(TodoItem)
        .where(TodoItem.list_id == list_id)
        .order_by(TodoItem.sort_order, TodoItem.id)
    )
    return [TodoItemRead.model_validate(i) for i in r.scalars().all()]


@router.post("/{list_id}/items", response_model=TodoItemRead, status_code=201)
async def create_item(
    list_id: int, schema: TodoItemCreate, db: AsyncSession = Depends(get_db)
):
    r = await db.execute(select(TodoList).where(TodoList.id == list_id))
    if not r.scalar_one_or_none():
        raise HTTPException(404, "List not found")
    item = TodoItem(list_id=list_id, **schema.model_dump())
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return TodoItemRead.model_validate(item)


@router.patch("/{list_id}/items/{item_id}", response_model=TodoItemRead)
async def update_item(
    list_id: int,
    item_id: int,
    schema: TodoItemUpdate,
    db: AsyncSession = Depends(get_db),
):
    r = await db.execute(
        select(TodoItem).where(
            TodoItem.id == item_id,
            TodoItem.list_id == list_id,
        )
    )
    item = r.scalar_one_or_none()
    if not item:
        raise HTTPException(404, "Item not found")
    for k, v in schema.model_dump(exclude_unset=True).items():
        setattr(item, k, v)
    await db.flush()
    await db.refresh(item)
    return TodoItemRead.model_validate(item)


@router.delete("/{list_id}/items/{item_id}", status_code=204)
async def delete_item(list_id: int, item_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(
        select(TodoItem).where(
            TodoItem.id == item_id,
            TodoItem.list_id == list_id,
        )
    )
    item = r.scalar_one_or_none()
    if not item:
        raise HTTPException(404, "Item not found")
    await db.delete(item)
    return None
