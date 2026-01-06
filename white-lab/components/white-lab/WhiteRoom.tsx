/**
 * White Room Component
 * Minimalist environment with reflective floor
 */

'use client';

import { MeshReflectorMaterial } from '@react-three/drei';
import { CONFIG } from '@/lib/config';

export function WhiteRoom() {
  const floorConfig = CONFIG.environment.floor;

  return (
    <>
      {/* Reflective floor */}
      <mesh rotation-x={-Math.PI / 2} position={[0, 0, 0]} receiveShadow>
        <planeGeometry args={[floorConfig.size, floorConfig.size]} />
        <MeshReflectorMaterial
          blur={floorConfig.blur}
          resolution={floorConfig.resolution}
          mixBlur={floorConfig.mixBlur}
          mixStrength={floorConfig.mixStrength}
          roughness={floorConfig.roughness}
          depthScale={floorConfig.depthScale}
          minDepthThreshold={floorConfig.minDepthThreshold}
          maxDepthThreshold={floorConfig.maxDepthThreshold}
          color={floorConfig.color}
          metalness={floorConfig.metalness}
          mirror={0}
        />
      </mesh>
      
      {/* Optional back wall - subtle light gray */}
      <mesh position={[0, 5, -10]}>
        <planeGeometry args={[20, 10]} />
        <meshStandardMaterial color="#f5f5f5" />
      </mesh>
    </>
  );
}
