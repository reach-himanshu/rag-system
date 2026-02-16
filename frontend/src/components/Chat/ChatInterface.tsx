import { useState, useEffect, useRef } from 'react';
import { Menu } from 'lucide-react';
import { Sidebar } from '../Layout/Sidebar';
import { MessageBubble } from './MessageBubble';
import { InputArea } from './InputArea';
import { useChatStream } from '../../hooks/useChatStream';
import { fetchSessions } from '../../services/api';
import { ChatSession } from '../../types/chat';

export function ChatInterface() {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [sessions, setSessions] = useState<ChatSession[]>([]);

    // Custom hook for chat logic
    const { messages, sendMessage, isLoading, streamingContent, clearChat } = useChatStream();

    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Auto-scroll to bottom
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, streamingContent]);

    // Load sessions (mock)
    useEffect(() => {
        fetchSessions().then(setSessions).catch(console.error);
    }, []);

    return (
        <div className="flex h-screen overflow-hidden bg-gray-50">
            {/* Sidebar */}
            <Sidebar
                sessions={sessions}
                isOpen={isSidebarOpen}
                onSelectSession={(id: string) => console.log("Select", id)}
                onNewChat={clearChat}
                currentSessionId={undefined}
            />

            {/* Overlay for mobile sidebar */}
            {isSidebarOpen && (
                <div
                    className="fixed inset-0 bg-black/50 z-40 md:hidden"
                    onClick={() => setIsSidebarOpen(false)}
                />
            )}

            {/* Main Content */}
            <div className="flex-1 flex flex-col h-full relative">
                {/* Mobile Header */}
                <div className="md:hidden p-4 border-b bg-white flex items-center justify-between">
                    <button onClick={() => setIsSidebarOpen(true)} className="p-2 -ml-2 text-gray-600">
                        <Menu />
                    </button>
                    <span className="font-semibold">Ops IQ</span>
                    <div className="w-8" />
                </div>

                {/* Messages Area */}
                <div className="flex-1 overflow-y-auto p-4 space-y-6">
                    {messages.length === 0 && (
                        <div className="flex flex-col items-center justify-center h-full text-center text-gray-400 space-y-4">
                            <div className="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mb-2">
                                <span className="text-3xl">👋</span>
                            </div>
                            <h2 className="text-xl font-semibold text-gray-600">Welcome to Ops IQ</h2>
                            <p className="max-w-md">
                                Ask questions about your documents, analyze data, or just chat.
                                I'll route your query to the right expert.
                            </p>
                        </div>
                    )}

                    {messages.map((msg) => (
                        <MessageBubble key={msg.id} message={msg} />
                    ))}

                    {/* Streaming Message Placeholder */}
                    {streamingContent && (
                        <MessageBubble
                            message={{
                                id: 'streaming',
                                role: 'assistant',
                                content: streamingContent,
                                timestamp: new Date().toISOString(),
                                route_decision: undefined // or derive from hook if known
                            }}
                            isStreaming
                        />
                    )}

                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <InputArea onSend={sendMessage} isLoading={isLoading} />
            </div>
        </div>
    );
}
