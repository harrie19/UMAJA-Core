import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface DNAHelixProps {
  position?: [number, number, number];
  data?: any;
}

/**
 * DNAHelix - Represents data flow and semantic coherence
 * Animated helix with color/thickness responding to data metrics
 */
export function DNAHelix({ position = [0, 1, 3], data }: DNAHelixProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  
  // Create helix curve
  const createHelixCurve = (): THREE.Curve<THREE.Vector3> => {
    const points: THREE.Vector3[] = [];
    const numPoints = 100;
    const rotations = 4; // 4 full rotations
    
    for (let i = 0; i < numPoints; i++) {
      const t = i / numPoints;
      const angle = t * rotations * Math.PI * 2;
      
      const x = Math.cos(angle) * 0.3;
      const y = (t * 3) - 1.5; // Centered at origin
      const z = Math.sin(angle) * 0.3;
      
      points.push(new THREE.Vector3(x, y, z));
    }
    
    return new THREE.CatmullRomCurve3(points);
  };

  const curve = createHelixCurve();
  
  // Animate rotation
  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.3;
    }
  });

  // Determine color and intensity based on data
  const getHelixColor = (): string => {
    if (!data) return '#00ff00';
    
    // If vector analysis data is available
    if (data.overall_score !== undefined) {
      const score = data.overall_score;
      if (score >= 0.7) return '#00ff00'; // Green - excellent
      if (score >= 0.5) return '#88ff00'; // Yellow-green - good
      if (score >= 0.3) return '#ffaa00'; // Orange - acceptable
      return '#ff4400'; // Red-orange - poor
    }
    
    return '#00ff00';
  };

  const getEmissiveIntensity = (): number => {
    if (!data) return 2;
    
    if (data.overall_score !== undefined) {
      // Higher score = brighter glow
      return 1 + (data.overall_score * 2);
    }
    
    return 2;
  };

  const color = getHelixColor();
  const emissiveIntensity = getEmissiveIntensity();

  // Pre-calculate ladder rungs to avoid creating objects in render
  const ladderRungs = useMemo(() => {
    const rungs = [];
    for (let i = 0; i < 20; i++) {
      const t = i / 20;
      const angle = t * 4 * Math.PI * 2;
      
      const x1 = Math.cos(angle) * 0.3;
      const y = (t * 3) - 1.5;
      const z1 = Math.sin(angle) * 0.3;
      
      const x2 = Math.cos(angle + Math.PI) * 0.3;
      const z2 = Math.sin(angle + Math.PI) * 0.3;
      
      const start = new THREE.Vector3(x1, y, z1);
      const end = new THREE.Vector3(x2, y, z2);
      const distance = start.distanceTo(end);
      const direction = end.clone().sub(start).normalize();
      const center = start.clone().add(end).multiplyScalar(0.5);
      const quaternion = new THREE.Quaternion().setFromUnitVectors(
        new THREE.Vector3(0, 1, 0),
        direction
      );
      
      rungs.push({ center, quaternion, distance });
    }
    return rungs;
  }, []); // Empty deps - only calculate once

  return (
    <group position={position} ref={meshRef}>
      <mesh>
        <tubeGeometry args={[curve, 100, 0.05, 8, false]} />
        <meshBasicMaterial 
          color={color}
          emissive={color}
          emissiveIntensity={emissiveIntensity}
          transparent={true}
          opacity={0.9}
        />
      </mesh>
      
      {/* Add connecting bars between strands (DNA ladder effect) */}
      {ladderRungs.map((rung, i) => (
        <mesh 
          key={i} 
          position={[rung.center.x, rung.center.y, rung.center.z]}
          quaternion={rung.quaternion}
        >
          <cylinderGeometry args={[0.02, 0.02, rung.distance, 6]} />
          <meshBasicMaterial 
            color={color}
            emissive={color}
            emissiveIntensity={emissiveIntensity * 0.5}
            transparent={true}
            opacity={0.6}
          />
        </mesh>
      ))}
    </group>
  );
}
