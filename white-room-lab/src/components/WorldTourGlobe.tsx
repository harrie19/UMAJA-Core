/**
 * World Tour 3D Globe
 * Earth with city pins and rotation
 */
'use client';

import { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { Text } from '@react-three/drei';
import { WORLD_TOUR_CITIES, type City } from '../lib/umaja-api';
import * as THREE from 'three';

interface CityPinProps {
  city: City;
  earthRadius: number;
  onClick: () => void;
}

function CityPin({ city, earthRadius, onClick }: CityPinProps) {
  const [hovered, setHovered] = useState(false);

  // Convert lat/lng to 3D position on sphere
  const phi = (90 - city.lat) * (Math.PI / 180);
  const theta = (city.lng + 180) * (Math.PI / 180);

  const x = -(earthRadius * Math.sin(phi) * Math.cos(theta));
  const z = earthRadius * Math.sin(phi) * Math.sin(theta);
  const y = earthRadius * Math.cos(phi);

  const position: [number, number, number] = [x, y, z];

  return (
    <group position={position}>
      <mesh
        onClick={onClick}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <cylinderGeometry args={[0.05, 0.05, 0.3, 8]} />
        <meshStandardMaterial
          color={city.visited ? '#4CAF50' : '#FF5722'}
          emissive={city.visited ? '#4CAF50' : '#FF5722'}
          emissiveIntensity={hovered ? 0.8 : 0.3}
        />
      </mesh>

      {hovered && (
        <Text
          position={[0, 0.5, 0]}
          fontSize={0.15}
          color="white"
          anchorX="center"
          anchorY="middle"
        >
          {city.name}
          {'\n'}
          {city.country}
          {city.visited && '\n✓ Visited'}
        </Text>
      )}
    </group>
  );
}

export default function WorldTourGlobe() {
  const groupRef = useRef<THREE.Group>(null);
  const [selectedCity, setSelectedCity] = useState<City | null>(null);

  // Rotate globe
  useFrame(() => {
    if (groupRef.current) {
      groupRef.current.rotation.y += 0.002;
    }
  });

  const earthRadius = 1.5;
  const visitedCount = WORLD_TOUR_CITIES.filter(c => c.visited).length;

  return (
    <group position={[-5, 0, -5]}>
      <group ref={groupRef}>
        {/* Earth Sphere */}
        <mesh>
          <sphereGeometry args={[earthRadius, 32, 32]} />
          <meshStandardMaterial
            color="#1976D2"
            emissive="#0D47A1"
            emissiveIntensity={0.2}
            metalness={0.4}
            roughness={0.6}
          />
        </mesh>

        {/* Simple continent shapes (stylized) */}
        {[
          // North America
          { lat: 40, lng: -100, size: 0.3 },
          // South America
          { lat: -10, lng: -60, size: 0.25 },
          // Europe
          { lat: 50, lng: 10, size: 0.2 },
          // Africa
          { lat: 0, lng: 20, size: 0.3 },
          // Asia
          { lat: 30, lng: 100, size: 0.4 },
          // Australia
          { lat: -25, lng: 135, size: 0.15 },
        ].map((continent, i) => {
          const phi = (90 - continent.lat) * (Math.PI / 180);
          const theta = (continent.lng + 180) * (Math.PI / 180);
          const x = -(earthRadius * 1.01 * Math.sin(phi) * Math.cos(theta));
          const z = earthRadius * 1.01 * Math.sin(phi) * Math.sin(theta);
          const y = earthRadius * 1.01 * Math.cos(phi);

          return (
            <mesh key={i} position={[x, y, z]}>
              <sphereGeometry args={[continent.size, 8, 8]} />
              <meshBasicMaterial color="#2E7D32" opacity={0.6} transparent />
            </mesh>
          );
        })}

        {/* City Pins */}
        {WORLD_TOUR_CITIES.map(city => (
          <CityPin
            key={city.name}
            city={city}
            earthRadius={earthRadius}
            onClick={() => setSelectedCity(city)}
          />
        ))}

        {/* Connection Lines between visited cities */}
        {WORLD_TOUR_CITIES.filter(c => c.visited).map((city, i, arr) => {
          if (i === arr.length - 1) return null;
          
          const nextCity = arr[i + 1];
          const phi1 = (90 - city.lat) * (Math.PI / 180);
          const theta1 = (city.lng + 180) * (Math.PI / 180);
          const x1 = -(earthRadius * 1.02 * Math.sin(phi1) * Math.cos(theta1));
          const z1 = earthRadius * 1.02 * Math.sin(phi1) * Math.sin(theta1);
          const y1 = earthRadius * 1.02 * Math.cos(phi1);

          const phi2 = (90 - nextCity.lat) * (Math.PI / 180);
          const theta2 = (nextCity.lng + 180) * (Math.PI / 180);
          const x2 = -(earthRadius * 1.02 * Math.sin(phi2) * Math.cos(theta2));
          const z2 = earthRadius * 1.02 * Math.sin(phi2) * Math.sin(theta2);
          const y2 = earthRadius * 1.02 * Math.cos(phi2);

          const curve = new THREE.QuadraticBezierCurve3(
            new THREE.Vector3(x1, y1, z1),
            new THREE.Vector3(0, 3, 0), // Arc through center
            new THREE.Vector3(x2, y2, z2)
          );

          const points = curve.getPoints(20);

          return (
            <line key={i}>
              <bufferGeometry>
                <bufferAttribute
                  attach="attributes-position"
                  count={points.length}
                  array={new Float32Array(points.flatMap(p => [p.x, p.y, p.z]))}
                  itemSize={3}
                />
              </bufferGeometry>
              <lineBasicMaterial color="#4FC3F7" opacity={0.4} transparent />
            </line>
          );
        })}
      </group>

      {/* Info Panel */}
      <Text position={[0, 2.5, 0]} fontSize={0.25} color="white" anchorX="center">
        World Tour
      </Text>
      <Text position={[0, 2.1, 0]} fontSize={0.15} color="#4CAF50" anchorX="center">
        {`${visitedCount}/${WORLD_TOUR_CITIES.length} cities visited`}
      </Text>

      {selectedCity && (
        <group position={[0, -2.5, 0]}>
          <Text position={[0, 0.3, 0]} fontSize={0.2} color="white" anchorX="center">
            {selectedCity.name}, {selectedCity.country}
          </Text>
          {selectedCity.visited && selectedCity.visit_date && (
            <Text position={[0, 0, 0]} fontSize={0.12} color="#4CAF50" anchorX="center">
              Visited: {selectedCity.visit_date}
            </Text>
          )}
        </group>
      )}

      {/* Ambient light for globe */}
      <ambientLight intensity={0.4} />
      <pointLight position={[5, 5, 5]} intensity={1} />
    </group>
  );
}
