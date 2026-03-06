"use client";
import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MessageSquare, X, Send, Lock, Loader2 } from 'lucide-react';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatPanelProps {
  isLocked: boolean;
  stateName: string | null;
  startYear: number;
  endYear: number;
}

export const ChatPanel = ({ isLocked, stateName, startYear, endYear }: ChatPanelProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  // Clear chat if state changes
  useEffect(() => {
    setMessages([]);
    setIsOpen(false);
  }, [stateName]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isLocked || isTyping) return;

    const userMsg = query.trim();
    setQuery('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setIsTyping(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: userMsg,
          state: stateName || 'Unknown Region',
          start_year: startYear,
          end_year: endYear
        })
      });

      if (!res.ok) throw new Error('API Error');

      const data = await res.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
      
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: "Connection error. Unable to reach analyst." }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <>
      <div className="fixed bottom-6 right-6 z-40">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className={`flex items-center gap-3 px-6 py-4 rounded-full shadow-2xl transition-all duration-300 font-mono text-sm tracking-wider uppercase font-bold border ${
            isLocked 
              ? 'bg-secondary/80 text-white/40 border-white/10 cursor-not-allowed hover:bg-secondary'
              : 'bg-cyan-gradient text-[#050A14] hover:shadow-[0_0_20px_rgba(0,212,255,0.4)] hover:scale-105 border-transparent'
          }`}
          title={isLocked ? "Run an analysis first to unlock the assistant" : "Chat with Intelligence Analyst"}
        >
          {isLocked ? <Lock className="w-5 h-5" /> : <MessageSquare className="w-5 h-5" />}
          <span>ASK ANALYST</span>
        </button>
      </div>

      <AnimatePresence>
        {isOpen && !isLocked && (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 50, scale: 0.9 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="fixed bottom-24 right-6 z-50 w-full max-w-[400px] h-[500px] max-h-[70vh] glass-panel flex flex-col overflow-hidden border border-primary/30 shadow-[0_10px_40px_rgba(0,0,0,0.5)]"
          >
            {/* Header */}
            <div className="bg-primary/10 border-b border-primary/20 px-4 py-3 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                <span className="font-mono text-xs text-primary uppercase tracking-widest font-bold">INTELLIGENCE ANALYST</span>
              </div>
              <button onClick={() => setIsOpen(false)} className="text-white/50 hover:text-white transition-colors">
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Context Badge */}
            <div className="bg-black/40 border-b border-white/5 px-4 py-2">
              <span className="font-mono text-[10px] text-white/50 p-1 bg-white/5 rounded border border-white/10 uppercase tracking-widest block text-center">
                CONTEXT: {stateName} | {startYear === endYear ? startYear : `${startYear}-${endYear}`}
              </span>
            </div>

            {/* Chat Area */}
            <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 flex flex-col gap-4 custom-scrollbar">
              {messages.length === 0 && (
                <div className="h-full flex flex-col items-center justify-center opacity-50 text-center gap-2">
                  <MessageSquare className="w-8 h-8 text-primary mb-2" />
                  <p className="text-sm">Analyst standing by.</p>
                  <p className="text-xs text-white/50 font-mono">Ask about environmental changes, risks, or actions.</p>
                </div>
              )}
              
              {messages.map((msg, i) => (
                <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[85%] rounded-lg p-3 text-sm ${
                    msg.role === 'user' 
                      ? 'bg-primary/20 text-white border border-primary/30 rounded-br-none'
                      : 'bg-secondary/80 text-white/90 border border-white/10 rounded-bl-none'
                  }`}>
                    {msg.content}
                  </div>
                </div>
              ))}
              
              {isTyping && (
                <div className="flex justify-start">
                  <div className="bg-secondary/40 border border-white/10 rounded-lg rounded-bl-none p-3 flex gap-1 items-center">
                    <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ repeat: Infinity, duration: 1.5, delay: 0 }} className="w-1.5 h-1.5 rounded-full bg-primary" />
                    <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ repeat: Infinity, duration: 1.5, delay: 0.3 }} className="w-1.5 h-1.5 rounded-full bg-primary" />
                    <motion.div animate={{ opacity: [0.3, 1, 0.3] }} transition={{ repeat: Infinity, duration: 1.5, delay: 0.6 }} className="w-1.5 h-1.5 rounded-full bg-primary" />
                  </div>
                </div>
              )}
            </div>

            {/* Input */}
            <form onSubmit={handleSend} className="p-3 border-t border-white/10 bg-black/40 flex gap-2">
              <input
                type="text"
                value={query}
                onChange={e => setQuery(e.target.value)}
                placeholder="Message analyst..."
                className="flex-1 bg-transparent border border-white/10 focus:border-primary/50 rounded-lg px-4 py-2 text-sm text-white focus:outline-none transition-colors"
                disabled={isTyping}
              />
              <button 
                type="submit" 
                disabled={isTyping || !query.trim()}
                className="bg-primary/20 text-primary w-10 h-10 rounded-lg flex items-center justify-center hover:bg-primary/30 disabled:opacity-50 transition-colors border border-primary/30"
              >
                {isTyping ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
              </button>
            </form>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};
