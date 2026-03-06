"use client";
import { motion } from 'framer-motion';

export type RiskLevel = 'Low' | 'Medium' | 'High';

interface RiskBarProps {
  label: string;
  level: RiskLevel;
  delay?: number;
}

export const RiskBar = ({ label, level, delay = 0 }: RiskBarProps) => {
  
  const percentageMap = { Low: 33, Medium: 66, High: 100 };
  const colorMap = {
    Low: 'bg-alert-low shadow-[0_0_10px_#10B981]',
    Medium: 'bg-alert-medium shadow-[0_0_10px_#F59E0B]',
    High: 'bg-alert-high shadow-[0_0_10px_#EF4444]'
  };
  const textMap = {
    Low: 'text-alert-low',
    Medium: 'text-alert-medium',
    High: 'text-alert-high'
  };

  const percentage = percentageMap[level];
  const colorClass = colorMap[level];

  return (
    <motion.div
      initial={{ opacity: 0, x: -10 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay, duration: 0.4 }}
      className="flex flex-col gap-2"
    >
      <div className="flex items-center justify-between text-xs font-mono uppercase tracking-widest">
        <span className="text-white/70">{label}</span>
        <span className={`${textMap[level]} font-bold`}>{level}</span>
      </div>
      
      <div className="h-1.5 w-full bg-white/10 rounded-full overflow-hidden flex">
        <motion.div 
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ delay: delay + 0.2, duration: 1, ease: "easeOut" }}
          className={`h-full ${colorClass} rounded-full`}
        />
      </div>
    </motion.div>
  );
};
