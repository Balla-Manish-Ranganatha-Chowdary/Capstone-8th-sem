"use client";
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import dynamic from 'next/dynamic';

import { StatusBar } from '@/components/ui/StatusBar';
import { Button } from '@/components/ui/Button';
import { ToastContainer, ToastType } from '@/components/ui/Toast';
import { LocationPanel } from '@/components/sidebar/LocationPanel';
import { TimeSelector } from '@/components/sidebar/TimeSelector';
import { MetricCard } from '@/components/analysis/MetricCard';
import { RiskBar, type RiskLevel } from '@/components/analysis/RiskBar';
import { ActionsList } from '@/components/analysis/ActionsList';
import { ChatPanel } from '@/components/chat/ChatPanel';

// Dynamic import for Leaflet map to strictly render client-side
const IndiaMap = dynamic(() => import('@/components/map/IndiaMap'), { ssr: false });

type ToastData = { id: string; message: string; type: ToastType };

interface StateData { name: string; latitude: number; longitude: number }

interface AnalysisResults {
  environmental_changes: {
    vegetation_change: number;
    water_change: number;
    built_up_change: number;
  };
  risk_forecast: {
    flood_risk: RiskLevel;
    heat_stress_risk: RiskLevel;
    land_degradation_risk: RiskLevel;
  };
  preventive_actions: {
    immediate: string[];
    medium_term: string[];
    long_term: string[];
  };
}

export default function Home() {
  const [mounted, setMounted] = useState(false);
  
  // Data State
  const [statesList, setStatesList] = useState<StateData[]>([]);
  
  // Selection State
  const [selectedState, setSelectedState] = useState<string | null>(null);
  const [selectedLocation, setSelectedLocation] = useState<{ latitude: number; longitude: number } | null>(null);
  const [startYear, setStartYear] = useState(2019);
  const [endYear, setEndYear] = useState(2024);
  
  // Analysis State
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState<AnalysisResults | null>(null);
  
  // UI State
  const [toasts, setToasts] = useState<ToastData[]>([]);

  useEffect(() => {
    setMounted(true);
    fetch('/api/states')
      .then(res => res.json())
      .then(data => setStatesList(data))
      .catch(() => addToast('Failed to load states data', 'error'));
  }, []);

  // Handlers
  const addToast = (message: string, type: ToastType = 'error') => {
    const id = Math.random().toString(36).substr(2, 9);
    setToasts(prev => [...prev, { id, message, type }]);
  };

  const removeToast = (id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  };

  const handleStateSelect = (stateName: string) => {
    const stateData = statesList.find(s => s.name === stateName);
    if (stateData) {
      if (selectedState !== stateName) setResults(null);
      setSelectedState(stateName);
      setSelectedLocation({ latitude: stateData.latitude, longitude: stateData.longitude });
    }
  };

  const handleMapClick = (lat: number, lon: number) => {
    if (selectedLocation?.latitude !== lat || selectedLocation?.longitude !== lon) {
      setResults(null); 
    }
    setSelectedLocation({ latitude: lat, longitude: lon });
    setSelectedState(null); // Clear dropdown selection when clicking custom point
  };

  const handleTimeChange = (start: number, end: number) => {
    setStartYear(start);
    setEndYear(end);
  };

  const handleAnalyze = async () => {
    if (!selectedLocation) {
      addToast('Please select a location on the map or from the dropdown first.', 'warning');
      return;
    }

    setIsAnalyzing(true);
    setResults(null);

    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          latitude: selectedLocation.latitude,
          longitude: selectedLocation.longitude,
          start_year: startYear,
          end_year: endYear
        })
      });

      if (!res.ok) {
        throw new Error('Analysis failed');
      }

      const data = await res.json();
      setResults(data);
      addToast('Analysis generated successfully', 'success');

    } catch (error) {
      addToast('Error communicating with intelligence backend.', 'error');
    } finally {
      setIsAnalyzing(false);
    }
  };

  if (!mounted) return null;

  return (
    <main className="min-h-screen pt-14 pb-6 px-4 md:px-6 flex flex-col items-center">
      <StatusBar />
      <ToastContainer toasts={toasts} removeToast={removeToast} />
      
      <div className="w-full max-w-[1800px] h-[calc(100vh-80px)] mt-4 grid grid-cols-1 xl:grid-cols-12 gap-6 relative">
        
        {/* LEFT SIDEBAR (Controls) */}
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="xl:col-span-3 flex flex-col gap-6 overflow-y-auto custom-scrollbar pr-2"
        >
          <LocationPanel 
            states={statesList}
            selectedState={selectedState}
            selectedLocation={selectedLocation}
            onStateSelect={handleStateSelect}
          />
          
          <TimeSelector 
            startYear={startYear}
            endYear={endYear}
            minYear={2019}
            maxYear={2024}
            onChange={handleTimeChange}
          />

          <Button 
            variant="primary" 
            onClick={handleAnalyze} 
            loading={isAnalyzing}
            className="w-full py-4 text-base shadow-[0_0_20px_rgba(0,212,255,0.2)]"
          >
            {isAnalyzing ? "Processing Data..." : "Run Analysis"}
          </Button>
        </motion.div>

        {/* CENTER PANEL (Map) */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="xl:col-span-6 h-[50vh] xl:h-full relative rounded-xl"
        >
          <IndiaMap 
            selectedLocation={selectedLocation} 
            onLocationSelect={handleMapClick} 
          />
        </motion.div>

        {/* RIGHT PANEL (Results) */}
        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="xl:col-span-3 flex flex-col gap-6 overflow-y-auto custom-scrollbar pl-2"
        >
          <div className="flex items-center gap-3 border-b border-white/10 pb-4">
            <div className="w-8 h-8 rounded shrink-0 bg-primary/20 flex items-center justify-center border border-primary/30">
              <span className="text-primary text-xl">📊</span>
            </div>
            <div>
              <h2 className="text-sm font-bold tracking-widest text-primary uppercase">Intelligence Report</h2>
              <p className="text-xs text-white/50 font-mono">
                {results ? 'ANALYSIS COMPLETE' : 'AWAITING DATA'}
              </p>
            </div>
          </div>

          <AnimatePresence mode="wait">
            {!results && !isAnalyzing && (
              <motion.div 
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex-1 flex flex-col items-center justify-center text-center p-8 gap-4 opacity-50"
              >
                <div className="w-16 h-16 rounded-full border border-white/20 border-dashed animate-[spin_10s_linear_infinite]" />
                <p className="font-mono text-xs tracking-widest">SELECT PARAMETERS<br/>AND RUN ANALYSIS</p>
              </motion.div>
            )}

            {isAnalyzing && (
              <motion.div 
                key="loading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex-1 flex flex-col items-center justify-center text-center p-8 gap-6"
              >
                <div className="relative w-20 h-20">
                  <div className="absolute inset-0 border-2 border-primary/30 rounded-full animate-ping" />
                  <div className="absolute inset-2 border-2 border-primary border-t-transparent rounded-full animate-spin" />
                </div>
                <div className="flex flex-col gap-2">
                  <p className="font-mono text-sm tracking-widest text-primary">ANALYZING SATELLITE DATA</p>
                  <p className="font-mono text-[10px] text-white/50 animate-pulse">Running neural network masks...</p>
                </div>
              </motion.div>
            )}

            {results && !isAnalyzing && (
              <motion.div 
                key="results"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="flex flex-col gap-6"
              >
                {/* Environmental Changes */}
                <div className="flex flex-col gap-3">
                  <h3 className="text-[10px] font-mono tracking-widest text-white/50 uppercase">Environmental Changes</h3>
                  <MetricCard title="Vegetation" value={results.environmental_changes.vegetation_change} type="vegetation" delay={0.1} />
                  <MetricCard title="Water Bodies" value={results.environmental_changes.water_change} type="water" delay={0.2} />
                  <MetricCard title="Built-up Area" value={results.environmental_changes.built_up_change} type="builtup" delay={0.3} />
                </div>

                {/* Risk Forecast */}
                <div className="glass-panel p-4 flex flex-col gap-4">
                  <h3 className="text-[10px] font-mono tracking-widest text-white/50 uppercase border-b border-white/10 pb-2">Risk Assessment</h3>
                  <RiskBar label="Flood Risk" level={results.risk_forecast.flood_risk} delay={0.4} />
                  <RiskBar label="Heat Stress" level={results.risk_forecast.heat_stress_risk} delay={0.5} />
                  <RiskBar label="Land Degradation" level={results.risk_forecast.land_degradation_risk} delay={0.6} />
                </div>

                {/* Actions List */}
                <ActionsList actions={results.preventive_actions} delay={0.7} />

              </motion.div>
            )}
          </AnimatePresence>

        </motion.div>

        <ChatPanel 
          isLocked={!results}
          stateName={selectedState}
          startYear={startYear}
          endYear={endYear}
        />

      </div>
    </main>
  );
}
