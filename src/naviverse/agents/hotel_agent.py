import logging
from typing import Dict, Any

from langchain_core.messages import AIMessage

from naviverse.tools.tavily_tool import tavily_search

logger = logging.getLogger(__name__)


def hotel_agent(state: Dict[str, Any]):
    """Independent hotel search agent.

    Returns only hotel_results and messages. No shared state mutation here.
    """
    query = state.get("user_query", "")
    logger.info("Hotel agent running for query: %s", query)

    hotel_results = tavily_search(f"Best hotels for {query}")

    return {
        "hotel_results": hotel_results,
        "messages": [AIMessage(content="Hotel information fetched.")],
    }
