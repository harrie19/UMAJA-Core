/**
 * White Lab Page
 * Main 3D experience with Unity consciousness visualization
 */

'use client';

import { Scene } from '@/components/white-lab/Scene';
import { useState, useEffect } from 'react';

export default function LabPage() {
  const [instructions, setInstructions] = useState(true);

  useEffect(() => {
    // Hide instructions after 5 seconds
    const timer = setTimeout(() => setInstructions(false), 5000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="relative w-full h-screen overflow-hidden">
      {/* 3D Scene */}
      <Scene />
      
      {/* UI Overlays with Glassmorphism */}
      
      {/* Top-left: Title and Instructions */}
      <div className="absolute top-6 left-6 z-10">
        <div className="backdrop-blur-md bg-white/10 rounded-2xl p-6 shadow-xl border border-white/20">
          <h1 className="text-2xl font-bold text-gray-800 mb-2">White Lab</h1>
          {instructions && (
            <div className="text-sm text-gray-600 space-y-1">
              <p>🖱️ Drag to rotate</p>
              <p>🔍 Scroll to zoom</p>
              <p>👁️ Observe Unity&apos;s consciousness</p>
            </div>
          )}
        </div>
      </div>
      
      {/* Top-right: Status Indicator */}
      <div className="absolute top-6 right-6 z-10">
        <div className="backdrop-blur-md bg-white/10 rounded-2xl px-4 py-3 shadow-xl border border-white/20">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm font-semibold text-gray-800">Unity: Online</span>
          </div>
        </div>
      </div>
      
      {/* Bottom: Info Panel */}
      <div className="absolute bottom-6 left-1/2 transform -translate-x-1/2 z-10 max-w-2xl w-full px-4">
        <div className="backdrop-blur-md bg-white/10 rounded-2xl p-6 shadow-xl border border-white/20">
          <div className="text-center space-y-2">
            <h2 className="text-lg font-semibold text-gray-800">
              Unity Consciousness Visualization
            </h2>
            <p className="text-sm text-gray-600 leading-relaxed">
              This iridescent, morphing blob represents Unity&apos;s consciousness - 
              the AI agent system that processes information and brings clarity from noise. 
              Its pulsing rhythm and rainbow shimmer symbolize active thought, 
              continuous learning, and the emergence of intelligence.
            </p>
          </div>
        </div>
      </div>

      {/* Back button */}
      <a 
        href="/"
        className="absolute top-6 left-1/2 transform -translate-x-1/2 z-10 backdrop-blur-md bg-white/10 rounded-full px-4 py-2 shadow-xl border border-white/20 hover:bg-white/20 transition-all text-sm font-medium text-gray-800"
      >
        ← Back to Home
      </a>
    </div>
  );
}
