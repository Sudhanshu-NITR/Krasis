'use client';

export default function BackgroundGrid() {
  return (
    <div className="absolute inset-0 z-0 pointer-events-none">
        {/* Base Grid */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-size-[24px_24px]"></div>
        
        {/* Radial Fade */}
        <div className="absolute inset-0 bg-black mask-[radial-gradient(ellipse_60%_50%_at_50%_0%,transparent_70%,black)]"></div>
    </div>
  )
}
