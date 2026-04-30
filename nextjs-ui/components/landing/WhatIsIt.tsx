import React from 'react';

export default function WhatIsIt() {
  const dataLayers = [
    { label: 'Vegetation', percentage: 38, color: 'bg-emerald-500', glow: 'shadow-[0_0_10px_#10b981]' },
    { label: 'Built-up', percentage: 31, color: 'bg-orange-500', glow: 'shadow-[0_0_10px_#f97316]' },
    { label: 'Barren', percentage: 19, color: 'bg-amber-400', glow: 'shadow-[0_0_10px_#fbbf24]' },
    { label: 'Water', percentage: 12, color: 'bg-cyan-500', glow: 'shadow-[0_0_10px_#06b6d4]' },
  ];

  return (
    <section id="what-is-it" className="py-24 relative z-10 w-full mb-20 bg-transparent">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          
          {/* Left Column: Content */}
          <div className="flex flex-col">
            <div className="mb-4 inline-block">
              <span className="text-xs font-bold tracking-[0.2em] text-primary uppercase border-l-2 border-primary pl-3">
                The Technology
              </span>
            </div>
            
            <h2 className="font-sans text-4xl md:text-5xl font-bold text-white mb-6 leading-tight">
              Satellite Eyes.<br />
              <span className="text-foreground-muted">AI Brain. Ground Truth.</span>
            </h2>
            
            <div className="space-y-6 text-foreground-muted text-lg leading-relaxed">
              <p>
                The system ingests raw multi-spectral telemetry (RGB + SWIR bands) directly from ISRO's earth-observation constellation. 
                Unlike standard optical imagery, the Short-Wave Infrared allows us to penetrate atmospheric haze and assess precise moisture content.
              </p>
              <p>
                A bespoke Convolutional Neural Network (ensembling DeepLabV3+ and ResNet50) autonomously segments every square kilometer of the Indian subcontinent. 
                It classifies terrain into distinct categories: Vegetation, Water, Barren, and Built-up sprawl.
              </p>
              <p>
                By executing temporal diff analysis from 2019 through present day, the engine tracks micro-changes year-over-year, creating a predictive foundation for an integrated 120B parameter LLM to forecast disaster risks before they manifest.
              </p>
            </div>
          </div>

          {/* Right Column: Visualization Card */}
          <div className="relative w-full overflow-hidden">
            <div className="glass-panel p-8 relative">
              <div className="absolute top-0 right-0 p-4 opacity-50 text-xs font-mono text-primary tracking-widest">
                SYS.ANLZ.043
              </div>
              
              <h3 className="text-xl font-bold text-white mb-8 border-b border-white/10 pb-4">
                Global Land Cover Breakdown
              </h3>
              
              <div className="space-y-6">
                {dataLayers.map((layer, index) => (
                  <div key={index} className="flex flex-col gap-2">
                    <div className="flex justify-between items-end">
                      <span className="font-sans font-medium text-white tracking-wide">
                        {layer.label}
                      </span>
                      <span className="font-mono text-foreground-muted text-sm">
                        {layer.percentage}%
                      </span>
                    </div>
                    {/* Progress Bar Track */}
                    <div className="w-full h-3 bg-[#0d1323] rounded-full overflow-hidden">
                      {/* Progress Fill */}
                      <div 
                        className={`h-full ${layer.color} ${layer.glow} rounded-full transition-all duration-1000 ease-out`}
                        style={{ width: `${layer.percentage}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>

              {/* Decorative scanline */}
              <div className="scanline" />
            </div>
          </div>
          
        </div>
      </div>
    </section>
  );
}
