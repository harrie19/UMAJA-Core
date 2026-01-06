/**
 * Lighting Component
 * Studio lighting setup for the White Lab environment
 */

import { CONFIG } from '@/lib/config';

export function Lighting() {
  return (
    <>
      {/* Ambient light for overall scene illumination */}
      <ambientLight intensity={CONFIG.lighting.ambient.intensity} />
      
      {/* Key light - main directional light from top-right */}
      <directionalLight
        position={CONFIG.lighting.directional.position}
        intensity={CONFIG.lighting.directional.intensity}
        castShadow
      />
      
      {/* Fill light - subtle light from left to reduce harsh shadows */}
      <pointLight
        position={CONFIG.lighting.fill.position}
        intensity={CONFIG.lighting.fill.intensity}
      />
      
      {/* Rim light - from behind to create separation */}
      <pointLight
        position={CONFIG.lighting.rim.position}
        intensity={CONFIG.lighting.rim.intensity}
      />
      
      {/* Simple hemisphere light for soft ambient lighting instead of Environment */}
      <hemisphereLight
        args={['#ffffff', '#8888ff', 0.4]}
        position={[0, 50, 0]}
      />
    </>
  );
}
