"""Calendar sync API - CalDAV."""
import asyncio
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..db import get_db
from ..models import Event
from ..sync.caldav_sync import sync_caldav

router = APIRouter(prefix="/api/sync", tags=["sync"])


class CalDAVConfig(BaseModel):
    url: str
    username: str
    password: str


class SyncResult(BaseModel):
    imported: int
    errors: list[str]


@router.post("/caldav", response_model=SyncResult)
async def run_caldav_sync(config: CalDAVConfig, db: AsyncSession = Depends(get_db)):
    """Sync events from a CalDAV server (iCloud, Nextcloud, etc.)."""
    try:
        events_data = await sync_caldav(config.url, config.username, config.password)
    except Exception as e:
        raise HTTPException(400, f"CalDAV sync failed: {str(e)}")

    imported = 0
    errors = []
    for ed in events_data:
        try:
            r = await db.execute(
                select(Event).where(
                    Event.external_id == ed.get("external_id"),
                    Event.source == "caldav",
                )
            )
            if r.scalar_one_or_none():
                continue
            ev = Event(**ed)
            db.add(ev)
            imported += 1
        except Exception as e:
            errors.append(str(e))
    await db.flush()

    return SyncResult(imported=imported, errors=errors[:5])
