'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Satellite, Menu, X } from 'lucide-react';

export default function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { name: 'About', href: '#what-is-it' },
    { name: 'How It Works', href: '#how-it-works' },
    { name: 'Capabilities', href: '#capabilities' },
    { name: 'Architecture', href: '#architecture' },
  ];

  return (
    <nav
      className={`fixed top-0 w-full z-50 transition-all duration-300 ${
        isScrolled ? 'backdrop-blur-md bg-black/30 border-b border-white/5' : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Left: Logo */}
          <div className="flex-shrink-0 flex items-center gap-2 cursor-pointer">
            <Satellite className="h-8 w-8 text-primary" />
            <span className="font-sans font-bold text-xl tracking-wide text-white">
              EO Intelligence
            </span>
          </div>

          {/* Right: Desktop Nav */}
          <div className="hidden md:flex items-center gap-8">
            <div className="flex items-baseline gap-6">
              {navLinks.map((link) => (
                <Link
                  key={link.name}
                  href={link.href}
                  className="text-foreground-muted hover:text-white transition-colors text-sm uppercase tracking-wider font-semibold"
                >
                  {link.name}
                </Link>
              ))}
            </div>
            <Link
              href="/dashboard"
              className="px-6 py-2.5 rounded-full bg-gradient-to-r from-primary to-[#00d2fd] text-[#004c5e] font-bold text-sm hover:shadow-[0_0_15px_rgba(0,212,255,0.4)] transition-all duration-300"
            >
              Try Now
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-white hover:text-primary focus:outline-none p-2"
            >
              {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden absolute top-20 left-0 w-full bg-[#0a0f1e]/95 backdrop-blur-xl border-b border-white/10 shadow-2xl">
          <div className="px-4 pt-2 pb-6 space-y-1">
            {navLinks.map((link) => (
              <Link
                key={link.name}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className="block px-3 py-4 text-base font-semibold text-white border-b border-white/5"
              >
                {link.name}
              </Link>
            ))}
            <div className="pt-6 pb-2">
              <Link
                href="/dashboard"
                onClick={() => setMobileMenuOpen(false)}
                className="block w-full text-center px-6 py-3 rounded-full bg-primary text-[#004c5e] font-bold"
              >
                Try Now
              </Link>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}
