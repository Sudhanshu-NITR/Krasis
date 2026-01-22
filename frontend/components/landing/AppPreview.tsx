'use client';
import { Cpu, Layers } from 'lucide-react';
import { useState } from 'react'

export default function AppPreview() {
    const [isHoveringDemo, setIsHoveringDemo] = useState(false);
    return (
        <section className="relative px-6 pb-24 overflow-hidden">
            <div
                className="max-w-6xl mx-auto transition-transform duration-700 ease-out transform hover:scale-[1.01]"
                onMouseEnter={() => setIsHoveringDemo(true)}
                onMouseLeave={() => setIsHoveringDemo(false)}
            >
                <div className="relative rounded-xl bg-[#09090b] border border-white/10 shadow-2xl overflow-hidden aspect-16/10 md:aspect-2/1 group">
                    {/* Header Mockup */}
                    <div className="absolute top-0 left-0 right-0 h-10 bg-white/5 border-b border-white/5 flex items-center px-4 gap-2 z-20">
                        <div className="flex gap-1.5">
                            <div className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/50"></div>
                            <div className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/50"></div>
                            <div className="w-3 h-3 rounded-full bg-green-500/20 border border-green-500/50"></div>
                        </div>
                        <div className="flex-1 text-center">
                            <div className="inline-block px-3 py-0.5 rounded bg-black/40 border border-white/5 text-[10px] text-zinc-500 font-mono">krasis-platform.internal</div>
                        </div>
                    </div>

                    {/* Inner App Content Mockup */}
                    <div className="absolute inset-0 pt-10 flex">
                        {/* Sidebar Mockup */}
                        <div className="w-64 border-r border-white/5 bg-zinc-900/30 hidden md:block p-4 space-y-4">
                            <div className="h-4 w-24 bg-white/10 rounded animate-pulse"></div>
                            <div className="space-y-2 pt-4">
                                <div className="text-[10px] font-bold text-zinc-600 uppercase tracking-wider mb-2">Data Sources</div>
                                <div className="flex items-center gap-2 text-zinc-400 text-xs py-1"><div className="w-2 h-2 rounded-full bg-blue-500"></div>LangChain</div>
                                <div className="flex items-center gap-2 text-zinc-400 text-xs py-1"><div className="w-2 h-2 rounded-full bg-emerald-500"></div>Stripe API</div>
                                <div className="flex items-center gap-2 text-zinc-400 text-xs py-1"><div className="w-2 h-2 rounded-full bg-white"></div>Internal Notion</div>
                            </div>
                        </div>

                        {/* Main Chat Mockup */}
                        <div className="flex-1 p-8 flex flex-col items-center justify-center relative">
                            <div className="absolute inset-0 bg-linear-to-tr from-indigo-500/5 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>

                            {/* Floating Chat Bubbles */}
                            <div className="w-full max-w-2xl space-y-6">
                                {/* User Query */}
                                <div className="flex gap-4 justify-end opacity-50 group-hover:opacity-100 transition-opacity duration-700 delay-200 transform translate-y-4 group-hover:translate-y-0">
                                    <div className="bg-indigo-600 p-4 rounded-2xl rounded-tr-sm text-sm font-medium shadow-lg shadow-indigo-500/20">
                                        How do I charge a card for a subscription?
                                    </div>
                                    <div className="w-8 h-8 rounded bg-zinc-700 border border-white/5"></div>
                                </div>

                                {/* System Thought Process (New for Technical Depth) */}
                                <div className="flex gap-4 opacity-0 group-hover:opacity-100 transition-all duration-700 delay-300 transform translate-y-4 group-hover:translate-y-0 justify-center">
                                    <div className="bg-black/40 border border-white/10 px-4 py-2 rounded-full text-[10px] text-zinc-400 font-mono flex items-center gap-2 backdrop-blur-md">
                                        <Cpu size={12} className="text-indigo-400" />
                                        <span>Reranking 12 candidates via Cross-Encoder...</span>
                                    </div>
                                </div>

                                {/* AI Response */}
                                <div className="flex gap-4 opacity-0 group-hover:opacity-100 transition-all duration-700 delay-500 transform translate-y-8 group-hover:translate-y-0">
                                    <div className="w-8 h-8 rounded bg-zinc-800 flex items-center justify-center border border-white/5">
                                        <Layers size={14} className="text-indigo-400" />
                                    </div>
                                    <div className="bg-zinc-800/50 border border-white/5 p-5 rounded-2xl rounded-tl-sm w-full shadow-xl shadow-black/50 backdrop-blur-md">
                                        <div className="mb-3 text-sm text-zinc-300 leading-relaxed">
                                            To handle subscriptions, you shouldn't just "charge a card". Instead, use the <code className="text-indigo-300 font-mono bg-white/5 px-1 rounded">PaymentIntents</code> API combined with <code className="text-indigo-300 font-mono bg-white/5 px-1 rounded">Subscription</code> objects.
                                        </div>
                                        <div className="p-3 bg-black/60 rounded border border-white/5 font-mono text-xs text-indigo-200 overflow-x-auto">
                                            stripe.paymentIntents.create({'{'} <br />
                                            &nbsp;&nbsp;amount: 2000, <br />
                                            &nbsp;&nbsp;currency: 'usd', <br />
                                            &nbsp;&nbsp;setup_future_usage: 'off_session' <br />
                                            {'}'})
                                        </div>
                                        <div className="mt-3 flex gap-2">
                                            <span className="text-[10px] px-2 py-1 rounded border border-indigo-500/30 bg-indigo-500/10 text-indigo-300">Stripe Docs v2023</span>
                                            <span className="text-[10px] px-2 py-1 rounded border border-white/10 bg-white/5 text-zinc-500">Relevance: 0.98</span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>

                    {/* Gradient Overlay for Fade Effect */}
                    <div className="absolute inset-0 bg-linear-to-t from-black via-transparent to-transparent pointer-events-none h-40 bottom-0 top-auto"></div>
                </div>
            </div>
        </section>
    )
}
