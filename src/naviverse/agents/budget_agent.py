import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def budget_agent(state: Dict[str, Any]):
    """Estimate trip budget using simple heuristics.

    Returns budget_results dict with estimated totals.
    """
    # Very rough defaults
    num_days = 3
    if state.get("itinerary") and isinstance(state["itinerary"], str):
        # crude parse: look for 'Day' occurrences
        num_days = max(1, state["itinerary"].lower().count("day")) or 3

    # flight cost estimate
    flight_est = 200.0 if state.get("flight_results") else 0.0
    # hotel per night estimate
    hotel_per_night = 100.0 if state.get("hotel_results") else 0.0
    hotel_est = hotel_per_night * num_days
    food_est = 30.0 * num_days
    transport_est = 20.0 * num_days
    misc_est = 50.0

    total = flight_est + hotel_est + food_est + transport_est + misc_est

    return {"budget_results": {
        "days": num_days,
        "flight_estimate": flight_est,
        "hotel_estimate": hotel_est,
        "food_estimate": food_est,
        "transport_estimate": transport_est,
        "misc_estimate": misc_est,
        "total_estimate": total
    }}
