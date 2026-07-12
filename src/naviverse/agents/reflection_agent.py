import logging
from typing import Dict, Any

from langchain_core.messages import SystemMessage, HumanMessage
import naviverse.agents.llm_client as llm_client

logger = logging.getLogger(__name__)


def reflection_agent(state: Dict[str, Any]):
    """Review the generated itinerary and suggest improvements.

    This agent should be idempotent and only read itinerary + merged_results.
    Returns reflection_results with suggested edits.
    """
    itinerary = state.get("itinerary")
    merged = state.get("merged_results", {})

    if not itinerary:
        return {"reflection_results": {"notes": ["No itinerary to reflect on."]}}

    prompt = f"""
You are an assistant that improves travel itineraries.
User Query: {state.get('user_query','')}
Merged Results: {merged}
Itinerary:
{itinerary}
Provide a concise list of suggested improvements.
"""
    try:
        llm = llm_client.get_llm()
        response = llm.invoke([
            SystemMessage(content="You are a travel reflection assistant."),
            HumanMessage(content=prompt)
        ])
        notes = [response.content]
    except Exception as e:
        logger.exception("Reflection agent failed: %s", e)
        notes = ["Reflection service unavailable."]

    return {"reflection_results": {"notes": notes}}
