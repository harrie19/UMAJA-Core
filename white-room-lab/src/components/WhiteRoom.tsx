'use client';

import { usePlane } from '@react-three/cannon';

export default function WhiteRoom() {
  // Floor
  const [floorRef] = usePlane(() => ({
    rotation: [-Math.PI / 2, 0, 0],
    position: [0, 0, 0],
    mass: 0, // Static body
  }));

  // Back wall
  const [backWallRef] = usePlane(() => ({
    rotation: [0, 0, 0],
    position: [0, 10, -25],
    mass: 0,
  }));

  return (
    <group>
      {/* Floor */}
      {/* @ts-ignore */}
      <mesh ref={floorRef} receiveShadow>
        <planeGeometry args={[50, 50]} />
        <meshStandardMaterial 
          color="#ffffff"
          metalness={0.8}
          roughness={0.2}
        />
      </mesh>

      {/* Back Wall */}
      {/* @ts-ignore */}
      <mesh ref={backWallRef} receiveShadow>
        <planeGeometry args={[50, 20]} />
        <meshStandardMaterial 
          color="#f5f5f5"
          metalness={0.1}
          roughness={0.8}
        />
      </mesh>

      {/* Left Wall */}
      <mesh position={[-25, 10, 0]} rotation={[0, Math.PI / 2, 0]} receiveShadow>
        <planeGeometry args={[50, 20]} />
        <meshStandardMaterial 
          color="#f8f8f8"
          metalness={0.1}
          roughness={0.8}
        />
      </mesh>

      {/* Right Wall */}
      <mesh position={[25, 10, 0]} rotation={[0, -Math.PI / 2, 0]} receiveShadow>
        <planeGeometry args={[50, 20]} />
        <meshStandardMaterial 
          color="#f8f8f8"
          metalness={0.1}
          roughness={0.8}
        />
      </mesh>

      {/* Grid helper for depth perception */}
      <gridHelper args={[50, 50, '#e0e0e0', '#f0f0f0']} position={[0, 0.01, 0]} />
    </group>
  );
}
