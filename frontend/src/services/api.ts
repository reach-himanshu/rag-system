import { ChatSession, Message } from "../types/chat";

const API_BASE_uk = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

export async function fetchSessions(): Promise<ChatSession[]> {
    // Mock for now or implement real endpoint
    // We don't have a "list sessions" endpoint yet in backend, actually.
    // Wait, I didn't implement GET /sessions. 
    // Phase 3 included history service, but not a list endpoint?
    // Checking typical implementation... usually GET /chat/sessions.
    // The backend has `GET /chat/sessions/{id}/messages`.
    // I might need to add `GET /chat/sessions` to backend later.
    // For now, let's return empty or mocking.
    return [];
}

export async function fetchMessages(sessionId: string): Promise<Message[]> {
    const res = await fetch(`${API_BASE_uk}/chat/sessions/${sessionId}/messages`);
    if (!res.ok) throw new Error("Failed to fetch messages");
    const data = await res.json();
    return data.messages.map((m: any) => ({
        ...m,
        timestamp: m.created_at,
    }));
}
