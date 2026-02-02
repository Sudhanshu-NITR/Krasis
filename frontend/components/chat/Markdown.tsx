import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import remarkGfm from 'remark-gfm';
import remarkBreaks from 'remark-breaks';
import { Copy, Check } from 'lucide-react';

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
        <div className="relative group my-5 rounded-xl overflow-hidden border border-white/10 bg-[#0e0e10]/80 backdrop-blur-sm shadow-md ring-1 ring-white/5 transition-all hover:ring-white/10">
            <div className="flex items-center justify-between px-4 py-2 bg-white/[0.03] border-b border-white/5">
                <span className="text-[10px] uppercase font-bold tracking-wider text-zinc-500 select-none">
                    {language || 'text'}
                </span>
                <button
                    onClick={handleCopy}
                    className="flex items-center gap-1.5 text-[10px] font-medium text-zinc-500 hover:text-zinc-200 transition-colors p-1.5 rounded hover:bg-white/5"
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
            <div className="overflow-x-auto custom-scrollbar">
                <SyntaxHighlighter
                    language={language}
                    style={vscDarkPlus}
                    customStyle={{
                        margin: 0,
                        padding: '1.25rem',
                        background: 'transparent',
                        fontSize: '13px',
                        lineHeight: '1.6',
                    }}
                    codeTagProps={{
                        style: {
                            fontFamily: 'var(--font-mono)',
                            fontSize: '13px',
                        },
                    }}
                >
                    {code}
                </SyntaxHighlighter>
            </div>
        </div>
    );
};

export const LightweightMarkdown = ({ content }: { content: string }) => {
    return (
        <div className="markdown-content text-zinc-300 leading-relaxed text-[15px]">
            <ReactMarkdown
                remarkPlugins={[remarkGfm, remarkBreaks]}
                components={{
                    h1: ({ children }) => (
                        <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-zinc-400 mt-8 mb-4 border-b border-white/5 pb-3">
                            {children}
                        </h1>
                    ),
                    h2: ({ children }) => (
                        <h2 className="text-xl font-bold text-zinc-100 mt-6 mb-3 flex items-center gap-2">
                            <div className="w-1 h-5 rounded-full bg-indigo-500/80"></div>
                            {children}
                        </h2>
                    ),
                    h3: ({ children }) => (
                        <h3 className="text-lg font-bold text-zinc-100 mt-5 mb-2">{children}</h3>
                    ),
                    h4: ({ children }) => (
                        <h4 className="text-base font-bold text-zinc-100 mt-4 mb-2">{children}</h4>
                    ),
                    p: ({ children }) => <p className="mb-4 last:mb-0">{children}</p>,
                    ul: ({ children }) => (
                        <ul className="list-disc list-outside ml-6 mb-4 space-y-1.5 marker:text-zinc-500">{children}</ul>
                    ),
                    ol: ({ children }) => (
                        <ol className="list-decimal list-outside ml-6 mb-4 space-y-1.5 marker:text-zinc-500">{children}</ol>
                    ),
                    li: ({ children }) => <li className="pl-1">{children}</li>,
                    a: ({ href, children }) => (
                        <a
                            href={href}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-indigo-400 hover:text-indigo-300 font-medium underline decoration-indigo-400/30 underline-offset-4 transition-colors hover:decoration-indigo-300"
                        >
                            {children}
                        </a>
                    ),
                    code: ({ className, children, ...props }) => {
                        const match = /language-(\w+)/.exec(className || '');
                        const isInline = !match; // If no language class, treat as inline

                        if (isInline) {
                            return (
                                <code
                                    className="bg-white/10 px-1.5 py-0.5 rounded-md text-zinc-200 font-mono text-[13px] border border-white/5 shadow-sm"
                                    {...props}
                                >
                                    {children}
                                </code>
                            );
                        }

                        return (
                            <CodeBlock
                                language={match![1]}
                                code={String(children).replace(/\n$/, '')}
                            />
                        );
                    },
                    blockquote: ({ children }) => (
                        <blockquote className="border-l-2 border-indigo-500/50 pl-4 py-2 my-5 text-zinc-400 italic bg-linear-to-r from-white/[0.03] to-transparent rounded-r-lg">
                            {children}
                        </blockquote>
                    ),
                    hr: () => <hr className="my-8 border-white/5" />,
                    table: ({ children }) => (
                        <div className="overflow-x-auto my-6 rounded-xl border border-white/10 shadow-lg shadow-black/20">
                            <table className="w-full text-left border-collapse">{children}</table>
                        </div>
                    ),
                    thead: ({ children }) => <thead className="bg-white/5 text-zinc-200">{children}</thead>,
                    th: ({ children }) => (
                        <th className="px-4 py-3 text-xs font-bold uppercase tracking-wider border-b border-white/10 text-zinc-400">
                            {children}
                        </th>
                    ),
                    td: ({ children }) => (
                        <td className="px-4 py-3 text-sm border-b border-white/5 bg-white/[0.01] last:border-0 hover:bg-white/5 transition-colors">
                            {children}
                        </td>
                    ),
                }}
            >
                {content}
            </ReactMarkdown>
        </div>
    );
};