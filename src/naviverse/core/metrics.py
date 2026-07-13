import time
from typing import Dict

# Simple in-memory metrics store; replace with Prometheus or similar in production
_metrics: Dict[str, Dict[str, float]] = {}


def record_agent_execution(agent_name: str, duration: float, status: str):
    now = time.time()
    _metrics.setdefault(agent_name, {})
    _metrics[agent_name]["last_duration"] = duration
    _metrics[agent_name]["last_status"] = 1 if status == "completed" else 0
    _metrics[agent_name]["last_executed_at"] = now


def get_metrics():
    return _metrics
