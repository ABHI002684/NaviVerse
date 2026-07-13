import time
import logging
from typing import Dict, Any
from naviverse.core.settings import settings

logger = logging.getLogger(__name__)


def trace_event(thread_id: str, event_name: str, metadata: Dict[str, Any]):
    """Simple tracing utility. In future, forward to LangSmith or other tracing backends.

    Currently logs trace events and keeps them lightweight.
    """
    ts = time.time()
    payload = {
        "thread_id": thread_id,
        "event": event_name,
        "timestamp": ts,
        "metadata": metadata,
    }
    # In production, integrate with LangSmith if API key present
    if getattr(settings, 'GROQ_API_KEY', None):
        logger.debug("Tracing event: %s", payload)
    else:
        logger.debug("Trace (no external): %s", payload)
