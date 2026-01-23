'use client';
import { Github, Globe, Layers } from 'lucide-react'

export default function Footer() {
    return (
        <footer className="border-t border-white/5 py-12 px-6 bg-black">
            <div className="max-w-7xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 text-sm">
                <div className="col-span-2 md:col-span-1">
                    <div className="flex items-center gap-2 mb-4">
                        <div className="w-6 h-6 rounded bg-indigo-600 flex items-center justify-center">
                            <Layers size={12} className="text-white" />
                        </div>
                        <span className="font-bold">Krasis</span>
                    </div>
                    <p className="text-zinc-500 mb-4">
                        Intelligent Developer Documentation Assistant.<br />
                        Combining Keyword & Semantic Search.
                    </p>
                    <div className="flex gap-4 text-zinc-400">
                        <a href="https://github.com/Sudhanshu-NITR/Krasis" target="_blank" rel="noopener noreferrer">
                            <Github size={20} className="hover:text-white cursor-pointer" />
                        </a>
                        <Globe size={20} className="hover:text-white cursor-pointer" />
                    </div>
                </div>

                <div>
                    <h4 className="font-bold text-white mb-4">Architecture</h4>
                    <ul className="space-y-2 text-zinc-500">
                        <li className="hover:text-zinc-300 cursor-pointer">Hybrid Search</li>
                        <li className="hover:text-zinc-300 cursor-pointer">Reranking</li>
                        <li className="hover:text-zinc-300 cursor-pointer">Vector Embeddings</li>
                    </ul>
                </div>

                <div>
                    <h4 className="font-bold text-white mb-4">Resources</h4>
                    <ul className="space-y-2 text-zinc-500">
                        <li className="hover:text-zinc-300 cursor-pointer">HackOn Amazon</li>
                        <li className="hover:text-zinc-300 cursor-pointer">Dataset Info</li>
                        <li className="hover:text-zinc-300 cursor-pointer">Implementation Guide</li>
                    </ul>
                </div>

                <div>
                    <h4 className="font-bold text-white mb-4">Legal</h4>
                    <ul className="space-y-2 text-zinc-500">
                        <li className="hover:text-zinc-300 cursor-pointer">Privacy</li>
                        <li className="hover:text-zinc-300 cursor-pointer">Terms</li>
                        <li className="hover:text-zinc-300 cursor-pointer">Security</li>
                    </ul>
                </div>
            </div>
        </footer>
    )
}
