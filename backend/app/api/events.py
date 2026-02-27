from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from ..db import get_db
from ..models import Event
from ..schemas import EventCreate, EventUpdate, EventRead

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("", response_model=list[EventRead])
async def list_events(
    start: datetime | None = None,
    end: datetime | None = None,
    db: AsyncSession = Depends(get_db),
):
    q = select(Event).order_by(Event.start)
    if start:
        q = q.where(Event.end >= start)
    if end:
        q = q.where(Event.start <= end)
    r = await db.execute(q)
    return [EventRead.model_validate(e) for e in r.scalars().all()]


@router.post("", response_model=EventRead, status_code=201)
async def create_event(schema: EventCreate, db: AsyncSession = Depends(get_db)):
    event = Event(**schema.model_dump())
    db.add(event)
    await db.flush()
    await db.refresh(event)
    return EventRead.model_validate(event)


@router.get("/{event_id}", response_model=EventRead)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Event).where(Event.id == event_id))
    event = r.scalar_one_or_none()
    if not event:
        raise HTTPException(404, "Event not found")
    return EventRead.model_validate(event)


@router.patch("/{event_id}", response_model=EventRead)
async def update_event(
    event_id: int, schema: EventUpdate, db: AsyncSession = Depends(get_db)
):
    r = await db.execute(select(Event).where(Event.id == event_id))
    event = r.scalar_one_or_none()
    if not event:
        raise HTTPException(404, "Event not found")
    data = schema.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(event, k, v)
    await db.flush()
    await db.refresh(event)
    return EventRead.model_validate(event)


@router.delete("/{event_id}", status_code=204)
async def delete_event(event_id: int, db: AsyncSession = Depends(get_db)):
    r = await db.execute(select(Event).where(Event.id == event_id))
    event = r.scalar_one_or_none()
    if not event:
        raise HTTPException(404, "Event not found")
    await db.delete(event)
    return None
