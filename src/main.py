from fastapi import FastAPI
from typing import List
import asyncio
import time

from .models import Event
from .consumer import queue, consumer, stats, processed_events
from .storage import init_db

app = FastAPI()

start_time = time.time()


@app.on_event("startup")
async def startup():
    init_db()
    asyncio.create_task(consumer())


@app.post("/publish")
async def publish(events: List[Event]):
    for event in events:
        await queue.put(event)
    return {"status": "accepted", "count": len(events)}


@app.get("/events")
def get_events(topic: str = None):
    if topic:
        return [e for e in processed_events if e["topic"] == topic]
    return processed_events


@app.get("/stats")
def get_stats():
    return {
        "received": stats["received"],
        "unique_processed": stats["unique_processed"],
        "duplicate_dropped": stats["duplicate_dropped"],
        "topics": list(stats["topics"]),
        "uptime": time.time() - start_time
    }