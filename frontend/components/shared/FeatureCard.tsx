'use client';
import React, { useRef, useState } from 'react'

const MouseSpotlight = ({ children, className = "" }: { children: React.ReactNode; className?: string }) => {
    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
    const containerRef = useRef<HTMLDivElement>(null);

    const handleMouseMove = (event: React.MouseEvent<HTMLDivElement>) => {
        if (containerRef.current) {
            const rect = containerRef.current.getBoundingClientRect();
            setMousePosition({
                x: event.clientX - rect.left,
                y: event.clientY - rect.top,
            });
        }
    };

    return (
        <div
            ref={containerRef}
            onMouseMove={handleMouseMove}
            className={`relative group overflow-hidden ${className}`}
        >
            <div
                className="pointer-events-none absolute -inset-px rounded-xl opacity-0 transition duration-300 group-hover:opacity-100 z-10"
                style={{
                    background: `radial-gradient(600px circle at ${mousePosition.x}px ${mousePosition.y}px, rgba(255,255,255,0.1), transparent 40%)`
                }}
            />
            {children}
        </div>
    );
};


export default function FeatureCard({ icon: Icon, title, description, delay }: { icon: any, title: string, description: string, delay: string }){
    return (
        <MouseSpotlight className="h-full bg-zinc-900/50 border border-white/5 rounded-2xl p-6 backdrop-blur-sm flex flex-col">
            <div className={`w-10 h-10 rounded-lg bg-zinc-800/50 flex items-center justify-center mb-4 border border-white/5 ${delay}`}>
                <Icon size={20} className="text-zinc-200" />
            </div>
            <h3 className="text-lg font-semibold text-zinc-100 mb-2">{title}</h3>
            <p className="text-sm text-zinc-400 leading-relaxed flex-1">{description}</p>
        </MouseSpotlight>
    )
}
