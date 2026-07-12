import logging
from typing import Optional

logger = logging.getLogger(__name__)

_llm_client = None


def get_llm():
    """Lazily initialize and return a ChatGroq LLM client.

    This function avoids creating the client at import time so test collection and
    other imports don't require API keys or network access.
    """
    global _llm_client
    if _llm_client is not None:
        return _llm_client

    # Import inside function to avoid import-time dependency failures
    try:
        from langchain_groq import ChatGroq
    except Exception as e:
        raise RuntimeError("LLM client package langchain_groq is not available") from e

    # Read API key lazily
    from naviverse.core.settings import settings
    api_key = settings.GROQ_API_KEY
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured. Set it in environment or .env")

    _llm_client = ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key)
    return _llm_client
