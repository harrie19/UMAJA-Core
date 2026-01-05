'use client';

import { useState, useEffect } from 'react';
import { PermissionRequest } from '@/types';

interface PermissionManagerProps {
  requests: PermissionRequest[];
  onAccept: (id: string) => void;
  onReject: (id: string) => void;
}

export default function PermissionManager({ requests, onAccept, onReject }: PermissionManagerProps) {
  const [currentRequest, setCurrentRequest] = useState<PermissionRequest | null>(null);

  useEffect(() => {
    if (requests.length > 0 && !currentRequest) {
      setCurrentRequest(requests[0]);
    }
  }, [requests, currentRequest]);

  if (!currentRequest) return null;

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low':
        return 'text-green-600';
      case 'medium':
        return 'text-yellow-600';
      case 'high':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  const getRiskIcon = (risk: string) => {
    switch (risk) {
      case 'low':
        return '🟢';
      case 'medium':
        return '🟡';
      case 'high':
        return '🔴';
      default:
        return '⚪';
    }
  };

  const handleAccept = () => {
    onAccept(currentRequest.id);
    setCurrentRequest(null);
  };

  const handleReject = () => {
    onReject(currentRequest.id);
    setCurrentRequest(null);
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 pointer-events-auto">
      <div className="bg-white rounded-xl shadow-2xl p-6 max-w-md w-full mx-4">
        {/* Header */}
        <div className="flex items-center gap-3 mb-4 pb-4 border-b border-gray-200">
          <div className="text-3xl">🔵</div>
          <h2 className="text-xl font-bold text-gray-800">Blue Bubble fragt um Erlaubnis</h2>
        </div>

        {/* Action */}
        <div className="mb-4">
          <h3 className="text-sm font-semibold text-gray-600 mb-2">Aktion:</h3>
          <p className="text-base text-gray-800">{currentRequest.action}</p>
        </div>

        {/* Details */}
        <div className="mb-6 bg-gray-50 rounded-lg p-4">
          <h3 className="text-sm font-semibold text-gray-600 mb-3">Details:</h3>
          <div className="space-y-2 text-sm">
            {currentRequest.details.tool && (
              <div className="flex justify-between">
                <span className="text-gray-600">Tool:</span>
                <span className="font-medium text-gray-800">{currentRequest.details.tool}</span>
              </div>
            )}
            {currentRequest.details.size && (
              <div className="flex justify-between">
                <span className="text-gray-600">Größe:</span>
                <span className="font-medium text-gray-800">{currentRequest.details.size}</span>
              </div>
            )}
            {currentRequest.details.source && (
              <div className="flex justify-between">
                <span className="text-gray-600">Quelle:</span>
                <span className="font-medium text-gray-800 truncate max-w-[200px]">
                  {currentRequest.details.source}
                </span>
              </div>
            )}
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Risiko:</span>
              <span className={`font-medium ${getRiskColor(currentRequest.details.risk)}`}>
                {getRiskIcon(currentRequest.details.risk)} {currentRequest.details.risk.toUpperCase()}
              </span>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-3">
          <button
            onClick={handleAccept}
            className="flex-1 bg-green-500 hover:bg-green-600 text-white font-semibold py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            <span>✅</span>
            <span>ACCEPT</span>
          </button>
          <button
            onClick={handleReject}
            className="flex-1 bg-red-500 hover:bg-red-600 text-white font-semibold py-3 px-4 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            <span>❌</span>
            <span>REJECT</span>
          </button>
        </div>

        {/* More Info */}
        <button className="w-full mt-3 text-blue-600 hover:text-blue-700 text-sm font-medium py-2">
          ℹ️ MORE INFO
        </button>
      </div>
    </div>
  );
}
