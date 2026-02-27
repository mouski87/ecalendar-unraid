# eCalendar - Daily Planner for Unraid

A standalone daily planner with events, chores, to-do lists, weather, and calendar sync (CalDAV).

## Features

- **Calendar** — Create and view events; month view
- **Chores** — Assign chores with due dates; track completion
- **Lists** — Multiple to-do lists with items
- **Weather** — Location-based weather (Open-Meteo)
- **Calendar Sync** — Import from CalDAV (iCloud, Nextcloud)

## Quick Start (Unraid)

1. Clone or copy this repo to your Unraid server.
2. From the project directory:
   ```bash
   docker compose up -d
   ```
3. Open http://YOUR_SERVER:8210 in your browser.

## Docker Compose

```yaml
version: "3.8"

services:
  ecalendar:
    build: .
    ports:
      - "8210:80"
    volumes:
      - ./data:/app/data
    environment:
      - TZ=America/New_York
      - SECRET_KEY=change-me
    restart: unless-stopped
```

## Environment Variables

| Variable   | Default       | Description                    |
|-----------|---------------|--------------------------------|
| `TZ`      | America/New_York | Timezone                    |
| `SECRET_KEY` | change-me   | Session/secret key             |
| `DATA_DIR` | /app/data   | Data directory (SQLite + files)|

## Data

- SQLite database: `./data/ecalendar.db`
- Backup by copying the `./data` folder.

## CalDAV Sync

Use the API to sync from CalDAV (iCloud, Nextcloud, etc.):

```bash
curl -X POST http://localhost:8210/api/sync/caldav \
  -H "Content-Type: application/json" \
  -d '{"url": "https://caldav.icloud.com", "username": "you@icloud.com", "password": "app-password"}'
```

For iCloud: create an app-specific password at appleid.apple.com.

## Development

```bash
# Backend
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend && npm install && npm run dev
```
