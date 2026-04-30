import Navbar from '@/components/landing/Navbar';
import HeroSection from '@/components/landing/HeroSection';
import ParallaxScene from '@/components/landing/ParallaxScene';
import WhatIsIt from '@/components/landing/WhatIsIt';
import WhyItMatters from '@/components/landing/WhyItMatters';
import HowItWorks from '@/components/landing/HowItWorks';
import Capabilities from '@/components/landing/Capabilities';
import Architecture from '@/components/landing/Architecture';
import CtaSection from '@/components/landing/CtaSection';
import Footer from '@/components/landing/Footer';

export default function Home() {
  return (
    <main className="relative bg-[#050A14] min-h-screen selection:bg-primary/30 selection:text-white">
      {/* Background Parallax Layer */}
      <ParallaxScene />

      {/* Main Content Layers */}
      <div className="relative z-10 antialiased font-sans">
        <Navbar />
        
        <div className="flex flex-col gap-0 md:gap-12">
          {/* Hero Section */}
          <HeroSection />

          {/* Technology Explanation */}
          <WhatIsIt />

          {/* Value Prop */}
          <WhyItMatters />

          {/* Pipeline Stepper */}
          <HowItWorks />

          {/* Grid of Capabilities */}
          <Capabilities />

          {/* System Diagram & Specs */}
          <Architecture />

          {/* Final Call to Action combined with Earth visual space */}
          <CtaSection />
        </div>

        {/* Footer */}
        <Footer />
      </div>
    </main>
  );
}
