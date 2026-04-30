'use client';

import React, { useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';

export default function ParallaxScene() {
  const containerRef = useRef(null);
  
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end end"]
  });

  // Satellite transforms
  const satScale = useTransform(scrollYProgress, [0, 0.2, 0.4, 0.6, 0.8, 1], [1.3, 1.3, 1.0, 0.5, 0.2, 0.0]);
  const satX = useTransform(scrollYProgress, [0, 0.2, 0.4, 0.6, 0.8, 1], ["0%", "0%", "30%", "50%", "60%", "70%"]);
  // Since useTransform expects numbers or CSS convertible strings, adjusting y mappings carefully:
  const satY = useTransform(scrollYProgress, [0, 0.2, 0.4, 0.6, 0.8, 1], ["-10%", "-10%", "-5%", "0%", "10%", "20%"]);
  const satOpacity = useTransform(scrollYProgress, [0, 0.2, 0.4, 0.6, 0.8, 1], [1, 1, 1, 0.6, 0.2, 0]);
  const satRotate = useTransform(scrollYProgress, [0, 0.2, 0.4, 0.6, 0.8, 1], [0, 0, -5, -10, -15, -20]);

  // Earth transforms
  const earthScale = useTransform(scrollYProgress, [0, 0.2, 0.4, 0.6, 0.8, 1], [0.5, 0.6, 0.8, 1.8, 2.6, 3.2]);
  const earthY = useTransform(scrollYProgress, [0, 0.2, 0.4, 0.6, 0.8, 1], ["30%", "25%", "15%", "0%", "-10%", "-20%"]);
  const earthOpacity = useTransform(scrollYProgress, [0, 0.2, 0.4, 0.6, 0.8, 1], [0.6, 0.7, 0.9, 1, 1, 1]);

  // Scan Grid Outline
  const gridOpacity = useTransform(scrollYProgress, [0.5, 0.65], [0, 0.4]);

  return (
    <div ref={containerRef} className="fixed inset-0 z-0 pointer-events-none overflow-hidden bg-[#050810]">
      
      {/* Animated Starfield Background via CSS */}
      <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20" />
      <div id="cosmic-depth" />

      {/* Earth Globe Container */}
      <motion.div 
        className="absolute inset-x-0 bottom-0 flex justify-center items-center"
        style={{
          scale: earthScale,
          y: earthY,
          opacity: earthOpacity,
          transformOrigin: 'bottom center'
        }}
      >
        <div className="relative w-[800px] h-[800px]">
          {/* Earth Body */}
          <div className="absolute inset-0 bg-[conic-gradient(from_90deg_at_50%_50%,#090e1c_0%,#0f172a_50%,#090e1c_100%)] rounded-full shadow-[inset_-40px_-40px_100px_rgba(0,0,0,0.9),0_0_100px_rgba(0,212,255,0.15)] border border-[#1e293b]/50 overflow-hidden">
            
            {/* Vague Continent Silhouettes (using radial gradients to fake it) */}
            <div className="absolute top-[20%] left-[10%] w-[40%] h-[30%] bg-[#050810] rounded-full filter blur-3xl opacity-60" />
            <div className="absolute top-[50%] right-[15%] w-[35%] h-[40%] bg-[#050810] rounded-full filter blur-3xl opacity-60" />
            
            {/* Atmospheric Glow Ring */}
            <div className="absolute inset-0 rounded-full border-t border-[rgba(0,212,255,0.3)] filter blur-sm" />
            
            {/* Scan Grid Overlay appearing over Earth */}
            <motion.div 
              style={{ opacity: gridOpacity }}
              className="absolute inset-0 bg-[linear-gradient(rgba(0,212,255,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(0,212,255,0.1)_1px,transparent_1px)] bg-[size:40px_40px]"
            />
          </div>
        </div>
      </motion.div>

      {/* EO Satellite Container */}
      <motion.div
        className="absolute top-[20%] right-[20%] w-64 h-64 flex justify-center items-center"
        style={{
          scale: satScale,
          x: satX,
          y: satY,
          opacity: satOpacity,
          rotate: satRotate,
        }}
      >
        <svg viewBox="0 0 200 200" className="w-full h-full drop-shadow-[0_0_15px_rgba(0,212,255,0.4)]" aria-label="EO Satellite">
          <defs>
            <linearGradient id="satPanel" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#004c5e" />
              <stop offset="100%" stopColor="#0a0f1e" />
            </linearGradient>
            <linearGradient id="satBody" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#e2e8f0" />
              <stop offset="100%" stopColor="#94a3b8" />
            </linearGradient>
          </defs>
          {/* Left Solar Panel */}
          <rect x="10" y="80" width="60" height="40" fill="url(#satPanel)" stroke="#00d4ff" strokeWidth="1" />
          <line x1="25" y1="80" x2="25" y2="120" stroke="#00d4ff" strokeWidth="0.5" opacity="0.5" />
          <line x1="40" y1="80" x2="40" y2="120" stroke="#00d4ff" strokeWidth="0.5" opacity="0.5" />
          <line x1="55" y1="80" x2="55" y2="120" stroke="#00d4ff" strokeWidth="0.5" opacity="0.5" />
          
          {/* Right Solar Panel */}
          <rect x="130" y="80" width="60" height="40" fill="url(#satPanel)" stroke="#00d4ff" strokeWidth="1" />
          <line x1="145" y1="80" x2="145" y2="120" stroke="#00d4ff" strokeWidth="0.5" opacity="0.5" />
          <line x1="160" y1="80" x2="160" y2="120" stroke="#00d4ff" strokeWidth="0.5" opacity="0.5" />
          <line x1="175" y1="80" x2="175" y2="120" stroke="#00d4ff" strokeWidth="0.5" opacity="0.5" />
          
          {/* Main Body */}
          <rect x="75" y="60" width="50" height="80" fill="url(#satBody)" rx="4" />
          
          {/* Golden Foil Details */}
          <rect x="80" y="65" width="40" height="70" fill="#ffaa00" opacity="0.8" />
          <path d="M80 75 h40 M80 85 h40 M80 95 h40 M80 105 h40 M80 115 h40 M80 125 h40" stroke="#d97706" strokeWidth="1" />
          
          {/* Antenna Dish */}
          <path d="M 85 60 C 85 40, 115 40, 115 60" fill="none" stroke="#e2e8f0" strokeWidth="3" />
          <circle cx="100" cy="50" r="3" fill="#00d4ff" className="animate-pulse" />
          
          {/* Connection Arms */}
          <rect x="70" y="95" width="5" height="10" fill="#94a3b8" />
          <rect x="125" y="95" width="5" height="10" fill="#94a3b8" />
        </svg>
      </motion.div>
      
    </div>
  );
}
