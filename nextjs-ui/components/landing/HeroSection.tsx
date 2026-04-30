'use client';

import React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';

export default function HeroSection() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0.3,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.8 } },
  };

  const stats = [
    { value: '36', label: 'Regions' },
    { value: '6', label: 'Years of Data' },
    { value: '3', label: 'Risk Dimensions' },
  ];

  return (
    <section className="relative min-h-screen flex items-center justify-center bg-transparent z-10 pt-20">
      <div className="absolute inset-0 bg-gradient-to-b from-[#050810]/80 via-transparent to-[#050810]/90 pointer-events-none" />
      
      <div className="relative z-10 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center flex flex-col items-center">
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="w-full flex flex-col items-center"
        >
          {/* Label Pill */}
          <motion.div variants={itemVariants} className="mb-8">
            <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/5 border border-white/10 backdrop-blur-md text-xs font-semibold tracking-widest text-primary uppercase">
              <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
              ISRO Satellite Intelligence Platform
            </span>
          </motion.div>

          {/* Headline */}
          <motion.h1 variants={itemVariants} className="font-sans text-5xl md:text-7xl font-bold tracking-tight text-white mb-6 leading-tight">
            Predict Natural Disasters.<br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-secondary-accent">
              Before They Strike.
            </span>
          </motion.h1>

          {/* Subheading */}
          <motion.p variants={itemVariants} className="max-w-3xl text-lg md:text-xl text-foreground-muted mb-12 leading-relaxed">
            Autonomous analysis of ISRO satellite telemetry across India. AI-powered CNN segmentation + LLM risk intelligence for flood, heat, and land degradation forecasting.
          </motion.p>

          {/* CTAs */}
          <motion.div variants={itemVariants} className="flex flex-col sm:flex-row gap-6 mb-20 w-full sm:w-auto">
            <Link 
              href="/dashboard"
              className="px-8 py-4 rounded-full bg-primary text-[#002c37] font-bold text-lg hover:shadow-[0_0_30px_rgba(0,212,255,0.4)] transition-all duration-300 transform hover:-translate-y-1 flex items-center justify-center gap-2"
            >
              Launch the System &rarr;
            </Link>
            <a 
              href="#how-it-works"
              className="px-8 py-4 rounded-full bg-white/5 backdrop-blur-md border border-primary/30 text-white font-bold text-lg hover:bg-white/10 hover:border-primary transition-all duration-300 flex items-center justify-center gap-2"
            >
              See How It Works &darr;
            </a>
          </motion.div>

          {/* Stats Bar */}
          <motion.div variants={itemVariants} className="w-full max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 pt-10 border-t border-white/10">
            {stats.map((stat, i) => (
              <div key={i} className="flex flex-col items-center">
                <div className="font-sans text-4xl md:text-5xl font-black text-white mb-2">
                  {stat.value}
                </div>
                <div className="text-sm font-semibold tracking-widest uppercase text-foreground-muted">
                  {stat.label}
                </div>
              </div>
            ))}
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
