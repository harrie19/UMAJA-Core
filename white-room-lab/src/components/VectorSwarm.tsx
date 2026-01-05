/**
 * Vector Agent Swarm Visualization
 * Mini-agents as colored spheres with connections
 */
'use client';

import { useEffect, useState, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Line } from '@react-three/drei';
import { generateMockAgents, type VectorAgent } from '../lib/umaja-api';
import * as THREE from 'three';

interface AgentMeshProps {
  agent: VectorAgent;
  onUpdate: (id: string, position: THREE.Vector3) => void;
}

function AgentMesh({ agent, onUpdate }: AgentMeshProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const posRef = useRef(new THREE.Vector3(...agent.position));
  const velRef = useRef(new THREE.Vector3(...agent.velocity));

  useFrame(() => {
    if (meshRef.current) {
      // Update position based on velocity
      posRef.current.add(velRef.current);

      // Bounce off boundaries
      if (Math.abs(posRef.current.x) > 5) velRef.current.x *= -1;
      if (Math.abs(posRef.current.y) > 3) velRef.current.y *= -1;
      if (Math.abs(posRef.current.z) > 5) velRef.current.z *= -1;

      meshRef.current.position.copy(posRef.current);
      onUpdate(agent.id, posRef.current);
    }
  });

  return (
    <mesh ref={meshRef} position={agent.position}>
      <sphereGeometry args={[0.1, 12, 12]} />
      <meshStandardMaterial
        color={agent.color}
        emissive={agent.color}
        emissiveIntensity={0.4}
        metalness={0.5}
        roughness={0.3}
      />
    </mesh>
  );
}

export default function VectorSwarm() {
  const [agents, setAgents] = useState<VectorAgent[]>([]);
  const [positions, setPositions] = useState<Map<string, THREE.Vector3>>(new Map());

  useEffect(() => {
    const initialAgents = generateMockAgents(15);
    setAgents(initialAgents);
    
    const initialPositions = new Map();
    initialAgents.forEach(agent => {
      initialPositions.set(agent.id, new THREE.Vector3(...agent.position));
    });
    setPositions(initialPositions);
  }, []);

  const handleAgentUpdate = (id: string, position: THREE.Vector3) => {
    setPositions(prev => {
      const next = new Map(prev);
      next.set(id, position.clone());
      return next;
    });
  };

  // Find nearby agents for connections
  const getConnections = (): Array<[THREE.Vector3, THREE.Vector3]> => {
    const connections: Array<[THREE.Vector3, THREE.Vector3]> = [];
    const agentArray = Array.from(positions.entries());

    for (let i = 0; i < agentArray.length; i++) {
      for (let j = i + 1; j < agentArray.length; j++) {
        const pos1 = agentArray[i][1];
        const pos2 = agentArray[j][1];
        const distance = pos1.distanceTo(pos2);

        if (distance < 2.5) {
          connections.push([pos1, pos2]);
        }
      }
    }

    return connections.slice(0, 30); // Limit connections for performance
  };

  const connections = getConnections();

  return (
    <group>
      {/* Agents */}
      {agents.map(agent => (
        <AgentMesh
          key={agent.id}
          agent={agent}
          onUpdate={handleAgentUpdate}
        />
      ))}

      {/* Connection Lines */}
      {connections.map((conn, i) => (
        <Line
          key={i}
          points={[conn[0].toArray(), conn[1].toArray()]}
          color="#4FC3F7"
          lineWidth={0.5}
          opacity={0.2}
          transparent
        />
      ))}

      {/* Legend */}
      <group position={[-5, -3, -3]}>
        <mesh position={[0, 0.5, 0]}>
          <sphereGeometry args={[0.05, 8, 8]} />
          <meshBasicMaterial color="#888888" />
        </mesh>
        <mesh position={[0, 0, 0]}>
          <sphereGeometry args={[0.05, 8, 8]} />
          <meshBasicMaterial color="#FFAA00" />
        </mesh>
        <mesh position={[0, -0.5, 0]}>
          <sphereGeometry args={[0.05, 8, 8]} />
          <meshBasicMaterial color="#4FC3F7" />
        </mesh>
      </group>
    </group>
  );
}
