import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { MeshTransmissionMaterial } from '@react-three/drei';
import * as THREE from 'three';

interface IridescentBlobProps {
  position?: [number, number, number];
  status?: string;
}

/**
 * IridescentBlob - Central consciousness visualization
 * Iridescent sphere with chromatic aberration and transmission effects
 * Color/intensity reacts to reality check status
 */
export function IridescentBlob({ position = [0, 1, 0], status = 'OK' }: IridescentBlobProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const timeRef = useRef(0);

  // Determine color based on status
  const getColorByStatus = (status: string): string => {
    switch (status?.toUpperCase()) {
      case 'OK':
      case 'HEALTHY':
        return '#00ff88'; // Green tint
      case 'WARNING':
        return '#ffaa00'; // Yellow/orange tint
      case 'CRITICAL':
      case 'ERROR':
        return '#ff0044'; // Red tint
      default:
        return '#ffffff'; // White/neutral
    }
  };

  // Animate rotation and floating
  useFrame((state, delta) => {
    if (meshRef.current) {
      timeRef.current += delta;
      
      // Gentle rotation
      meshRef.current.rotation.x += delta * 0.1;
      meshRef.current.rotation.y += delta * 0.15;
      
      // Floating sin wave motion
      const floatY = Math.sin(timeRef.current * 0.5) * 0.2;
      meshRef.current.position.y = position[1] + floatY;
    }
  });

  const color = getColorByStatus(status);

  return (
    <mesh ref={meshRef} position={position}>
      <sphereGeometry args={[1, 128, 128]} />
      <MeshTransmissionMaterial
        transmission={1}
        thickness={0.8}
        roughness={0.1}
        chromaticAberration={0.5}
        anisotropicBlur={0.4}
        distortion={0.3}
        distortionScale={0.5}
        temporalDistortion={0.2}
        color={color}
        ior={1.5}
        transparent={true}
        opacity={0.9}
      />
    </mesh>
  );
}
