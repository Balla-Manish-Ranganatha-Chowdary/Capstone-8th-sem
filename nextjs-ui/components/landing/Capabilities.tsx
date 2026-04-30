import React from 'react';
import { Sprout, Building2, Waves, Flame, MountainSnow, MessageSquareText } from 'lucide-react';

export default function Capabilities() {
  const capabilities = [
    {
      title: "Vegetation Loss Detection",
      desc: "Autonomously identify deforestation and crop health degradation using NDWI and NDVI spectral indices.",
      icon: <Sprout className="w-8 h-8 text-[#00ff88]" />,
      gradient: "from-[rgba(0,255,136,0.05)]"
    },
    {
      title: "Urban Sprawl Mapping",
      desc: "Track unauthorized settlements and infrastructure expansion via synthetic aperture radar and SWIR anomalies.",
      icon: <Building2 className="w-8 h-8 text-[#00d4ff]" />,
      gradient: "from-[rgba(0,212,255,0.05)]"
    },
    {
      title: "Flood Risk Forecasting",
      desc: "Simulate hydrological dynamics by intersecting topological models with impending monsoon satellite telemetry.",
      icon: <Waves className="w-8 h-8 text-blue-400" />,
      gradient: "from-[rgba(96,165,250,0.05)]"
    },
    {
      title: "Heat Stress Assessment",
      desc: "Measure land surface temperature variations to map urban heat islands and agricultural thermal stress.",
      icon: <Flame className="w-8 h-8 text-[#ffaa00]" />,
      gradient: "from-[rgba(255,170,0,0.05)]"
    },
    {
      title: "Land Degradation Scoring",
      desc: "Assess topsoil erosion and desertification across arid regions using multi-temporal texture analysis.",
      icon: <MountainSnow className="w-8 h-8 text-rose-400" />,
      gradient: "from-[rgba(251,113,133,0.05)]"
    },
    {
      title: "Conversational Geo-Intelligence",
      desc: "Query spatial data using natural language. The 120B parameter LLM converts complex GIS queries into instant insights.",
      icon: <MessageSquareText className="w-8 h-8 text-purple-400" />,
      gradient: "from-[rgba(192,132,252,0.05)]"
    }
  ];

  return (
    <section id="capabilities" className="py-24 relative z-10 w-full mb-20 bg-transparent">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="font-sans text-3xl md:text-5xl font-bold text-white mb-4">
            What the System Detects
          </h2>
          <div className="h-1 w-24 bg-gradient-to-r from-transparent via-[#00ff88] to-transparent mx-auto rounded-full shadow-[0_0_10px_#00ff88]" />
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {capabilities.map((cap, i) => (
            <div 
              key={i}
              className={`group relative glass-panel p-8 bg-gradient-to-br ${cap.gradient} to-transparent border border-white/5 transition-all duration-300 hover:-translate-y-2 hover:shadow-[0_10px_30px_-10px_rgba(0,0,0,0.5)]`}
            >
              <div className="mb-6 flex justify-between items-start">
                <div className="p-3 rounded-xl bg-white/5 border border-white/10 shadow-[inset_0_1px_1px_rgba(255,255,255,0.1)] group-hover:scale-110 transition-transform duration-300">
                  {cap.icon}
                </div>
                <div className="text-white/10 font-mono text-sm tracking-widest font-bold group-hover:text-white/20 transition-colors">
                  0{i + 1}
                </div>
              </div>
              
              <h3 className="text-xl font-bold text-white mb-3">
                {cap.title}
              </h3>
              
              <p className="text-foreground-muted text-sm leading-relaxed">
                {cap.desc}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
