import React from 'react';
import { ArrowRight, Database, Cpu, Network, LayoutDashboard } from 'lucide-react';

export default function Architecture() {
  const flowSteps = [
    { icon: <Database className="w-6 h-6" />, label: "ISRO Satellite" },
    { icon: <Cpu className="w-6 h-6" />, label: "CNN Model" },
    { icon: <Network className="w-6 h-6" />, label: "Temporal Engine" },
    { icon: <BrainIcon className="w-6 h-6" />, label: "LLM Report Generator" },
    { icon: <LayoutDashboard className="w-6 h-6" />, label: "Next.js Dashboard" }
  ];

  return (
    <section id="architecture" className="py-24 relative z-10 w-full mb-20 bg-transparent">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        <div className="glass-panel p-8 md:p-12 border border-[#1e253b] bg-[#0d1323]/90 relative overflow-hidden">
          {/* subtle background glow */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[80%] h-[80%] bg-primary/5 blur-[120px] rounded-full pointer-events-none" />

          <div className="text-center mb-16 relative z-10">
            <h2 className="font-sans text-3xl md:text-5xl font-bold text-white mb-4">
              System Architecture
            </h2>
            <p className="text-foreground-muted max-w-2xl mx-auto">
              A decoupled, asymmetric microservices design to handle high-bandwidth telemetry and variable inference loads.
            </p>
          </div>

          {/* Visual Flow Diagram */}
          <div className="relative z-10 flex flex-col md:flex-row items-center justify-between mb-20">
            {flowSteps.map((step, index) => (
              <React.Fragment key={index}>
                <div className="flex flex-col items-center group">
                  <div className="w-16 h-16 rounded-2xl bg-[#13192b] border border-white/10 flex items-center justify-center text-primary mb-4 group-hover:border-primary/50 group-hover:shadow-[0_0_15px_rgba(0,212,255,0.3)] transition-all duration-300">
                    {step.icon}
                  </div>
                  <span className="text-sm font-bold text-white tracking-wide text-center max-w-[120px]">
                    {step.label}
                  </span>
                </div>
                {index < flowSteps.length - 1 && (
                  <div className="hidden md:flex text-[#434759] mx-2">
                    <ArrowRight className="w-6 h-6" />
                  </div>
                )}
                {index < flowSteps.length - 1 && (
                  <div className="md:hidden text-[#434759] my-4 transform rotate-90">
                    <ArrowRight className="w-6 h-6" />
                  </div>
                )}
              </React.Fragment>
            ))}
          </div>

          {/* Technical Specs */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 relative z-10 mb-12">
            {/* CNN Column */}
            <div className="p-6 rounded-2xl bg-[#090e1c]/80 border border-white/5 group hover:border-[#00ff88]/30 transition-colors">
              <h3 className="text-[#00ff88] font-mono text-xs tracking-[0.2em] font-bold mb-4 uppercase">
                Vision Engine
              </h3>
              <ul className="space-y-4">
                <li className="flex items-start gap-3 text-sm text-foreground-muted">
                  <div className="mt-1 w-1.5 h-1.5 rounded-full bg-[#00ff88]" />
                  <span><strong>Architecture:</strong> Hybrid DeepLabV3+ with ResNet50 backbone for spatial precision.</span>
                </li>
                <li className="flex items-start gap-3 text-sm text-foreground-muted">
                  <div className="mt-1 w-1.5 h-1.5 rounded-full bg-[#00ff88]" />
                  <span><strong>Input Telemetry:</strong> 4-channel multi-spectral (Red, Green, Blue, SWIR).</span>
                </li>
                <li className="flex items-start gap-3 text-sm text-foreground-muted">
                  <div className="mt-1 w-1.5 h-1.5 rounded-full bg-[#00ff88]" />
                  <span><strong>Output Tensor:</strong> 4-class semantic segmentation (Vegetation, Water, Built-up, Barren).</span>
                </li>
              </ul>
            </div>

            {/* LLM Column */}
            <div className="p-6 rounded-2xl bg-[#090e1c]/80 border border-white/5 group hover:border-primary/30 transition-colors">
              <h3 className="text-primary font-mono text-xs tracking-[0.2em] font-bold mb-4 uppercase">
                Reasoning Engine
              </h3>
              <ul className="space-y-4">
                <li className="flex items-start gap-3 text-sm text-foreground-muted">
                  <div className="mt-1 w-1.5 h-1.5 rounded-full bg-primary" />
                  <span><strong>Model Size:</strong> 120B parameter open-weight LLM, natively quantized.</span>
                </li>
                <li className="flex items-start gap-3 text-sm text-foreground-muted">
                  <div className="mt-1 w-1.5 h-1.5 rounded-full bg-primary" />
                  <span><strong>Memory Management:</strong> Recursive Context Manager to handle multi-year diff arrays.</span>
                </li>
                <li className="flex items-start gap-3 text-sm text-foreground-muted">
                  <div className="mt-1 w-1.5 h-1.5 rounded-full bg-primary" />
                  <span><strong>Security context:</strong> Strict location and time-range context locks to prevent hallucination.</span>
                </li>
              </ul>
            </div>
          </div>

          <div className="pt-6 border-t border-white/10 text-center relative z-10">
            <p className="text-xs text-[#707588] font-mono leading-relaxed">
              Frontend runs on mock API endpoints (/api/analyze, /api/chat).<br />
              Backend CNN/LLM integration ready via strict API contracts.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

// Simple Brain icon for the flow diagram since Brain isn't imported from lucide
function BrainIcon(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z" />
      <path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z" />
      <path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4" />
      <path d="M17.599 6.5a3 3 0 0 0 .399-1.375" />
      <path d="M6.003 5.125A3 3 0 0 0 6.401 6.5" />
      <path d="M3.477 10.896a4 4 0 0 1 .585-.396" />
      <path d="M19.938 10.5a4 4 0 0 1 .585.396" />
      <path d="M6 18a4 4 0 0 1-1.967-.516" />
      <path d="M19.967 17.484A4 4 0 0 1 18 18" />
    </svg>
  );
}
