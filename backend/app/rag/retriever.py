from typing import List

from pgvector.psycopg import to_db

from app.core.config import get_settings
from app.core.db import db_execute, db_fetchall
from app.embeddings.encoder import EmbeddingEncoder


class Retriever:
    def __init__(self, encoder: EmbeddingEncoder) -> None:
        self.encoder = encoder
        self.settings = get_settings()

    def index_documents(self, documents: list[object]) -> int:
        contents = [doc.content for doc in documents]
        vectors = self.encoder.embed_batch(contents)
        for doc, vector in zip(documents, vectors):
            db_execute(
                "insert into documents (content, metadata, embedding) values (%s, %s, %s)",
                (doc.content, doc.metadata, to_db(vector)),
            )
        return len(documents)

    def search(self, query: str, top_k: int | None = None) -> List[dict]:
        vector = self.encoder.embed(query)
        limit = top_k or self.settings.rag_top_k
        rows = db_fetchall(
            "select id, content, metadata, 1 - (embedding <=> %s) as score "
            "from documents order by embedding <=> %s limit %s",
            (to_db(vector), to_db(vector), limit),
        )
        return rows
