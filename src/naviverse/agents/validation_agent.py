import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


def validation_agent(state: Dict[str, Any]):
    """Validate available flight/hotel/itinerary data for obvious issues.

    Returns a validation_results dict with 'ok': bool and 'issues': list.
    """
    issues: List[str] = []

    # Basic checks
    flights = state.get("flight_results")
    hotels = state.get("hotel_results")
    itinerary = state.get("itinerary")

    if flights and isinstance(flights, dict):
        # example check: presence of origin/destination keys
        if not flights.get("origin") or not flights.get("destination"):
            issues.append("Flight data missing origin or destination.")

    if hotels and isinstance(hotels, list):
        # ensure hotel entries have a name
        for h in hotels:
            if not h.get("name"):
                issues.append("One of the hotel entries is missing a name.")

    # Itinerary consistency: dates present
    if itinerary and isinstance(itinerary, str):
        if "Day" not in itinerary and "day" not in itinerary:
            issues.append("Itinerary looks short or missing day-by-day structure.")

    ok = len(issues) == 0
    return {"validation_results": {"ok": ok, "issues": issues}}
