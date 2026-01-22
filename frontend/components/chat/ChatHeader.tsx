import React from 'react';
import { Search, MoreHorizontal, icons, LayoutGrid } from 'lucide-react';
import { ModeConfig } from '@/types/types';
import { UserButton } from '@clerk/nextjs';

interface ChatHeaderProps {
  activeMode: ModeConfig;
}

export const ChatHeader: React.FC<ChatHeaderProps> = ({ activeMode }) => {
  return (
    <header className="h-14 flex items-center justify-between px-6 border-b border-white/5 bg-[#09090b]/80 backdrop-blur-sm z-10 sticky top-0">
      <div className="flex items-center gap-2">
        <LayoutGrid size={16} className="text-zinc-500" />
             <span className="text-zinc-500 text-sm">/</span>
             <span className="flex items-center gap-2 text-sm font-medium text-zinc-200">
                <activeMode.icon size={14} className={activeMode.color} />
                {activeMode.name}
             </span>
      </div>
      <div className="flex gap-4">
        <button className="text-zinc-500 hover:text-zinc-300 transition-colors">
          <Search size={16} />
        </button>
        <UserButton />
      </div>
    </header>
  );
};