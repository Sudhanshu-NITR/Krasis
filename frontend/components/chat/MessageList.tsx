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

  // Auto-scroll logic: scrolls whenever messages array changes or loading state changes
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto p-4 md:p-8 custom-scrollbar scroll-smooth">
      <div className="max-w-3xl mx-auto space-y-8 pb-4">

        {/* Empty State */}
        {messages.length === 0 && (
          <div className="mt-12 text-center animate-in fade-in slide-in-from-bottom-5 duration-700">
            <div className="inline-flex items-center justify-center p-4 rounded-2xl bg-white/5 border border-white/5 mb-8 shadow-2xl">
              <activeMode.icon size={48} className={activeMode.color} />
            </div>
            <h1 className="text-3xl font-bold tracking-tight text-white mb-3">
              How can I help with {activeMode.name}?
            </h1>
            <p className="text-zinc-400 max-w-lg mx-auto mb-10 text-base leading-relaxed">
              {activeMode.description}. I have indexed the documentation version <span className="font-mono text-zinc-300 bg-white/5 px-1 py-0.5 rounded text-xs">{activeMode.context.version}</span>.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
              {activeMode.suggestions.map((text, i) => (
                <button
                  key={i}
                  onClick={() => onSuggestionClick(text)}
                  className="group flex items-center justify-between p-4 rounded-xl border border-white/5 bg-white/2 hover:bg-white/5 hover:border-white/10 transition-all text-left"
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
            className={`group flex gap-4 md:gap-6 animate-in fade-in slide-in-from-bottom-2 duration-500 ${msg.role === 'user' ? 'justify-end' : ''}`}
          >
            {msg.role === 'assistant' && (
              <div className="flex-none w-8 h-8 rounded bg-white/5 border border-white/5 flex items-center justify-center mt-1">
                <Bot size={16} className={activeMode.color} />
              </div>
            )}

            <div className={`flex flex-col max-w-[85%] md:max-w-2xl ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div
                className={`relative px-5 py-3.5 rounded-2xl text-sm md:text-[15px] leading-7 shadow-sm overflow-hidden
                ${msg.role === 'user'
                    ? 'bg-white text-zinc-900 font-medium rounded-tr-sm'
                    : 'bg-zinc-900/50 border border-white/5 text-zinc-100 rounded-tl-sm min-h-[3rem]'}`}
              >
                {msg.role === 'user' ? (
                  msg.content
                ) : (
                  // Pass the streaming content to Markdown renderer
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
                      className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md bg-white/5 border border-white/5 hover:bg-white/10 hover:border-white/20 text-xs text-zinc-400 hover:text-zinc-100 transition-all"
                    >
                      <BookOpen size={12} />
                      <span className="truncate max-w-[200px]">{s.title}</span>
                    </a>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {/* Loading Spinner (Only shows when connecting, disappears when streaming starts) */}
        {isLoading && (
          <div className="flex gap-4 md:gap-6 animate-in fade-in duration-300">
            <div className="flex-none w-8 h-8 rounded bg-white/5 border border-white/5 flex items-center justify-center mt-1">
              <Sparkles size={14} className="animate-spin text-zinc-500" />
            </div>
            <div className="flex flex-col gap-2 pt-2">
              <div className="flex gap-1">
                <span className="w-1.5 h-1.5 bg-zinc-600 rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                <span className="w-1.5 h-1.5 bg-zinc-600 rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                <span className="w-1.5 h-1.5 bg-zinc-600 rounded-full animate-bounce"></span>
              </div>
              <span className="text-xs text-zinc-500 font-medium">Reading docs...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} className="h-4" />
      </div>
    </div>
  );
};