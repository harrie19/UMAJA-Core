/**
 * Scene Component
 * Main Three.js scene container that combines all elements
 */

'use client';

import { Canvas } from '@react-three/fiber';
import { UnityBlob } from './UnityBlob';
import { WhiteRoom } from './WhiteRoom';
import { Lighting } from './Lighting';
import { Camera } from './Camera';

export function Scene() {
  return (
    <div className="w-full h-screen">
      <Canvas
        shadows
        gl={{
          antialias: true,
          alpha: false,
          powerPreference: 'high-performance',
        }}
        dpr={[1, 2]}
      >
        <color attach="background" args={['#ffffff']} />
        <fog attach="fog" args={['#ffffff', 10, 50]} />
        
        <Camera />
        <Lighting />
        <WhiteRoom />
        <UnityBlob />
      </Canvas>
    </div>
  );
}
