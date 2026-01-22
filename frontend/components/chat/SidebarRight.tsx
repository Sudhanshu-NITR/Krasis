import React from 'react';
import { Globe, Cpu, ExternalLink, BookOpen } from 'lucide-react';
import { ModeConfig } from '@/types/types';

interface SidebarRightProps {
  activeMode: ModeConfig;
}

export const SidebarRight: React.FC<SidebarRightProps> = ({ activeMode }) => {
  return (
    <aside className="hidden xl:flex w-72 flex-col border-l border-white/5 bg-[#09090b]">
      <div className="p-5 border-b border-white/5">
         <h3 className="text-xs font-bold text-zinc-500 uppercase tracking-widest mb-1">Active Context</h3>
         <div className="flex items-center gap-2 mt-3">
            <activeMode.icon size={20} className={activeMode.color} />
            <span className="font-semibold text-zinc-200">{activeMode.name}</span>
         </div>
         <p className="text-xs text-zinc-500 mt-2 leading-relaxed">
           {activeMode.description}
         </p>
      </div>

      <div className="p-5 space-y-6 flex-1 overflow-y-auto">
         {/* Meta Info */}
         <div className="space-y-4">
            <div className="flex items-start gap-3">
               <div className="mt-0.5"><Globe size={14} className="text-zinc-600" /></div>
               <div>
                  <div className="text-[11px] font-medium text-zinc-500 uppercase">Base URL</div>
                  <div className="text-xs text-zinc-300 font-mono mt-0.5 break-all">{activeMode.context.baseUrl}</div>
               </div>
            </div>
            <div className="flex items-start gap-3">
               <div className="mt-0.5"><Cpu size={14} className="text-zinc-600" /></div>
               <div>
                  <div className="text-[11px] font-medium text-zinc-500 uppercase">Version</div>
                  <div className="text-xs text-zinc-300 font-mono mt-0.5">{activeMode.context.version}</div>
               </div>
            </div>
         </div>

         {/* Divider */}
         <div className="h-px bg-white/5 w-full my-2"></div>

         {/* Popular Endpoints */}
         <div>
            <div className="text-[11px] font-medium text-zinc-500 uppercase mb-3">Popular Endpoints</div>
            <div className="space-y-2">
               {activeMode.context.popularEndpoints.map((ep, i) => (
                  <div key={i} className="group flex items-center justify-between p-2 rounded border border-white/5 bg-white/2 hover:bg-white/5 transition-colors cursor-pointer">
                     <code className="text-[11px] text-zinc-400 group-hover:text-indigo-300 font-mono">{ep}</code>
                     <ExternalLink size={10} className="opacity-0 group-hover:opacity-100 text-zinc-500" />
                  </div>
               ))}
            </div>
         </div>
      </div>

      <div className="p-4 border-t border-white/5 bg-white/2">
         <a href={activeMode.context.documentationUrl} target="_blank" rel="noopener noreferrer">
            <button className="w-full flex items-center justify-center gap-2 py-2 rounded border border-white/10 hover:bg-white/5 text-xs font-medium text-zinc-400 hover:text-zinc-200 transition-colors  cursor-pointer">
               <BookOpen size={14} />
                  Open Full Documentation
            </button>
         </a>
      </div>
    </aside>
  );
};