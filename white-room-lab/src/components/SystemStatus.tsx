'use client';

import { useState, useEffect } from 'react';
import { useFrame } from '@react-three/fiber';
import { SystemMetrics } from '@/types';

export default function SystemStatus() {
  const [metrics, setMetrics] = useState<SystemMetrics>({
    fps: 60,
    objectCount: 1,
    physicsActive: true,
    currentForm: 'bubble',
    activeSimulations: 0,
  });

  const [fps, setFps] = useState(60);
  const [frameCount, setFrameCount] = useState(0);
  const [lastTime, setLastTime] = useState(Date.now());

  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      const delta = (now - lastTime) / 1000;
      const currentFps = Math.round(frameCount / delta);
      
      setFps(currentFps || 60);
      setFrameCount(0);
      setLastTime(now);
      
      setMetrics(prev => ({
        ...prev,
        fps: currentFps || 60,
      }));
    }, 1000);

    return () => clearInterval(interval);
  }, [frameCount, lastTime]);

  const getStatusColor = (value: number, threshold: number) => {
    return value >= threshold ? 'text-green-500' : 'text-yellow-500';
  };

  return (
    <div className="bg-white/90 backdrop-blur-sm rounded-lg shadow-lg p-4 min-w-[200px]">
      <h3 className="text-sm font-bold text-gray-700 mb-3 border-b border-gray-200 pb-2">
        System Status
      </h3>
      
      <div className="space-y-2 text-xs font-mono">
        <div className="flex justify-between items-center">
          <span className="text-gray-600">FPS:</span>
          <span className={`font-bold ${getStatusColor(metrics.fps, 50)}`}>
            {metrics.fps}
          </span>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-gray-600">Objects:</span>
          <span className="font-bold text-blue-600">{metrics.objectCount}</span>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-gray-600">Physics:</span>
          <span className={`font-bold ${metrics.physicsActive ? 'text-green-500' : 'text-red-500'}`}>
            {metrics.physicsActive ? '🟢 Active' : '🔴 Inactive'}
          </span>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-gray-600">Form:</span>
          <span className="font-bold text-purple-600">{metrics.currentForm}</span>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-gray-600">Simulations:</span>
          <span className="font-bold text-orange-600">{metrics.activeSimulations}</span>
        </div>
      </div>
      
      <div className="mt-3 pt-3 border-t border-gray-200">
        <div className="text-xs text-gray-500 text-center">
          🔵 White Room Lab v0.1
        </div>
      </div>
    </div>
  );
}
