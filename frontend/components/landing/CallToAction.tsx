'use client';
import { CheckCircle2 } from 'lucide-react'

export default function CallToAction() {
    return (
        <section className="py-32 px-6 text-center relative overflow-hidden">
            <div className="absolute inset-0 bg-indigo-600/5"></div>
            <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-150 h-100 bg-indigo-500/20 blur-[120px] rounded-full pointer-events-none"></div>

            <div className="max-w-3xl mx-auto relative z-10">
                <h2 className="text-4xl md:text-5xl font-bold mb-6 tracking-tight">Search that speaks Developer.</h2>
                <p className="text-xl text-zinc-400 mb-10">
                    Ingest your Stripe, LangChain, or Notion docs today.
                </p>
                <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                    <button className="w-full sm:w-auto px-8 py-4 rounded-full bg-white text-black font-bold text-lg hover:bg-zinc-200 transition-colors shadow-[0_0_20px_rgba(255,255,255,0.3)]">
                        Deploy Instance
                    </button>
                    <button className="w-full sm:w-auto px-8 py-4 rounded-full bg-black border border-zinc-800 text-white font-medium hover:bg-zinc-900 transition-colors">
                        Read the Whitepaper
                    </button>
                </div>
                <div className="mt-8 flex items-center justify-center gap-6 text-sm text-zinc-500">
                    <span className="flex items-center gap-2"><CheckCircle2 size={16} className="text-green-500" /> Open Source Core</span>
                    <span className="flex items-center gap-2"><CheckCircle2 size={16} className="text-green-500" /> Self-Hostable</span>
                </div>
            </div>
        </section>

    )
}
