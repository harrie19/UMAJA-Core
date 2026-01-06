/**
 * White Lab Configuration
 * Constants and configuration for the 3D Unity visualization
 */

export const CONFIG = {
  // Unity Blob Configuration
  blob: {
    position: [0, 1, 0] as [number, number, number],
    distort: 0.4,
    speed: 1.5,
    metalness: 1.0,
    roughness: 0.1,
    geometry: {
      segments: 128,
    },
    animation: {
      pulseMin: 1.0,
      pulseMax: 1.05,
      rotationSpeed: 0.001,
    },
  },

  // Camera Configuration
  camera: {
    position: [0, 2, 5] as [number, number, number],
    fov: 50,
    minDistance: 3,
    maxDistance: 10,
  },

  // Lighting Configuration
  lighting: {
    ambient: {
      intensity: 0.5,
    },
    directional: {
      intensity: 1.0,
      position: [5, 5, 5] as [number, number, number],
    },
    fill: {
      intensity: 0.3,
      position: [-3, 2, 2] as [number, number, number],
    },
    rim: {
      intensity: 0.5,
      position: [0, 2, -5] as [number, number, number],
    },
  },

  // Environment Configuration
  environment: {
    floor: {
      size: 20,
      resolution: 2048,
      blur: [300, 100] as [number, number],
      mixBlur: 1,
      mixStrength: 80,
      roughness: 1,
      depthScale: 1.2,
      minDepthThreshold: 0.4,
      maxDepthThreshold: 1.4,
      color: '#ffffff',
      metalness: 0.5,
    },
  },

  // Performance Configuration
  performance: {
    targetFPS: 60,
    mobileFPS: 30,
  },
} as const;

export type Config = typeof CONFIG;
