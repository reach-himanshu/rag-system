import { MessageSquare, Plus, LibraryBig } from 'lucide-react';
import { cn } from '../../lib/utils';
import { ChatSession } from '../../types/chat';

interface SidebarProps {
    sessions: ChatSession[];
    currentSessionId?: string;
    onSelectSession: (id: string) => void;
    onNewChat: () => void;
    isOpen: boolean;
}

export function Sidebar({ sessions, currentSessionId, onSelectSession, onNewChat, isOpen }: SidebarProps) {
    return (
        <div className={cn(
            "fixed inset-y-0 left-0 z-50 w-64 bg-slate-900 text-slate-300 transform transition-transform duration-300 ease-in-out md:relative md:translate-x-0",
            isOpen ? "translate-x-0" : "-translate-x-full"
        )}>
            <div className="flex flex-col h-full">
                {/* Header */}
                <div className="p-4 border-b border-slate-800">
                    <h1 className="flex items-center gap-2 font-semibold text-white text-lg">
                        <LibraryBig className="text-blue-500" />
                        Ops IQ
                    </h1>
                </div>

                {/* New Chat Button */}
                <div className="p-4">
                    <button
                        onClick={onNewChat}
                        className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white py-2.5 px-4 rounded-lg transition-colors shadow-sm font-medium"
                    >
                        <Plus size={18} />
                        New Chat
                    </button>
                </div>

                {/* Session List */}
                <div className="flex-1 overflow-y-auto px-2 py-2 space-y-1">
                    <div className="px-2 py-1 text-xs font-semibold text-slate-500 uppercase tracking-wider">
                        History
                    </div>

                    {sessions.length === 0 ? (
                        <div className="text-center py-8 text-slate-600 text-sm">
                            No history yet.
                        </div>
                    ) : (
                        sessions.map((session) => (
                            <button
                                key={session.id}
                                onClick={() => onSelectSession(session.id)}
                                className={cn(
                                    "w-full text-left px-3 py-2.5 rounded-lg flex items-center gap-3 transition-colors text-sm truncate",
                                    currentSessionId === session.id
                                        ? "bg-slate-800 text-white"
                                        : "hover:bg-slate-800/50 hover:text-white"
                                )}
                            >
                                <MessageSquare size={16} />
                                <span className="truncate">{session.title || "Untitled Chat"}</span>
                            </button>
                        ))
                    )}
                </div>

                {/* Footer */}
                <div className="p-4 border-t border-slate-800 text-xs text-slate-600 text-center">
                    v1.0.0 • RAG System
                </div>
            </div>
        </div>
    );
}
