import Markdown from 'react-markdown';
import { Bot, User, StickyNote, Database } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Message } from '../../types/chat';

interface MessageBubbleProps {
    message: Message;
    isStreaming?: boolean;
}

export function MessageBubble({ message, isStreaming }: MessageBubbleProps) {
    const isUser = message.role === 'user';

    // Determine icon based on route (if assistant)
    const getIcon = () => {
        if (isUser) return <User size={18} />;
        const route = message.route_decision;
        if (route === 'rag') return <StickyNote size={18} />;
        if (route === 'sql') return <Database size={18} />;
        return <Bot size={18} />;
    };

    return (
        <div className={cn(
            "flex w-full gap-4 max-w-4xl mx-auto p-4",
            isUser ? "flex-row-reverse" : "flex-row"
        )}>
            {/* Avatar */}
            <div className={cn(
                "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center shadow-sm",
                isUser ? "bg-blue-600 text-white" : "bg-emerald-600 text-white"
            )}>
                {getIcon()}
            </div>

            {/* Content */}
            <div className={cn(
                "flex flex-col max-w-[80%]",
                isUser ? "items-end" : "items-start"
            )}>
                <div className={cn(
                    "rounded-2xl px-5 py-3 shadow-sm text-sm leading-relaxed",
                    isUser
                        ? "bg-blue-600 text-white rounded-tr-none"
                        : "bg-white border border-gray-100 text-gray-800 rounded-tl-none"
                )}>
                    {isUser ? (
                        <p className="whitespace-pre-wrap">{message.content}</p>
                    ) : (
                        <div className="prose prose-sm max-w-none prose-slate dark:prose-invert">
                            <Markdown>{message.content}</Markdown>
                            {isStreaming && (
                                <span className="inline-block w-2 h-4 ml-1 align-middle bg-emerald-500 animate-pulse" />
                            )}
                        </div>
                    )}
                </div>

                {/* Metadata / Timestamp */}
                <div className="mt-1 text-xs text-gray-400 px-1">
                    {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    {!isUser && message.route_decision && (
                        <span className="ml-2 capitalize opacity-75">• {message.route_decision.replace('_', ' ')}</span>
                    )}
                </div>
            </div>
        </div>
    );
}
