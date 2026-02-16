export interface Message {
    id: string;
    role: "user" | "assistant";
    content: string;
    timestamp: string;
    route_decision?: "rag" | "sql" | "general_chat";
    metadata?: Record<string, any>;
}

export interface ChatSession {
    id: string;
    title: string;
    created_at: string;
}

export interface ChatState {
    messages: Message[];
    isLoading: boolean;
    streamingContent: string;
    error: string | null;
}
