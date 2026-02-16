"""SQL Database tool wrapper for Northwind."""

import logging

from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine

from app.config import settings
from app.core.sql_safety import validate_sql

logger = logging.getLogger(__name__)


class NorthwindDatabase:
    """Wrapper around LangChain's SQLDatabase with safety checks."""

    def __init__(self):
        # We need a synchronous engine for LangChain's SQLDatabase
        # Reuse settings but use psycopg2 (default) or asyncpg with run_sync?
        # LangChain SQLDatabase uses sqlalchemy core, usually sync.
        # Let's construct a sync URL from settings.
        sync_url = (
            f"postgresql://{settings.postgres_user}:{settings.postgres_password}"
            f"@{settings.postgres_host}:{settings.postgres_port}/{settings.northwind_db}"
        )
        self.engine = create_engine(sync_url)
        self.db = SQLDatabase(self.engine)

    def list_tables(self) -> list[str]:
        """List all usable tables in the Northwind database."""
        return self.db.get_usable_table_names()

    def get_schema(self, table_names: list[str]) -> str:
        """Get DDL schema for specific tables."""
        return self.db.get_table_info(table_names)

    def run_query(self, query: str) -> str:
        """Execute a safe SQL query."""
        if not validate_sql(query):
            return "Error: Query blocked by safety policy. Only SELECT statements are allowed."

        try:
            return self.db.run(query)
        except Exception as e:
            logger.error("Query execution failed: %s", e)
            return f"Error executing query: {e}"
