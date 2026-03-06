"use client";
import { motion } from 'framer-motion';

export const StatusBar = () => {
  const dateStr = new Date().toISOString().split('T')[0];

  return (
    <header className="fixed top-0 left-0 right-0 h-14 bg-background/90 backdrop-blur border-b border-white/10 z-40 px-6 flex items-center justify-between font-mono text-xs text-white/70">
      
      {/* Target Logo & Wordmark */}
      <div className="flex items-center gap-3">
        <span className="text-xl">🛰️</span>
        <span className="tracking-[0.2em] font-bold text-white uppercase hidden sm:inline-block">
          India EO Intelligence
        </span>
      </div>

      {/* Center Animated Status */}
      <div className="flex items-center gap-4 bg-white/5 px-4 py-1.5 rounded-full border border-white/5">
        <div className="w-2 h-2 rounded-full bg-alert-low animate-pulse shadow-[0_0_8px_#10B981]" />
        <span className="tracking-wider">SYSTEM ONLINE | DATA SOURCE: ISRO | LIVE</span>
      </div>

      {/* Right Stats */}
      <div className="flex items-center gap-4 hidden md:flex">
        <span>{dateStr}</span>
        <span className="px-2 py-1 bg-primary/10 text-primary border border-primary/20 rounded">
          v1.0.0
        </span>
      </div>
      
    </header>
  );
};
