import logging
from typing import Tuple

logger = logging.getLogger(__name__)

_conn = None
_checkpointer = None


def get_connection_and_checkpointer() -> Tuple[object, object]:
    """Lazily create and return a psycopg connection and a PostgresSaver.

    Imports and actual connections are deferred until this function is called so
    that importing the module is safe in test/collection environments.
    """
    global _conn, _checkpointer
    if _conn and _checkpointer:
        return _conn, _checkpointer

    # Lazy imports to avoid import-time failures during test collection
    try:
        import psycopg
        from psycopg.rows import dict_row
    except Exception:
        raise RuntimeError("psycopg is required for database operations")

    # Build database URL
    from naviverse.core.settings import settings
    database_url = settings.DATABASE_URL
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured")

    if "sslmode=" not in database_url:
        separator = "&" if "?" in database_url else "?"
        database_url = f"{database_url}{separator}sslmode=require"

    _conn = psycopg.connect(database_url, autocommit=True, row_factory=dict_row)

    # Try importing LangGraph's PostgresSaver; fall back to a simple dummy saver if unavailable
    try:
        from langgraph.checkpoint.postgres import PostgresSaver
    except Exception:
        class PostgresSaver:
            def __init__(self, conn):
                self.conn = conn
            def setup(self):
                return None

    _checkpointer = PostgresSaver(_conn)
    _checkpointer.setup()

    logger.info("Database connection and checkpointer initialized")
    return _conn, _checkpointer
