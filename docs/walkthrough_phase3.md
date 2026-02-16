# Walkthrough: Phase 3 - RAG Query Pipeline

I have implemented the core Retrieval-Augmented Generation (RAG) pipeline, allowing the system to answer questions based on uploaded documents.

## 🏗️ Architecture Implemented

The RAG pipeline follows this flow:
1.  **User Question** → `POST /api/v1/chat`
2.  **History Lookup** → `history_service` retrieves past messages from PostgreSQL.
3.  **Context Retrieval** → `document_search` tool embeds the query (OpenAI) and searches Qdrant.
4.  **Synthesis** → `chat_service` constructs a prompt with Context + History + Question.
5.  **Generation** → `ChatOpenAI` (GPT-4o) generates the answer.
6.  **Persistence** → Answer is saved to DB with metadata (sources).

## 🧩 Key Components

### 1. Document Search Tool (`agents/tools/document_search.py`)
- Wraps Qdrant vector search.
- Embeds queries using `text-embedding-3-small`.
- Formats results into a context string: `[Document: file.pdf (Score: 0.85)] Content...`

### 2. Chat Service (`services/chat_service.py`)
- Orchestrates the entire flow using LangChain Expression Language (LCEL).
- Handles session creation/resumption.
- Saves full conversation history (User & Assistant) to PostgreSQL.

### 3. History Service (`services/history_service.py`)
- Manages `ChatSession` and `ChatMessage` DB operations.
- Uses `selectinload` for efficient relationship loading.

## ✅ Verification Results

I have verified the implementation using `pytest` unit tests.

### Unit Tests (`tests/unit/test_chat_service.py`)
- **Coverage**:
  - Full RAG flow (History + Search + LLM + Save).
  - Session creation logic (new vs. existing).
  - Async DB operations and internal mocking.
- **Result**: **Passed** (2 tests, 100% success).

```bash
$ pytest tests/unit/test_chat_service.py -v
TestProcessMessage::test_successful_rag_flow PASSED
TestProcessMessage::test_creates_new_session_if_none_provided PASSED
```

## ⏭️ Next Steps (Phase 4)
- Implement **Text-to-SQL Pipeline** to query the Northwind database.
- Combine RAG and SQL into a unified agent.
