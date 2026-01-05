import { useState, useEffect } from 'react';
import { io, Socket } from 'socket.io-client';

interface RealityCheck {
  name: string;
  status: 'OK' | 'WARNING' | 'CRITICAL' | 'ERROR';
  confidence: number;
  message: string;
  details: Record<string, any>;
  timestamp: string;
}

interface RealityData {
  timestamp: string;
  overall_status: string;
  checks: RealityCheck[];
}

interface UseRealityStreamReturn {
  realityData: RealityData | null;
  isConnected: boolean;
  error: string | null;
  requestUpdate: () => void;
}

/**
 * React hook for consuming Reality Agent WebSocket data
 * Automatically connects to the reality stream server and provides live updates
 */
export function useRealityStream(): UseRealityStreamReturn {
  const [realityData, setRealityData] = useState<RealityData | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [socket, setSocket] = useState<Socket | null>(null);

  useEffect(() => {
    // Connect to WebSocket server
    const socketUrl = import.meta.env.VITE_REALITY_STREAM_URL || 'http://localhost:3002';
    const newSocket = io(socketUrl);

    // Connection events
    newSocket.on('connect', () => {
      console.log('🟢 Connected to Reality Stream');
      setIsConnected(true);
      setError(null);
    });

    newSocket.on('disconnect', () => {
      console.log('🔴 Disconnected from Reality Stream');
      setIsConnected(false);
    });

    // Data events
    newSocket.on('reality-update', (data: RealityData) => {
      console.log('📡 Reality update received:', data);
      setRealityData(data);
      setError(null);
    });

    newSocket.on('reality-error', (errorData: { message: string; timestamp: string }) => {
      console.error('❌ Reality error:', errorData);
      setError(errorData.message);
    });

    // Connection errors
    newSocket.on('connect_error', (err) => {
      console.error('❌ Connection error:', err.message);
      setError(`Connection error: ${err.message}`);
      setIsConnected(false);
    });

    setSocket(newSocket);

    // Cleanup on unmount
    return () => {
      console.log('👋 Disconnecting from Reality Stream');
      newSocket.disconnect();
    };
  }, []);

  // Function to manually request an update
  const requestUpdate = () => {
    if (socket && isConnected) {
      console.log('🔄 Requesting manual update...');
      socket.emit('request-update');
    } else {
      console.warn('⚠️ Cannot request update: not connected');
    }
  };

  return { 
    realityData, 
    isConnected, 
    error,
    requestUpdate 
  };
}
