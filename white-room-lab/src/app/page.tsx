'use client';

import { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Environment } from '@react-three/drei';
import { Physics } from '@react-three/cannon';
import BlueBubble from '@/components/BlueBubble';
import WhiteRoom from '@/components/WhiteRoom';
import ChatInterface from '@/components/ChatInterface';
import PermissionManager from '@/components/PermissionManager';
import SystemStatus from '@/components/SystemStatus';
import VoiceInput from '@/components/VoiceInput';
import { PermissionRequest, FormType } from '@/types';

export default function WhiteRoomLab() {
  const [permissionRequests, setPermissionRequests] = useState<PermissionRequest[]>([]);
  const [currentForm, setCurrentForm] = useState<FormType>('bubble');

  const handleCommand = (command: any) => {
    console.log('Command received:', command);

    if (command.type === 'permission_request') {
      const request: PermissionRequest = {
        id: Date.now().toString(),
        action: command.action === 'install_cad_tool' 
          ? `CAD-Werkzeug installieren für: ${command.target}`
          : command.action,
        details: {
          tool: 'FreeCAD.js',
          size: '2.3 MB',
          source: 'npm registry',
          risk: 'low',
        },
        timestamp: Date.now(),
      };
      setPermissionRequests([...permissionRequests, request]);
    } else if (command.type === 'transform') {
      setCurrentForm(command.form);
    }
  };

  const handleAcceptPermission = (id: string) => {
    console.log('Permission accepted:', id);
    setPermissionRequests(permissionRequests.filter(req => req.id !== id));
    // Here you would actually install/enable the requested feature
  };

  const handleRejectPermission = (id: string) => {
    console.log('Permission rejected:', id);
    setPermissionRequests(permissionRequests.filter(req => req.id !== id));
  };

  const handleVoiceTranscript = (text: string) => {
    console.log('Voice transcript:', text);
    // Could automatically send to chat interface
  };

  return (
    <div className="h-screen w-screen bg-white relative overflow-hidden">
      {/* 3D Lab Scene */}
      <Canvas 
        camera={{ position: [0, 5, 10], fov: 50 }}
        shadows
        gl={{ antialias: true, alpha: false }}
      >
        {/* Lighting Setup */}
        <ambientLight intensity={0.4} />
        <spotLight 
          position={[10, 15, 10]} 
          angle={0.3} 
          penumbra={1} 
          intensity={1}
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
        />
        <pointLight position={[-10, 10, -10]} intensity={0.5} />
        
        {/* Physics World */}
        <Physics gravity={[0, -9.81, 0]}>
          {/* Environment */}
          <WhiteRoom />
          
          {/* Blue Bubble AI Agent */}
          <BlueBubble 
            position={[0, 2, 0]} 
            onFormChange={(form) => setCurrentForm(form)}
          />
        </Physics>
        
        {/* Camera Controls */}
        <OrbitControls 
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          minDistance={3}
          maxDistance={50}
          maxPolarAngle={Math.PI / 2}
        />
        
        {/* Studio Lighting Environment */}
        <Environment preset="studio" />
      </Canvas>
      
      {/* UI Overlay */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="pointer-events-auto absolute top-4 right-4">
          <SystemStatus />
        </div>
        
        <div className="pointer-events-auto absolute bottom-4 left-4 right-4 flex gap-4 items-end">
          <ChatInterface onCommand={handleCommand} />
          <VoiceInput onTranscript={handleVoiceTranscript} />
        </div>
      </div>
      
      {/* Permission Modal (rendered conditionally) */}
      {permissionRequests.length > 0 && (
        <PermissionManager 
          requests={permissionRequests}
          onAccept={handleAcceptPermission}
          onReject={handleRejectPermission}
        />
      )}
    </div>
  );
}
