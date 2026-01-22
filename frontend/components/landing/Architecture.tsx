'use client';
import React from 'react'
import FeatureCard from '../shared/FeatureCard'
import { Code2, Cpu, Link, Split, Terminal, Zap } from 'lucide-react'

export default function Architecture() {
    return (
        <section id="architecture" className="py-24 px-6 max-w-7xl mx-auto relative">
            <div className="mb-16 md:text-center max-w-2xl mx-auto">
                <h2 className="text-3xl md:text-4xl font-bold mb-4">Ensemble Retrieval Architecture</h2>
                <p className="text-zinc-400">
                    Single-method search fails on technical jargon. Krasis implements a production-grade RAG pipeline designed for platform engineering teams.
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <FeatureCard
                    icon={Split}
                    title="Ensemble Retrievers"
                    description="Combines BM25 (sparse vectors) for keyword matching with Dense Vector Retrievers for concept matching. We don't miss exact function names."
                    delay="delay-0"
                />
                <FeatureCard
                    icon={Code2}
                    title="Code-Aware Splitting"
                    description="Standard text splitters break code. Our ingestion pipeline uses language-specific splitters (Python, JS, Go) to keep class structures intact."
                    delay="delay-100"
                />
                <FeatureCard
                    icon={Cpu}
                    title="RRF & Reranking"
                    description="Results are re-ordered using Reciprocal Rank Fusion and a Cross-Encoder Reranker (Cohere) to ensure the most technically relevant hit appears first."
                    delay="delay-200"
                />
                <FeatureCard
                    icon={Link}
                    title="Deep Linking"
                    description="We don't just point to a page. The generation model provides precise anchor links to the exact section of the documentation."
                    delay="delay-300"
                />
                <FeatureCard
                    icon={Zap}
                    title="IDE Integration"
                    description="Designed to run as a sidecar in VS Code. JSON-ready outputs allow seamless integration into developer workflows."
                    delay="delay-400"
                />
                <FeatureCard
                    icon={Terminal}
                    title="Zero Hallucinations"
                    description="Strictly grounded in your indexed documentation (Stripe, LangChain, Notion). If it's not in the docs, we won't invent it."
                    delay="delay-500"
                />
            </div>
        </section>
    )
}
