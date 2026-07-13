from typing import List, Dict, Any
import logging

from naviverse.db.checkpoint import get_connection_and_checkpointer

logger = logging.getLogger(__name__)


def ensure_tables():
    conn, _ = get_connection_and_checkpointer()
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS conversation_messages (
                id SERIAL PRIMARY KEY,
                thread_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT,
                created_at TIMESTAMPTZ DEFAULT now()
            );
            """
        )


def save_message(thread_id: str, role: str, content: str):
    conn, _ = get_connection_and_checkpointer()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO conversation_messages (thread_id, role, content) VALUES (%s, %s, %s)",
            (thread_id, role, content)
        )


def get_messages(thread_id: str) -> List[Dict[str, Any]]:
    conn, _ = get_connection_and_checkpointer()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, thread_id, role, content, created_at FROM conversation_messages WHERE thread_id = %s ORDER BY created_at ASC",
            (thread_id,)
        )
        rows = cur.fetchall()
    return [dict(r) for r in rows]


# Tables are created on-demand by calling ensure_tables().
# Avoid running DB migrations on module import to keep imports lightweight and testable.
