import logging
from typing import Dict, Any

from naviverse.tools.weather_tool import fetch_weather_for_destination

logger = logging.getLogger(__name__)


def weather_agent(state: Dict[str, Any]):
    """Fetches weather for the primary destination inferred from user_query or merged_results."""
    dest = None
    # try to infer destination from merged_results first
    merged = state.get("merged_results", {}) or {}
    dest = merged.get("destination") or state.get("user_query","")

    try:
        weather = fetch_weather_for_destination(dest, days=7)
    except Exception as e:
        logger.exception("Weather agent failed: %s", e)
        return {"weather_results": None}

    return {"weather_results": weather}
