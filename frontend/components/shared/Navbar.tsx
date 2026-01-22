'use client';
import { SignedIn, SignedOut, SignInButton, SignUpButton, UserButton } from '@clerk/nextjs';
import { Github, Layers } from 'lucide-react'

export default function Navbar() {
    return (
        <nav className='fixed top-0 left-0 right-0 z-50 border-b border-white/5 bg-black/50 backdrop-blur-xl'>
            <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
                <div className='flex items-center gap-2'>
                    <div className="w-8 h-8 rounded bg-linear-to-tr from-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
                        <Layers size={18} className="text-white" />
                    </div>
                    <span className="font-bold tracking-tight text-lg text-white">Krasis</span>
                </div>

                <div className="hidden md:flex items-center gap-8 text-sm font-medium text-zinc-400">
                    <a href="#architecture" className="hover:text-white transition-colors">Architecture</a>
                    <a href="#integration" className="hover:text-white transition-colors">Integration</a>
                    <a href="#pricing" className="hover:text-white transition-colors">Enterprise</a>
                </div>

                <div className="flex items-center gap-4">
                    <a href="https://github.com/Sudhanshu-NITR/Krasis" target="_blank" className="hidden md:flex items-center gap-2 text-sm text-zinc-400 hover:text-white transition-colors">
                        <Github size={16} />
                        <span>Source</span>
                    </a>
                    {/* <button className="bg-white text-black px-4 py-2 rounded-full text-sm font-semibold hover:bg-zinc-200 transition-colors">
                        Get Started
                    </button> */}
                    <SignedOut>
                        <SignInButton>
                            <button className="text-sm text-zinc-400 hover:text-white transition-colors">
                                Sign In
                            </button>
                        </SignInButton>
                        <SignUpButton>
                            <button className="bg-white text-black px-4 py-2 rounded-full text-sm font-semibold hover:bg-zinc-200 transition-colors">
                                Get Started
                            </button>
                        </SignUpButton>
                    </SignedOut>
                    <SignedIn>
                        <UserButton />
                    </SignedIn>
                </div>
            </div>
        </nav>
    )
}
