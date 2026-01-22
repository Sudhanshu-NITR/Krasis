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
        <div className="flex-none p-6 pt-2 bg-linear-to-t from-[#09090b] via-[#09090b] to-transparent z-20">
            <div className="max-w-3xl mx-auto relative">
                <div className="absolute inset-0 bg-white/5 rounded-xl blur-lg transform scale-95 opacity-0 focus-within:opacity-100 transition-opacity duration-500"></div>
                <div className="relative bg-[#18181b] border border-white/10 rounded-xl shadow-2xl overflow-hidden ring-1 ring-white/5 focus-within:ring-white/20 transition-all">
                    <textarea
                        ref={inputRef}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Ask anything..."
                        className="w-full bg-transparent text-zinc-200 placeholder:text-zinc-600 p-4 min-h-14 max-h-48 resize-none focus:outline-none text-[15px] leading-relaxed scrollbar-hide"
                        rows={1}
                    />
                    <div className="flex justify-between items-center px-4 pb-3 pt-1">
                        <div className="flex gap-2">
                            <button className="p-1.5 rounded hover:bg-white/5 text-zinc-500 transition-colors"><Hash size={16} /></button>
                            <button className="p-1.5 rounded hover:bg-white/5 text-zinc-500 transition-colors"><Zap size={16} /></button>
                        </div>
                        <div className="flex items-center gap-3">
                            <span className="text-[10px] text-zinc-600 font-medium hidden md:block">CMD + ENTER</span>
                            <button
                                onClick={onSend}
                                disabled={!input.trim() || isLoading}
                                className={`p-2 rounded-lg transition-all duration-200 ${input.trim() ? 'bg-white text-black hover:bg-zinc-200' : 'bg-white/10 text-zinc-600 cursor-not-allowed'}`}
                            >
                                <Send size={16} />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};