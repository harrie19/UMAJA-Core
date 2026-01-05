import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface ParticleCloudProps {
  count?: number;
  status?: string;
}

/**
 * ParticleCloud - Organic data visualization using InstancedMesh
 * Performance-optimized particle system with 5000+ particles
 */
export function ParticleCloud({ count = 5000, status = 'OK' }: ParticleCloudProps) {
  const meshRef = useRef<THREE.InstancedMesh>(null);
  
  // Generate particle data (positions, velocities, phases)
  const particles = useMemo(() => {
    const temp = [];
    for (let i = 0; i < count; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos((Math.random() * 2) - 1);
      const radius = 2 + Math.random() * 2; // Random radius between 2 and 4
      
      temp.push({
        position: new THREE.Vector3(
          radius * Math.sin(phi) * Math.cos(theta),
          radius * Math.sin(phi) * Math.sin(theta),
          radius * Math.cos(phi)
        ),
        velocity: new THREE.Vector3(
          (Math.random() - 0.5) * 0.02,
          (Math.random() - 0.5) * 0.02,
          (Math.random() - 0.5) * 0.02
        ),
        phase: Math.random() * Math.PI * 2,
        speed: 0.5 + Math.random() * 0.5,
      });
    }
    return temp;
  }, [count]);

  // Determine color based on status
  const getColorByStatus = (status: string): THREE.Color => {
    switch (status?.toUpperCase()) {
      case 'OK':
      case 'HEALTHY':
        return new THREE.Color('#00ff88'); // Green
      case 'WARNING':
        return new THREE.Color('#ffaa00'); // Orange
      case 'CRITICAL':
      case 'ERROR':
        return new THREE.Color('#ff0044'); // Red
      default:
        return new THREE.Color('#00aaff'); // Blue
    }
  };

  const baseColor = getColorByStatus(status);
  
  // Animate particles
  useFrame((state, delta) => {
    if (!meshRef.current) return;

    const time = state.clock.elapsedTime;
    const dummy = new THREE.Object3D();
    const color = new THREE.Color();

    for (let i = 0; i < count; i++) {
      const particle = particles[i];
      
      // Update position with velocity
      particle.position.add(particle.velocity);
      
      // Boundary check - keep particles within sphere
      const distance = particle.position.length();
      if (distance > 4 || distance < 2) {
        particle.velocity.multiplyScalar(-1);
      }
      
      // Pulsating size based on phase
      const pulseScale = 0.8 + Math.sin(time * particle.speed + particle.phase) * 0.3;
      
      dummy.position.copy(particle.position);
      dummy.scale.setScalar(pulseScale);
      dummy.updateMatrix();
      
      meshRef.current.setMatrixAt(i, dummy.matrix);
      
      // Color variation - mix with base color
      const colorMix = 0.5 + Math.sin(time * particle.speed + particle.phase) * 0.5;
      color.copy(baseColor).lerp(new THREE.Color('#ffffff'), colorMix * 0.3);
      meshRef.current.setColorAt(i, color);
    }
    
    meshRef.current.instanceMatrix.needsUpdate = true;
    if (meshRef.current.instanceColor) {
      meshRef.current.instanceColor.needsUpdate = true;
    }
  });

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[0.02, 8, 8]} />
      <meshBasicMaterial 
        color={baseColor}
        transparent={true}
        opacity={0.8}
        toneMapped={false}
      />
    </instancedMesh>
  );
}
