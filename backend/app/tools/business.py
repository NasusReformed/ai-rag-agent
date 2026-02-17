from typing import Any, Dict

from app.core.db import db_execute, db_fetchone


def log_event(args: Dict[str, Any]) -> Dict[str, Any]:
    event_type = args.get("event_type", "generic")
    payload = args.get("payload") or {}
    db_execute(
        "insert into events (event_type, payload) values (%s, %s)",
        (event_type, payload),
    )
    return {"status": "logged", "event_type": event_type}


def create_ticket(args: Dict[str, Any]) -> Dict[str, Any]:
    title = args.get("title", "").strip()
    priority = args.get("priority", "medium")
    user_id = args.get("user_id")
    context = args.get("context") or {}
    if not title:
        return {"error": "title is required"}
    ticket = db_fetchone(
        "insert into tickets (title, priority, user_id, context) values (%s, %s, %s, %s) "
        "returning id, status",
        (title, priority, user_id, context),
    )
    return {"ticket": ticket}
