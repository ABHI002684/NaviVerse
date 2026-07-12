import logging
from typing import Dict, Any, List

from pydantic import BaseModel, ValidationError
from langchain_core.messages import SystemMessage, HumanMessage

import naviverse.agents.llm_client as llm_client

logger = logging.getLogger(__name__)


class SupervisorDecision(BaseModel):
    # extendable: add new boolean fields for future agents without changing agents
    flight: bool = False
    hotel: bool = False
    itinerary: bool = False
    weather: bool = False
    budget: bool = False
    attractions: bool = False
    validation: bool = False
    reflection: bool = False
    reason: str = ""


def supervisor_agent(state: Dict[str, Any]):
    """Decide which specialist agents should run.

    This agent strictly returns a structured decision. It does NOT generate travel content.
    It returns:
      - supervisor_decision: dict
      - required_agents: list[str]
      - execution_plan: dict
      - messages: [LLM response]

    State mutation (execution_log, completed_agents, timestamps) is handled by the graph-level wrapper.
    """
    user_query = state.get("user_query", "")

    prompt = f"""
You are a supervisor whose only job is to decide which specialist agents to run.
Output ONLY a JSON object with the following shape:

{{
  "flight": boolean,
  "hotel": boolean,
  "itinerary": boolean,
  "weather": boolean,
  "budget": boolean,
  "attractions": boolean,
  "validation": boolean,
  "reflection": boolean,
  "reason": string
}}

Be concise in the reason field. Use the user query to decide which agents are necessary.

User query: {user_query}
"""

    llm = llm_client.get_llm()
    response = llm.invoke([
        SystemMessage(content="You are a meta-orchestrator. Respond only in JSON."),
        HumanMessage(content=prompt)
    ])

    raw = response.content
    try:
        parsed = SupervisorDecision.parse_raw(raw)
    except ValidationError:
        # Tolerant parse: extract first JSON object
        try:
            start = raw.index("{")
            end = raw.rindex("}") + 1
            candidate = raw[start:end]
            parsed = SupervisorDecision.parse_raw(candidate)
        except Exception:
            logger.exception("Failed to parse supervisor LLM output as JSON")
            # safe fallback: run itinerary only
            parsed = SupervisorDecision(itinerary=True, reason="Fallback: parsing failed")

    decision: Dict[str, Any] = parsed.dict()

    # required_agents derived from the decision booleans (keeps it declarative)
    required: List[str] = [k for k, v in decision.items() if k in ("flight", "hotel", "itinerary") and v]

    execution_plan = {"order": required}

    logger.info("Supervisor decision: %s", required)

    return {
        "supervisor_decision": decision,
        "required_agents": required,
        "execution_plan": execution_plan,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
