"""SQL safety utilities."""

import logging

import sqlparse

logger = logging.getLogger(__name__)


def validate_sql(query: str) -> bool:
    """Validate that a SQL query is safe to execute (read-only).

    Checks:
    1. Only one statement.
    2. Statement type is SELECT.
    3. No system table access (pg_).

    Args:
        query: The SQL query string.

    Returns:
        True if safe, False otherwise.
    """
    try:
        parsed = sqlparse.parse(query)
        if not parsed:
            return False

        # 1. Only one statement allowed
        if len(parsed) > 1:
            logger.warning("SQL Safety: Multiple statements detected")
            return False

        statement = parsed[0]

        # 2. Must be a SELECT statement
        if statement.get_type().upper() != "SELECT":
            logger.warning("SQL Safety: Non-SELECT statement detected: %s", statement.get_type())
            return False

        # 3. No system table access or obvious modification keywords
        # Convert to token list to inspect identifiers
        # This is a basic check; robust RAG usually relies on DB role permissions too.
        query_upper = query.upper()
        forbidden_keywords = [
            "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE",
            "GRANT", "REVOKE", "CREATE", "REPLACE",
            "PG_", "INFORMATION_SCHEMA"
        ]

        for keyword in forbidden_keywords:
            if keyword in query_upper:
                # Check if it's a false positive (e.g. "update" inside a string literal)
                # For now, we'll be strict.
                logger.warning("SQL Safety: Forbidden keyword detected: %s", keyword)
                return False

        return True

    except Exception as e:
        logger.error("SQL Safety Check Failed: %s", e)
        return False
