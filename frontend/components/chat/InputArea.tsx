import React, { useRef, useEffect } from 'react';
import { Send, Hash, Zap } from 'lucide-react';
import { DocMode } from '@/types/types';

interface InputAreaProps {
    input: string;
    setInput: (value: string) => void;
    onSend: () => void;
    isLoading: boolean;
    docMode: DocMode; // Needed to trigger auto-focus on mode switch
}

export const InputArea: React.FC<InputAreaProps> = ({
    input,
    setInput,
    onSend,
    isLoading,
    docMode
}) => {
    const inputRef = useRef<HTMLTextAreaElement>(null);

    // Focus input when docMode changes
    useEffect(() => {
        inputRef.current?.focus();
    }, [docMode]);

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            onSend();
        }
    };

    return (
        <div className="flex-none p-6 pt-2 z-20 bg-gradient-to-t from-black via-black/80 to-transparent pb-8">
            <div className="max-w-3xl mx-auto relative group">
                {/* Glow effect */}
                <div className="absolute -inset-0.5 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 rounded-2xl blur-lg opacity-0 group-focus-within:opacity-100 transition-opacity duration-500" />

                <div className="relative glass-panel rounded-2xl overflow-hidden shadow-2xl transition-all duration-300">
                    <textarea
                        ref={inputRef}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Ask anything..."
                        className="w-full bg-transparent text-zinc-100 placeholder:text-zinc-500 p-4 min-h-[60px] max-h-48 resize-none focus:outline-none text-[15px] leading-relaxed scrollbar-hide"
                        rows={1}
                    />
                    <div className="flex justify-between items-center px-4 pb-3 pt-1">
                        <div className="flex gap-2">
                            <button className="p-2 rounded-lg hover:bg-white/10 text-zinc-500 hover:text-indigo-400 transition-colors"><Hash size={16} /></button>
                            <button className="p-2 rounded-lg hover:bg-white/10 text-zinc-500 hover:text-purple-400 transition-colors"><Zap size={16} /></button>
                        </div>
                        <div className="flex items-center gap-4">
                            <span className="text-[10px] text-zinc-600 font-bold tracking-wider hidden md:block">CMD + ENTER</span>
                            <button
                                onClick={onSend}
                                disabled={!input.trim() || isLoading}
                                className={`p-2.5 rounded-lg transition-all duration-300 transform 
                                    ${input.trim()
                                        ? 'bg-white text-black hover:bg-zinc-200 hover:scale-105 shadow-lg shadow-white/10'
                                        : 'bg-white/5 text-zinc-600 cursor-not-allowed'}`}
                            >
                                <Send size={16} className={input.trim() ? "fill-current" : ""} />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};