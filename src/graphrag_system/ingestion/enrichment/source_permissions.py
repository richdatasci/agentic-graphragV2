from pydantic import BaseModel, Field


class SourcePermissions(BaseModel):
    allowed_roles: list[str] = Field(default_factory=lambda: ["admin"])
    classification: str = "internal"
