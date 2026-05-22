from abc import ABC, abstractmethod
from pydantic import BaseModel, Field


class SourceDocument(BaseModel):
    id: str
    title: str
    content: str
    source_type: str
    uri: str | None = None
    metadata: dict = Field(default_factory=dict)


class BaseConnector(ABC):
    @abstractmethod
    def load(self) -> list[SourceDocument]:
        raise NotImplementedError
