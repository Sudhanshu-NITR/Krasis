import React, { useEffect, useRef } from 'react';
import { Bot, ArrowRight, Sparkles, BookOpen } from 'lucide-react';
import { Message, ModeConfig } from '@/types/types';
import { LightweightMarkdown } from './Markdown';

interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
  activeMode: ModeConfig;
  onSuggestionClick: (text: string) => void;
}

export const MessageList: React.FC<MessageListProps> = ({
  messages,
  isLoading,
  activeMode,
  onSuggestionClick
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll logic
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto p-4 md:p-8 custom-scrollbar scroll-smooth">
      <div className="max-w-3xl mx-auto space-y-8 pb-4">

        {/* Empty State */}
        {messages.length === 0 && (
          <div className="mt-16 text-center animate-in fade-in slide-in-from-bottom-5 duration-700">
            <div className="inline-flex items-center justify-center p-6 rounded-3xl bg-white/[0.03] border border-white/5 mb-8 shadow-2xl relative overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <activeMode.icon size={56} className={`${activeMode.color} relative z-10 drop-shadow-md`} />
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-white mb-4 bg-clip-text text-transparent bg-gradient-to-b from-white to-white/60">
              How can I help with {activeMode.name}?
            </h1>
            <p className="text-zinc-400 max-w-lg mx-auto mb-10 text-base leading-relaxed">
              {activeMode.description}. I have indexed the documentation version <span className="font-mono text-zinc-300 bg-white/10 px-1.5 py-0.5 rounded text-xs border border-white/5">{activeMode.context.version}</span>.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
              {activeMode.suggestions.map((text, i) => (
                <button
                  key={i}
                  onClick={() => onSuggestionClick(text)}
                  className="group flex items-center justify-between p-4 rounded-xl border border-white/5 bg-white/[0.02] hover:bg-white/5 hover:border-white/10 transition-all text-left shadow-lg shadow-black/20"
                >
                  <span className="text-sm text-zinc-300 group-hover:text-white transition-colors">{text}</span>
                  <ArrowRight size={14} className="text-zinc-600 group-hover:text-zinc-300 transform group-hover:translate-x-1 transition-all" />
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Message List */}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`group flex gap-4 md:gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500 ${msg.role === 'user' ? 'justify-end' : ''}`}
          >
            {msg.role === 'assistant' && (
              <div className="flex-none w-9 h-9 rounded-xl bg-white/[0.03] border border-white/5 flex items-center justify-center mt-1 shadow-md">
                <Bot size={18} className={activeMode.color} />
              </div>
            )}

            <div className={`flex flex-col max-w-[85%] md:max-w-2xl ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div
                className={`relative px-6 py-4 rounded-2xl text-sm md:text-[15px] leading-7 shadow-lg
                ${msg.role === 'user'
                    ? 'bg-gradient-to-br from-indigo-600 to-indigo-700 text-white font-medium rounded-tr-sm shadow-indigo-500/10'
                    : 'glass-panel text-zinc-100 rounded-tl-sm min-h-[3rem]'}`}
              >
                {msg.role === 'user' ? (
                  msg.content
                ) : (
                  <LightweightMarkdown content={msg.content} />
                )}
              </div>

              {/* Source Chips */}
              {msg.role === 'assistant' && msg.sources && msg.sources.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-2 pl-1 animate-in fade-in duration-500 delay-150">
                  {msg.sources.map((s, i) => (
                    <a
                      key={i}
                      href={s.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/5 border border-white/5 hover:bg-white/10 hover:border-white/20 text-xs text-zinc-400 hover:text-zinc-100 transition-all cursor-pointer group/chip"
                    >
                      <BookOpen size={12} className="text-indigo-400 group-hover/chip:text-indigo-300" />
                      <span className="truncate max-w-[200px]">{s.title}</span>
                    </a>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {/* Loading Spinner */}
        {isLoading && (
          <div className="flex gap-4 md:gap-6 animate-in fade-in duration-300 ml-1">
            <div className="flex-none w-9 h-9 rounded-xl bg-white/[0.03] border border-white/5 flex items-center justify-center mt-1">
              <Sparkles size={16} className="animate-spin text-zinc-500" />
            </div>
            <div className="flex flex-col gap-2 pt-2">
              <div className="flex gap-1.5">
                <span className="w-2 h-2 bg-zinc-600/80 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                <span className="w-2 h-2 bg-zinc-600/80 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                <span className="w-2 h-2 bg-zinc-600/80 rounded-full animate-bounce"></span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} className="h-4" />
      </div>
    </div>
  );
};