/**
 * Voice input handling using Web Speech API
 */

interface VoiceInputCallbacks {
  onResult?: (text: string) => void;
  onError?: (error: string) => void;
  onStart?: () => void;
  onEnd?: () => void;
}

export interface VoiceInputInstance {
  isSupported: () => boolean;
  start: () => void;
  stop: () => void;
  onResult: (callback: (text: string) => void) => void;
  onError: (callback: (error: string) => void) => void;
  onStart: (callback: () => void) => void;
  onEnd: (callback: () => void) => void;
}

/**
 * Create voice input instance using Web Speech API
 */
export function createVoiceInput(): VoiceInputInstance {
  let recognition: any = null;
  const callbacks: VoiceInputCallbacks = {};

  // Check for Web Speech API support
  const SpeechRecognition = 
    typeof window !== 'undefined' &&
    ((window as any).SpeechRecognition || (window as any).webkitSpeechRecognition);

  if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'de-DE'; // German by default, can be changed

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      if (callbacks.onResult) {
        callbacks.onResult(transcript);
      }
    };

    recognition.onerror = (event: any) => {
      const error = event.error || 'Unknown error';
      if (callbacks.onError) {
        callbacks.onError(error);
      }
    };

    recognition.onstart = () => {
      if (callbacks.onStart) {
        callbacks.onStart();
      }
    };

    recognition.onend = () => {
      if (callbacks.onEnd) {
        callbacks.onEnd();
      }
    };
  }

  return {
    isSupported: () => !!SpeechRecognition,
    
    start: () => {
      if (recognition) {
        try {
          recognition.start();
        } catch (error) {
          console.error('Voice input start error:', error);
          if (callbacks.onError) {
            callbacks.onError('Failed to start voice input');
          }
        }
      }
    },

    stop: () => {
      if (recognition) {
        try {
          recognition.stop();
        } catch (error) {
          console.error('Voice input stop error:', error);
        }
      }
    },

    onResult: (callback: (text: string) => void) => {
      callbacks.onResult = callback;
    },

    onError: (callback: (error: string) => void) => {
      callbacks.onError = callback;
    },

    onStart: (callback: () => void) => {
      callbacks.onStart = callback;
    },

    onEnd: (callback: () => void) => {
      callbacks.onEnd = callback;
    },
  };
}

/**
 * Set language for voice recognition
 */
export function setVoiceLanguage(language: 'de-DE' | 'en-US' | 'en-GB'): void {
  // This would need to be integrated with the recognition instance
  // For now, it's a placeholder
  console.log(`Voice language set to: ${language}`);
}

/**
 * Get supported languages
 */
export function getSupportedLanguages(): string[] {
  return [
    'de-DE', // German
    'en-US', // English (US)
    'en-GB', // English (UK)
  ];
}
