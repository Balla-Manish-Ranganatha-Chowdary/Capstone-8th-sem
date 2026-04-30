"use client";
import React from 'react';
import { motion } from 'framer-motion';

// Helper to generate random drifting animations
const useDriftAnimation = (duration: number, yOffset: number, xOffset: number, rotation: number) => ({
  y: [0, -yOffset, yOffset / 2, 0],
  x: [0, xOffset, -xOffset / 2, 0],
  rotate: [0, rotation, -rotation, 0],
  transition: {
    duration: duration,
    repeat: Infinity,
    ease: "linear" as const
  }
});

export const FloatingParticles = () => {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden" aria-hidden="true">
      {/* Large Ring - Slow Float */}
      <motion.div 
        className="absolute w-40 h-40 rounded-full border border-white/[0.04]"
        style={{ top: '15%', left: '8%' }}
        animate={useDriftAnimation(35, 40, 20, -5)}
      />

      {/* Small Cross - Medium Float */}
      <motion.div 
        className="absolute w-10 h-10 flex items-center justify-center opacity-50 text-white/[0.07]"
        style={{ top: '40%', right: '6%' }}
        animate={useDriftAnimation(28, 25, -30, 10)}
      >
        <div className="absolute w-full h-[1px] bg-current" />
        <div className="absolute h-full w-[1px] bg-current" />
      </motion.div>

      {/* Medium Ring - Fast Float */}
      <motion.div 
        className="absolute w-20 h-20 rounded-full border border-white/[0.06]"
        style={{ top: '70%', left: '15%' }}
        animate={useDriftAnimation(20, -35, 25, 15)}
      />

      {/* Small Dot */}
      <motion.div 
        className="absolute w-1.5 h-1.5 rounded-full bg-white/[0.08]"
        style={{ top: '25%', right: '20%' }}
        animate={useDriftAnimation(40, 15, -15, 0)}
      />

      {/* Horizontal Line */}
      <motion.div 
        className="absolute h-[1px] w-32 bg-white/[0.05]"
        style={{ top: '55%', right: '12%' }}
        animate={useDriftAnimation(45, -20, 10, -2)}
      />
    </div>
  );
};
