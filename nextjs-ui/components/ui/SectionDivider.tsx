"use client";
import React from 'react';
import { motion } from 'framer-motion';

export const SectionDivider = ({ label }: { label: string }) => {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.7, ease: [0.16, 1, 0.3, 1] }}
      className="flex items-center gap-4 w-full py-6 group"
    >
      <div className="flex-1 h-[1px] bg-white/10 transition-colors duration-300 group-hover:bg-white/20" />
      {label && (
        <span className="uppercase tracking-[0.2em] text-[0.65rem] font-bold text-white/30 transition-colors duration-300 group-hover:text-white/60 whitespace-nowrap">
          {label}
        </span>
      )}
      <div className="flex-1 h-[1px] bg-white/10 transition-colors duration-300 group-hover:bg-white/20" />
    </motion.div>
  );
};
