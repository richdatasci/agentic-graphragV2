from pydantic import BaseModel, Field


class ParsedDocument(BaseModel):
    document_id: str
    title: str
    text: str
    source_type: str
    metadata: dict = Field(default_factory=dict)


class DocumentChunk(BaseModel):
    id: str
    document_id: str
    text: str
    index: int
    page_number: int | None = None
    metadata: dict = Field(default_factory=dict)
