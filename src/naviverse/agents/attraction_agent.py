import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


def attraction_agent(state: Dict[str, Any]):
    """Recommend attractions based on destination and duration.

    Returns attraction_results as a list of recommended places.
    """
    merged = state.get("merged_results", {})
    dest = merged.get("destination") or state.get("user_query", "")

    # Placeholder: static recommendations; replace with real API later
    recommendations: List[Dict[str, str]] = [
        {"name": f"Top Museum in {dest}", "type": "museum"},
        {"name": f"Historic Center of {dest}", "type": "landmark"},
        {"name": f"Famous Park in {dest}", "type": "park"},
    ]

    return {"attraction_results": recommendations}
