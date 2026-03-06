import { LucideIcon } from 'lucide-react';
import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'glass';
  icon?: LucideIcon;
  loading?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className = '', variant = 'primary', icon: Icon, loading, children, disabled, ...props }, ref) => {
    
    const baseStyles = "relative overflow-hidden inline-flex items-center justify-center gap-2 px-6 py-3 rounded-lg font-mono text-sm uppercase tracking-wider font-bold transition-all duration-300 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed";
    
    const variants = {
      primary: "bg-cyan-gradient text-[#050A14] hover:shadow-[0_0_20px_rgba(0,212,255,0.4)] hover:brightness-110",
      secondary: "bg-secondary text-white hover:bg-white/10 border border-white/10",
      glass: "glass-panel text-primary hover:bg-white/5",
    };

    return (
      <button 
        ref={ref}
        className={`${baseStyles} ${variants[variant]} ${className}`}
        disabled={loading || disabled}
        {...props}
      >
        {/* Radar hover effect for primary buttons */}
        {variant === 'primary' && !disabled && !loading && (
          <div className="absolute inset-0 opacity-0 hover:opacity-100 transition-opacity bg-[conic-gradient(from_0deg_at_50%_50%,rgba(0,0,0,0)_0%,rgba(255,255,255,0)_80%,rgba(255,255,255,0.4)_100%)] animate-radar-sweep pointer-events-none" />
        )}
        
        {loading ? (
          <div className="w-5 h-5 border-2 border-[currentColor] border-t-transparent rounded-full animate-spin" />
        ) : Icon ? (
          <Icon className="w-5 h-5" />
        ) : null}
        
        <span className="relative z-10">{children}</span>
      </button>
    );
  }
);
Button.displayName = 'Button';
