import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment } from '@react-three/drei';
import { WhiteLaboratory } from './scenes/WhiteLaboratory';
import { IridescentBlob } from './components/IridescentBlob';
import { HolographicPanel } from './components/HolographicPanel';
import { DNAHelix } from './components/DNAHelix';
import { ParticleCloud } from './components/ParticleCloud';
import { useRealityStream } from '../hooks/useRealityStream';

/**
 * RealityLabUI - Genesis Core 3D Interface
 * Cohesive integration of WhiteLab environment with real-time analytics engine
 * 
 * Philosophy: Real-time TRUTH visualization with cinema-quality aesthetics
 * Mission: AI-human collaboration in the UMAJA OS WhiteLab
 */
export function RealityLabUI() {
  const { realityData, isConnected, error, requestUpdate } = useRealityStream();
  
  return (
    <div style={{ width: '100vw', height: '100vh', background: '#000000' }}>
      <Canvas 
        camera={{ position: [0, 3, 8], fov: 60 }}
        gl={{ 
          antialias: true, 
          alpha: false,
          powerPreference: 'high-performance'
        }}
      >
        {/* Studio environment lighting */}
        <Environment preset="studio" />
        
        {/* White Laboratory Scene - Expanded Spatial Design */}
        <WhiteLaboratory />
        
        {/* Central Morphing Liquid Avatar (Genesis Core consciousness) */}
        <IridescentBlob 
          position={[0, 2, 0]} 
          status={realityData?.overall_status} 
        />
        
        {/* Left Panel - Reality Checks (Analytics Surface) */}
        <HolographicPanel 
          position={[-5, 2.5, 0]} 
          data={realityData?.checks}
          type="checks"
        />
        
        {/* Right Panel - System Metrics (Engine Analytics) */}
        <HolographicPanel 
          position={[5, 2.5, 0]} 
          data={realityData}
          type="metrics"
        />
        
        {/* DNA Helix - Data Flow Visualization */}
        <DNAHelix 
          position={[0, 2, 4]} 
          data={realityData?.vector_analysis} 
        />
        
        {/* Particle Cloud - Organic data visualization atmosphere */}
        <ParticleCloud 
          count={realityData?.checks?.length ? realityData.checks.length * 100 : 5000}
          status={realityData?.overall_status}
        />
        
        {/* Camera Controls - Enhanced for larger space */}
        <OrbitControls 
          enableDamping 
          dampingFactor={0.08}
          maxPolarAngle={Math.PI / 2}
          minDistance={5}
          maxDistance={15}
          target={[0, 2, 0]}
        />
      </Canvas>
      
      {/* Genesis Core HUD - Analytics Engine UI */}
      
      {/* Connection Status Indicator */}
      <div style={{
        position: 'absolute',
        top: 20,
        right: 20,
        padding: '12px 24px',
        background: isConnected 
          ? 'linear-gradient(135deg, rgba(0, 255, 136, 0.15), rgba(0, 255, 136, 0.05))' 
          : 'linear-gradient(135deg, rgba(255, 0, 68, 0.15), rgba(255, 0, 68, 0.05))',
        border: `2px solid ${isConnected ? '#00ff88' : '#ff0044'}`,
        borderRadius: '8px',
        color: 'white',
        fontFamily: '"Courier New", monospace',
        fontSize: '13px',
        fontWeight: 'bold',
        backdropFilter: 'blur(12px)',
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        zIndex: 1000,
        boxShadow: isConnected 
          ? '0 0 20px rgba(0, 255, 136, 0.3)' 
          : '0 0 20px rgba(255, 0, 68, 0.3)',
        textTransform: 'uppercase',
        letterSpacing: '1.5px',
      }}>
        <span style={{ fontSize: '20px', filter: isConnected ? 'drop-shadow(0 0 5px #0f0)' : 'drop-shadow(0 0 5px #f00)' }}>
          {isConnected ? '⬢' : '⬡'}
        </span>
        <span>
          {isConnected ? 'GENESIS CORE LIVE' : 'CORE OFFLINE'}
        </span>
      </div>

      {/* System Metrics Display */}
      <div style={{
        position: 'absolute',
        top: 80,
        right: 20,
        padding: '12px 20px',
        background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.02))',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        borderRadius: '8px',
        color: 'rgba(255, 255, 255, 0.9)',
        fontFamily: '"Courier New", monospace',
        fontSize: '11px',
        backdropFilter: 'blur(12px)',
        minWidth: '200px',
        zIndex: 1000,
      }}>
        <div style={{ marginBottom: '8px', color: '#00ff88', fontWeight: 'bold', letterSpacing: '1px' }}>ENGINE ANALYTICS</div>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
          <span style={{ opacity: 0.7 }}>STATUS:</span>
          <span style={{ color: '#00ff88' }}>{realityData?.overall_status || 'INITIALIZING'}</span>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
          <span style={{ opacity: 0.7 }}>CHECKS:</span>
          <span>{realityData?.checks?.length || 0}</span>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          <span style={{ opacity: 0.7 }}>UPTIME:</span>
          <span>{Math.floor(performance.now() / 1000)}s</span>
        </div>
      </div>

      {/* Error Display - Enhanced */}
      {error && (
        <div style={{
          position: 'absolute',
          top: 200,
          right: 20,
          padding: '12px 20px',
          background: 'linear-gradient(135deg, rgba(255, 0, 68, 0.2), rgba(255, 0, 68, 0.05))',
          border: '2px solid #ff0044',
          borderRadius: '8px',
          color: 'white',
          fontFamily: '"Courier New", monospace',
          fontSize: '11px',
          backdropFilter: 'blur(12px)',
          maxWidth: '300px',
          zIndex: 1000,
          boxShadow: '0 0 20px rgba(255, 0, 68, 0.3)',
        }}>
          <strong style={{ color: '#ff0044', letterSpacing: '1px' }}>⚠ SYSTEM ERROR:</strong>
          <div style={{ marginTop: '8px', opacity: 0.9 }}>{error}</div>
        </div>
      )}

      {/* Manual Refresh Button - Analytics Style */}
      <button
        onClick={requestUpdate}
        disabled={!isConnected}
        style={{
          position: 'absolute',
          top: 20,
          left: 20,
          padding: '12px 24px',
          background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.05))',
          border: '2px solid rgba(255, 255, 255, 0.3)',
          borderRadius: '8px',
          color: 'white',
          fontFamily: '"Courier New", monospace',
          fontSize: '13px',
          fontWeight: 'bold',
          cursor: isConnected ? 'pointer' : 'not-allowed',
          backdropFilter: 'blur(12px)',
          opacity: isConnected ? 1 : 0.4,
          transition: 'all 0.3s ease',
          zIndex: 1000,
          textTransform: 'uppercase',
          letterSpacing: '1.5px',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
        }}
        onMouseEnter={(e) => {
          if (isConnected) {
            e.currentTarget.style.background = 'linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1))';
            e.currentTarget.style.boxShadow = '0 0 20px rgba(255, 255, 255, 0.3)';
          }
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.background = 'linear-gradient(135deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.05))';
          e.currentTarget.style.boxShadow = 'none';
        }}
      >
        <span style={{ fontSize: '16px' }}>⟳</span>
        <span>Refresh Data</span>
      </button>

      {/* Title/Branding - Genesis Core */}
      <div style={{
        position: 'absolute',
        bottom: 30,
        left: '50%',
        transform: 'translateX(-50%)',
        padding: '14px 40px',
        background: 'linear-gradient(135deg, rgba(0, 255, 136, 0.15), rgba(0, 255, 136, 0.05))',
        border: '2px solid rgba(0, 255, 136, 0.4)',
        borderRadius: '30px',
        color: 'white',
        fontFamily: '"Courier New", monospace',
        fontSize: '16px',
        fontWeight: 'bold',
        backdropFilter: 'blur(12px)',
        letterSpacing: '3px',
        zIndex: 1000,
        textTransform: 'uppercase',
        boxShadow: '0 0 30px rgba(0, 255, 136, 0.2)',
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
      }}>
        <span style={{ fontSize: '20px', filter: 'drop-shadow(0 0 5px #0f8)' }}>◬</span>
        <span>UMAJA OS • Genesis Core WhiteLab</span>
      </div>
    </div>
  );
}
