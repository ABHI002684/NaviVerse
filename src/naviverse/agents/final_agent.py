import logging
from typing import Dict, Any

from langchain_core.messages import SystemMessage, HumanMessage

import naviverse.agents.llm_client as llm_client

logger = logging.getLogger(__name__)


def final_agent(state: Dict[str, Any]):
    """Format the final response using available results and execution summary.

    Final agent does not orchestrate; it only formats content using state fields:
      - original query
      - flight_results (if any)
      - hotel_results (if any)
      - itinerary (if any)
      - execution summary (logs and completed agents)

    It should gracefully report missing information when agents failed or were skipped.
    """
    final_prompt = f"""
Generate the final travel response for the user.

User Request:
{state.get('user_query','')}

Flights:
{state.get('flight_results','(not available)')}

Hotels:
{state.get('hotel_results','(not available)')}

Itinerary:
{state.get('itinerary','(not available)')}

Execution Summary:
Completed agents: {state.get('completed_agents', [])}
Execution log:
{state.get('execution_log','')}

Format the final answer using these sections:
1. Trip Summary
2. Flight Information
3. Hotel Suggestions
4. Day-by-Day Itinerary
5. Estimated Budget
6. Final Recommendations

Also briefly describe what agents were run and why (based on supervisor decision).
"""

    llm = llm_client.get_llm()
    response = llm.invoke([
        SystemMessage(content="You are a professional AI travel booking assistant."),
        HumanMessage(content=final_prompt)
    ])

    logger.info("Final agent completed. Completed agents: %s", state.get('completed_agents', []))

    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
