"use client";
import { useEffect, useRef, useState } from 'react';
import { MapContainer, TileLayer, Marker, useMapEvents, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix Leaflet marker icon issue in Next.js
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Create custom glowing marker icon
const pulsingIcon = L.divIcon({
  className: 'custom-div-icon',
  html: `
    <div class="relative w-4 h-4 rounded-full bg-primary shadow-[0_0_10px_#00D4FF]">
      <div class="absolute inset-0 rounded-full animate-ripple border-2 border-primary/60"></div>
    </div>
  `,
  iconSize: [16, 16],
  iconAnchor: [8, 8],
});

interface IndiaMapProps {
  selectedLocation: { latitude: number; longitude: number } | null;
  onLocationSelect: (lat: number, lon: number) => void;
}

// Controller to handle programmatic fly-to
function MapController({ center }: { center: { latitude: number; longitude: number } | null }) {
  const map = useMap();
  
  useEffect(() => {
    if (center) {
      map.flyTo([center.latitude, center.longitude], 6, {
        animate: true,
        duration: 1.5,
        easeLinearity: 0.25,
      });
    }
  }, [center, map]);
  
  return null;
}

// Component to catch click events
function ClickHandler({ onSelect }: { onSelect: (lat: number, lon: number) => void }) {
  useMapEvents({
    click(e) {
      const { lat, lng } = e.latlng;
      // India approximate bounds
      if (lat >= 6 && lat <= 37 && lng >= 68 && lng <= 97) {
        onSelect(lat, lng);
      }
    },
  });
  return null;
}

export default function IndiaMap({ selectedLocation, onLocationSelect }: IndiaMapProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <div className="w-full h-full min-h-[500px] glass-panel flex items-center justify-center">
        <div className="w-8 h-8 md:w-16 md:h-16 border-2 border-primary border-t-transparent flex items-center justify-center rounded-full animate-spin" />
      </div>
    );
  }

  // India Center coordinates
  const defaultCenter: [number, number] = [20.5937, 78.9629];

  return (
    <div className="relative w-full h-full min-h-[500px] rounded-xl overflow-hidden border border-white/10 shadow-[0_0_30px_rgba(0,0,0,0.5)] bg-black">
      
      {/* Decorative Scanlines */}
      <div className="scanline" />
      
      {/* Vignette Overlay */}
      <div className="absolute inset-0 pointer-events-none z-[400] bg-[radial-gradient(circle_at_center,transparent_40%,rgba(0,0,0,0.8)_100%)]" />

      {/* Satellite Badge */}
      <div className="absolute top-4 right-4 z-[400] bg-black/80 backdrop-blur border border-primary/30 px-3 py-1.5 rounded flex items-center gap-2">
        <div className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
        <span className="text-[10px] font-mono text-primary tracking-widest uppercase">SATELLITE VIEW ACTIVE</span>
      </div>

      <MapContainer
        center={defaultCenter}
        zoom={5}
        minZoom={4}
        maxZoom={12}
        className="w-full h-full z-0"
        zoomControl={false}
        // India bounds approximately
        maxBounds={[
          [6.0, 68.0],
          [37.0, 97.0]
        ]}
      >
        <TileLayer
          attribution='&copy; <a href="https://carto.com/attributions">CARTO</a>'
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          className="filter contrast-[1.1] saturate-[1.2]"
        />
        
        {/* Draw India bounds box for visual effect */}
        {/* Skipping actual polygon for performance, sticking to Carto tiles + Bounds logic */}

        <ClickHandler onSelect={onLocationSelect} />
        <MapController center={selectedLocation} />

        {selectedLocation && (
          <Marker 
            position={[selectedLocation.latitude, selectedLocation.longitude]} 
            icon={pulsingIcon}
          />
        )}
      </MapContainer>
    </div>
  );
}
