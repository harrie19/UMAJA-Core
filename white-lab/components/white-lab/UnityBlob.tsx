/**
 * Unity Blob Component
 * The iridescent, morphing consciousness visualization
 */

'use client';

import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { MeshDistortMaterial } from '@react-three/drei';
import * as THREE from 'three';
import { CONFIG } from '@/lib/config';

export function UnityBlob() {
  const meshRef = useRef<THREE.Mesh>(null);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const materialRef = useRef<any>(null);

  useFrame((state) => {
    if (!meshRef.current) return;

    // Gentle pulsing animation
    const pulse = Math.sin(state.clock.elapsedTime * 0.5) * 0.05;
    const scale = CONFIG.blob.animation.pulseMin + pulse;
    meshRef.current.scale.set(scale, scale, scale);

    // Slow rotation on Y-axis
    meshRef.current.rotation.y += CONFIG.blob.animation.rotationSpeed;

    // Dynamic iridescent color shift
    if (materialRef.current) {
      const hue = (state.clock.elapsedTime * 0.05) % 1;
      const color = new THREE.Color().setHSL(hue, 0.7, 0.9);
      materialRef.current.color = color;
    }
  });

  return (
    <mesh ref={meshRef} position={CONFIG.blob.position} castShadow>
      <sphereGeometry 
        args={[
          1, 
          CONFIG.blob.geometry.segments, 
          CONFIG.blob.geometry.segments
        ]} 
      />
      <MeshDistortMaterial
        ref={materialRef}
        distort={CONFIG.blob.distort}
        speed={CONFIG.blob.speed}
        metalness={CONFIG.blob.metalness}
        roughness={CONFIG.blob.roughness}
        color="#ffffff"
        emissive="#ffffff"
        emissiveIntensity={0.2}
      />
    </mesh>
  );
}
