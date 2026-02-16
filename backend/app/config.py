"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    app_name: str = "RAG System"
    app_version: str = "1.0.0"
    log_level: str = "INFO"
    api_key: str = "changeme"
    backend_cors_origins: str = "http://localhost:3000"

    # PostgreSQL (app database)
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "raguser"
    postgres_password: str = "changeme"
    postgres_db: str = "rag_system"

    # PostgreSQL (Northwind - text-to-SQL)
    northwind_db: str = "northwind"

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection_name: str = "documents"

    # OpenAI
    openai_api_key: str = ""

    @property
    def app_database_url(self) -> str:
        """Construct the PostgreSQL async connection URL for the app DB."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def northwind_database_url(self) -> str:
        """Construct the PostgreSQL async connection URL for Northwind."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.northwind_db}"
        )

    openai_embedding_model: str = "text-embedding-3-small"
    openai_chat_model: str = "gpt-4o"

    # LangSmith
    langchain_tracing_v2: bool = True
    langchain_api_key: str = ""
    langchain_project: str = "rag-system"

    @property
    def app_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def northwind_database_url(self) -> str:
        """Sync URL for LangChain SQL agent (uses psycopg2 driver)."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.northwind_db}"
        )

    @property
    def northwind_readonly_url(self) -> str:
        """Read-only connection for SQL agent safety."""
        return (
            f"postgresql://rag_readonly:readonly_password"
            f"@{self.postgres_host}:{self.postgres_port}/{self.northwind_db}"
        )

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",")]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
