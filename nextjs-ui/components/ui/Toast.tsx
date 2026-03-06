"use client";
import { motion, AnimatePresence } from 'framer-motion';
import { AlertCircle, CheckCircle2, X } from 'lucide-react';
import { useEffect } from 'react';

export type ToastType = 'success' | 'error' | 'warning';

interface ToastProps {
  id: string;
  message: string;
  type: ToastType;
  onClose: (id: string) => void;
}

export const Toast = ({ id, message, type, onClose }: ToastProps) => {
  useEffect(() => {
    const timer = setTimeout(() => onClose(id), 4000);
    return () => clearTimeout(timer);
  }, [id, onClose]);

  const typeConfig = {
    success: { icon: CheckCircle2, color: 'text-alert-low', border: 'border-alert-low/50' },
    warning: { icon: AlertCircle, color: 'text-alert-medium', border: 'border-alert-medium/50' },
    error: { icon: AlertCircle, color: 'text-alert-high', border: 'border-alert-high/50' },
  };

  const Icon = typeConfig[type].icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: -20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95, transition: { duration: 0.2 } }}
      className={`glass-panel border-l-4 pr-12 pl-4 py-3 relative flex items-center gap-3 ${typeConfig[type].border}`}
    >
      <Icon className={`w-5 h-5 shrink-0 ${typeConfig[type].color}`} />
      <span className="font-mono text-sm text-white/90">{message}</span>
      <button 
        onClick={() => onClose(id)}
        className="absolute right-3 text-white/50 hover:text-white transition-colors"
      >
        <X className="w-4 h-4" />
      </button>
    </motion.div>
  );
};

export const ToastContainer = ({ toasts, removeToast }: { toasts: Omit<ToastProps, 'onClose'>[], removeToast: (id: string) => void }) => {
  return (
    <div className="fixed top-6 right-6 z-50 flex flex-col gap-3 min-w-[300px] pointer-events-none">
      <AnimatePresence>
        {toasts.map(toast => (
          <div key={toast.id} className="pointer-events-auto">
            <Toast {...toast} onClose={removeToast} />
          </div>
        ))}
      </AnimatePresence>
    </div>
  );
};
