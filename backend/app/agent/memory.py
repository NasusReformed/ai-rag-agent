from typing import Optional

from app.core.db import db_execute, db_fetchall, db_fetchone


def ensure_session(session_id: Optional[str], user_id: Optional[str]) -> str:
    if session_id:
        return session_id
    result = db_fetchone(
        "insert into agent_sessions (user_id) values (%s) returning id", (user_id,)
    )
    return result["id"]


def add_message(session_id: str, role: str, content: str) -> None:
    db_execute(
        "insert into agent_messages (session_id, role, content) values (%s, %s, %s)",
        (session_id, role, content),
    )


def get_recent_messages(session_id: str, limit: int = 6) -> list[dict]:
    return db_fetchall(
        "select role, content from agent_messages where session_id = %s "
        "order by created_at desc limit %s",
        (session_id, limit),
    )
