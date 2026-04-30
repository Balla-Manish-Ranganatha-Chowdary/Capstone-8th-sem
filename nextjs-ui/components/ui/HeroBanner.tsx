"use client";
import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

export const HeroBanner = () => {
  const [displayText, setDisplayText] = useState('');
  const fullText = "India Earth-Observation\nIntelligence System";
  
  // Typewriter effect logic
  useEffect(() => {
    let index = 0;
    const timeoutIds: NodeJS.Timeout[] = [];
    
    // Initial delay before typing starts
    const startDelay = setTimeout(() => {
      const typeChar = () => {
        if (index < fullText.length) {
          setDisplayText(fullText.slice(0, index + 1));
          index++;
          // Randomize typing speed slightly for natural feel (15ms - 45ms)
          timeoutIds.push(setTimeout(typeChar, Math.random() * 30 + 15));
        }
      };
      typeChar();
    }, 500);
    
    timeoutIds.push(startDelay);
    return () => timeoutIds.forEach(clearTimeout);
  }, []);

  return (
    <motion.div 
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
      className="py-8 relative z-10 w-full max-w-4xl"
    >
      <div className="text-[0.65rem] tracking-[0.25em] uppercase text-white/35 mb-3 font-mono">
        ISRO Satellite Intelligence
      </div>
      
      <h1 className="font-sans text-3xl md:text-5xl font-bold tracking-tight text-white leading-tight mb-4 min-h-[5rem] md:min-h-[7rem] whitespace-pre-line">
        {displayText}
        <span className="animate-pulse ml-1 inline-block bg-primary/80 w-3 h-8 md:h-10 -mb-1 md:-mb-2" />
      </h1>
      
      <motion.p 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5, duration: 0.8 }}
        className="text-sm md:text-base text-white/45 tracking-wide m-0"
      >
        Analyze environmental changes · Assess risks · Explore satellite insights
      </motion.p>
      
      <motion.div 
        initial={{ width: "0%" }}
        animate={{ width: "100%" }}
        transition={{ delay: 2.0, duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
        className="h-[1px] bg-white/10 mt-6"
      />
    </motion.div>
  );
};
