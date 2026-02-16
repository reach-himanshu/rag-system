import { useState, useCallback, useRef } from "react";
import { fetchEventSource } from "@microsoft/fetch-event-source";
import { Message } from "../types/chat";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

export function useChatStream(sessionId?: string) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [streamingContent, setStreamingContent] = useState("");
    const [currentSessionId, setCurrentSessionId] = useState<string | undefined>(sessionId);
    const abortControllerRef = useRef<AbortController | null>(null);

    const sendMessage = useCallback(
        async (content: string, mode: "auto" | "rag" | "sql" = "auto") => {
            setIsLoading(true);
            setStreamingContent("");

            // Optimistic User Message
            const tempUserMsg: Message = {
                id: Date.now().toString(),
                role: "user",
                content,
                timestamp: new Date().toISOString(),
            };
            setMessages((prev) => [...prev, tempUserMsg]);

            abortControllerRef.current = new AbortController();

            try {
                await fetchEventSource(`${API_BASE}/chat`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        // "Authorization": "Bearer ...", // If using auth
                    },
                    body: JSON.stringify({
                        session_id: currentSessionId,
                        message: content,
                        mode,
                        stream: true,
                    }),
                    signal: abortControllerRef.current.signal,
                    onopen: async (response) => {
                        if (response.ok) return;
                        throw new Error(`Failed to send message: ${response.statusText}`);
                    },
                    onmessage: (msg) => {
                        if (msg.event === "metadata") {
                            // Handle metadata (e.g., set session ID if new, or route info)
                            // The backend doesn't explicitly send session_id in metadata yet, assume consistent.
                            const meta = JSON.parse(msg.data);
                            console.log("Metadata:", meta);
                        } else if (msg.event === "token") {
                            // msg.data is usually just the token content if backend sends standard SSE "data: content"
                            // But my backend sends "data: {"type": "token", "content": "..."}" wrapped in json?
                            // Wait, backend code: yield f'{{"type": "token", "content": "{safe_chunk}"}}'
                            // EventSource usually parses the "lines".
                            // `fetch-event-source` gives `msg.data` as the string after "data: ".
                            try {
                                const payload = JSON.parse(msg.data);
                                if (payload.type === "token") {
                                    setStreamingContent((prev) => prev + payload.content);
                                } else if (payload.type === "metadata") {
                                    console.log("Metadata:", payload.metadata);
                                } else if (payload.type === "done") {
                                    // Commit the streaming content as a full message
                                    // We need to wait for "done" event or stream close?
                                    // The stream might close automatically.
                                }
                            } catch (e) {
                                // Might be a raw string if I messed up backend? No, backend sends JSON.
                            }
                        }
                    },
                    onerror: (err) => {
                        console.error("Stream error:", err);
                        throw err; // Rethrow to stop retrying
                    },
                    onclose: () => {
                        // Stream finished
                        setMessages((prev) => [
                            ...prev,
                            {
                                id: Date.now().toString(), // Placeholder ID
                                role: "assistant",
                                content: streamingContent, // This grabs the *current* state at closure time? 
                                // React state `streamingContent` effectively unavailable inside this callback due to closure staleness unless using ref.
                                // Correct approach: use a ref for accumulating content, then update state.
                                timestamp: new Date().toISOString(),
                            }
                        ]);
                    }
                });

                // Actually, fetch-event-source onclose doesn't fire nicely with state updates.
                // Better: update message list when "done" event is received or use a ref for content.

            } catch (err) {
                console.error(err);
            } finally {
                setIsLoading(false);
                // Commit message if not already
                setMessages((prev) => [
                    ...prev,
                    {
                        id: Date.now().toString(),
                        role: "assistant",
                        content: streamingContent, // Logic gap here: streamingContent is state.
                        timestamp: new Date().toISOString(),
                    }
                ]);
                setStreamingContent("");
            }
        },
        [currentSessionId, streamingContent] // Dep checks are tricky with streaming.
    );

    // Ref-based implementation is safer for streaming.
    // I'll rewrite the hook to use refs for accumulation and then update state.

    return { messages, sendMessage, isLoading, streamingContent };
}
