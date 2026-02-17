from typing import Any, Dict

from pgvector.psycopg import to_db

from app.core.db import db_execute, db_fetchall, db_fetchone
from app.embeddings.encoder import get_encoder


def save_document(args: Dict[str, Any]) -> Dict[str, Any]:
    content = args.get("content", "").strip()
    metadata = args.get("metadata") or {}
    if not content:
        return {"error": "content is required"}
    encoder = get_encoder()
    vector = encoder.embed(content)
    db_execute(
        "insert into documents (content, metadata, embedding) values (%s, %s, %s)",
        (content, metadata, to_db(vector)),
    )
    return {"status": "saved"}


def search_documents(args: Dict[str, Any]) -> Dict[str, Any]:
    query = args.get("query", "")
    top_k = int(args.get("top_k") or 4)
    encoder = get_encoder()
    vector = encoder.embed(query)
    rows = db_fetchall(
        "select id, content, metadata, 1 - (embedding <=> %s) as score "
        "from documents order by embedding <=> %s limit %s",
        (to_db(vector), to_db(vector), top_k),
    )
    return {"results": rows}


def get_user(args: Dict[str, Any]) -> Dict[str, Any]:
    user_id = args.get("user_id")
    if not user_id:
        return {"error": "user_id is required"}
    user = db_fetchone("select * from users where id = %s", (user_id,))
    return {"user": user}
