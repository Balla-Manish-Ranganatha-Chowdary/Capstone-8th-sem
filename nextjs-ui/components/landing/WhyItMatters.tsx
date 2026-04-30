import React from 'react';
import { ThermometerSun, Search, BrainCircuit } from 'lucide-react';

export default function WhyItMatters() {
  const cards = [
    {
      title: "Climate Risk Is Accelerating",
      description: "India faces increasing frequency of floods, droughts, and extreme heat events. Early detection is no longer optional—it is a critical national requirement.",
      icon: <ThermometerSun className="w-8 h-8 text-primary" />,
      glowClass: "group-hover:shadow-[0_0_25px_rgba(0,212,255,0.2)] group-hover:border-primary/50",
      iconGlow: "text-primary filter drop-shadow-[0_0_8px_rgba(0,212,255,0.8)]"
    },
    {
      title: "Manual Analysis Can't Scale",
      description: "Human review of satellite data is too slow for real-time disaster preparedness at national scale. The volume of petabyte-level telemetry demands autonomous processing.",
      icon: <Search className="w-8 h-8 text-[#ffaa00]" />,
      glowClass: "group-hover:shadow-[0_0_25px_rgba(255,170,0,0.2)] group-hover:border-[#ffaa00]/50",
      iconGlow: "text-[#ffaa00] filter drop-shadow-[0_0_8px_rgba(255,170,0,0.8)]"
    },
    {
      title: "AI Closes the Gap",
      description: "Deep learning segmentation combined with LLM reasoning converts raw satellite telemetry into actionable, localized risk intelligence in minutes, not months.",
      icon: <BrainCircuit className="w-8 h-8 text-[#00ff88]" />,
      glowClass: "group-hover:shadow-[0_0_25px_rgba(0,255,136,0.2)] group-hover:border-[#00ff88]/50",
      iconGlow: "text-[#00ff88] filter drop-shadow-[0_0_8px_rgba(0,255,136,0.8)]"
    }
  ];

  return (
    <section className="py-24 relative z-10 w-full mb-20 bg-transparent">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="font-sans text-3xl md:text-5xl font-bold text-white mb-4">
            Why It Matters
          </h2>
          <div className="h-1 w-20 bg-primary mx-auto rounded-full shadow-[0_0_10px_rgba(0,212,255,0.5)]" />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {cards.map((card, index) => (
            <div 
              key={index}
              className={`group relative glass-panel p-8 bg-[#0d1323]/80 border border-white/5 transition-all duration-500 hover:-translate-y-2 cursor-default ${card.glowClass}`}
            >
              <div className="mb-6 intial-scale-100 group-hover:scale-110 transition-transform duration-300 origin-left">
                <div className={card.iconGlow}>
                  {card.icon}
                </div>
              </div>
              
              <h3 className="text-xl font-bold text-white mb-4 tracking-wide group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-foreground-muted transition-colors duration-300">
                {card.title}
              </h3>
              
              <p className="text-foreground-muted leading-relaxed">
                {card.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
