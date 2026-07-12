import logging
from typing import Dict, Any

from langchain_core.messages import AIMessage

from naviverse.tools.flight_tool import search_flights

logger = logging.getLogger(__name__)


def flight_agent(state: Dict[str, Any]):
    """Independent flight search agent.

    Accepts TravelState and returns only its own output (flight_results, messages).
    Does not mutate shared execution bookkeeping; the graph wrapper handles that.
    """
    query = state.get("user_query", "")
    logger.info("Flight agent running for query: %s", query)

    flight_data = search_flights(query)

    return {
        "flight_results": flight_data,
        "messages": [AIMessage(content="Flight results fetched.")],
    }
