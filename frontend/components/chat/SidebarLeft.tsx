import React from 'react';
import { Sparkles, Settings, Layers } from 'lucide-react';
import { DocMode } from '@/types/types';
import { MOCK_MODES } from '@/config/config';
import { useClerk } from "@clerk/nextjs";
import Link from 'next/link';

interface SidebarLeftProps {
  docMode: DocMode;
  setDocMode: (mode: DocMode) => void;
  onModeSwitch: () => void; // Used to clear messages
}

export const SidebarLeft: React.FC<SidebarLeftProps> = ({ docMode, setDocMode, onModeSwitch }) => {
  const { openUserProfile, user } = useClerk();

  return (
    <aside className="w-64 flex flex-col border-r border-white/5 bg-black/20 backdrop-blur-xl">
      {/* Brand */}
      <div className="p-4 h-16 flex items-center border-b border-white/5 bg-white/[0.02]">
        <div className="flex items-center gap-3 text-zinc-100">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20 ring-1 ring-white/10">
            <Layers size={16} className="text-white" />
          </div>
          <Link href="/">
            <span className="font-bold tracking-tight text-base bg-clip-text text-transparent bg-gradient-to-r from-white to-zinc-400">
              Krasis
            </span>
          </Link>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex-1 overflow-y-auto p-4 space-y-8 custom-scrollbar">
        <div>
          <div className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest px-3 mb-3">Documentation</div>
          <nav className="space-y-1">
            {(Object.keys(MOCK_MODES) as DocMode[]).map((mode) => {
              const m = MOCK_MODES[mode];
              const isActive = docMode === mode;
              return (
                <button
                  key={mode}
                  onClick={() => { setDocMode(mode); onModeSwitch(); }}
                  className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-300 group relative overflow-hidden
                    ${isActive
                      ? 'text-white font-medium bg-white/5 shadow-inner ring-1 ring-white/5'
                      : 'text-zinc-400 hover:text-zinc-200 hover:bg-white/5'}`}
                >
                  <div className={`absolute inset-0 bg-gradient-to-r from-indigo-500/10 to-transparent opacity-0 transition-opacity duration-300 ${isActive ? 'opacity-100' : 'group-hover:opacity-50'}`} />

                  <m.icon size={18} className={`relative z-10 transition-colors duration-300 ${isActive ? m.color : 'text-zinc-500 group-hover:text-zinc-300'}`} />
                  <span className="relative z-10">{m.name}</span>

                  {isActive && (
                    <div className="ml-auto w-1.5 h-1.5 rounded-full bg-indigo-500 shadow-[0_0_8px_rgba(99,102,241,0.8)] relative z-10" />
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        <div>
          <div className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest px-3 mb-3">Your Library</div>
          <div className="px-3 py-4 rounded-lg border border-dashed border-white/5 bg-white/[0.01] text-center">
            <span className="text-xs text-zinc-600 italic">No saved threads yet</span>
          </div>
        </div>
      </div>

      {/* User Footer */}
      <div className="p-4 border-t border-white/5 bg-white/[0.02]">
        <button
          onClick={() => openUserProfile()}
          className="w-full flex items-center gap-3 p-2 rounded-xl hover:bg-white/5 transition-all duration-200 group border border-transparent hover:border-white/5 text-left"
        >
          <img
            src={user?.imageUrl}
            alt="User Profile"
            className="w-9 h-9 rounded-full ring-2 ring-white/5 shadow-lg group-hover:scale-105 transition-transform duration-200"
          />
          <div className="flex-1 min-w-0">
            <div className="text-xs font-semibold text-zinc-200 truncate group-hover:text-white transition-colors">
              {user?.fullName}
            </div>
            <div className="text-[10px] text-zinc-500 truncate group-hover:text-zinc-400 transition-colors">
              {user?.emailAddresses?.[0]?.emailAddress}
            </div>
          </div>

          <Settings className="text-zinc-600 group-hover:text-zinc-300 transition-colors" size={16} />
        </button>
      </div>
    </aside>
  );
};