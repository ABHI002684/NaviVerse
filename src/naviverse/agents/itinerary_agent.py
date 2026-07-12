import logging
from typing import Dict, Any

from langchain_core.messages import SystemMessage, HumanMessage

import naviverse.agents.llm_client as llm_client

logger = logging.getLogger(__name__)


def itinerary_agent(state: Dict[str, Any]):
    """Generate itinerary using ONLY merged results provided in the TravelState.

    The agent must be pure: accepts TravelState and returns only its own output.
    """
    prompt = f"""
Create a complete travel itinerary.

User Query:
{state.get('user_query','')}

Merged Results:
{state.get('merged_results', {})}

Make the itinerary practical, budget-aware, and easy to follow.
"""

    llm = llm_client.get_llm()
    response = llm.invoke([
        SystemMessage(content="You are an expert travel planner."),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
