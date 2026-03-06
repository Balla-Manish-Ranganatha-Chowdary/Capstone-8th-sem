"use client";
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ShieldCheck, ChevronRight } from 'lucide-react';

interface ActionsListProps {
  actions: {
    immediate: string[];
    medium_term: string[];
    long_term: string[];
  };
  delay?: number;
}

type TabType = 'immediate' | 'medium_term' | 'long_term';

export const ActionsList = ({ actions, delay = 0 }: ActionsListProps) => {
  const [activeTab, setActiveTab] = useState<TabType>('immediate');

  const tabs: { id: TabType; label: string }[] = [
    { id: 'immediate', label: 'IMMEDIATE' },
    { id: 'medium_term', label: 'MEDIUM-TERM' },
    { id: 'long_term', label: 'LONG-TERM' }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.4 }}
      className="bg-black/40 border border-white/10 rounded-lg overflow-hidden flex flex-col h-full min-h-[220px]"
    >
      <div className="flex items-center gap-2 p-3 border-b border-white/10 bg-white/5">
        <ShieldCheck className="w-4 h-4 text-primary" />
        <span className="text-[10px] font-mono tracking-widest text-primary uppercase">Preventive Actions</span>
      </div>

      <div className="flex border-b border-white/5">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex-1 py-2 text-[10px] font-mono tracking-wider transition-colors relative ${
              activeTab === tab.id ? 'text-primary bg-primary/5' : 'text-white/40 hover:text-white/70 hover:bg-white/5'
            }`}
          >
            {tab.label}
            {activeTab === tab.id && (
              <motion.div
                layoutId="activeTab"
                className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary"
              />
            )}
          </button>
        ))}
      </div>

      <div className="p-4 flex-1 relative overflow-hidden">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, x: 10 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -10 }}
            transition={{ duration: 0.2 }}
            className="absolute inset-0 p-4 overflow-y-auto custom-scrollbar"
          >
            <ul className="flex flex-col gap-3">
              {actions[activeTab].map((action, idx) => (
                <motion.li 
                  key={idx}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.1 * idx, duration: 0.3 }}
                  className="flex items-start gap-2 text-sm text-white/80 group cursor-default"
                >
                  <ChevronRight className="w-4 h-4 mt-0.5 text-white/30 shrink-0 group-hover:text-primary transition-colors" />
                  <span className="group-hover:text-primary/90 transition-colors">{action}</span>
                </motion.li>
              ))}
            </ul>
          </motion.div>
        </AnimatePresence>
      </div>
    </motion.div>
  );
};
