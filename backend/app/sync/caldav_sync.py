"""CalDAV sync - works with iCloud, Nextcloud, and other CalDAV servers."""
from datetime import datetime
import caldav


def sync_caldav_fetch(url: str, username: str, password: str) -> list[dict]:
    """Fetch events from CalDAV server. Returns list of event dicts for upsert."""
    client = caldav.DAVClient(url=url, username=username, password=password)
    principal = client.principal()
    calendars = principal.calendars()

    events_out = []
    for calendar in calendars:
        try:
            events = calendar.events()
            for event in events:
                try:
                    ical = event.icalendar_component
                    if not ical:
                        continue
                    for comp in ical.walk():
                        if comp.name == "VEVENT":
                            dtstart = comp.get("dtstart")
                            dtend = comp.get("dtend")
                            if dtstart and dtend:
                                start = dtstart.dt if hasattr(dtstart.dt, "year") else datetime.combine(dtstart.dt, datetime.min.time())
                                end = dtend.dt if hasattr(dtend.dt, "year") else datetime.combine(dtend.dt, datetime.min.time())
                                summary = str(comp.get("summary", ""))
                                desc = str(comp.get("description", ""))
                                uid = str(comp.get("uid", ""))
                                events_out.append({
                                    "title": summary,
                                    "description": desc or None,
                                    "start": start,
                                    "end": end,
                                    "all_day": not hasattr(dtstart.dt, "hour"),
                                    "external_id": uid,
                                    "source": "caldav",
                                })
                except Exception:
                    continue
        except Exception:
            continue

    return events_out


async def sync_caldav(url: str, username: str, password: str) -> list[dict]:
    """Async wrapper - runs sync in thread pool."""
    import asyncio
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, sync_caldav_fetch, url, username, password)
