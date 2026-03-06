"use client";
import { motion, useSpring, useTransform } from 'framer-motion';
import { Leaf, Droplets, Building2, TrendingUp, TrendingDown } from 'lucide-react';
import React, from 'react';

interface MetricCardProps {
  title: string;
  value: number;
  type: 'vegetation' | 'water' | 'builtup';
  delay?: number;
}

export const MetricCard = ({ title, value, type, delay = 0 }: MetricCardProps) => {
  const spring = useSpring(0, { bounce: 0, duration: 2000 });
  
  React.useEffect(() => {
    spring.set(Math.abs(value));
  }, [value, spring]);

  const display = useTransform(spring, (current) => current.toFixed(1));

  const icons = {
    vegetation: Leaf,
    water: Droplets,
    builtup: Building2
  };
  const Icon = icons[type];

  // Logic for color coding the delta
  // Vegetation/Water: Positive=Good(Green), Negative=Bad(Red)
  // BuiltUp: Positive=Bad(Red), Negative=Neutral(Grey)  -- just an interpretation for the ops center feel
  let isPositiveDelta = value >= 0;
  let colorClass = "";
  if (type === 'vegetation' || type === 'water') {
     colorClass = isPositiveDelta ? "text-alert-low" : "text-alert-high";
  } else {
     colorClass = isPositiveDelta ? "text-alert-high" : "text-white/50";
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.4 }}
      className="bg-black/40 border border-white/10 rounded-lg p-4 relative overflow-hidden group hover:border-primary/30 transition-colors"
    >
      <div className="absolute top-0 left-0 w-1 h-full bg-primary/20 group-hover:bg-primary transition-colors" />
      
      <div className="flex items-start justify-between mb-4 pl-2">
        <div className="flex items-center gap-2">
          <Icon className="w-4 h-4 text-white/50 group-hover:text-primary transition-colors" />
          <span className="text-xs font-mono tracking-widest text-white/50 uppercase">{title}</span>
        </div>
      </div>

      <div className="pl-2 flex items-baseline gap-2">
        <motion.span className="text-3xl font-mono text-white">
          {display}
        </motion.span>
        <span className="text-sm font-mono text-white/50">%</span>
        
        <div className={`ml-auto flex items-center gap-1 ${colorClass} bg-current/10 px-2 py-0.5 rounded text-xs font-mono`}>
          {isPositiveDelta ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
          {Math.abs(value).toFixed(1)}%
        </div>
      </div>
    </motion.div>
  );
};
