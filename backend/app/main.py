from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .config import settings
from .db import init_db
from .models import Event, Chore, TodoList, TodoItem, Category, CalendarSync
from .api import events, chores, lists, categories, weather, sync


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    pass


app = FastAPI(
    title="eCalendar",
    description="Daily planner - events, chores, lists, weather",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router)
app.include_router(chores.router)
app.include_router(lists.router)
app.include_router(categories.router)
app.include_router(weather.router)
app.include_router(sync.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
