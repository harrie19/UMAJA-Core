/**
 * GitHub PR Visualization Component
 * Displays pull requests as 3D network in White Room
 */
'use client';

import { useEffect, useState, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Text, Line } from '@react-three/drei';
import { fetchGitHubPRs, type GitHubPR } from '../lib/umaja-api';
import * as THREE from 'three';

interface PRNodeProps {
  pr: GitHubPR;
  position: [number, number, number];
  onClick: () => void;
}

function PRNode({ pr, position, onClick }: PRNodeProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);

  // Color based on state
  const getColor = () => {
    if (pr.merged_at) return '#2196F3'; // Blue for merged
    if (pr.state === 'open') return '#4CAF50'; // Green for open
    return '#888888'; // Gray for closed
  };

  useFrame((state) => {
    if (meshRef.current) {
      // Gentle floating animation
      meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime + pr.number) * 0.1;
      
      // Scale on hover
      const targetScale = hovered ? 1.3 : 1.0;
      meshRef.current.scale.lerp(new THREE.Vector3(targetScale, targetScale, targetScale), 0.1);
    }
  });

  return (
    <group position={position}>
      <mesh
        ref={meshRef}
        onClick={onClick}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <sphereGeometry args={[0.15, 16, 16]} />
        <meshStandardMaterial
          color={getColor()}
          emissive={getColor()}
          emissiveIntensity={hovered ? 0.5 : 0.2}
          metalness={0.3}
          roughness={0.4}
        />
      </mesh>
      
      {hovered && (
        <Text
          position={[0, 0.5, 0]}
          fontSize={0.15}
          color="white"
          anchorX="center"
          anchorY="middle"
          maxWidth={3}
        >
          {`PR #${pr.number}\n${pr.title.substring(0, 40)}...`}
        </Text>
      )}
    </group>
  );
}

export default function PRVisualization() {
  const [prs, setPRs] = useState<GitHubPR[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadPRs() {
      try {
        setLoading(true);
        const data = await fetchGitHubPRs();
        setPRs(data.slice(0, 30)); // Limit to 30 for performance
        setError(null);
      } catch (err) {
        setError('Failed to load PRs');
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    loadPRs();
  }, []);

  if (loading) {
    return (
      <Text position={[0, 3, -5]} fontSize={0.3} color="white">
        Loading GitHub PRs...
      </Text>
    );
  }

  if (error) {
    return (
      <Text position={[0, 3, -5]} fontSize={0.3} color="#ff5555">
        {error}
      </Text>
    );
  }

  // Calculate positions based on PR data
  const calculatePosition = (pr: GitHubPR, index: number): [number, number, number] => {
    // X-axis: PR number (normalized)
    const maxPRNumber = Math.max(...prs.map(p => p.number));
    const x = (pr.number / maxPRNumber) * 8 - 4;

    // Y-axis: Age (log scale)
    const age = Date.now() - new Date(pr.created_at).getTime();
    const ageDays = age / (1000 * 60 * 60 * 24);
    const y = Math.log(ageDays + 1) - 2;

    // Z-axis: Comments
    const z = -3 - (pr.comments * 0.1);

    return [x, y, z];
  };

  const handlePRClick = (pr: GitHubPR) => {
    window.open(pr.html_url, '_blank');
  };

  // Draw connection lines between PRs (simplified - just connect sequential PRs)
  const connections = prs.slice(0, -1).map((pr, i) => {
    const start = calculatePosition(pr, i);
    const end = calculatePosition(prs[i + 1], i + 1);
    return { start, end };
  });

  return (
    <group>
      {/* PR Nodes */}
      {prs.map((pr, index) => (
        <PRNode
          key={pr.id}
          pr={pr}
          position={calculatePosition(pr, index)}
          onClick={() => handlePRClick(pr)}
        />
      ))}

      {/* Connection Lines */}
      {connections.map((conn, i) => (
        <Line
          key={i}
          points={[conn.start, conn.end]}
          color="#4FC3F7"
          lineWidth={1}
          opacity={0.3}
          transparent
        />
      ))}

      {/* Labels */}
      <Text position={[-5, -3, -3]} fontSize={0.2} color="#888">
        PR Number →
      </Text>
      <Text position={[-5, 0, -3]} fontSize={0.2} color="#888" rotation={[0, 0, Math.PI / 2]}>
        Age (days)
      </Text>
      <Text position={[0, -3, -5]} fontSize={0.2} color="#888">
        ← Comments
      </Text>

      {/* Info Panel */}
      <Text position={[0, 4, -5]} fontSize={0.25} color="white">
        {`GitHub PRs: ${prs.length} total`}
      </Text>
      <Text position={[0, 3.5, -5]} fontSize={0.15} color="#4FC3F7">
        🟢 Open  🔵 Merged  ⚫ Closed
      </Text>
    </group>
  );
}
