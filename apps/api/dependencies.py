from functools import lru_cache
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    environment: str = Field(default="local", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    cors_allow_origins: str = Field(default="*", alias="CORS_ALLOW_ORIGINS")

    postgres_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, alias="POSTGRES_PORT")
    postgres_db: str = Field(default="agentic_graphrag", alias="POSTGRES_DB")
    postgres_user: str = Field(default="graphrag", alias="POSTGRES_USER")
    postgres_password: str = Field(default="graphrag", alias="POSTGRES_PASSWORD")

    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    neo4j_uri: str = Field(default="bolt://localhost:7687", alias="NEO4J_URI")
    neo4j_user: str = Field(default="neo4j", alias="NEO4J_USER")
    neo4j_password: str = Field(default="agentic-graphrag-password", alias="NEO4J_PASSWORD")

    qdrant_url: str = Field(default="http://localhost:6333", alias="QDRANT_URL")
    qdrant_api_key: str = Field(default="INSERT API KEY HERE", alias="QDRANT_API_KEY")
    qdrant_collection: str = Field(default="documents", alias="QDRANT_COLLECTION")
    vector_size: int = Field(default=384, alias="VECTOR_SIZE")

    minio_endpoint: str = Field(default="localhost:9000", alias="MINIO_ENDPOINT")
    minio_access_key: str = Field(default="minioadmin", alias="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field(default="minioadmin", alias="MINIO_SECRET_KEY")
    minio_bucket: str = Field(default="agentic-graphrag", alias="MINIO_BUCKET")

    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    default_llm_provider: str = Field(default="ollama", alias="DEFAULT_LLM_PROVIDER")
    default_llm_model: str = Field(default="llama3.1:8b", alias="DEFAULT_LLM_MODEL")
    default_embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        alias="DEFAULT_EMBEDDING_MODEL",
    )

    openai_api_key: str = Field(default="INSERT API KEY HERE", alias="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="INSERT API KEY HERE", alias="ANTHROPIC_API_KEY")

    @property
    def postgres_sync_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def cors_origins_list(self) -> list[str]:
        if self.cors_allow_origins.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_allow_origins.split(",") if origin.strip()]


class AppContainer:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.services: dict[str, Any] = {}

    async def startup(self) -> None:
        self.services["started"] = True

    async def shutdown(self) -> None:
        self.services.clear()

    async def readiness_check(self) -> dict[str, Any]:
        return {
            "ready": True,
            "checks": {
                "api": "ok",
                "settings": "loaded",
                "postgres_config": "present",
                "neo4j_config": "present",
                "qdrant_config": "present",
                "redis_config": "present",
            },
            "environment": self.settings.environment,
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_app_container() -> AppContainer:
    return AppContainer(settings=get_settings())
