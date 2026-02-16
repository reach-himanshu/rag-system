import { useState, useCallback, useRef } from "react";
import { fetchEventSource } from "@microsoft/fetch-event-source";
import { Message } from "../types/chat";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

export function useChatStream(sessionId?: string) {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [streamingContent, setStreamingContent] = useState("");
    const [currentSessionId, setCurrentSessionId] = useState<string | undefined>(sessionId);

    // Use refs for values needed inside closures without dependency re-creation
    const streamingContentRef = useRef("");
    const routeDecisionRef = useRef<string | undefined>(undefined);
    const abortControllerRef = useRef<AbortController | null>(null);

    const sendMessage = useCallback(
        async (content: string, mode: "auto" | "rag" | "sql" = "auto") => {
            setIsLoading(true);
            setStreamingContent("");
            streamingContentRef.current = "";
            routeDecisionRef.current = undefined;

            // Optimistic User Message
            const tempUserMsg: Message = {
                id: Date.now().toString(),
                role: "user",
                content,
                timestamp: new Date().toISOString(),
            };
            setMessages((prev) => [...prev, tempUserMsg]);

            // Abort previous request if any
            if (abortControllerRef.current) {
                abortControllerRef.current.abort();
            }
            abortControllerRef.current = new AbortController();

            const API_KEY = import.meta.env.VITE_API_KEY || "rag-demo-api-key-change-me";

            try {
                await fetchEventSource(`${API_BASE}/chat`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-API-Key": API_KEY,
                    },
                    body: JSON.stringify({
                        session_id: currentSessionId, // Use ref if this changes dynamically? For now state is OK.
                        message: content,
                        mode,
                        stream: true,
                    }),
                    signal: abortControllerRef.current.signal,

                    async onopen(response) {
                        if (response.ok) return;
                        throw new Error(`Failed to send message: ${response.statusText}`);
                    },

                    onmessage(msg) {
                        try {
                            // Parse our JSON event data
                            const payload = JSON.parse(msg.data);

                            if (payload.type === "token") {
                                streamingContentRef.current += payload.content;
                                setStreamingContent(streamingContentRef.current);
                            } else if (payload.type === "metadata") {
                                // Capture route decision
                                if (payload.metadata && payload.metadata.route) {
                                    routeDecisionRef.current = payload.metadata.route;
                                }
                            } else if (payload.type === "done") {
                                // Done event received
                            }
                        } catch (e) {
                            console.error("Error parsing SSE message:", e);
                        }
                    },

                    onclose() {
                        // Connection closed logic
                    },

                    onerror(err) {
                        console.error("Stream error:", err);
                        throw err; // Stop retrying
                    }
                });

            } catch (err) {
                console.error("Chat Stream Error:", err);
            } finally {
                setIsLoading(false);

                // Commit the final assistant message
                if (streamingContentRef.current) {
                    const assistantMsg: Message = {
                        id: Date.now().toString(),
                        role: "assistant", // "assistant"
                        content: streamingContentRef.current,
                        timestamp: new Date().toISOString(),
                        route_decision: routeDecisionRef.current,
                    };
                    setMessages((prev) => [...prev, assistantMsg]);
                }

                setStreamingContent("");
                streamingContentRef.current = "";
            }
        },
        [currentSessionId]
    );

    const clearChat = useCallback(() => {
        setMessages([]);
        setCurrentSessionId(undefined); // Or create new UUID
    }, []);

    return {
        messages,
        sendMessage,
        isLoading,
        streamingContent,
        clearChat
    };
}
