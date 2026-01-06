import { useRef, useMemo, useState } from 'react';
import { useFrame, ThreeEvent } from '@react-three/fiber';
import { MeshTransmissionMaterial } from '@react-three/drei';
import * as THREE from 'three';

interface IridescentBlobProps {
  position?: [number, number, number];
  status?: string;
}

/**
 * IridescentBlob - Morphing Liquid Avatar
 * Advanced fluid visualization with noise-based displacement
 * Features enhanced iridescence, chromatic aberration, and interactive presence
 */
export function IridescentBlob({ position = [0, 1, 0], status = 'OK' }: IridescentBlobProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  const timeRef = useRef(0);
  const [hovered, setHovered] = useState(false);

  // Determine color based on status
  const getColorByStatus = (status: string): string => {
    switch (status?.toUpperCase()) {
      case 'OK':
      case 'HEALTHY':
        return '#00ff88'; // Green tint
      case 'WARNING':
        return '#ffaa00'; // Yellow/orange tint
      case 'CRITICAL':
      case 'ERROR':
        return '#ff0044'; // Red tint
      default:
        return '#ffffff'; // White/neutral
    }
  };

  // Create custom shader for noise-based displacement (morphing liquid effect)
  const shaderMaterial = useMemo(() => {
    return new THREE.ShaderMaterial({
      uniforms: {
        time: { value: 0 },
        color: { value: new THREE.Color(getColorByStatus(status)) },
        hoverIntensity: { value: 0 },
      },
      vertexShader: `
        uniform float time;
        uniform float hoverIntensity;
        varying vec3 vNormal;
        varying vec3 vPosition;
        
        // Simplex 3D noise function
        vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
        vec4 mod289(vec4 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
        vec4 permute(vec4 x) { return mod289(((x*34.0)+1.0)*x); }
        vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }
        
        float snoise(vec3 v) {
          const vec2 C = vec2(1.0/6.0, 1.0/3.0);
          const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);
          vec3 i  = floor(v + dot(v, C.yyy));
          vec3 x0 = v - i + dot(i, C.xxx);
          vec3 g = step(x0.yzx, x0.xyz);
          vec3 l = 1.0 - g;
          vec3 i1 = min(g.xyz, l.zxy);
          vec3 i2 = max(g.xyz, l.zxy);
          vec3 x1 = x0 - i1 + C.xxx;
          vec3 x2 = x0 - i2 + C.yyy;
          vec3 x3 = x0 - D.yyy;
          i = mod289(i);
          vec4 p = permute(permute(permute(i.z + vec4(0.0, i1.z, i2.z, 1.0)) + i.y + vec4(0.0, i1.y, i2.y, 1.0)) + i.x + vec4(0.0, i1.x, i2.x, 1.0));
          float n_ = 0.142857142857;
          vec3 ns = n_ * D.wyz - D.xzx;
          vec4 j = p - 49.0 * floor(p * ns.z * ns.z);
          vec4 x_ = floor(j * ns.z);
          vec4 y_ = floor(j - 7.0 * x_);
          vec4 x = x_ *ns.x + ns.yyyy;
          vec4 y = y_ *ns.x + ns.yyyy;
          vec4 h = 1.0 - abs(x) - abs(y);
          vec4 b0 = vec4(x.xy, y.xy);
          vec4 b1 = vec4(x.zw, y.zw);
          vec4 s0 = floor(b0)*2.0 + 1.0;
          vec4 s1 = floor(b1)*2.0 + 1.0;
          vec4 sh = -step(h, vec4(0.0));
          vec4 a0 = b0.xzyw + s0.xzyw*sh.xxyy;
          vec4 a1 = b1.xzyw + s1.xzyw*sh.zzww;
          vec3 p0 = vec3(a0.xy, h.x);
          vec3 p1 = vec3(a0.zw, h.y);
          vec3 p2 = vec3(a1.xy, h.z);
          vec3 p3 = vec3(a1.zw, h.w);
          vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2,p2), dot(p3,p3)));
          p0 *= norm.x;
          p1 *= norm.y;
          p2 *= norm.z;
          p3 *= norm.w;
          vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
          m = m * m;
          return 42.0 * dot(m*m, vec4(dot(p0,x0), dot(p1,x1), dot(p2,x2), dot(p3,x3)));
        }
        
        void main() {
          vNormal = normalize(normalMatrix * normal);
          vPosition = position;
          
          // Multi-layered noise for fluid morphing effect
          float noise1 = snoise(position * 2.0 + time * 0.3);
          float noise2 = snoise(position * 4.0 + time * 0.5);
          float noise3 = snoise(position * 8.0 - time * 0.4);
          
          // Combine noise layers for complex liquid motion
          float displacement = noise1 * 0.15 + noise2 * 0.1 + noise3 * 0.05;
          
          // Add hover effect intensity
          displacement += hoverIntensity * 0.1;
          
          // Apply displacement along normal for organic morphing
          vec3 newPosition = position + normal * displacement;
          
          gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
        }
      `,
      fragmentShader: `
        uniform vec3 color;
        varying vec3 vNormal;
        varying vec3 vPosition;
        
        void main() {
          // Simple shading (transmission material will be layered on top)
          vec3 light = normalize(vec3(1.0, 1.0, 1.0));
          float dProd = max(0.0, dot(vNormal, light));
          gl_FragColor = vec4(color * (0.5 + 0.5 * dProd), 1.0);
        }
      `,
      transparent: true,
    });
  }, [status]);

  // Animate rotation, floating, and morphing
  useFrame((_, delta) => {
    if (meshRef.current) {
      timeRef.current += delta;
      
      // Update shader time uniform for morphing animation
      if (meshRef.current.material && 'uniforms' in meshRef.current.material) {
        (meshRef.current.material as THREE.ShaderMaterial).uniforms.time.value = timeRef.current;
        
        // Smooth hover transition
        const currentHover = (meshRef.current.material as THREE.ShaderMaterial).uniforms.hoverIntensity.value;
        const targetHover = hovered ? 1.0 : 0.0;
        (meshRef.current.material as THREE.ShaderMaterial).uniforms.hoverIntensity.value = 
          THREE.MathUtils.lerp(currentHover, targetHover, 0.1);
      }
      
      // Gentle rotation
      meshRef.current.rotation.x += delta * 0.1;
      meshRef.current.rotation.y += delta * 0.15;
      
      // Floating sin wave motion with multiple frequencies
      const floatY = Math.sin(timeRef.current * 0.5) * 0.2 + 
                     Math.sin(timeRef.current * 0.3) * 0.1;
      meshRef.current.position.y = position[1] + floatY;
    }
  });

  const color = getColorByStatus(status);

  // Interactive pointer events
  const handlePointerOver = (e: ThreeEvent<PointerEvent>) => {
    e.stopPropagation();
    setHovered(true);
    document.body.style.cursor = 'pointer';
  };

  const handlePointerOut = (e: ThreeEvent<PointerEvent>) => {
    e.stopPropagation();
    setHovered(false);
    document.body.style.cursor = 'default';
  };

  return (
    <group position={position}>
      {/* Inner morphing core with shader */}
      <mesh 
        ref={meshRef}
        material={shaderMaterial}
        onPointerOver={handlePointerOver}
        onPointerOut={handlePointerOut}
      >
        <sphereGeometry args={[0.95, 128, 128]} />
      </mesh>
      
      {/* Outer transmission shell for iridescence */}
      <mesh 
        scale={hovered ? 1.05 : 1}
        onPointerOver={handlePointerOver}
        onPointerOut={handlePointerOut}
      >
        <sphereGeometry args={[1, 128, 128]} />
        <MeshTransmissionMaterial
          transmission={1}
          thickness={1.2}
          roughness={0.05}
          chromaticAberration={0.8}
          anisotropicBlur={0.6}
          distortion={0.5}
          distortionScale={0.8}
          temporalDistortion={0.4}
          color={color}
          ior={1.8}
          transparent={true}
          opacity={0.85}
          metalness={0.1}
          {...{ clearcoat: 1, clearcoatRoughness: 0.1 }}
        />
      </mesh>
    </group>
  );
}
