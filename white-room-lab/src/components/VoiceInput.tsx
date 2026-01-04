'use client';

import { useState, useEffect } from 'react';
import { createVoiceInput } from '@/lib/voice';

interface VoiceInputProps {
  onTranscript?: (text: string) => void;
  onError?: (error: string) => void;
}

export default function VoiceInput({ onTranscript, onError }: VoiceInputProps) {
  const [isListening, setIsListening] = useState(false);
  const [isSupported, setIsSupported] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [voiceInput, setVoiceInput] = useState<any>(null);

  useEffect(() => {
    const voice = createVoiceInput();
    setVoiceInput(voice);
    setIsSupported(voice.isSupported());

    voice.onResult((text) => {
      setTranscript(text);
      if (onTranscript) {
        onTranscript(text);
      }
    });

    voice.onError((error) => {
      console.error('Voice input error:', error);
      if (onError) {
        onError(error);
      }
      setIsListening(false);
    });
  }, [onTranscript, onError]);

  const toggleListening = () => {
    if (!voiceInput) return;

    if (isListening) {
      voiceInput.stop();
      setIsListening(false);
    } else {
      voiceInput.start();
      setIsListening(true);
      setTranscript('');
    }
  };

  if (!isSupported) {
    return null; // Hide component if not supported
  }

  return (
    <div className="bg-white/90 backdrop-blur-sm rounded-lg shadow-lg p-4">
      <button
        onClick={toggleListening}
        className={`w-full flex items-center justify-center gap-3 px-6 py-3 rounded-lg font-medium transition-all ${
          isListening
            ? 'bg-red-500 hover:bg-red-600 text-white animate-pulse'
            : 'bg-blue-500 hover:bg-blue-600 text-white'
        }`}
      >
        <span className="text-2xl">🎤</span>
        <span>{isListening ? 'Höre zu...' : 'Spracheingabe'}</span>
      </button>
      
      {transcript && (
        <div className="mt-3 p-3 bg-gray-100 rounded-lg">
          <p className="text-sm text-gray-700 italic">"{transcript}"</p>
        </div>
      )}
    </div>
  );
}
