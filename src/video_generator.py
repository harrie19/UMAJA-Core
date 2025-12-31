"""
UMAJA WORLDTOUR - Video Generator
Creates videos from text + audio + images with lyric-style and avatar modes
"""

import os
import hashlib
from pathlib import Path
from typing import Dict, Literal, Optional, List
import logging

# Conditional imports for video generation
try:
    from moviepy.editor import (
        VideoClip, TextClip, ImageClip, AudioFileClip,
        CompositeVideoClip, concatenate_videoclips
    )
    import moviepy.video.fx.all as vfx
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoGenerator:
    """
    Creates videos from text + audio + images.
    Supports lyric-style videos and avatar videos with lip-sync.
    """
    
    PERSONALITIES = ['the_professor', 'the_worrier', 'the_enthusiast']
    
    def __init__(self, output_dir: str = "static/videos"):
        """
        Initialize the video generator.
        
        Args:
            output_dir: Directory to save generated videos
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Personality-themed backgrounds and styles
        self.video_themes = {
            'the_professor': {
                'bg_color': (52, 73, 94),  # Scholarly blue-gray
                'text_color': (236, 240, 241),
                'accent_color': (52, 152, 219),
                'font': 'Arial',
                'font_size': 60,
                'animation_style': 'thoughtful'
            },
            'the_worrier': {
                'bg_color': (149, 165, 166),  # Gentle gray
                'text_color': (44, 62, 80),
                'accent_color': (127, 140, 141),
                'font': 'Arial',
                'font_size': 58,
                'animation_style': 'gentle'
            },
            'the_enthusiast': {
                'bg_color': (241, 196, 15),  # Bright yellow
                'text_color': (44, 62, 80),
                'accent_color': (230, 126, 34),
                'font': 'Arial',
                'font_size': 65,
                'animation_style': 'energetic'
            }
        }
    
    def _get_cache_path(self, content_hash: str, video_type: str) -> Path:
        """Generate cache path for video file."""
        filename = f"{video_type}_{content_hash}.mp4"
        return self.output_dir / filename
    
    def _create_lyric_video_moviepy(self,
                                    text: str,
                                    audio_path: str,
                                    personality: str,
                                    output_path: Path,
                                    duration: float) -> bool:
        """
        Create lyric-style video with text synced to audio using MoviePy.
        
        Args:
            text: Text content
            audio_path: Path to audio file
            personality: Personality theme
            output_path: Where to save video
            duration: Video duration in seconds
            
        Returns:
            True if successful
        """
        if not MOVIEPY_AVAILABLE:
            return False
        
        try:
            theme = self.video_themes[personality]
            
            # Load audio
            audio = AudioFileClip(audio_path)
            actual_duration = min(duration, audio.duration)
            
            # Create background clip
            bg_clip = ColorClip(
                size=(1080, 1920),  # Vertical video for TikTok/Instagram
                color=theme['bg_color'],
                duration=actual_duration
            )
            
            # Split text into chunks for animation
            words = text.split()
            words_per_line = 4
            lines = [' '.join(words[i:i+words_per_line]) 
                    for i in range(0, len(words), words_per_line)]
            
            # Calculate timing for each line
            time_per_line = actual_duration / len(lines)
            
            # Create text clips for each line
            text_clips = []
            for i, line in enumerate(lines):
                start_time = i * time_per_line
                
                txt_clip = TextClip(
                    line,
                    fontsize=theme['font_size'],
                    color='white',
                    bg_color=None,
                    font=theme['font'],
                    size=(900, None),
                    method='caption'
                ).set_start(start_time).set_duration(time_per_line).set_position('center')
                
                # Add fade in/out
                txt_clip = txt_clip.crossfadein(0.3).crossfadeout(0.3)
                
                text_clips.append(txt_clip)
            
            # Composite video
            video = CompositeVideoClip([bg_clip] + text_clips)
            video = video.set_audio(audio)
            
            # Write video file
            video.write_videofile(
                str(output_path),
                fps=30,
                codec='libx264',
                audio_codec='aac',
                preset='medium'
            )
            
            # Clean up
            video.close()
            audio.close()
            
            logger.info(f"Created lyric video with MoviePy: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"MoviePy video creation failed: {e}")
            return False
    
    def _create_simple_video_cv2(self,
                                text: str,
                                image_path: str,
                                personality: str,
                                output_path: Path,
                                duration: float) -> bool:
        """
        Create simple video from image using OpenCV.
        
        Args:
            text: Text content (for title)
            image_path: Path to background image
            personality: Personality theme
            output_path: Where to save video
            duration: Video duration in seconds
            
        Returns:
            True if successful
        """
        if not CV2_AVAILABLE:
            return False
        
        try:
            theme = self.video_themes[personality]
            
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                logger.error(f"Could not read image: {image_path}")
                return False
            
            # Resize to 1080p
            img = cv2.resize(img, (1920, 1080))
            
            # Video writer
            fps = 30
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(str(output_path), fourcc, fps, (1920, 1080))
            
            # Write frames (static image)
            total_frames = int(duration * fps)
            for _ in range(total_frames):
                out.write(img)
            
            out.release()
            
            logger.info(f"Created simple video with OpenCV: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"OpenCV video creation failed: {e}")
            return False
    
    def create_lyric_video(self,
                          text: str,
                          audio_path: str,
                          personality: Literal['the_professor', 'the_worrier', 'the_enthusiast'],
                          background_image: Optional[str] = None) -> Dict:
        """
        Create lyric-style video with text synced to audio.
        
        Args:
            text: Text content
            audio_path: Path to audio file
            personality: Personality theme to use
            background_image: Optional background image path
            
        Returns:
            Dictionary with video info
        """
        if personality not in self.PERSONALITIES:
            raise ValueError(f"Unknown personality: {personality}")
        
        # Generate cache path
        content_hash = hashlib.md5(f"{text}_{personality}".encode()).hexdigest()[:12]
        cache_path = self._get_cache_path(content_hash, f'lyric_{personality}')
        
        # Estimate duration from text (assuming ~2.5 words per second)
        duration = len(text.split()) / 2.5
        
        # Try MoviePy first
        success = False
        backend = None
        
        if MOVIEPY_AVAILABLE:
            logger.info("Attempting video creation with MoviePy...")
            success = self._create_lyric_video_moviepy(
                text, audio_path, personality, cache_path, duration
            )
            if success:
                backend = 'moviepy'
        
        if not success and CV2_AVAILABLE and background_image:
            logger.info("Falling back to OpenCV...")
            success = self._create_simple_video_cv2(
                text, background_image, personality, cache_path, duration
            )
            if success:
                backend = 'opencv'
        
        if not success:
            return {
                'success': False,
                'video_path': None,
                'personality': personality,
                'error': 'Video generation failed. MoviePy or OpenCV required.'
            }
        
        file_size = cache_path.stat().st_size if cache_path.exists() else 0
        
        return {
            'success': True,
            'video_path': str(cache_path),
            'personality': personality,
            'type': 'lyric_video',
            'duration': duration,
            'backend': backend,
            'file_size': file_size,
            'resolution': '1920x1080',
            'format': 'mp4'
        }
    
    def create_avatar_video(self,
                           text: str,
                           audio_path: str,
                           personality: Literal['the_professor', 'the_worrier', 'the_enthusiast'],
                           avatar_image: Optional[str] = None) -> Dict:
        """
        Create avatar video with lip-sync (requires Wav2Lip model).
        
        Args:
            text: Text content
            audio_path: Path to audio file
            personality: Personality theme
            avatar_image: Path to avatar image
            
        Returns:
            Dictionary with video info
        """
        # This is a placeholder for Wav2Lip integration
        # Full implementation would require the Wav2Lip model
        
        logger.warning("Avatar video with lip-sync not yet implemented")
        logger.info("Falling back to lyric video...")
        
        # Fallback to lyric video
        return self.create_lyric_video(text, audio_path, personality, avatar_image)
    
    def create_slideshow_video(self,
                              images: List[str],
                              audio_path: str,
                              personality: Literal['the_professor', 'the_worrier', 'the_enthusiast'],
                              transition_duration: float = 1.0) -> Dict:
        """
        Create slideshow video from multiple images with audio.
        
        Args:
            images: List of image paths
            audio_path: Path to audio file
            personality: Personality theme
            transition_duration: Duration of transitions in seconds
            
        Returns:
            Dictionary with video info
        """
        if personality not in self.PERSONALITIES:
            raise ValueError(f"Unknown personality: {personality}")
        
        if not MOVIEPY_AVAILABLE:
            return {
                'success': False,
                'video_path': None,
                'personality': personality,
                'error': 'MoviePy required for slideshow videos'
            }
        
        try:
            # Generate cache path
            content_hash = hashlib.md5(f"{'_'.join(images)}_{personality}".encode()).hexdigest()[:12]
            cache_path = self._get_cache_path(content_hash, f'slideshow_{personality}')
            
            # Load audio
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            
            # Calculate duration per image
            duration_per_image = duration / len(images)
            
            # Create image clips
            clips = []
            for img_path in images:
                clip = ImageClip(img_path).set_duration(duration_per_image)
                clip = clip.resize(height=1080)  # Standardize height
                clips.append(clip)
            
            # Concatenate with transitions
            video = concatenate_videoclips(clips, method='compose')
            video = video.set_audio(audio)
            
            # Write video file
            video.write_videofile(
                str(cache_path),
                fps=30,
                codec='libx264',
                audio_codec='aac',
                preset='medium'
            )
            
            # Clean up
            video.close()
            audio.close()
            
            logger.info(f"Created slideshow video: {cache_path}")
            
            return {
                'success': True,
                'video_path': str(cache_path),
                'personality': personality,
                'type': 'slideshow_video',
                'duration': duration,
                'image_count': len(images),
                'file_size': cache_path.stat().st_size,
                'resolution': '1920x1080',
                'format': 'mp4'
            }
            
        except Exception as e:
            logger.error(f"Slideshow video creation failed: {e}")
            return {
                'success': False,
                'video_path': None,
                'personality': personality,
                'error': str(e)
            }
    
    def export_for_platform(self,
                           video_path: str,
                           platform: Literal['tiktok', 'youtube', 'instagram']) -> Dict:
        """
        Optimize video for specific social media platform.
        
        Args:
            video_path: Path to video file
            platform: Target platform
            
        Returns:
            Dictionary with optimized video info
        """
        platform_specs = {
            'tiktok': {
                'resolution': (1080, 1920),  # Vertical
                'max_duration': 180,  # 3 minutes
                'format': 'mp4'
            },
            'youtube': {
                'resolution': (1920, 1080),  # Horizontal
                'max_duration': None,  # No limit
                'format': 'mp4'
            },
            'instagram': {
                'resolution': (1080, 1350),  # 4:5 ratio
                'max_duration': 60,  # 1 minute for feed
                'format': 'mp4'
            }
        }
        
        specs = platform_specs.get(platform, platform_specs['youtube'])
        
        # For now, just return the original video
        # Full implementation would resize/crop video
        
        return {
            'success': True,
            'video_path': video_path,
            'platform': platform,
            'optimized': False,
            'specs': specs,
            'note': 'Platform-specific optimization not yet implemented'
        }


# Helper class for MoviePy color clip
class ColorClip:
    """Simple color background clip for MoviePy."""
    def __init__(self, size, color, duration):
        self.size = size
        self.color = color
        self.duration = duration
    
    def __call__(self, *args, **kwargs):
        if MOVIEPY_AVAILABLE:
            # Use MoviePy's ColorClip if available
            from moviepy.editor import ColorClip as MPColorClip
            return MPColorClip(size=self.size, color=self.color, duration=self.duration)
        return None


# Example usage and testing
if __name__ == "__main__":
    generator = VideoGenerator()
    
    print("Video Generator Test")
    print("=" * 60)
    
    # Check available backends
    print(f"MoviePy available: {MOVIEPY_AVAILABLE}")
    print(f"OpenCV available: {CV2_AVAILABLE}")
    
    if not MOVIEPY_AVAILABLE and not CV2_AVAILABLE:
        print("\n⚠️  No video backends available. Install moviepy or opencv-python.")
    else:
        print("\n✓ Video generation ready")
