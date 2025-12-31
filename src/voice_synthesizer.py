"""
UMAJA WORLDTOUR - Voice Synthesizer
Text-to-Speech with personality voices supporting multiple TTS backends
"""

import os
import hashlib
from pathlib import Path
from typing import Dict, Literal, Optional
import logging

# Conditional imports for TTS backends
try:
    from elevenlabs import generate, set_api_key, voices
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceSynthesizer:
    """
    Text-to-Speech with personality voices.
    Supports ElevenLabs (premium), Google TTS (fallback), pyttsx3 (offline).
    """
    
    PERSONALITIES = ['the_professor', 'the_worrier', 'the_enthusiast']
    
    def __init__(self, output_dir: str = "static/audio"):
        """
        Initialize the voice synthesizer.
        
        Args:
            output_dir: Directory to save audio files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Voice profiles for each personality
        self.voice_profiles = {
            'the_professor': {
                'description': 'Warm, thoughtful, curious voice',
                'pitch': 0.9,  # Slightly lower, thoughtful
                'speed': 0.9,  # Measured, considered pace
                'tone': 'warm',
                'elevenlabs_voice': 'Antoni',  # Deep, sophisticated
                'gtts_lang': 'en',
                'gtts_tld': 'com',
                'pyttsx3_rate': 150,  # Words per minute
                'pyttsx3_volume': 0.9
            },
            'the_worrier': {
                'description': 'Gentle, concerned, caring voice',
                'pitch': 1.1,  # Slightly higher, anxious
                'speed': 1.0,  # Normal but with pauses
                'tone': 'caring',
                'elevenlabs_voice': 'Arnold',  # Clear, formal
                'gtts_lang': 'en',
                'gtts_tld': 'com',
                'pyttsx3_rate': 160,  # Slightly faster when worried
                'pyttsx3_volume': 0.95
            },
            'the_enthusiast': {
                'description': 'Bright, energetic, joyful voice',
                'pitch': 1.2,  # Higher, excited
                'speed': 1.1,  # Faster, energetic
                'tone': 'joyful',
                'elevenlabs_voice': 'Adam',  # Warm, expressive
                'gtts_lang': 'en',
                'gtts_tld': 'com',
                'pyttsx3_rate': 180,  # Fast-paced
                'pyttsx3_volume': 1.0
            }
        }
        
        # Initialize ElevenLabs if available
        if ELEVENLABS_AVAILABLE:
            api_key = os.getenv('ELEVENLABS_API_KEY')
            if api_key:
                try:
                    set_api_key(api_key)
                    logger.info("ElevenLabs API initialized")
                except Exception as e:
                    logger.warning(f"ElevenLabs initialization failed: {e}")
    
    def _get_cache_path(self, text: str, personality: str, format: str) -> Path:
        """
        Generate cache path for audio file.
        
        Args:
            text: Text content (for hash)
            personality: Personality name
            format: Audio format
            
        Returns:
            Path to cached audio file
        """
        # Create hash of text for caching
        text_hash = hashlib.md5(text.encode()).hexdigest()[:12]
        filename = f"{personality}_{text_hash}.{format}"
        return self.output_dir / filename
    
    def _synthesize_elevenlabs(self, text: str, personality: str, output_path: Path) -> bool:
        """
        Synthesize using ElevenLabs API.
        
        Args:
            text: Text to synthesize
            personality: Personality to use
            output_path: Where to save audio
            
        Returns:
            True if successful
        """
        if not ELEVENLABS_AVAILABLE:
            return False
        
        try:
            profile = self.voice_profiles[personality]
            voice_name = profile['elevenlabs_voice']
            
            # Generate audio
            audio = generate(
                text=text,
                voice=voice_name,
                model="eleven_monolingual_v1"
            )
            
            # Save to file
            with open(output_path, 'wb') as f:
                f.write(audio)
            
            logger.info(f"Generated audio with ElevenLabs: {output_path}")
            return True
            
        except Exception as e:
            logger.warning(f"ElevenLabs synthesis failed: {e}")
            return False
    
    def _synthesize_gtts(self, text: str, personality: str, output_path: Path) -> bool:
        """
        Synthesize using Google Text-to-Speech.
        
        Args:
            text: Text to synthesize
            personality: Personality to use
            output_path: Where to save audio
            
        Returns:
            True if successful
        """
        if not GTTS_AVAILABLE:
            return False
        
        try:
            profile = self.voice_profiles[personality]
            
            # Create TTS object
            tts = gTTS(
                text=text,
                lang=profile['gtts_lang'],
                tld=profile['gtts_tld'],
                slow=False
            )
            
            # Save to file
            tts.save(str(output_path))
            
            logger.info(f"Generated audio with gTTS: {output_path}")
            return True
            
        except Exception as e:
            logger.warning(f"gTTS synthesis failed: {e}")
            return False
    
    def _synthesize_pyttsx3(self, text: str, personality: str, output_path: Path) -> bool:
        """
        Synthesize using pyttsx3 offline TTS.
        
        Args:
            text: Text to synthesize
            personality: Personality to use
            output_path: Where to save audio
            
        Returns:
            True if successful
        """
        if not PYTTSX3_AVAILABLE:
            return False
        
        try:
            profile = self.voice_profiles[personality]
            
            # Initialize engine
            engine = pyttsx3.init()
            
            # Set properties
            engine.setProperty('rate', profile['pyttsx3_rate'])
            engine.setProperty('volume', profile['pyttsx3_volume'])
            
            # Try to set voice based on personality
            voices_list = engine.getProperty('voices')
            if personality == 'the_professor' and len(voices_list) > 0:
                # Try to find a warm, thoughtful voice
                for voice in voices_list:
                    if 'english' in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
            
            # Save to file
            engine.save_to_file(text, str(output_path))
            engine.runAndWait()
            
            logger.info(f"Generated audio with pyttsx3: {output_path}")
            return True
            
        except Exception as e:
            logger.warning(f"pyttsx3 synthesis failed: {e}")
            return False
    
    def synthesize(self, 
                   text: str,
                   personality: Literal['the_professor', 'the_worrier', 'the_enthusiast'],
                   format: str = 'mp3',
                   use_cache: bool = True) -> Dict:
        """
        Synthesize text to speech with personality voice.
        
        Args:
            text: Text to synthesize
            personality: Personality voice to use
            format: Audio format (mp3, wav)
            use_cache: Whether to use cached audio if available
            
        Returns:
            Dictionary containing:
                - success: Whether synthesis succeeded
                - audio_path: Path to audio file
                - personality: Personality used
                - backend: TTS backend used
                - duration_estimate: Estimated duration in seconds
                - file_size: File size in bytes (if available)
        """
        if personality not in self.PERSONALITIES:
            raise ValueError(f"Unknown personality: {personality}")
        
        # Check cache
        cache_path = self._get_cache_path(text, personality, format)
        if use_cache and cache_path.exists():
            logger.info(f"Using cached audio: {cache_path}")
            return {
                'success': True,
                'audio_path': str(cache_path),
                'personality': personality,
                'backend': 'cache',
                'duration_estimate': len(text.split()) / 2.5,  # ~2.5 words per second
                'file_size': cache_path.stat().st_size
            }
        
        # Try backends in order of preference
        backends = []
        
        # Check which backends are available and configured
        if ELEVENLABS_AVAILABLE and os.getenv('ELEVENLABS_API_KEY'):
            backends.append(('elevenlabs', self._synthesize_elevenlabs))
        
        if GTTS_AVAILABLE:
            backends.append(('gtts', self._synthesize_gtts))
        
        if PYTTSX3_AVAILABLE:
            backends.append(('pyttsx3', self._synthesize_pyttsx3))
        
        # Try each backend
        for backend_name, backend_func in backends:
            logger.info(f"Trying {backend_name} for {personality}...")
            success = backend_func(text, personality, cache_path)
            
            if success:
                file_size = cache_path.stat().st_size if cache_path.exists() else 0
                return {
                    'success': True,
                    'audio_path': str(cache_path),
                    'personality': personality,
                    'backend': backend_name,
                    'duration_estimate': len(text.split()) / 2.5,
                    'file_size': file_size
                }
        
        # All backends failed
        logger.error(f"All TTS backends failed for {personality}")
        return {
            'success': False,
            'audio_path': None,
            'personality': personality,
            'backend': None,
            'duration_estimate': 0,
            'file_size': 0,
            'error': 'All TTS backends failed. Please install gtts or pyttsx3.'
        }
    
    def generate_preview(self,
                        text: str,
                        personality: Literal['the_professor', 'the_worrier', 'the_enthusiast'],
                        duration: int = 30,
                        format: str = 'mp3') -> Dict:
        """
        Generate a preview sample (first N seconds of audio).
        
        Args:
            text: Full text
            personality: Personality to use
            duration: Preview duration in seconds
            format: Audio format
            
        Returns:
            Same as synthesize() but for preview
        """
        # Estimate words for duration (assuming ~2.5 words per second)
        words = text.split()
        preview_words = int(duration * 2.5)
        preview_text = ' '.join(words[:preview_words])
        
        # Add indicator that this is a preview
        if len(words) > preview_words:
            preview_text += "... [preview ends here]"
        
        result = self.synthesize(preview_text, personality, format)
        result['is_preview'] = True
        result['preview_duration'] = duration
        
        return result
    
    def get_voice_profile(self, personality: str) -> Dict:
        """
        Get voice profile information for a personality.
        
        Args:
            personality: Personality name
            
        Returns:
            Voice profile dictionary
        """
        if personality not in self.PERSONALITIES:
            raise ValueError(f"Unknown personality: {personality}")
        
        return self.voice_profiles[personality].copy()
    
    def list_available_backends(self) -> Dict:
        """
        List available TTS backends and their status.
        
        Returns:
            Dictionary of backend availability
        """
        return {
            'elevenlabs': {
                'available': ELEVENLABS_AVAILABLE,
                'configured': ELEVENLABS_AVAILABLE and bool(os.getenv('ELEVENLABS_API_KEY')),
                'quality': 'premium',
                'description': 'High-quality AI voices'
            },
            'gtts': {
                'available': GTTS_AVAILABLE,
                'configured': GTTS_AVAILABLE,
                'quality': 'good',
                'description': 'Google Text-to-Speech (requires internet)'
            },
            'pyttsx3': {
                'available': PYTTSX3_AVAILABLE,
                'configured': PYTTSX3_AVAILABLE,
                'quality': 'basic',
                'description': 'Offline TTS using system voices'
            }
        }


# Example usage and testing
if __name__ == "__main__":
    synthesizer = VoiceSynthesizer()
    
    # Check available backends
    print("Available TTS Backends:")
    backends = synthesizer.list_available_backends()
    for name, info in backends.items():
        status = "✓ Ready" if info['configured'] else "✗ Not available"
        print(f"  {name}: {status} - {info['description']}")
    
    print("\n" + "="*60)
    
    # Test synthesis for each personality
    test_texts = {
        'the_professor': "I've been studying New York pizza and what fascinates me is how it brings people together in the most delightful way.",
        'the_worrier': "Does anyone else get nervous about trying New York pizza? I want to make sure everyone enjoys it safely!",
        'the_enthusiast': "Can we talk about how AMAZING New York pizza is?! It's absolutely the best thing ever!"
    }
    
    for personality, text in test_texts.items():
        print(f"\nTesting {personality}:")
        result = synthesizer.synthesize(text, personality)
        
        if result['success']:
            print(f"  ✓ Success using {result['backend']}")
            print(f"  Audio: {result['audio_path']}")
            print(f"  Est. duration: {result['duration_estimate']:.1f}s")
            print(f"  File size: {result['file_size']} bytes")
        else:
            print(f"  ✗ Failed: {result.get('error', 'Unknown error')}")
