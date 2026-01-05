import { Html } from '@react-three/drei';

interface HolographicPanelProps {
  position: [number, number, number];
  data: any;
  type: 'checks' | 'metrics';
}

/**
 * HolographicPanel - Transparent floating UI with glassmorphism effect
 * Displays reality check data or system metrics
 */
export function HolographicPanel({ position, data, type }: HolographicPanelProps) {
  return (
    <Html
      transform
      position={position}
      distanceFactor={1.5}
      style={{
        width: '300px',
        pointerEvents: 'auto',
      }}
    >
      <div
        style={{
          background: 'rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(10px)',
          WebkitBackdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.3)',
          borderRadius: '12px',
          padding: '20px',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
          color: '#ffffff',
          fontFamily: 'monospace',
          fontSize: '12px',
          maxHeight: '400px',
          overflowY: 'auto',
        }}
      >
        {type === 'checks' ? (
          <ChecksPanel data={data} />
        ) : (
          <MetricsPanel data={data} />
        )}
      </div>
    </Html>
  );
}

/**
 * Panel showing individual reality checks
 */
function ChecksPanel({ data }: { data: any }) {
  if (!data || !Array.isArray(data)) {
    return (
      <div>
        <h3 style={{ marginTop: 0, color: '#ffffff', fontSize: '14px', fontWeight: 'bold' }}>
          Reality Checks
        </h3>
        <p style={{ color: 'rgba(255, 255, 255, 0.7)' }}>No data available</p>
      </div>
    );
  }

  const getStatusEmoji = (status: string): string => {
    switch (status?.toUpperCase()) {
      case 'OK':
        return '✅';
      case 'WARNING':
        return '⚠️';
      case 'CRITICAL':
        return '🚨';
      case 'ERROR':
        return '❌';
      default:
        return '❓';
    }
  };

  const getStatusColor = (status: string): string => {
    switch (status?.toUpperCase()) {
      case 'OK':
        return '#00ff88';
      case 'WARNING':
        return '#ffaa00';
      case 'CRITICAL':
      case 'ERROR':
        return '#ff0044';
      default:
        return '#ffffff';
    }
  };

  return (
    <div>
      <h3 style={{ marginTop: 0, color: '#ffffff', fontSize: '14px', fontWeight: 'bold', marginBottom: '15px' }}>
        Reality Checks
      </h3>
      {data.map((check: any, index: number) => (
        <div
          key={index}
          style={{
            marginBottom: '12px',
            padding: '10px',
            background: 'rgba(255, 255, 255, 0.05)',
            borderRadius: '8px',
            borderLeft: `3px solid ${getStatusColor(check.status)}`,
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '5px' }}>
            <span style={{ fontSize: '16px' }}>{getStatusEmoji(check.status)}</span>
            <span style={{ color: '#ffffff', fontWeight: 'bold', fontSize: '11px' }}>
              {check.name}
            </span>
          </div>
          <div style={{ marginLeft: '24px' }}>
            {/* Confidence bar */}
            <div style={{ marginBottom: '5px' }}>
              <div style={{ 
                background: 'rgba(255, 255, 255, 0.1)', 
                borderRadius: '4px', 
                height: '6px',
                overflow: 'hidden'
              }}>
                <div style={{ 
                  background: getStatusColor(check.status), 
                  width: `${(check.confidence || 0) * 100}%`, 
                  height: '100%',
                  transition: 'width 0.3s ease'
                }} />
              </div>
              <span style={{ color: 'rgba(255, 255, 255, 0.7)', fontSize: '10px' }}>
                {((check.confidence || 0) * 100).toFixed(0)}% confidence
              </span>
            </div>
            {/* Message */}
            <p style={{ 
              margin: '5px 0 0 0', 
              color: 'rgba(255, 255, 255, 0.8)', 
              fontSize: '10px',
              lineHeight: '1.4'
            }}>
              {check.message}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}

/**
 * Panel showing system metrics
 */
function MetricsPanel({ data }: { data: any }) {
  if (!data) {
    return (
      <div>
        <h3 style={{ marginTop: 0, color: '#ffffff', fontSize: '14px', fontWeight: 'bold' }}>
          System Metrics
        </h3>
        <p style={{ color: 'rgba(255, 255, 255, 0.7)' }}>No data available</p>
      </div>
    );
  }

  const checks = data.checks || [];
  const totalChecks = checks.length;
  const passedChecks = checks.filter((c: any) => c.status === 'OK').length;
  const successRate = totalChecks > 0 ? (passedChecks / totalChecks * 100).toFixed(1) : '0.0';
  const avgConfidence = totalChecks > 0 
    ? (checks.reduce((sum: number, c: any) => sum + (c.confidence || 0), 0) / totalChecks * 100).toFixed(1)
    : '0.0';

  return (
    <div>
      <h3 style={{ marginTop: 0, color: '#ffffff', fontSize: '14px', fontWeight: 'bold', marginBottom: '15px' }}>
        System Metrics
      </h3>
      
      {/* Overall Status */}
      <div style={{ marginBottom: '12px', padding: '10px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '8px' }}>
        <div style={{ color: 'rgba(255, 255, 255, 0.7)', fontSize: '10px', marginBottom: '3px' }}>
          Overall Status
        </div>
        <div style={{ color: '#ffffff', fontSize: '16px', fontWeight: 'bold' }}>
          {data.overall_status || 'UNKNOWN'}
        </div>
      </div>

      {/* Checks Passed */}
      <div style={{ marginBottom: '12px', padding: '10px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '8px' }}>
        <div style={{ color: 'rgba(255, 255, 255, 0.7)', fontSize: '10px', marginBottom: '3px' }}>
          Checks Passed
        </div>
        <div style={{ color: '#00ff88', fontSize: '16px', fontWeight: 'bold' }}>
          {passedChecks} / {totalChecks}
        </div>
      </div>

      {/* Success Rate */}
      <div style={{ marginBottom: '12px', padding: '10px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '8px' }}>
        <div style={{ color: 'rgba(255, 255, 255, 0.7)', fontSize: '10px', marginBottom: '3px' }}>
          Success Rate
        </div>
        <div style={{ color: '#ffffff', fontSize: '16px', fontWeight: 'bold' }}>
          {successRate}%
        </div>
      </div>

      {/* Average Confidence */}
      <div style={{ marginBottom: '12px', padding: '10px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '8px' }}>
        <div style={{ color: 'rgba(255, 255, 255, 0.7)', fontSize: '10px', marginBottom: '3px' }}>
          Avg Confidence
        </div>
        <div style={{ color: '#ffffff', fontSize: '16px', fontWeight: 'bold' }}>
          {avgConfidence}%
        </div>
      </div>

      {/* Last Update */}
      <div style={{ marginBottom: '0', padding: '10px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '8px' }}>
        <div style={{ color: 'rgba(255, 255, 255, 0.7)', fontSize: '10px', marginBottom: '3px' }}>
          Last Update
        </div>
        <div style={{ color: '#ffffff', fontSize: '10px' }}>
          {data.timestamp ? new Date(data.timestamp).toLocaleTimeString() : 'N/A'}
        </div>
      </div>
    </div>
  );
}
