import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#050A14", 
        foreground: "#FFFFFF",
        primary: "#00D4FF", // Electric cyan
        secondary: "#1E293B", // Dark slate
        card: "rgba(15, 23, 42, 0.7)", // Glassmorphism base
        alert: {
          low: "#10B981", // Green
          medium: "#F59E0B", // Amber
          high: "#EF4444", // Red
        }
      },
      fontFamily: {
        sans: ['var(--font-space-grotesk)'],
        mono: ['var(--font-jetbrains-mono)'],
      },
      backgroundImage: {
        'cyan-gradient': 'linear-gradient(135deg, #00D4FF 0%, #0072FF 100%)',
      },
      animation: {
        'radar-sweep': 'radar-sweep 2s linear infinite',
        'ripple': 'ripple 2s cubic-bezier(0, 0.2, 0.8, 1) infinite',
      },
      keyframes: {
        'radar-sweep': {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
        'ripple': {
          '0%': {
            top: '50%',
            left: '50%',
            width: '0',
            height: '0',
            opacity: '1',
            transform: 'translate(-50%, -50%)',
          },
          '100%': {
            top: '50%',
            left: '50%',
            width: '60px',
            height: '60px',
            opacity: '0',
            transform: 'translate(-50%, -50%)',
          },
        }
      }
    },
  },
  plugins: [],
};
export default config;
