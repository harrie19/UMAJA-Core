/**
 * Energy Monitor Visualization
 * Displays energy data with particle system
 */
'use client';

import { useEffect, useState, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Text } from '@react-three/drei';
import { createMockEnergyStream, type EnergyData } from '../lib/umaja-api';
import * as THREE from 'three';

interface Particle {
  id: number;
  position: THREE.Vector3;
  velocity: THREE.Vector3;
  life: number;
}

export default function EnergyVisualization() {
  const [energyData, setEnergyData] = useState<EnergyData | null>(null);
  const [particles, setParticles] = useState<Particle[]>([]);
  const particleRefs = useRef<(THREE.Mesh | null)[]>([]);

  // Subscribe to energy stream
  useEffect(() => {
    const unsubscribe = createMockEnergyStream((data) => {
      setEnergyData(data);
    });

    return unsubscribe;
  }, []);

  // Generate particles based on energy data
  useEffect(() => {
    if (!energyData) return;

    const newParticles: Particle[] = [];
    const count = Math.floor((energyData.current_power / energyData.max_power) * 20);

    for (let i = 0; i < count; i++) {
      newParticles.push({
        id: Date.now() + i,
        position: new THREE.Vector3(
          (Math.random() - 0.5) * 2,
          -2 + Math.random() * 0.5,
          -5 + (Math.random() - 0.5) * 2
        ),
        velocity: new THREE.Vector3(
          (Math.random() - 0.5) * 0.02,
          0.02 + Math.random() * 0.03,
          (Math.random() - 0.5) * 0.02
        ),
        life: 1.0,
      });
    }

    setParticles(newParticles);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [energyData?.timestamp]);

  // Animate particles
  useFrame(() => {
    particles.forEach((particle, i) => {
      particle.position.add(particle.velocity);
      particle.life -= 0.01;

      const mesh = particleRefs.current[i];
      if (mesh) {
        mesh.position.copy(particle.position);
        mesh.scale.setScalar(particle.life * 0.1);
      }
    });

    // Remove dead particles
    setParticles(prev => prev.filter(p => p.life > 0));
  });

  if (!energyData) {
    return (
      <Text position={[5, 3, -5]} fontSize={0.3} color="white">
        Connecting to energy monitor...
      </Text>
    );
  }

  const getEnergyColor = () => {
    switch (energyData.energy_type) {
      case 'renewable': return '#4CAF50';
      case 'fossil': return '#F44336';
      default: return '#FFC107';
    }
  };

  const powerPercent = (energyData.current_power / energyData.max_power * 100).toFixed(0);
  const efficiencyPercent = (energyData.efficiency * 100).toFixed(0);

  return (
    <group>
      {/* Energy Meter Display */}
      <group position={[5, 2, -5]}>
        <Text
          position={[0, 1, 0]}
          fontSize={0.4}
          color="white"
          anchorX="center"
        >
          Energy Monitor
        </Text>

        <Text
          position={[0, 0.3, 0]}
          fontSize={0.3}
          color={getEnergyColor()}
          anchorX="center"
        >
          {`${energyData.current_power.toFixed(1)} W`}
        </Text>

        <Text
          position={[0, -0.2, 0]}
          fontSize={0.15}
          color="#aaa"
          anchorX="center"
        >
          {`${powerPercent}% of ${energyData.max_power}W`}
        </Text>

        <Text
          position={[0, -0.6, 0]}
          fontSize={0.15}
          color={getEnergyColor()}
          anchorX="center"
        >
          {`⚡ ${energyData.energy_type.toUpperCase()}`}
        </Text>

        <Text
          position={[0, -0.9, 0]}
          fontSize={0.12}
          color="#888"
          anchorX="center"
        >
          {`Efficiency: ${efficiencyPercent}%`}
        </Text>

        {/* Power Bar */}
        <mesh position={[0, -1.3, 0]}>
          <boxGeometry args={[2, 0.2, 0.1]} />
          <meshBasicMaterial color="#333" />
        </mesh>

        <mesh position={[(-1 + energyData.current_power / energyData.max_power), -1.3, 0.06]}>
          <boxGeometry args={[(energyData.current_power / energyData.max_power) * 2, 0.2, 0.1]} />
          <meshBasicMaterial color={getEnergyColor()} />
        </mesh>
      </group>

      {/* Particle System */}
      {particles.map((particle, i) => (
        <mesh
          key={particle.id}
          ref={el => { particleRefs.current[i] = el; }}
          position={particle.position.toArray()}
        >
          <sphereGeometry args={[0.05, 8, 8]} />
          <meshBasicMaterial
            color={getEnergyColor()}
            transparent
            opacity={particle.life}
          />
        </mesh>
      ))}

      {/* Pulsating energy source */}
      <mesh position={[5, -2, -5]}>
        <sphereGeometry args={[0.3, 16, 16]} />
        <meshStandardMaterial
          color={getEnergyColor()}
          emissive={getEnergyColor()}
          emissiveIntensity={0.5 + Math.sin(Date.now() * 0.005) * 0.3}
        />
      </mesh>

      {/* Point light for glow effect */}
      <pointLight
        position={[5, -2, -5]}
        color={getEnergyColor()}
        intensity={1}
        distance={5}
      />
    </group>
  );
}
