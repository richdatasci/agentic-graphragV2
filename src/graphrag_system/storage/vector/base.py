from abc import ABC, abstractmethod
from pydantic import BaseModel, Field


class VectorRecord(BaseModel):
    id: str
    vector: list[float]
    text: str
    metadata: dict = Field(default_factory=dict)


class BaseVectorStore(ABC):
    @abstractmethod
    def upsert(self, records: list[VectorRecord]) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(self, vector: list[float], top_k: int = 8) -> list[dict]:
        raise NotImplementedError
