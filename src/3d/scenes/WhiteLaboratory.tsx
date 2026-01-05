import { MeshReflectorMaterial } from '@react-three/drei';

/**
 * WhiteLaboratory Scene
 * Minimalist white room with reflective floor and frames
 * Embodies the "White Lab" aesthetic - clean, futuristic, scientific
 */
export function WhiteLaboratory() {
  return (
    <group>
      {/* Floor with reflection */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]}>
        <planeGeometry args={[10, 10]} />
        <MeshReflectorMaterial
          blur={[400, 100]}
          resolution={2048}
          mixBlur={1}
          mixStrength={80}
          roughness={1}
          depthScale={1.2}
          minDepthThreshold={0.4}
          maxDepthThreshold={1.4}
          color="#ffffff"
          metalness={0.8}
          mirror={0.8}
        />
      </mesh>

      {/* Back Wall */}
      <mesh position={[0, 5, -5]}>
        <planeGeometry args={[10, 10]} />
        <meshStandardMaterial color="#ffffff" roughness={0.9} />
      </mesh>

      {/* Left Wall */}
      <mesh position={[-5, 5, 0]} rotation={[0, Math.PI / 2, 0]}>
        <planeGeometry args={[10, 10]} />
        <meshStandardMaterial color="#ffffff" roughness={0.9} />
      </mesh>

      {/* Right Wall */}
      <mesh position={[5, 5, 0]} rotation={[0, -Math.PI / 2, 0]}>
        <planeGeometry args={[10, 10]} />
        <meshStandardMaterial color="#ffffff" roughness={0.9} />
      </mesh>

      {/* Left Frame (Empty Canvas) */}
      <group position={[-4.9, 2, 0]} rotation={[0, Math.PI / 2, 0]}>
        <mesh>
          <planeGeometry args={[3, 2]} />
          <meshStandardMaterial 
            color="#f0f0f0" 
            roughness={0.8}
            emissive="#ffffff"
            emissiveIntensity={0.1}
          />
        </mesh>
        {/* Frame border */}
        <lineSegments>
          <edgesGeometry args={[new THREE.PlaneGeometry(3, 2)]} />
          <lineBasicMaterial color="#cccccc" />
        </lineSegments>
      </group>

      {/* Right Frame (Empty Canvas) */}
      <group position={[4.9, 2, 0]} rotation={[0, -Math.PI / 2, 0]}>
        <mesh>
          <planeGeometry args={[3, 2]} />
          <meshStandardMaterial 
            color="#f0f0f0" 
            roughness={0.8}
            emissive="#ffffff"
            emissiveIntensity={0.1}
          />
        </mesh>
        {/* Frame border */}
        <lineSegments>
          <edgesGeometry args={[new THREE.PlaneGeometry(3, 2)]} />
          <lineBasicMaterial color="#cccccc" />
        </lineSegments>
      </group>

      {/* Ambient Lighting */}
      <ambientLight intensity={0.5} />

      {/* RectAreaLight - Left */}
      <rectAreaLight
        position={[-5, 5, 0]}
        intensity={20}
        width={2}
        height={2}
        color="#ffffff"
      />

      {/* RectAreaLight - Right */}
      <rectAreaLight
        position={[5, 5, 0]}
        intensity={20}
        width={2}
        height={2}
        color="#ffffff"
      />
    </group>
  );
}

// Need to import THREE for EdgesGeometry
import * as THREE from 'three';
