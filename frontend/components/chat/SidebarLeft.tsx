import React from 'react';
import { Sparkles, Settings, Layers } from 'lucide-react';
import { DocMode } from '@/types/types';
import { MOCK_MODES } from '@/config/config';
import { useClerk, UserButton } from "@clerk/nextjs";
import Image from 'next/image';

interface SidebarLeftProps {
  docMode: DocMode;
  setDocMode: (mode: DocMode) => void;
  onModeSwitch: () => void; // Used to clear messages
}

export const SidebarLeft: React.FC<SidebarLeftProps> = ({ docMode, setDocMode, onModeSwitch }) => {
  const { openUserProfile, user } = useClerk();
  return (
    <aside className="w-64 flex flex-col border-r border-white/5 bg-[#09090b]">
      {/* Brand */}
      <div className="p-4 h-14 flex items-center border-b border-white/5">
        <div className="flex items-center gap-2 text-zinc-100">
          <div className="w-6 h-6 rounded bg-linear-to-tr from-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <Layers size={14} className="text-white" />
          </div>
          <span className="font-bold tracking-tight text-sm">Krasis</span>
        </div>
      </div>

      {/* Navigation */}
      <div className="flex-1 overflow-y-auto p-3 space-y-6">
        <div>
          <div className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest px-2 mb-2">Documentation</div>
          <nav className="space-y-0.5">
            {(Object.keys(MOCK_MODES) as DocMode[]).map((mode) => {
              const m = MOCK_MODES[mode];
              const isActive = docMode === mode;
              return (
                <button
                  key={mode}
                  onClick={() => { setDocMode(mode); onModeSwitch(); }}
                  className={`w-full flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-all duration-200 group
                    ${isActive
                      ? 'bg-zinc-800 text-white shadow-inner font-medium'
                      : 'text-zinc-400 hover:text-zinc-200 hover:bg-white/5'}`}
                >
                  <m.icon size={16} className={`${isActive ? m.color : 'text-zinc-500 group-hover:text-zinc-400'}`} />
                  <span>{m.name}</span>
                  {isActive && <div className="ml-auto w-1.5 h-1.5 rounded-full bg-white shadow-[0_0_8px_rgba(255,255,255,0.5)]" />}
                </button>
              );
            })}
          </nav>
        </div>

        <div>
          <div className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest px-2 mb-2">Your Library</div>
          <div className="px-2 py-1 text-sm text-zinc-600 italic">No saved threads yet</div>
        </div>
      </div>

      {/* User Footer */}
      <button onClick={() => openUserProfile()}>
        <div className="p-4 border-t border-white/5">
          <div className="flex items-center gap-3 px-2 py-3 rounded-lg hover:bg-white/5 transition-colors cursor-pointer text-zinc-400 hover:text-zinc-200">
            {/* <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-zinc-700 to-zinc-600 flex items-center justify-center text-xs font-medium text-white shadow-lg">
              <Image src={user?.imageUrl || ''} alt="User Avatar" width={32} height={32} className="rounded-full" />
              JS
            </div> */}
            <img 
              src={user?.imageUrl} 
              alt="User Profile" 
              className="w-8 h-8 rounded-full bg-linear-to-tr from-zinc-700 to-zinc-600 flex items-center justify-center text-xs font-medium text-white shadow-lg"
            />
            <div className="flex-1 min-w-0">
              <div className="text-xs font-medium truncate">{user?.fullName}</div>
              <div className="text-[10px] text-zinc-500">{user?.emailAddresses?.[0]?.emailAddress}</div>
            </div>
            
            <Settings className='ml-2' size={14} />
          </div>
        </div>
      </button>
    </aside>
  );
};