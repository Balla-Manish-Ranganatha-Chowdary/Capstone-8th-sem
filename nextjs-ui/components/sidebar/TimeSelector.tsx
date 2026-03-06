"use client";
import React from 'react';

interface TimeSelectorProps {
  startYear: number;
  endYear: number;
  minYear: number;
  maxYear: number;
  onChange: (start: number, end: number) => void;
}

export const TimeSelector = ({ startYear, endYear, minYear, maxYear, onChange }: TimeSelectorProps) => {

  const handleStartChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newStart = parseInt(e.target.value, 10);
    if (newStart <= endYear) {
      onChange(newStart, endYear);
    } else {
      onChange(newStart, newStart); // Auto-correct bounds
    }
  };

  const handleEndChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newEnd = parseInt(e.target.value, 10);
    if (newEnd >= startYear) {
      onChange(startYear, newEnd);
    } else {
      onChange(newEnd, newEnd); // Auto-correct bounds
    }
  };

  const years = Array.from({ length: maxYear - minYear + 1 }, (_, i) => minYear + i);

  return (
    <div className="glass-panel p-6 flex flex-col gap-6">
      <div className="flex items-center gap-3 border-b border-white/10 pb-4">
        <div className="w-8 h-8 rounded shrink-0 bg-primary/20 flex items-center justify-center border border-primary/30">
          <span className="text-primary text-xl">📅</span>
        </div>
        <div>
          <h2 className="text-sm font-bold tracking-widest text-primary uppercase">Time Range</h2>
          <p className="text-xs text-white/50 font-mono">TEMPORAL BOUNDS</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="flex flex-col gap-2">
          <label className="text-[10px] font-mono text-primary/70 uppercase tracking-widest">START YEAR</label>
          <div className="relative">
            <select 
              className="w-full bg-secondary/50 border border-white/10 rounded-lg px-3 py-2 text-sm appearance-none focus:outline-none focus:border-primary/50 text-white/90 cursor-pointer"
              value={startYear}
              onChange={handleStartChange}
            >
              {years.map(y => <option key={`start-${y}`} value={y} className="bg-secondary">{y}</option>)}
            </select>
            <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-white/30 text-xs">▼</div>
          </div>
        </div>

        <div className="flex flex-col gap-2">
          <label className="text-[10px] font-mono text-primary/70 uppercase tracking-widest">END YEAR</label>
          <div className="relative">
            <select 
              className="w-full bg-secondary/50 border border-white/10 rounded-lg px-3 py-2 text-sm appearance-none focus:outline-none focus:border-primary/50 text-white/90 cursor-pointer"
              value={endYear}
              onChange={handleEndChange}
            >
              {years.map(y => <option key={`end-${y}`} value={y} className="bg-secondary">{y}</option>)}
            </select>
            <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-white/30 text-xs">▼</div>
          </div>
        </div>
      </div>

      {/* Visual Timeline Bar */}
      <div className="pt-2">
        <div className="h-2 w-full bg-black/50 rounded-full flex overflow-hidden border border-white/5 relative">
          <div 
            className="absolute h-full bg-primary/60 transition-all duration-300 shadow-[0_0_10px_#00D4FF]"
            style={{ 
              left: `${((startYear - minYear) / (maxYear - minYear)) * 100}%`,
              right: `${100 - ((endYear - minYear) / (maxYear - minYear)) * 100}%`
            }}
          />
        </div>
        <div className="flex justify-between mt-2 text-[10px] font-mono text-white/30">
          <span>{minYear}</span>
          <span>{maxYear}</span>
        </div>
      </div>
    </div>
  );
};
