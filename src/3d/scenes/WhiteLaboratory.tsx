import { MeshReflectorMaterial } from '@react-three/drei';
import * as THREE from 'three';

/**
 * WhiteLaboratory Scene - Spatial Upgrade
 * Expanded minimalist white studio with reflective floor and high-gloss interaction surfaces
 * Embodies the "WhiteLab" aesthetic - clean, spacious, futuristic, scientific
 */
export function WhiteLaboratory() {
  return (
    <group>
      {/* Floor with enhanced reflection - scaled up */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 0]}>
        <planeGeometry args={[20, 20]} />
        <MeshReflectorMaterial
          blur={[512, 256]}
          resolution={2048}
          mixBlur={1}
          mixStrength={90}
          roughness={0.8}
          depthScale={1.5}
          minDepthThreshold={0.3}
          maxDepthThreshold={1.6}
          color="#fafafa"
          metalness={0.9}
          mirror={0.85}
        />
      </mesh>

      {/* Back Wall - scaled up */}
      <mesh position={[0, 7.5, -10]}>
        <planeGeometry args={[20, 15]} />
        <meshStandardMaterial color="#ffffff" roughness={0.85} />
      </mesh>

      {/* Left Wall - scaled up */}
      <mesh position={[-10, 7.5, 0]} rotation={[0, Math.PI / 2, 0]}>
        <planeGeometry args={[20, 15]} />
        <meshStandardMaterial color="#ffffff" roughness={0.85} />
      </mesh>

      {/* Right Wall - scaled up */}
      <mesh position={[10, 7.5, 0]} rotation={[0, -Math.PI / 2, 0]}>
        <planeGeometry args={[20, 15]} />
        <meshStandardMaterial color="#ffffff" roughness={0.85} />
      </mesh>

      {/* Left Whiteboard - High-Gloss Interaction Surface (Upgraded) */}
      <group position={[-9.8, 3.5, 0]} rotation={[0, Math.PI / 2, 0]}>
        <mesh>
          <planeGeometry args={[6, 4]} />
          <meshStandardMaterial 
            color="#f8f8f8" 
            roughness={0.15}
            metalness={0.3}
            emissive="#ffffff"
            emissiveIntensity={0.15}
            {...{ clearcoat: 1, clearcoatRoughness: 0.05 }}
          />
        </mesh>
        {/* Frame border - thicker and more prominent */}
        <lineSegments>
          <edgesGeometry args={[new THREE.PlaneGeometry(6, 4)]} />
          <lineBasicMaterial color="#d0d0d0" linewidth={2} />
        </lineSegments>
      </group>

      {/* Right Whiteboard - High-Gloss Interaction Surface (Upgraded) */}
      <group position={[9.8, 3.5, 0]} rotation={[0, -Math.PI / 2, 0]}>
        <mesh>
          <planeGeometry args={[6, 4]} />
          <meshStandardMaterial 
            color="#f8f8f8" 
            roughness={0.15}
            metalness={0.3}
            emissive="#ffffff"
            emissiveIntensity={0.15}
            {...{ clearcoat: 1, clearcoatRoughness: 0.05 }}
          />
        </mesh>
        {/* Frame border - thicker and more prominent */}
        <lineSegments>
          <edgesGeometry args={[new THREE.PlaneGeometry(6, 4)]} />
          <lineBasicMaterial color="#d0d0d0" linewidth={2} />
        </lineSegments>
      </group>

      {/* Enhanced Studio Lighting System */}
      {/* Ambient base light */}
      <ambientLight intensity={0.6} />
      
      {/* Key lights from above - soft studio lighting */}
      <rectAreaLight
        position={[0, 12, 0]}
        intensity={50}
        width={8}
        height={8}
        color="#ffffff"
        rotation={[-Math.PI / 2, 0, 0]}
      />

      {/* Left whiteboard spotlight */}
      <rectAreaLight
        position={[-9.5, 5, 0]}
        intensity={35}
        width={6}
        height={4}
        color="#ffffff"
        rotation={[0, Math.PI / 2, 0]}
      />

      {/* Right whiteboard spotlight */}
      <rectAreaLight
        position={[9.5, 5, 0]}
        intensity={35}
        width={6}
        height={4}
        color="#ffffff"
        rotation={[0, -Math.PI / 2, 0]}
      />

      {/* Accent rim lights for depth */}
      <rectAreaLight
        position={[-5, 8, -8]}
        intensity={20}
        width={4}
        height={4}
        color="#f0f8ff"
      />
      
      <rectAreaLight
        position={[5, 8, -8]}
        intensity={20}
        width={4}
        height={4}
        color="#f0f8ff"
      />

      {/* Fill light from back */}
      <rectAreaLight
        position={[0, 6, 8]}
        intensity={15}
        width={10}
        height={6}
        color="#ffffff"
        rotation={[0, Math.PI, 0]}
      />
    </group>
  );
}
