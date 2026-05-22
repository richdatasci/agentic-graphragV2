from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CoreSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: str = Field(default="local", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    openai_api_key: str = Field(default="INSERT API KEY HERE", alias="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="INSERT API KEY HERE", alias="ANTHROPIC_API_KEY")
    qdrant_api_key: str = Field(default="INSERT API KEY HERE", alias="QDRANT_API_KEY")
    neo4j_uri: str = Field(default="bolt://localhost:7687", alias="NEO4J_URI")
    neo4j_user: str = Field(default="neo4j", alias="NEO4J_USER")
    neo4j_password: str = Field(default="agentic-graphrag-password", alias="NEO4J_PASSWORD")
    qdrant_url: str = Field(default="http://localhost:6333", alias="QDRANT_URL")
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    default_llm_provider: str = Field(default="ollama", alias="DEFAULT_LLM_PROVIDER")
    default_llm_model: str = Field(default="llama3.1:8b", alias="DEFAULT_LLM_MODEL")
    default_embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2", alias="DEFAULT_EMBEDDING_MODEL")
