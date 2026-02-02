import React from 'react';
import { Globe, Cpu, ExternalLink, BookOpen } from 'lucide-react';
import { ModeConfig } from '@/types/types';

interface SidebarRightProps {
   activeMode: ModeConfig;
}

export const SidebarRight: React.FC<SidebarRightProps> = ({ activeMode }) => {
   return (
      <aside className="hidden xl:flex w-72 flex-col border-l border-white/5 bg-black/20 backdrop-blur-xl">
         <div className="p-6 border-b border-white/5 bg-white/[0.02]">
            <h3 className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-3">Active Context</h3>
            <div className="flex items-center gap-3 mt-1 p-3 rounded-xl bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/5 shadow-inner">
               <activeMode.icon size={22} className={activeMode.color} />
               <span className="font-semibold text-zinc-100 text-sm">{activeMode.name}</span>
            </div>
            <p className="text-xs text-zinc-400 mt-3 leading-relaxed opacity-80">
               {activeMode.description}
            </p>
         </div>

         <div className="p-6 space-y-8 flex-1 overflow-y-auto custom-scrollbar">
            {/* Meta Info */}
            <div className="space-y-5">
               <div className="flex items-start gap-4 group">
                  <div className="mt-1 p-1.5 rounded-md bg-white/5 group-hover:bg-indigo-500/10 transition-colors">
                     <Globe size={14} className="text-zinc-500 group-hover:text-indigo-400 transition-colors" />
                  </div>
                  <div>
                     <div className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider">Base URL</div>
                     <div className="text-xs text-zinc-300 font-mono mt-1 break-all bg-white/5 px-2 py-1 rounded border border-white/5">
                        {activeMode.context.baseUrl}
                     </div>
                  </div>
               </div>
               <div className="flex items-start gap-4 group">
                  <div className="mt-1 p-1.5 rounded-md bg-white/5 group-hover:bg-purple-500/10 transition-colors">
                     <Cpu size={14} className="text-zinc-500 group-hover:text-purple-400 transition-colors" />
                  </div>
                  <div>
                     <div className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider">Version</div>
                     <div className="text-xs text-zinc-300 font-mono mt-1 inline-block bg-white/5 px-2 py-1 rounded border border-white/5">
                        {activeMode.context.version}
                     </div>
                  </div>
               </div>
            </div>

            {/* Divider */}
            <div className="h-px bg-gradient-to-r from-transparent via-white/10 to-transparent w-full"></div>

            {/* Popular Endpoints */}
            <div>
               <div className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-4">Popular Endpoints</div>
               <div className="space-y-2.5">
                  {activeMode.context.popularEndpoints.map((ep, i) => (
                     <div key={i} className="group flex items-center justify-between p-2.5 rounded-lg border border-white/5 bg-white/[0.02] hover:bg-white/5 hover:border-indigo-500/30 transition-all cursor-pointer shadow-sm">
                        <code className="text-[10px] text-zinc-400 group-hover:text-indigo-300 font-mono transition-colors">{ep}</code>
                        <ExternalLink size={12} className="opacity-0 group-hover:opacity-100 text-indigo-400 -translate-x-2 group-hover:translate-x-0 transition-all duration-300" />
                     </div>
                  ))}
               </div>
            </div>
         </div>

         <div className="p-4 border-t border-white/5 bg-white/[0.02]">
            <a href={activeMode.context.documentationUrl} target="_blank" rel="noopener noreferrer">
               <button className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl border border-white/10 bg-white/5 hover:bg-indigo-600 hover:border-indigo-500 hover:text-white hover:shadow-lg hover:shadow-indigo-500/20 text-xs font-semibold text-zinc-400 transition-all duration-300 cursor-pointer group">
                  <BookOpen size={14} className="group-hover:scale-110 transition-transform" />
                  Open Full Documentation
               </button>
            </a>
         </div>
      </aside>
   );
};