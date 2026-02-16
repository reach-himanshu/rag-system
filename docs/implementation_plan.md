# Phase 6: React Frontend

Implement a modern, responsive chat interface using React, Vite, and Tailwind CSS.

## Proposed Changes

### Project Structure (Frontend)

Initialize `frontend/` directory with Vite + React + TypeScript.
```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm install lucide-react clsx tailwind-merge framer-motion react-markdown
```

### Components

#### [NEW] [frontend/src/components/chat/ChatInterface.tsx](file:///c:/Users/nigam/Projects/RAG_System/frontend/src/components/chat/ChatInterface.tsx)
- Main container.
- Layout: Sidebar (History) + Main Chat Area.

#### [NEW] [frontend/src/components/chat/MessageBubble.tsx](file:///c:/Users/nigam/Projects/RAG_System/frontend/src/components/chat/MessageBubble.tsx)
- Renders user/assistant messages.
- Supports Markdown rendering (for RAG/SQL answers).
- Shows metadata (sources/SQL query) in a collapsible details view.

#### [NEW] [frontend/src/components/chat/InputArea.tsx](file:///c:/Users/nigam/Projects/RAG_System/frontend/src/components/chat/InputArea.tsx)
- Text input with auto-resize.
- File upload button (paperclip).
- Send button.

#### [NEW] [frontend/src/components/layout/Sidebar.tsx](file:///c:/Users/nigam/Projects/RAG_System/frontend/src/components/layout/Sidebar.tsx)
- List of recent chat sessions.
- "New Chat" button.

### State & Logic

#### [NEW] [frontend/src/hooks/useChatStream.ts](file:///c:/Users/nigam/Projects/RAG_System/frontend/src/hooks/useChatStream.ts)
- Manages SSE connection using `fetch-event-source` (or native `EventSource`).
- State: `messages`, `isLoading`, `streamingContent`.
- Handles `metadata` events to update message sources.

#### [NEW] [frontend/src/services/api.ts](file:///c:/Users/nigam/Projects/RAG_System/frontend/src/services/api.ts)
- `sendMessage(message, sessionId, mode)`
- `getHistory(sessionId)`
- `uploadFile(file)`

### Styling
- **Tailwind Config**: Extend colors for a premium feel (slate/zinc, blue/indigo accents).
- **Dark Mode**: Support system preference or toggle.

## Verification Plan

### Manual Verification
1. **Start Backend**: `cd backend && python -m uvicorn app.main:app --reload`.
2. **Start Frontend**: `cd frontend && npm run dev`.
3. **Test Flows**:
   - Send "Hello" -> Verify General Chat response.
   - Send "Summarize report" -> Verify RAG response + References.
   - Send "Count customers" -> Verify SQL query display + Result.
   - Verify Streaming (text appears token by token).
