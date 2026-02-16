# Walkthrough: Phase 4 - Text-to-SQL Pipeline

I have implemented the Text-to-SQL capability, allowing the system to safely query the Northwind database using natural language.

## 🏗️ Architecture Implemented

The pipeline flow (`sql_service.py`):
1.  **Request** → `POST /api/v1/chat` with `mode="sql"`.
2.  **Schema Retrieval** → `sql_db.py` lists available tables and fetches DDL.
3.  **Generation** → `text_to_sql.py` prompt + GPT-4o generates a Postgres query.
4.  **Safety Check** → `sql_safety.py` validates using `sqlparse` (SELECT-only, no semicolons).
5.  **Execution** → Query runs against Northwind DB.
6.  **Response** → Result is returned and saved to chat history.

## 🛡️ SQL Safety

I implemented a strict read-only policy using `sqlparse`.

- **Allowed**: `SELECT` statements.
- **Blocked**: `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`, `GRANT`, etc.
- **Blocked**: Multiple statements (`;`).
- **Blocked**: System tables (`pg_`, `information_schema`).

## ✅ Verification Results

I verified the safety module with unit tests.

### Unit Tests (`tests/unit/test_sql_safety.py`)
- **Coverage**:
  - Safe SELECTs pass.
  - Destructive commands (DELETE, DROP) are blocked.
  - Multi-statement injections are blocked.
  - System table access is blocked.
- **Result**: **Passed** (5 tests).

```bash
$ pytest tests/unit/test_sql_safety.py -v
TestValidateSql::test_safe_select PASSED
TestValidateSql::test_block_multiple_statements PASSED
TestValidateSql::test_block_modification_keywords PASSED
TestValidateSql::test_block_system_tables PASSED
TestValidateSql::test_block_complex_unsafe_patterns PASSED
```

## ⏭️ Next Steps (Phase 5)
- Implement **LangGraph Router Agent**.
- Dynamically route questions to RAG (docs) or SQL (data) based on intent.
- Implement SSE streaming for better UX.
