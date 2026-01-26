import React, { useState } from 'react';
import { Copy, Check } from 'lucide-react';

// --- Sub-component for Code Blocks ---
interface CodeBlockProps {
    language: string;
    code: string;
}

const CodeBlock: React.FC<CodeBlockProps> = ({ language, code }) => {
    const [isCopied, setIsCopied] = useState(false);

    const handleCopy = async () => {
        await navigator.clipboard.writeText(code);
        setIsCopied(true);
        setTimeout(() => setIsCopied(false), 2000);
    };

    return (
        <div className="relative group my-4 rounded-lg overflow-hidden border border-white/10 bg-[#0e0e10] shadow-sm">
            <div className="flex items-center justify-between px-3 py-2 bg-white/[0.03] border-b border-white/5">
                <span className="text-[10px] uppercase font-bold tracking-wider text-zinc-500 select-none">
                    {language || 'CODE'}
                </span>
                <button
                    onClick={handleCopy}
                    className="flex items-center gap-1.5 text-[10px] font-medium text-zinc-500 hover:text-zinc-200 transition-colors"
                >
                    {isCopied ? (
                        <>
                            <Check size={12} className="text-emerald-400" />
                            <span className="text-emerald-400">Copied</span>
                        </>
                    ) : (
                        <>
                            <Copy size={12} />
                            <span>Copy</span>
                        </>
                    )}
                </button>
            </div>
            <div className="p-4 overflow-x-auto custom-scrollbar">
                <pre className="font-mono text-[13px] leading-relaxed text-zinc-300 whitespace-pre font-normal">
                    {code}
                </pre>
            </div>
        </div>
    );
};

// --- Main Markdown Parser ---
export const LightweightMarkdown = ({ content }: { content: string }) => {
    const parts = content.split(/```(\w*)\n([\s\S]*?)```/g);

    return (
        <div className="space-y-2 text-zinc-300 leading-relaxed text-[15px]">
            {parts.map((part, index) => {
                if (index % 3 === 1) return null; // Skip language capture group

                if (index % 3 === 2) {
                    const language = parts[index - 1];
                    return <CodeBlock key={index} language={language} code={part.trim()} />;
                }

                if (!part.trim()) return null;

                return (
                    <div key={index} dangerouslySetInnerHTML={{
                        __html: part
                            // 1. Headers - (Note: I reduced mt-8 to mt-6 for tighter spacing)
                            .replace(/^## (.*$)/gm, '<h2 class="text-xl font-bold text-zinc-100 mt-6 mb-3 border-b border-white/5 pb-2">$1</h2>')
                            .replace(/^### (.*$)/gm, '<h3 class="text-lg font-bold text-zinc-100 mt-4 mb-2">$1</h3>')
                            .replace(/^#### (.*$)/gm, '<h4 class="text-base font-bold text-zinc-100 mt-4 mb-2">$1</h4>')

                            // 2. CRITICAL FIX: Eat newlines surrounding the headers
                            // This prevents <br/> tags from being generated next to headers
                            .replace(/\n+(<h[2-4])/g, '$1')  // Removes newlines BEFORE headers
                            .replace(/(<\/h[2-4]>)\n+/g, '$1') // Removes newlines AFTER headers

                            // 3. Inline Styles
                            .replace(/\*\*(.*?)\*\*/g, '<strong class="text-zinc-100 font-semibold">$1</strong>')
                            .replace(/`([^`]+)`/g, '<code class="bg-white/10 px-1.5 py-0.5 rounded-md text-zinc-200 font-mono text-[13px] border border-white/5">$1</code>')
                            .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" class="text-indigo-400 hover:text-indigo-300 underline decoration-indigo-400/30 underline-offset-4 transition-colors">$1</a>')

                            // 4. Convert remaining newlines to breaks
                            .replace(/\n/g, '<br/>')
                    }} />
                );
            })}
        </div>
    );
};