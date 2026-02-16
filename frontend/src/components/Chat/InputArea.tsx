import React, { useRef, useEffect } from 'react';
import { Send, Paperclip, Loader2 } from 'lucide-react';
import { cn } from '../../lib/utils';

interface InputAreaProps {
    onSend: (message: string) => void;
    isLoading: boolean;
    disabled?: boolean;
}

export function InputArea({ onSend, isLoading, disabled }: InputAreaProps) {
    const [input, setInput] = React.useState('');
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const handleSubmit = (e?: React.FormEvent) => {
        e?.preventDefault();
        if (!input.trim() || isLoading || disabled) return;
        onSend(input);
        setInput('');
        // Reset height
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    // Auto-resize textarea
    const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setInput(e.target.value);
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
        }
    };

    return (
        <div className="p-4 border-t border-gray-200 bg-white">
            <form onSubmit={handleSubmit} className="relative flex items-end gap-2 max-w-4xl mx-auto">
                <button
                    type="button"
                    className="p-2 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-100 transition-colors"
                    title="Attach file (coming soon)"
                    disabled
                >
                    <Paperclip size={20} />
                </button>

                <div className="flex-1 relative">
                    <textarea
                        ref={textareaRef}
                        value={input}
                        onChange={handleInput}
                        onKeyDown={handleKeyDown}
                        placeholder="Ask anything..."
                        className="w-full p-3 pr-12 bg-gray-50 border border-gray-200 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none max-h-[200px] overflow-y-auto"
                        rows={1}
                        disabled={isLoading || disabled}
                    />
                    <div className="absolute right-2 bottom-2">
                        <button
                            type="submit"
                            disabled={!input.trim() || isLoading || disabled}
                            className={cn(
                                "p-1.5 rounded-full transition-all duration-200",
                                input.trim()
                                    ? "bg-blue-600 text-white hover:bg-blue-700 shadow-md"
                                    : "bg-gray-200 text-gray-400 cursor-not-allowed"
                            )}
                        >
                            {isLoading ? <Loader2 size={18} className="animate-spin" /> : <Send size={18} />}
                        </button>
                    </div>
                </div>
            </form>
            <div className="text-center mt-2 text-xs text-gray-400">
                AI can make mistakes. Check important info.
            </div>
        </div>
    );
}
