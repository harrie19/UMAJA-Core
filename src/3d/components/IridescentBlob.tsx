import { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { MeshTransmissionMaterial, Text, Float } from '@react-three/drei';
import * as THREE from 'three';

interface IridescentBlobProps {
  position?: [number, number, number];
  status?: 'OK' | 'WARNING' | 'ERROR' | 'THINKING';
  label?: string;
  isThinking?: boolean;
  onClick?: () => void;
}

/**
 * UMAJA IridescentBlob - The living core of an AI Agent
 */
export function IridescentBlob({ 
  position = [0, 1, 0], 
  status = 'OK', 
  label = 'UMAJA Core',
  isThinking = false,
  onClick 
}: IridescentBlobProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);
  const timeRef = useRef(0);
  const scaleRef = useRef(1);

  // Helper for colors
  const getColorByStatus = (s: string, thinking: boolean): string => {
    if (hovered) return '#ffffff';
    if (thinking || s.toUpperCase() === 'THINKING') return '#00d4ff'; // Bright Blue
    switch (s.toUpperCase()) {
      case 'WARNING': return '#ffaa00';
      case 'ERROR': return '#ff0044';
      default: return '#00ff88'; // Harmony Green
    }
  };

  useFrame((state, delta) => {
    if (meshRef.current) {
      timeRef.current += delta;
      
      // Speed up animation if thinking
      const speedMultiplier = (isThinking || status === 'THINKING') ? 3.0 : 1.0;
      
      // Rotation
      meshRef.current.rotation.x += delta * 0.2 * speedMultiplier;
      meshRef.current.rotation.y += delta * 0.3 * speedMultiplier;
      
      // Spring-like scaling effect for interaction
      const targetScale = hovered ? 1.2 : 1.0;
      // Smooth interpolation for spring-like feel
      scaleRef.current += (targetScale - scaleRef.current) * 0.15;
      
      // Pulsating scale
      const pulse = 1 + Math.sin(timeRef.current * 2 * speedMultiplier) * 0.05;
      meshRef.current.scale.setScalar(scaleRef.current * pulse);
      
      // Floating motion
      const floatY = Math.sin(timeRef.current * 0.5) * 0.2;
      meshRef.current.position.y = position[1] + floatY;
    }
  });

  return (
    <group position={position}>
      <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
        <mesh
          ref={meshRef}
          onClick={(e) => {
            e.stopPropagation();
            onClick?.();
          }}
          onPointerOver={(e) => {
            e.stopPropagation();
            setHovered(true);
          }}
          onPointerOut={(e) => {
            e.stopPropagation();
            setHovered(false);
          }}
        >
          <sphereGeometry args={[1, 128, 128]} />
          <MeshTransmissionMaterial
            backside
            samples={4}
            thickness={1.5}
            chromaticAberration={0.6}
            anisotropy={0.3}
            distortion={0.5}
            distortionScale={0.5}
            temporalDistortion={0.1}
            transmission={1}
            color={getColorByStatus(status, isThinking)}
            roughness={0.1}
            ior={1.2}
          />
        </mesh>

        {/* Floating Label */}
        <Text
          position={[0, 1.5, 0]}
          fontSize={0.2}
          color="white"
          anchorX="center"
          anchorY="middle"
          font="https://fonts.gstatic.com/s/raleway/v22/1Ptxg8zYS_SKggPN4iEgvnxyumZJWZIK957p.woff"
        >
          {label}
        </Text>
        
        {/* Status indicator ring */}
        <mesh rotation-x={Math.PI / 2} position={[0, -1.2, 0]}>
          <ringGeometry args={[0.8, 0.9, 64]} />
          <meshBasicMaterial 
            color={getColorByStatus(status, isThinking)} 
            transparent 
            opacity={0.5} 
            side={THREE.DoubleSide} 
          />
        </mesh>
      </Float>
    </group>
  );
}
