import React from 'react';
import { Search, LayoutGrid, PanelLeft, PanelRight } from 'lucide-react';
import { ModeConfig } from '@/types/types';
import { UserButton } from '@clerk/nextjs';

interface ChatHeaderProps {
  activeMode: ModeConfig;
  isLeftOpen: boolean;
  toggleLeft: () => void;
  isRightOpen: boolean;
  toggleRight: () => void;
}

export const ChatHeader: React.FC<ChatHeaderProps> = ({
  activeMode,
  isLeftOpen,
  toggleLeft,
  isRightOpen,
  toggleRight
}) => {
  return (
    <header className="h-14 flex items-center justify-between px-4 border-b border-white/5 bg-[#09090b]/80 backdrop-blur-sm z-10 sticky top-0 shrink-0">
      <div className="flex items-center gap-3">
        <button
          onClick={toggleLeft}
          className={`p-2 rounded-lg hover:bg-white/5 transition-colors ${!isLeftOpen ? 'text-zinc-400' : 'text-zinc-500'}`}
          title="Toggle Sidebar"
        >
          <PanelLeft size={18} />
        </button>

        <div className="h-4 w-px bg-white/10 mx-1 hidden md:block" />

        <div className="flex items-center gap-2">
          {/* <LayoutGrid size={16} className="text-zinc-500" /> 
           <span className="text-zinc-500 text-sm">/</span> */}
          <span className="flex items-center gap-2 text-sm font-medium text-zinc-200">
            <activeMode.icon size={16} className={activeMode.color} />
            {activeMode.name}
          </span>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button className="p-2 rounded-lg hover:bg-white/5 text-zinc-500 hover:text-zinc-300 transition-colors">
          <Search size={18} />
        </button>

        <div className="ml-2">
          <UserButton />
        </div>

        <button
          onClick={toggleRight}
          className={`p-2 rounded-lg hover:bg-white/5 transition-colors ${!isRightOpen ? 'text-zinc-400' : 'text-zinc-500'} hidden xl:block`}
          title="Toggle Details"
        >
          <PanelRight size={18} />
        </button>
      </div>
    </header>
  );
};