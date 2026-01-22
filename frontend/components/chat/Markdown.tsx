'use client';
import { Command } from 'lucide-react';

export const LightweightMarkdown = ({ content }: { content: string }) => {
    const parts = content.split(/(```[\s\S]*?```)/g);
    return (
        <div className="space-y-4 text-zinc-300 leading-relaxed text-sm">
            {parts.map((part, index) => {
                if (part.startsWith('```')) {
                    const lines = part.split('\n');
                    const lang = lines[0].replace('```', '');
                    const code = lines.slice(1, -1).join('\n');
                    return (
                        <div key={index} className="relative group my-4 rounded-md overflow-hidden border border-white/5 bg-[#09090b] shadow-lg">
                            <div className="flex items-center justify-between px-3 py-2 bg-white/5 border-b border-white/5">
                                <span className="text-[10px] uppercase font-bold tracking-wider text-zinc-500">{lang || 'CODE'}</span>
                                <button
                                    onClick={() => navigator.clipboard.writeText(code)}
                                    className="text-xs text-zinc-500 hover:text-white transition-colors flex items-center gap-1"
                                >
                                    <Command size={10} /> Copy
                                </button>
                            </div>
                            <div className="p-4 overflow-x-auto custom-scrollbar">
                                <pre className="font-mono text-[13px] text-zinc-300 whitespace-pre">{code}</pre>
                            </div>
                        </div>
                    );
                }
                return (
                    <p key={index} dangerouslySetInnerHTML={{
                        __html: part
                            .replace(/\*\*(.*?)\*\*/g, '<strong class="text-white font-medium">$1</strong>')
                            .replace(/`([^`]+)`/g, '<code class="bg-white/10 px-1.5 py-0.5 rounded text-zinc-200 font-mono text-[12px]">$1</code>')
                            .replace(/\n/g, '<br/>')
                    }} />
                );
            })}
        </div>
    );
};