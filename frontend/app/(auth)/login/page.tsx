"use client";

import React, { useState } from 'react';
import {
  Github,
  Mail,
  Lock,
  ArrowRight,
  Sparkles,
  CheckCircle2,
  Command,
  Loader2,
  Eye,
  EyeOff
} from 'lucide-react';

// --- COMPONENTS REUSED FOR CONSISTENCY ---

const BackgroundGrid = () => (
  <div className="absolute inset-0 z-0 pointer-events-none overflow-hidden">
    <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-size-[24px_24px]"></div>
    <div className="absolute inset-0 bg-black mask-[radial-gradient(ellipse_60%_50%_at_50%_50%,transparent_20%,black)]"></div>
  </div>
);

// --- MAIN COMPONENT ---

export default function AuthPage() {
  const [authMode, setAuthMode] = useState<'signin' | 'signup'>('signin');
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  // Form State
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');

  const toggleMode = () => {
    setAuthMode(prev => prev === 'signin' ? 'signup' : 'signin');
    // Reset basic states
    setIsLoading(false);
    setShowPassword(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) return;

    setIsLoading(true);
    // Simulate network request
    await new Promise(resolve => setTimeout(resolve, 2000));
    setIsLoading(false);
    alert(`Successfully ${authMode === 'signin' ? 'logged in' : 'signed up'}! (Demo)`);
  };

  return (
    <div className="min-h-screen bg-black text-white font-sans selection:bg-indigo-500/30 flex flex-col relative overflow-hidden">

      {/* Background Ambience */}
      <BackgroundGrid />
      <div className="absolute top-[-20%] left-[-10%] w-150 h-150 bg-indigo-500/10 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-[-20%] right-[-10%] w-125 h-125 bg-purple-500/10 rounded-full blur-[100px] pointer-events-none"></div>

      {/* Navbar (Minimal) */}
      <nav className="relative z-10 w-full p-6 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded bg-linear-to-tr from-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <Sparkles size={16} className="text-white" />
          </div>
          <span className="font-bold tracking-tight text-lg">DevDocs</span>
        </div>
        <a href="/" className="text-sm text-zinc-500 hover:text-white transition-colors">
          Back to Home
        </a>
      </nav>

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center p-6 relative z-10">
        <div className="w-full max-w-md">

          {/* Card Container */}
          <div className="relative group">
            <div className="absolute -inset-0.5 bg-linear-to-b from-indigo-500/20 to-purple-500/20 rounded-2xl opacity-75 blur transition duration-1000 group-hover:opacity-100 group-hover:duration-200"></div>

            <div className="relative bg-[#09090b] border border-white/10 rounded-xl p-8 shadow-2xl">

              {/* Header */}
              <div className="text-center mb-8">
                <h1 className="text-2xl font-bold tracking-tight mb-2 text-white">
                  {authMode === 'signin' ? 'Welcome back' : 'Create an account'}
                </h1>
                <p className="text-zinc-400 text-sm">
                  {authMode === 'signin'
                    ? 'Enter your credentials to access your workspace.'
                    : 'Get started with intelligent documentation search.'}
                </p>
              </div>

              {/* Social Login */}
              <div className="space-y-3 mb-8">
                <button className="w-full flex items-center justify-center gap-3 bg-white text-black font-medium py-2.5 rounded-lg hover:bg-zinc-200 transition-colors">
                  <Github size={20} />
                  <span>Continue with GitHub</span>
                </button>
                <button className="w-full flex items-center justify-center gap-3 bg-zinc-900 border border-zinc-800 text-zinc-300 font-medium py-2.5 rounded-lg hover:bg-zinc-800 hover:text-white transition-colors">
                  <Command size={20} className="text-zinc-500" />
                  <span>Continue with SSO</span>
                </button>
              </div>

              {/* Divider */}
              <div className="relative mb-8">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-white/10"></div>
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-[#09090b] px-2 text-zinc-500">Or continue with email</span>
                </div>
              </div>

              {/* Form */}
              <form onSubmit={handleSubmit} className="space-y-4">
                {authMode === 'signup' && (
                  <div className="space-y-1.5">
                    <label className="text-xs font-medium text-zinc-400 ml-1">Full Name</label>
                    <div className="relative">
                      <input
                        type="text"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Jane Senior"
                        className="w-full bg-zinc-900/50 border border-white/10 rounded-lg px-4 py-2.5 text-sm text-white placeholder:text-zinc-600 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all"
                        required
                      />
                    </div>
                  </div>
                )}

                <div className="space-y-1.5">
                  <label className="text-xs font-medium text-zinc-400 ml-1">Email Address</label>
                  <div className="relative">
                    <Mail size={16} className="absolute left-3 top-3 text-zinc-500" />
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="jane@company.com"
                      className="w-full bg-zinc-900/50 border border-white/10 rounded-lg pl-10 pr-4 py-2.5 text-sm text-white placeholder:text-zinc-600 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all"
                      required
                    />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-medium text-zinc-400 ml-1">Password</label>
                  <div className="relative">
                    <Lock size={16} className="absolute left-3 top-3 text-zinc-500" />
                    <input
                      type={showPassword ? "text" : "password"}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="••••••••"
                      className="w-full bg-zinc-900/50 border border-white/10 rounded-lg pl-10 pr-10 py-2.5 text-sm text-white placeholder:text-zinc-600 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500/50 transition-all"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-3 text-zinc-500 hover:text-zinc-300 transition-colors"
                    >
                      {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                    </button>
                  </div>
                </div>

                {authMode === 'signup' && (
                  <div className="flex items-start gap-2 pt-1">
                    <div className="mt-1 w-4 h-4 rounded border border-zinc-700 bg-zinc-900 flex items-center justify-center cursor-pointer">
                      <CheckCircle2 size={10} className="text-indigo-500 opacity-0 hover:opacity-100" />
                    </div>
                    <p className="text-xs text-zinc-500 leading-normal">
                      I agree to the <a href="#" className="underline hover:text-zinc-300">Terms of Service</a> and <a href="#" className="underline hover:text-zinc-300">Privacy Policy</a>.
                    </p>
                  </div>
                )}

                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full bg-linear-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 text-white font-medium py-2.5 rounded-lg shadow-lg shadow-indigo-500/25 transition-all flex items-center justify-center gap-2 mt-2 group"
                >
                  {isLoading ? (
                    <Loader2 size={18} className="animate-spin" />
                  ) : (
                    <>
                      {authMode === 'signin' ? 'Sign In' : 'Create Account'}
                      <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
                    </>
                  )}
                </button>
              </form>
            </div>
          </div>

          {/* Footer Toggle */}
          <div className="text-center mt-6">
            <p className="text-sm text-zinc-500">
              {authMode === 'signin' ? "Don't have an account? " : "Already have an account? "}
              <button
                onClick={toggleMode}
                className="text-indigo-400 hover:text-indigo-300 font-medium transition-colors"
              >
                {authMode === 'signin' ? 'Sign up' : 'Sign in'}
              </button>
            </p>
          </div>

        </div>
      </main>

      {/* Footer Links */}
      <footer className="relative z-10 py-6 text-center">
        <div className="flex items-center justify-center gap-6 text-xs text-zinc-600">
          <a href="#" className="hover:text-zinc-400 transition-colors">Privacy</a>
          <a href="#" className="hover:text-zinc-400 transition-colors">Terms</a>
          <a href="#" className="hover:text-zinc-400 transition-colors">Contact</a>
        </div>
      </footer>
    </div>
  );
}