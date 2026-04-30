'use client';

import React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';

export default function CtaSection() {
  return (
    <section className="relative min-h-screen flex items-center justify-center bg-transparent z-10">
      <div className="absolute inset-0 bg-gradient-to-t from-[#050810] via-transparent to-transparent pointer-events-none" />
      
      <div className="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center flex flex-col items-center">
        
        <h2 className="font-sans text-5xl md:text-7xl font-bold tracking-tight text-white mb-6 leading-tight">
          Predict. Prevent. <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary-accent">Protect.</span>
        </h2>
        
        <p className="text-xl md:text-2xl text-foreground-muted mb-12 max-w-2xl leading-relaxed">
          Explore ISRO satellite intelligence for any state in India. Select a region, set your timeframe, and let the AI do the rest.
        </p>
        
        <div className="flex flex-col items-center">
          <motion.div
            animate={{ boxShadow: ['0 0 20px rgba(0,212,255,0.4)', '0 0 60px rgba(0,212,255,0.8)', '0 0 20px rgba(0,212,255,0.4)'] }}
            transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
            className="rounded-full rounded-full"
          >
            <Link 
              href="/dashboard"
              className="px-10 py-5 rounded-full bg-primary text-[#002c37] font-bold text-xl transition-all duration-300 transform hover:scale-105 flex items-center justify-center gap-3 relative overflow-hidden group"
            >
              <span className="relative z-10">Launch the System &rarr;</span>
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent -translate-x-[150%] skew-x-[-15deg] group-hover:transition-transform group-hover:duration-1000 group-hover:translate-x-[150%]" />
            </Link>
          </motion.div>
          
          <p className="mt-8 text-sm font-mono text-foreground-muted/70 flex items-center gap-2">
            No setup required <span className="text-primary">•</span> Mock data available <span className="text-primary">•</span> Backend integration ready
          </p>
        </div>

      </div>
    </section>
  );
}
