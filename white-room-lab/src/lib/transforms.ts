/**
 * Transformation Library for White Room Lab
 * Implements various 3D forms that the Blue Bubble can morph into
 */

import * as THREE from 'three';

export type FormType = 
  | 'bubble'
  | 'human'
  | 'dna'
  | 'turbine'
  | 'neural'
  | 'molecule'
  | 'city'
  | 'galaxy'
  | 'tool'
  | 'vehicle'
  | 'bugs_bunny';

export interface Transform {
  type: FormType;
  name: string;
  description: string;
  generate: () => JSX.Element;
}

/**
 * DNA Helix - Double helix with base pairs
 */
export function DNAHelix(): JSX.Element {
  const basePairs = 20;
  const height = 2;
  const radius = 0.3;

  const bases = [];
  const backbones = [];

  for (let i = 0; i < basePairs; i++) {
    const y = (i / basePairs) * height - height / 2;
    const angle = (i / basePairs) * Math.PI * 4; // 2 full rotations

    // Helix 1
    const x1 = Math.cos(angle) * radius;
    const z1 = Math.sin(angle) * radius;

    // Helix 2 (opposite side)
    const x2 = Math.cos(angle + Math.PI) * radius;
    const z2 = Math.sin(angle + Math.PI) * radius;

    // Base pair colors (alternating A-T, G-C)
    const isAT = i % 2 === 0;
    const color1 = isAT ? '#FF0000' : '#00FF00'; // A=red, G=green
    const color2 = isAT ? '#0000FF' : '#FFFF00'; // T=blue, C=yellow

    bases.push(
      <group key={`base-${i}`}>
        {/* Nucleotide 1 */}
        <mesh position={[x1, y, z1]}>
          <sphereGeometry args={[0.08, 8, 8]} />
          <meshStandardMaterial color={color1} />
        </mesh>

        {/* Nucleotide 2 */}
        <mesh position={[x2, y, z2]}>
          <sphereGeometry args={[0.08, 8, 8]} />
          <meshStandardMaterial color={color2} />
        </mesh>

        {/* Connection between bases */}
        <mesh position={[(x1 + x2) / 2, y, (z1 + z2) / 2]} rotation={[0, 0, Math.atan2(z2 - z1, x2 - x1)]}>
          <cylinderGeometry args={[0.02, 0.02, Math.sqrt((x2-x1)**2 + (z2-z1)**2), 8]} />
          <meshStandardMaterial color="#FFFFFF" />
        </mesh>
      </group>
    );

    // Backbone cylinders
    if (i < basePairs - 1) {
      const nextAngle = ((i + 1) / basePairs) * Math.PI * 4;
      const nextY = ((i + 1) / basePairs) * height - height / 2;

      backbones.push(
        <group key={`backbone-${i}`}>
          {/* Backbone 1 */}
          <mesh position={[x1, (y + nextY) / 2, z1]}>
            <cylinderGeometry args={[0.03, 0.03, height / basePairs, 8]} />
            <meshStandardMaterial color="#FFFFFF" opacity={0.8} transparent />
          </mesh>

          {/* Backbone 2 */}
          <mesh position={[x2, (y + nextY) / 2, z2]}>
            <cylinderGeometry args={[0.03, 0.03, height / basePairs, 8]} />
            <meshStandardMaterial color="#FFFFFF" opacity={0.8} transparent />
          </mesh>
        </group>
      );
    }
  }

  return (
    <group rotation={[0, Date.now() * 0.0001, 0]}>
      {bases}
      {backbones}
    </group>
  );
}

/**
 * Neural Network - 3 layers with connections
 */
export function NeuralNetwork(): JSX.Element {
  const layers = [
    { nodes: 4, x: -1.5 },
    { nodes: 6, x: 0 },
    { nodes: 2, x: 1.5 },
  ];

  const nodes = [];
  const connections = [];

  layers.forEach((layer, layerIndex) => {
    const yStart = -(layer.nodes - 1) * 0.5 * 0.5;

    for (let i = 0; i < layer.nodes; i++) {
      const y = yStart + i * 0.5;
      const activation = 0.3 + Math.sin(Date.now() * 0.001 + i) * 0.4;

      nodes.push(
        <mesh key={`node-${layerIndex}-${i}`} position={[layer.x, y, 0]}>
          <sphereGeometry args={[0.2, 16, 16]} />
          <meshStandardMaterial
            color={new THREE.Color().setHSL(0.6, 1, 0.3 + activation * 0.4)}
            emissive={new THREE.Color().setHSL(0.6, 1, activation)}
            emissiveIntensity={0.5}
          />
        </mesh>
      );

      // Connections to next layer
      if (layerIndex < layers.length - 1) {
        const nextLayer = layers[layerIndex + 1];
        const nextYStart = -(nextLayer.nodes - 1) * 0.5 * 0.5;

        for (let j = 0; j < nextLayer.nodes; j++) {
          const nextY = nextYStart + j * 0.5;
          const weight = 0.3 + Math.random() * 0.7;

          connections.push(
            <line key={`conn-${layerIndex}-${i}-${j}`}>
              <bufferGeometry>
                <bufferAttribute
                  attach="attributes-position"
                  count={2}
                  array={new Float32Array([layer.x, y, 0, layers[layerIndex + 1].x, nextY, 0])}
                  itemSize={3}
                />
              </bufferGeometry>
              <lineBasicMaterial color="#4FC3F7" opacity={weight * 0.5} transparent />
            </line>
          );
        }
      }
    }
  });

  return (
    <group>
      {connections}
      {nodes}
    </group>
  );
}

/**
 * Molecule - H2O with proper angles
 */
export function Molecule(): JSX.Element {
  const angle = 104.5 * (Math.PI / 180); // H2O bond angle

  return (
    <group>
      {/* Oxygen (center, red, large) */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.3, 16, 16]} />
        <meshStandardMaterial color="#FF0000" metalness={0.3} roughness={0.4} />
      </mesh>

      {/* Hydrogen 1 (white, small) */}
      <mesh position={[0.5 * Math.cos(angle / 2), 0.5 * Math.sin(angle / 2), 0]}>
        <sphereGeometry args={[0.15, 12, 12]} />
        <meshStandardMaterial color="#FFFFFF" metalness={0.2} roughness={0.5} />
      </mesh>

      {/* Hydrogen 2 */}
      <mesh position={[0.5 * Math.cos(angle / 2), -0.5 * Math.sin(angle / 2), 0]}>
        <sphereGeometry args={[0.15, 12, 12]} />
        <meshStandardMaterial color="#FFFFFF" metalness={0.2} roughness={0.5} />
      </mesh>

      {/* Bond 1 */}
      <mesh
        position={[0.25 * Math.cos(angle / 2), 0.25 * Math.sin(angle / 2), 0]}
        rotation={[0, 0, angle / 2]}
      >
        <cylinderGeometry args={[0.05, 0.05, 0.5, 8]} />
        <meshStandardMaterial color="#CCCCCC" />
      </mesh>

      {/* Bond 2 */}
      <mesh
        position={[0.25 * Math.cos(angle / 2), -0.25 * Math.sin(angle / 2), 0]}
        rotation={[0, 0, -angle / 2]}
      >
        <cylinderGeometry args={[0.05, 0.05, 0.5, 8]} />
        <meshStandardMaterial color="#CCCCCC" />
      </mesh>
    </group>
  );
}

/**
 * City - Procedural 10x10 grid
 */
export function City(): JSX.Element {
  const gridSize = 10;
  const spacing = 0.4;
  const buildings = [];
  const streets = [];

  for (let x = 0; x < gridSize; x++) {
    for (let z = 0; z < gridSize; z++) {
      const height = 0.5 + Math.random() * 2.5; // 0.5-3m
      const posX = (x - gridSize / 2) * spacing;
      const posZ = (z - gridSize / 2) * spacing;

      buildings.push(
        <mesh key={`building-${x}-${z}`} position={[posX, height / 2, posZ]}>
          <boxGeometry args={[0.3, height, 0.3]} />
          <meshStandardMaterial
            color="#555555"
            emissive="#FFAA00"
            emissiveIntensity={0.1}
          />
        </mesh>
      );
    }
  }

  // Streets (dark gray planes)
  for (let i = 0; i <= gridSize; i++) {
    const pos = (i - gridSize / 2) * spacing;
    streets.push(
      <mesh key={`street-x-${i}`} position={[pos, 0, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[0.1, gridSize * spacing]} />
        <meshBasicMaterial color="#222222" />
      </mesh>,
      <mesh key={`street-z-${i}`} position={[0, 0, pos]} rotation={[-Math.PI / 2, 0, 0]}>
        <planeGeometry args={[gridSize * spacing, 0.1]} />
        <meshBasicMaterial color="#222222" />
      </mesh>
    );
  }

  return (
    <group>
      {streets}
      {buildings}
    </group>
  );
}

/**
 * Galaxy - 10,000 particle spiral
 */
export function Galaxy(): JSX.Element {
  const particleCount = 10000;
  const positions = new Float32Array(particleCount * 3);
  const colors = new Float32Array(particleCount * 3);

  for (let i = 0; i < particleCount; i++) {
    // Spiral arms (2 arms, logarithmic)
    const armAngle = (i % 2) * Math.PI;
    const radius = Math.pow(i / particleCount, 0.5) * 5;
    const angle = armAngle + (i / particleCount) * Math.PI * 6;

    const x = Math.cos(angle) * radius + (Math.random() - 0.5) * 0.5;
    const y = (Math.random() - 0.5) * 0.3;
    const z = Math.sin(angle) * radius + (Math.random() - 0.5) * 0.5;

    positions[i * 3] = x;
    positions[i * 3 + 1] = y;
    positions[i * 3 + 2] = z;

    // Color gradient: center=yellow, outer=blue
    const colorMix = i / particleCount;
    colors[i * 3] = 1 - colorMix * 0.5; // R
    colors[i * 3 + 1] = 1 - colorMix * 0.7; // G
    colors[i * 3 + 2] = 0.3 + colorMix * 0.7; // B
  }

  return (
    <group rotation={[Math.PI / 4, Date.now() * 0.00005, 0]}>
      <points>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={particleCount}
            array={positions}
            itemSize={3}
          />
          <bufferAttribute
            attach="attributes-color"
            count={particleCount}
            array={colors}
            itemSize={3}
          />
        </bufferGeometry>
        <pointsMaterial size={0.02} vertexColors transparent opacity={0.8} />
      </points>
    </group>
  );
}

/**
 * Transform registry
 */
export const TRANSFORMS: Record<FormType, Transform> = {
  bubble: {
    type: 'bubble',
    name: 'Blue Bubble',
    description: 'Default pulsating sphere',
    generate: () => <></>, // Handled by BlueBubble component
  },
  dna: {
    type: 'dna',
    name: 'DNA Helix',
    description: 'Double helix with 20 base pairs',
    generate: DNAHelix,
  },
  neural: {
    type: 'neural',
    name: 'Neural Network',
    description: '3-layer network with animated activations',
    generate: NeuralNetwork,
  },
  molecule: {
    type: 'molecule',
    name: 'Water Molecule',
    description: 'H2O with 104.5° bond angle',
    generate: Molecule,
  },
  city: {
    type: 'city',
    name: 'Procedural City',
    description: '10x10 grid of buildings',
    generate: City,
  },
  galaxy: {
    type: 'galaxy',
    name: 'Spiral Galaxy',
    description: '10,000 particle spiral with 2 arms',
    generate: Galaxy,
  },
  human: {
    type: 'human',
    name: 'Human Form',
    description: 'Simplified humanoid figure',
    generate: () => <></>, // Placeholder
  },
  turbine: {
    type: 'turbine',
    name: 'Wind Turbine',
    description: 'Rotating turbine with blades',
    generate: () => <></>, // Placeholder
  },
  tool: {
    type: 'tool',
    name: 'Hammer',
    description: 'Simple tool demonstration',
    generate: () => <></>, // Placeholder
  },
  vehicle: {
    type: 'vehicle',
    name: 'Simple Car',
    description: 'Basic vehicle with wheels',
    generate: () => <></>, // Placeholder
  },
  bugs_bunny: {
    type: 'bugs_bunny',
    name: 'Bugs Bunny',
    description: 'Fun character demo',
    generate: () => <></>, // Placeholder
  },
};
