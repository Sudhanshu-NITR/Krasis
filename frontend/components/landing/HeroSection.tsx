'use client';
import BackgroundGrid from '@/components/shared/BackgroundGrid'
import { SignedOut, SignUpButton } from '@clerk/nextjs';
import { ArrowRight, Terminal } from 'lucide-react'
import Link from 'next/link';

export default function HeroSection() {
    return (
        <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 px-6">
            <BackgroundGrid />

            {/* Animated Glows */}
            <div className="absolute top-20 left-1/2 -translate-x-1/2 w-125 h-125 bg-indigo-500/20 rounded-full blur-[120px] pointer-events-none animate-pulse"></div>
            <div className="absolute top-40 left-1/4 w-75 h-75 bg-purple-500/10 rounded-full blur-[100px] pointer-events-none"></div>

            <div className="max-w-5xl mx-auto text-center relative z-10">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-xs font-medium text-indigo-300 mb-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                    <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
                    </span>
                    Krasis: perfect blend of Keyword Precision and Semantic Intent
                </div>

                <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6 bg-clip-text text-transparent bg-linear-to-b from-white via-white to-zinc-500 animate-in fade-in slide-in-from-bottom-6 duration-700">
                    The <span className="text-indigo-400">Hybrid Search</span> Platform <br /> for Developer Documentations.
                </h1>

                <p className="text-lg md:text-xl text-zinc-400 mb-10 max-w-2xl mx-auto leading-relaxed animate-in fade-in slide-in-from-bottom-8 duration-700 delay-100">
                    Hybrid search that understands intent. Krasis blends keyword accuracy with vector intelligence to deliver the right snippet, the first time. Built for platform engineering.
                </p>

                <div className="flex flex-col md:flex-row items-center justify-center gap-4 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200">
                    <SignedOut>
                        <SignUpButton>
                            <button className="w-full md:w-auto px-8 py-3.5 rounded-full bg-white text-black font-semibold hover:bg-zinc-200 transition-all flex items-center justify-center gap-2 group cursor-pointer">
                                Start Building
                                <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
                            </button>
                        </SignUpButton>
                    </SignedOut>
                    <Link href="#architecture">
                        <button className="w-full md:w-auto px-8 py-3.5 rounded-full bg-zinc-900 border border-zinc-800 text-zinc-300 font-medium hover:bg-zinc-800 transition-all flex items-center justify-center gap-2 cursor-pointer">
                            <Terminal size={16} className="text-zinc-500" />
                            View Architecture
                        </button>
                    </Link>
                </div>
            </div>
        </section>
    )
}
