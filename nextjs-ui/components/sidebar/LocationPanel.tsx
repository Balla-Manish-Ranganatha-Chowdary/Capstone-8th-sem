"use client";
import React, from 'react';
import { motion, useSpring, useTransform } from 'framer-motion';

// Animated number ticker component
const NumberTicker = ({ value }: { value: number | null }) => {
  const spring = useSpring(0, { bounce: 0, duration: 800 });
  
  React.useEffect(() => {
    if (value !== null) spring.set(value);
  }, [value, spring]);

  const display = useTransform(spring, (current) => 
    current === 0 && value === null ? "---.----" : current.toFixed(4)
  );

  return <motion.span>{display}</motion.span>;
};

interface LocationPanelProps {
  states: Array<{ name: string; latitude: number; longitude: number }>;
  selectedState: string | null;
  selectedLocation: { latitude: number; longitude: number } | null;
  onStateSelect: (stateName: string) => void;
}

export const LocationPanel = ({ states, selectedState, selectedLocation, onStateSelect }: LocationPanelProps) => {
  return (
    <div className="glass-panel p-6 flex flex-col gap-6">
      <div className="flex items-center gap-3 border-b border-white/10 pb-4">
        <div className="w-8 h-8 rounded shrink-0 bg-primary/20 flex items-center justify-center border border-primary/30">
          <span className="text-primary text-xl">📍</span>
        </div>
        <div>
          <h2 className="text-sm font-bold tracking-widest text-primary uppercase">Location</h2>
          <p className="text-xs text-white/50 font-mono">SELECT TARGET AREA</p>
        </div>
      </div>

      <div className="flex flex-col gap-2">
        <label className="text-xs font-mono text-white/50 uppercase tracking-wider">Territory / State</label>
        <div className="relative">
          <select 
            className="w-full bg-secondary/50 border border-white/10 rounded-lg px-4 py-3 text-sm appearance-none focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all cursor-pointer text-white/90"
            value={selectedState || ""}
            onChange={(e) => onStateSelect(e.target.value)}
          >
            <option value="" disabled>-- Select a State --</option>
            {states.map(s => (
              <option key={s.name} value={s.name} className="bg-secondary">{s.name}</option>
            ))}
          </select>
          <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-white/30 text-xs">▼</div>
        </div>
      </div>

      <div className="flex items-center gap-4 py-2 opacity-50">
        <div className="h-px bg-white/20 flex-1" />
        <span className="text-xs font-mono tracking-widest">OR</span>
        <div className="h-px bg-white/20 flex-1" />
      </div>

      <div className="text-center text-xs text-white/50 font-mono mb-2">
        CLICK MAP TO SELECT COORDS
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-black/40 border border-white/5 rounded-lg p-3 flex flex-col gap-1">
          <span className="text-[10px] text-primary/70 uppercase tracking-widest font-mono">LATITUDE</span>
          <span className="font-mono text-sm text-white/90">
            <NumberTicker value={selectedLocation?.latitude ?? null} />°N
          </span>
        </div>
        <div className="bg-black/40 border border-white/5 rounded-lg p-3 flex flex-col gap-1">
          <span className="text-[10px] text-primary/70 uppercase tracking-widest font-mono">LONGITUDE</span>
          <span className="font-mono text-sm text-white/90">
            <NumberTicker value={selectedLocation?.longitude ?? null} />°E
          </span>
        </div>
      </div>
    </div>
  );
};
