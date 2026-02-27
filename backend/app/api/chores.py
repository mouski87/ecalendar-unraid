from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..db import get_db
from ..models import Chore
from ..schemas import ChoreCreate, ChoreUpdate, ChoreRead

router = APIRouter(prefix="/api/chores", tags=["chores"])


@router.get("", response_model=list[ChoreRead])
async def list_chores(
    completed: bool | None = None,
    due_before: date | None = None,
    assignee: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    q = select(Chore).order_by(Chore.due_date.asc().nullslast(), Chore.created_at.desc())
    if completed is not None:
        q = q.where(Chore.completed == completed)
    if due_before:
        q = q.where(Chore.due_date <= due_before)
    if assignee:
        q = q.where(Chore.assignee == assignee)
    r = await db.execute(q)
    return [ChoreRead.model_validate(c) for c in r.scalars().all()]


@router.post("", response_model=ChoreRead, status_code=201)
async def create_chore(schema: ChoreCreate, db: AsyncSession = Depends(get_db)):
    chore = Chore(**schema.model_dump())
    db.add(chore)
    await db.flush()
    await db.refresh(chore)
    return ChoreRead.model_validate(chore)


@router.get("/{chore_id}", response_model=ChoreRead)
async def get_chore(chore_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Chore).where(Chore.id == chore_id))
    chore = r.scalar_one_or_none()
    if not chore:
        raise HTTPException(404, "Chore not found")
    return ChoreRead.model_validate(chore)


@router.patch("/{chore_id}", response_model=ChoreRead)
async def update_chore(
    chore_id: int, schema: ChoreUpdate, db: AsyncSession = Depends(get_db)
):
    r = await db.execute(select(Chore).where(Chore.id == chore_id))
    chore = r.scalar_one_or_none()
    if not chore:
        raise HTTPException(404, "Chore not found")
    data = schema.model_dump(exclude_unset=True)
    if data.get("completed") and not chore.completed:
        from datetime import datetime
        data["completed_at"] = datetime.utcnow()
    elif data.get("completed") is False:
        data["completed_at"] = None
    for k, v in data.items():
        setattr(chore, k, v)
    await db.flush()
    await db.refresh(chore)
    return ChoreRead.model_validate(chore)


@router.delete("/{chore_id}", status_code=204)
async def delete_chore(chore_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Chore).where(Chore.id == chore_id))
    chore = r.scalar_one_or_none()
    if not chore:
        raise HTTPException(404, "Chore not found")
    await db.delete(chore)
    return None
