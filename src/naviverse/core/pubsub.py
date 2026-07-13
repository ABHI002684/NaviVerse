import asyncio
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

_queues: Dict[str, asyncio.Queue] = {}


def get_queue(thread_id: str) -> asyncio.Queue:
    q = _queues.get(thread_id)
    if not q:
        q = asyncio.Queue()
        _queues[thread_id] = q
    return q


async def publish(thread_id: str, event: Dict[str, Any]):
    q = get_queue(thread_id)
    await q.put(event)


async def subscribe(thread_id: str):
    q = get_queue(thread_id)
    while True:
        event = await q.get()
        yield event
