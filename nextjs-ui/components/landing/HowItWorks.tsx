import React from 'react';

export default function HowItWorks() {
  const steps = [
    {
      num: 1,
      title: "Satellite Acquisition",
      desc: "ISRO captures continuous RGB + SWIR imagery of the subcontinent."
    },
    {
      num: 2,
      title: "CNN Segmentation",
      desc: "DeepLabV3+ and ResNet50 classify millions of pixels into land cover groups."
    },
    {
      num: 3,
      title: "Temporal Analysis",
      desc: "Year-over-year spatial change detection engine identifies anomalies."
    },
    {
      num: 4,
      title: "LLM Risk Report",
      desc: "120B parameter model interprets data matrices into structured risk insights."
    },
    {
      num: 5,
      title: "Action Intelligence",
      desc: "Platform delivers immediate, medium, and long-term actionable strategies."
    }
  ];

  return (
    <section id="how-it-works" className="py-24 relative z-10 w-full mb-20 bg-[#060913]/80">
      <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-primary/50 to-transparent" />
      <div className="absolute inset-x-0 bottom-0 h-px bg-gradient-to-r from-transparent via-primary/20 to-transparent" />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-20">
          <h2 className="font-sans text-3xl md:text-5xl font-bold text-white mb-6">
            The Intelligence Pipeline
          </h2>
          <p className="text-foreground-muted max-w-2xl mx-auto">
            From geostationary orbit to actionable insight in under two minutes. Our architecture is built for absolute precision.
          </p>
        </div>

        {/* Desktop / Horizontal Stepper */}
        <div className="hidden md:block relative w-full pt-12 pb-8">
          {/* Connecting Line */}
          <div className="absolute top-[4.5rem] left-[10%] right-[10%] h-[2px] bg-[#1e253b] z-0" />
          <div className="absolute top-[4.5rem] left-[10%] w-[30%] h-[2px] bg-gradient-to-r from-primary to-[#00ff88] z-0 shadow-[0_0_10px_#00d4ff]" />

          <div className="relative z-10 grid grid-cols-5 gap-4">
            {steps.map((step, index) => {
              const isActive = index <= 1; // Highlight first 2 for visual effect
              return (
                <div key={index} className="flex flex-col items-center text-center group">
                  <div 
                    className={`w-12 h-12 rounded-full flex items-center justify-center font-mono font-bold text-lg mb-6 transition-all duration-500
                      ${isActive 
                        ? 'bg-[#0a0f1e] text-primary border-2 border-primary shadow-[0_0_20px_rgba(0,212,255,0.4)]' 
                        : 'bg-[#0a0f1e] text-foreground-muted border-2 border-[#1e253b] group-hover:border-primary/50 group-hover:text-white'
                      }`}
                  >
                    {step.num}
                  </div>
                  <h3 className={`text-sm font-bold tracking-widest uppercase mb-3 ${isActive ? 'text-white' : 'text-foreground-muted'}`}>
                    {step.title}
                  </h3>
                  <p className="text-xs text-foreground-muted/80 px-2 leading-relaxed">
                    {step.desc}
                  </p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Mobile / Vertical Stepper */}
        <div className="md:hidden relative border-l-2 border-[#1e253b] ml-6 pl-8 space-y-12">
          {/* Active section line overlay */}
          <div className="absolute top-0 bottom-0 left-[-2px] w-[2px] h-[35%] bg-gradient-to-b from-primary to-[#00ff88] shadow-[0_0_10px_#00d4ff]" />
          
          {steps.map((step, index) => {
             const isActive = index <= 1;
             return (
               <div key={index} className="relative">
                 <div 
                   className={`absolute -left-[3.5rem] w-10 h-10 rounded-full flex flex-col justify-center items-center font-mono font-bold
                     ${isActive 
                       ? 'bg-[#0a0f1e] text-primary border-2 border-primary shadow-[0_0_15px_rgba(0,212,255,0.4)]' 
                       : 'bg-[#0a0f1e] border-2 border-[#1e253b] text-foreground-muted'}`}
                 >
                   {step.num}
                 </div>
                 <h3 className={`text-lg font-bold mb-2 ${isActive ? 'text-white' : 'text-foreground-muted'}`}>
                   {step.title}
                 </h3>
                 <p className="text-sm text-foreground-muted leading-relaxed">
                   {step.desc}
                 </p>
               </div>
             );
          })}
        </div>
      </div>
    </section>
  );
}
