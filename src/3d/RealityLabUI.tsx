import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment } from '@react-three/drei';
import { WhiteLaboratory } from './scenes/WhiteLaboratory';
import { IridescentBlob } from './components/IridescentBlob';
import { HolographicPanel } from './components/HolographicPanel';
import { DNAHelix } from './components/DNAHelix';
import { ParticleCloud } from './components/ParticleCloud';
import { useRealityStream } from '../hooks/useRealityStream';

/**
 * RealityLabUI - Main 3D scene integrating all WhiteLab components
 * Combines white laboratory environment with real-time reality check visualization
 * 
 * Philosophy: Real-time TRUTH visualization with Hollywood-quality aesthetics
 */
export function RealityLabUI() {
  const { realityData, isConnected, error, requestUpdate } = useRealityStream();
  
  return (
    <div style={{ width: '100vw', height: '100vh', background: '#000000' }}>
      <Canvas 
        camera={{ position: [0, 2, 5], fov: 75 }}
        gl={{ antialias: true, alpha: false }}
      >
        {/* Environment lighting */}
        <Environment preset="studio" />
        
        {/* White Laboratory Scene */}
        <WhiteLaboratory />
        
        {/* Central Iridescent Blob (reacts to overall status) */}
        <IridescentBlob 
          position={[0, 1, 0]} 
          status={realityData?.overall_status} 
        />
        
        {/* Left Panel - Reality Checks */}
        <HolographicPanel 
          position={[-3, 1.5, 0]} 
          data={realityData?.checks}
          type="checks"
        />
        
        {/* Right Panel - System Metrics */}
        <HolographicPanel 
          position={[3, 1.5, 0]} 
          data={realityData}
          type="metrics"
        />
        
        {/* DNA Helix - Data Flow Visualization */}
        <DNAHelix 
          position={[0, 1, 3]} 
          data={realityData?.vector_analysis} 
        />
        
        {/* Particle Cloud - Organic data visualization */}
        <ParticleCloud 
          count={realityData?.checks?.length ? realityData.checks.length * 100 : 5000}
          status={realityData?.overall_status}
        />
        
        {/* Camera Controls */}
        <OrbitControls 
          enableDamping 
          dampingFactor={0.05}
          maxPolarAngle={Math.PI / 2}
          minDistance={3}
          maxDistance={10}
        />
      </Canvas>
      
      {/* Connection Status Indicator */}
      <div style={{
        position: 'absolute',
        top: 20,
        right: 20,
        padding: '10px 20px',
        background: isConnected ? 'rgba(0, 255, 0, 0.2)' : 'rgba(255, 0, 0, 0.2)',
        border: `1px solid ${isConnected ? '#0f0' : '#f00'}`,
        borderRadius: '5px',
        color: 'white',
        fontFamily: 'monospace',
        fontSize: '14px',
        backdropFilter: 'blur(10px)',
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        zIndex: 1000,
      }}>
        <span style={{ fontSize: '18px' }}>
          {isConnected ? '🟢' : '🔴'}
        </span>
        <span>
          {isConnected ? 'LIVE' : 'DISCONNECTED'}
        </span>
      </div>

      {/* Error Display */}
      {error && (
        <div style={{
          position: 'absolute',
          top: 80,
          right: 20,
          padding: '10px 20px',
          background: 'rgba(255, 0, 0, 0.2)',
          border: '1px solid #f00',
          borderRadius: '5px',
          color: 'white',
          fontFamily: 'monospace',
          fontSize: '12px',
          backdropFilter: 'blur(10px)',
          maxWidth: '300px',
          zIndex: 1000,
        }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Manual Refresh Button */}
      <button
        onClick={requestUpdate}
        disabled={!isConnected}
        style={{
          position: 'absolute',
          top: 20,
          left: 20,
          padding: '10px 20px',
          background: 'rgba(255, 255, 255, 0.1)',
          border: '1px solid rgba(255, 255, 255, 0.3)',
          borderRadius: '5px',
          color: 'white',
          fontFamily: 'monospace',
          fontSize: '14px',
          cursor: isConnected ? 'pointer' : 'not-allowed',
          backdropFilter: 'blur(10px)',
          opacity: isConnected ? 1 : 0.5,
          transition: 'all 0.2s ease',
          zIndex: 1000,
        }}
        onMouseEnter={(e) => {
          if (isConnected) {
            e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)';
          }
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)';
        }}
      >
        🔄 Refresh
      </button>

      {/* Title/Branding */}
      <div style={{
        position: 'absolute',
        bottom: 20,
        left: '50%',
        transform: 'translateX(-50%)',
        padding: '10px 30px',
        background: 'rgba(255, 255, 255, 0.05)',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        borderRadius: '25px',
        color: 'white',
        fontFamily: 'monospace',
        fontSize: '16px',
        fontWeight: 'bold',
        backdropFilter: 'blur(10px)',
        letterSpacing: '2px',
        zIndex: 1000,
      }}>
        🥽 WHITELAB REALITY ANALYSER
      </div>
    </div>
  );
}
