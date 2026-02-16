"""Unit tests for SQL safety."""


from app.core.sql_safety import validate_sql


class TestValidateSql:
    """Tests for the validate_sql function."""

    def test_safe_select(self):
        """Should allow simple SELECT statements."""
        assert validate_sql("SELECT * FROM customers")
        assert validate_sql("SELECT count(*) FROM orders WHERE id = 5")
        assert validate_sql("select name from products")

    def test_block_multiple_statements(self):
        """Should block queries with multiple statements."""
        assert not validate_sql("SELECT * FROM customers; DROP TABLE orders")
        assert not validate_sql("SELECT 1; SELECT 2")

    def test_block_modification_keywords(self):
        """Should block INSERT, UPDATE, DELETE, DROP."""
        assert not validate_sql("DELETE FROM customers")
        assert not validate_sql("DROP TABLE orders")
        assert not validate_sql("UPDATE products SET price = 0")
        assert not validate_sql("INSERT INTO users VALUES (1)")
        assert not validate_sql("TRUNCATE TABLE logs")
        assert not validate_sql("ALTER TABLE users ADD column x")

    def test_block_system_tables(self):
        """Should block access to system tables (pg_)."""
        assert not validate_sql("SELECT * FROM pg_tables")
        assert not validate_sql("SELECT * FROM information_schema.tables")

    def test_block_complex_unsafe_patterns(self):
        """Should block attempts to obfuscate commands."""
        # Note: Generic sqlparse might not catch everything, but these checks cover basic hygiene
        assert not validate_sql("   DELETE   FROM   customers   ")
