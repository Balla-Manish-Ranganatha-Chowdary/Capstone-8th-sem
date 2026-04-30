import React from 'react';
import Link from 'next/link';
import { Satellite } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="w-full bg-[#050810] border-t border-white/5 pt-16 pb-8 relative z-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center md:items-start gap-8 border-b border-white/5 pb-12 mb-8">
          
          {/* Left: Brand */}
          <div className="flex flex-col items-center md:items-start">
            <div className="flex items-center gap-2 mb-4">
              <Satellite className="h-6 w-6 text-primary" />
              <span className="font-sans font-bold text-lg tracking-wide text-white">
                EO Intelligence
              </span>
            </div>
            <p className="text-sm text-foreground-muted max-w-xs text-center md:text-left">
              Advanced Earth-Observation platform powered by Deep Learning and LLM reasoning.
            </p>
          </div>

          {/* Center: Links */}
          <div className="flex gap-6">
            <Link href="#what-is-it" className="text-sm font-semibold text-foreground-muted hover:text-primary transition-colors uppercase tracking-wider">
              Technology
            </Link>
            <Link href="#how-it-works" className="text-sm font-semibold text-foreground-muted hover:text-primary transition-colors uppercase tracking-wider">
              Pipeline
            </Link>
            <Link href="#architecture" className="text-sm font-semibold text-foreground-muted hover:text-primary transition-colors uppercase tracking-wider">
              Architecture
            </Link>
          </div>

          {/* Right: Tagline */}
          <div className="text-center md:text-right">
            <h4 className="text-sm font-bold text-white uppercase tracking-widest border-b border-primary/30 inline-block pb-1">
              Data Source
            </h4>
            <p className="mt-3 text-sm text-foreground-muted">
              Built for ISRO satellite<br />telemetry research
            </p>
          </div>

        </div>

        {/* Bottom Strip */}
        <div className="flex flex-col md:flex-row justify-between items-center text-xs font-mono text-foreground-muted/50 gap-4">
          <p>
            &copy; {new Date().getFullYear()} India Earth-Observation Intelligence System.
          </p>
          <p>
            Architecture designed for educational and research purposes
          </p>
        </div>
      </div>
    </footer>
  );
}
