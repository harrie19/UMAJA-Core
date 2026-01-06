/**
 * Camera Component
 * Camera controls with OrbitControls for user interaction
 */

'use client';

import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import { CONFIG } from '@/lib/config';

export function Camera() {
  return (
    <>
      <PerspectiveCamera
        makeDefault
        position={CONFIG.camera.position}
        fov={CONFIG.camera.fov}
      />
      <OrbitControls
        enablePan={false}
        minDistance={CONFIG.camera.minDistance}
        maxDistance={CONFIG.camera.maxDistance}
        enableDamping
        dampingFactor={0.05}
        rotateSpeed={0.5}
      />
    </>
  );
}
