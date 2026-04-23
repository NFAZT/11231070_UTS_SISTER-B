import asyncio
from .storage import is_duplicate, save_event

queue = asyncio.Queue()

stats = {
    "received": 0,
    "unique_processed": 0,
    "duplicate_dropped": 0,
    "topics": set()
}

processed_events = []


async def consumer():
    while True:
        event = await queue.get()

        stats["received"] += 1

        if is_duplicate(event.event_id):
            print("DUPLICATE DETECTED:", event.event_id)
            stats["duplicate_dropped"] += 1
        else:
            print("PROCESSING EVENT:", event.event_id)
            save_event(event.event_id, event.topic)

            stats["unique_processed"] += 1
            stats["topics"].add(event.topic)

            processed_events.append(event.dict())

        queue.task_done()