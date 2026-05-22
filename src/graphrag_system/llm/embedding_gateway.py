import hashlib
import math
from typing import Iterable


class EmbeddingGateway:
    """Local-first embedding gateway.

    It tries sentence-transformers first. If the model is unavailable, it falls
    back to a deterministic hashing embedding so the app remains runnable.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", vector_size: int = 384) -> None:
        self.model_name = model_name
        self.vector_size = vector_size
        self._model = None

    @property
    def model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
            except Exception:
                self._model = False
        return self._model

    def embed_text(self, text: str) -> list[float]:
        if self.model:
            vector = self.model.encode(text, normalize_embeddings=True)
            return [float(v) for v in vector.tolist()]
        return self._hash_embedding(text)

    def embed_many(self, texts: Iterable[str]) -> list[list[float]]:
        return [self.embed_text(text) for text in texts]

    def _hash_embedding(self, text: str) -> list[float]:
        vector = [0.0] * self.vector_size
        tokens = [token.strip().lower() for token in text.split() if token.strip()]
        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            idx = int.from_bytes(digest[:4], "big") % self.vector_size
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[idx] += sign
        norm = math.sqrt(sum(v * v for v in vector)) or 1.0
        return [v / norm for v in vector]
