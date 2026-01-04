'use client';

import { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import { useSphere } from '@react-three/cannon';
import * as THREE from 'three';
import { FormType } from '@/types';

interface BlueBubbleProps {
  position: [number, number, number];
  onFormChange?: (form: FormType) => void;
}

export default function BlueBubble({ position, onFormChange }: BlueBubbleProps) {
  const [currentForm, setCurrentForm] = useState<FormType>('bubble');
  const [hovered, setHovered] = useState(false);
  const [speechBubbleText, setSpeechBubbleText] = useState<string | null>(null);
  const meshRef = useRef<THREE.Mesh>(null);
  const materialRef = useRef<THREE.MeshStandardMaterial>(null);
  
  // Physics body for the bubble
  const [ref, api] = useSphere(() => ({
    mass: 0, // Float in place
    position,
    args: [1], // radius
  }));

  // Pulsation animation
  useFrame((state) => {
    if (meshRef.current) {
      const scale = 1 + Math.sin(state.clock.elapsedTime * 2) * 0.1;
      meshRef.current.scale.setScalar(scale);
    }
    
    // Update emissive intensity on hover
    if (materialRef.current) {
      materialRef.current.emissiveIntensity = hovered ? 1.5 : 1.0;
    }
  });

  const handleClick = () => {
    setSpeechBubbleText('Hallo! Ich kann mich in viele Formen verwandeln. Was möchtest du bauen?');
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
      setSpeechBubbleText(null);
    }, 5000);
  };

  const handleTransform = (newForm: FormType) => {
    setCurrentForm(newForm);
    setSpeechBubbleText(`Verwandle mich in ${newForm}...`);
    
    if (onFormChange) {
      onFormChange(newForm);
    }
    
    setTimeout(() => {
      setSpeechBubbleText(`Ich bin jetzt ${newForm}!`);
      setTimeout(() => setSpeechBubbleText(null), 3000);
    }, 1000);
  };

  return (
    <group>
      {/* @ts-ignore */}
      <mesh
        ref={(node) => {
          meshRef.current = node;
          // @ts-ignore
          ref.current = node;
        }}
        onClick={handleClick}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <sphereGeometry args={[1, 32, 32]} />
        <meshStandardMaterial
          ref={materialRef}
          color="#4FC3F7"
          emissive="#2196F3"
          emissiveIntensity={1.0}
          metalness={0.3}
          roughness={0.2}
          transparent
          opacity={0.9}
        />
      </mesh>
      
      {/* Point light for glow effect */}
      <pointLight position={position} color="#4FC3F7" intensity={hovered ? 2 : 1} distance={5} />
      
      {/* Speech bubble */}
      {speechBubbleText && (
        <Html position={[0, 2, 0]} center>
          <div className="bg-white rounded-lg shadow-xl p-4 max-w-xs pointer-events-none">
            <div className="text-sm text-gray-800">{speechBubbleText}</div>
            <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-full">
              <div className="w-0 h-0 border-l-8 border-l-transparent border-r-8 border-r-transparent border-t-8 border-t-white"></div>
            </div>
          </div>
        </Html>
      )}
    </group>
  );
}
