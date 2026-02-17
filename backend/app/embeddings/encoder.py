from functools import lru_cache
from typing import List

from sentence_transformers import SentenceTransformer

from app.core.config import get_settings


class EmbeddingEncoder:
    def __init__(self, model_name: str) -> None:
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> List[float]:
        vector = self.model.encode([text], normalize_embeddings=True)[0]
        return vector.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        vectors = self.model.encode(texts, normalize_embeddings=True)
        return [vector.tolist() for vector in vectors]


@lru_cache(maxsize=1)
def get_encoder() -> EmbeddingEncoder:
    settings = get_settings()
    return EmbeddingEncoder(settings.embeddings_model)
