"""
UMAJA WORLDTOUR - Image Generator
AI image generation + Quote cards using Stable Diffusion and PIL
"""

import os
import hashlib
from pathlib import Path
from typing import Dict, Literal, Optional, Tuple
import logging
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Conditional imports for AI image generation
try:
    from diffusers import StableDiffusionPipeline
    import torch
    DIFFUSERS_AVAILABLE = True
except ImportError:
    DIFFUSERS_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageGenerator:
    """
    AI image generation + Quote cards.
    Supports Stable Diffusion for AI images and PIL for quote cards.
    """
    
    PERSONALITIES = ['john_cleese', 'c3po', 'robin_williams']
    
    def __init__(self, output_dir: str = "static/images"):
        """
        Initialize the image generator.
        
        Args:
            output_dir: Directory to save generated images
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Personality-themed prompt templates
        self.prompt_templates = {
            'john_cleese': {
                'style_keywords': ['Monty Python style', 'British comedy', 'surreal', 'absurdist'],
                'background_themes': ['British countryside', 'Ministry office', 'comedy stage'],
                'color_palette': ['muted', 'classic', 'sophisticated'],
                'mood': 'dry, witty, sophisticated'
            },
            'c3po': {
                'style_keywords': ['Star Wars', 'protocol droid', 'futuristic', 'metallic'],
                'background_themes': ['spaceship interior', 'desert planet', 'command center'],
                'color_palette': ['gold', 'metallic', 'sci-fi blues'],
                'mood': 'precise, anxious, formal'
            },
            'robin_williams': {
                'style_keywords': ['energetic', 'colorful', 'warm', 'theatrical'],
                'background_themes': ['comedy club', 'Broadway stage', 'vibrant cityscape'],
                'color_palette': ['vibrant', 'warm tones', 'dynamic'],
                'mood': 'energetic, warm, improvisational'
            }
        }
        
        # Quote card themes
        self.quote_card_themes = {
            'john_cleese': {
                'bg_color': (45, 52, 54),  # Dark gray
                'text_color': (236, 240, 241),  # Off white
                'accent_color': (231, 76, 60),  # British red
                'font_style': 'classic'
            },
            'c3po': {
                'bg_color': (44, 62, 80),  # Dark blue
                'text_color': (241, 196, 15),  # Gold
                'accent_color': (52, 152, 219),  # Bright blue
                'font_style': 'futuristic'
            },
            'robin_williams': {
                'bg_color': (230, 126, 34),  # Warm orange
                'text_color': (255, 255, 255),  # White
                'accent_color': (155, 89, 182),  # Purple
                'font_style': 'playful'
            }
        }
        
        # Initialize Stable Diffusion if available and configured
        self.sd_pipeline = None
        if DIFFUSERS_AVAILABLE and os.getenv('USE_LOCAL_STABLE_DIFFUSION', 'false').lower() == 'true':
            self._init_stable_diffusion()
    
    def _init_stable_diffusion(self):
        """Initialize Stable Diffusion pipeline."""
        try:
            logger.info("Initializing Stable Diffusion...")
            # Use smaller model for faster generation
            model_id = "runwayml/stable-diffusion-v1-5"
            
            # Check if CUDA is available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
            self.sd_pipeline = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32
            )
            self.sd_pipeline = self.sd_pipeline.to(device)
            
            # Enable memory optimizations
            if device == "cuda":
                self.sd_pipeline.enable_attention_slicing()
            
            logger.info(f"Stable Diffusion initialized on {device}")
        except Exception as e:
            logger.warning(f"Stable Diffusion initialization failed: {e}")
            self.sd_pipeline = None
    
    def _get_cache_path(self, content_hash: str, image_type: str, format: str = 'png') -> Path:
        """
        Generate cache path for image file.
        
        Args:
            content_hash: Hash of content
            image_type: Type of image (ai, quote, infographic)
            format: Image format
            
        Returns:
            Path to cached image file
        """
        filename = f"{image_type}_{content_hash}.{format}"
        return self.output_dir / filename
    
    def _create_gradient_background(self, size: Tuple[int, int], 
                                   color1: Tuple[int, int, int],
                                   color2: Tuple[int, int, int]) -> Image.Image:
        """
        Create a gradient background image.
        
        Args:
            size: Image size (width, height)
            color1: Start color
            color2: End color
            
        Returns:
            PIL Image with gradient
        """
        image = Image.new('RGB', size)
        draw = ImageDraw.Draw(image)
        
        # Create vertical gradient
        for y in range(size[1]):
            ratio = y / size[1]
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.line([(0, y), (size[0], y)], fill=(r, g, b))
        
        return image
    
    def _get_font(self, size: int = 40) -> ImageFont.FreeTypeFont:
        """
        Get font for text rendering.
        
        Args:
            size: Font size
            
        Returns:
            PIL Font object
        """
        # Try to use system fonts
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "C:\\Windows\\Fonts\\arial.ttf"
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except Exception:
                    continue
        
        # Fallback to default font
        return ImageFont.load_default()
    
    def generate_quote_card(self,
                           quote: str,
                           personality: Literal['john_cleese', 'c3po', 'robin_williams'],
                           author_name: Optional[str] = None,
                           size: Tuple[int, int] = (1080, 1080),
                           format: str = 'png') -> Dict:
        """
        Generate a quote card with text on beautiful background.
        
        Args:
            quote: Quote text
            personality: Personality theme to use
            author_name: Optional author attribution
            size: Image size (width, height)
            format: Image format
            
        Returns:
            Dictionary with image info
        """
        if personality not in self.PERSONALITIES:
            raise ValueError(f"Unknown personality: {personality}")
        
        # Get theme
        theme = self.quote_card_themes[personality]
        
        # Generate cache path
        content_hash = hashlib.md5(quote.encode()).hexdigest()[:12]
        cache_path = self._get_cache_path(content_hash, f'quote_{personality}', format)
        
        # Create gradient background
        bg_color1 = theme['bg_color']
        # Slightly darker for gradient
        bg_color2 = tuple(max(0, c - 30) for c in bg_color1)
        
        image = self._create_gradient_background(size, bg_color1, bg_color2)
        draw = ImageDraw.Draw(image)
        
        # Calculate text area
        margin = size[0] // 10
        text_width = size[0] - (2 * margin)
        
        # Wrap quote text
        font_size = size[0] // 20  # Responsive font size
        font = self._get_font(font_size)
        
        # Wrap text to fit width
        chars_per_line = int(text_width / (font_size * 0.6))
        wrapped_lines = textwrap.wrap(quote, width=chars_per_line)
        
        # Calculate total text height
        line_height = font_size + 10
        total_text_height = len(wrapped_lines) * line_height
        
        # Center vertically
        start_y = (size[1] - total_text_height) // 2
        
        # Draw quote text
        current_y = start_y
        for line in wrapped_lines:
            # Center each line horizontally
            bbox = draw.textbbox((0, 0), line, font=font)
            text_line_width = bbox[2] - bbox[0]
            x = (size[0] - text_line_width) // 2
            
            # Draw text with shadow for better readability
            shadow_offset = 3
            draw.text((x + shadow_offset, current_y + shadow_offset), 
                     line, fill=(0, 0, 0, 128), font=font)
            draw.text((x, current_y), line, fill=theme['text_color'], font=font)
            
            current_y += line_height
        
        # Add author attribution if provided
        if author_name:
            author_font = self._get_font(font_size // 2)
            author_text = f"— {author_name}"
            bbox = draw.textbbox((0, 0), author_text, font=author_font)
            author_width = bbox[2] - bbox[0]
            author_x = (size[0] - author_width) // 2
            author_y = current_y + 30
            
            draw.text((author_x, author_y), author_text, 
                     fill=theme['accent_color'], font=author_font)
        
        # Add decorative elements (corner brackets)
        accent = theme['accent_color']
        corner_size = 40
        line_width = 5
        
        # Top-left corner
        draw.line([(margin, margin), (margin + corner_size, margin)], 
                 fill=accent, width=line_width)
        draw.line([(margin, margin), (margin, margin + corner_size)], 
                 fill=accent, width=line_width)
        
        # Bottom-right corner
        draw.line([(size[0] - margin - corner_size, size[1] - margin), 
                  (size[0] - margin, size[1] - margin)], 
                 fill=accent, width=line_width)
        draw.line([(size[0] - margin, size[1] - margin - corner_size), 
                  (size[0] - margin, size[1] - margin)], 
                 fill=accent, width=line_width)
        
        # Save image
        image.save(cache_path, format=format.upper())
        
        logger.info(f"Generated quote card: {cache_path}")
        
        return {
            'success': True,
            'image_path': str(cache_path),
            'personality': personality,
            'type': 'quote_card',
            'size': size,
            'file_size': cache_path.stat().st_size
        }
    
    def generate_ai_image(self,
                         topic: str,
                         personality: Literal['john_cleese', 'c3po', 'robin_williams'],
                         size: Tuple[int, int] = (512, 512),
                         format: str = 'png') -> Dict:
        """
        Generate AI image using Stable Diffusion.
        
        Args:
            topic: Topic/subject for the image
            personality: Personality theme to use
            size: Image size (width, height)
            format: Image format
            
        Returns:
            Dictionary with image info
        """
        if personality not in self.PERSONALITIES:
            raise ValueError(f"Unknown personality: {personality}")
        
        # Generate cache path
        content_hash = hashlib.md5(f"{topic}_{personality}".encode()).hexdigest()[:12]
        cache_path = self._get_cache_path(content_hash, f'ai_{personality}', format)
        
        # Check if Stable Diffusion is available
        if not self.sd_pipeline:
            logger.warning("Stable Diffusion not available, generating placeholder")
            # Create a placeholder image with text
            return self._generate_placeholder_image(topic, personality, size, cache_path, format)
        
        try:
            # Build prompt from personality theme
            theme = self.prompt_templates[personality]
            style = ', '.join(theme['style_keywords'])
            background = theme['background_themes'][0]
            mood = theme['mood']
            
            prompt = f"{topic}, {style}, {background}, {mood}, high quality, detailed, artistic"
            
            logger.info(f"Generating AI image with prompt: {prompt}")
            
            # Generate image
            with torch.no_grad():
                result = self.sd_pipeline(
                    prompt,
                    height=size[1],
                    width=size[0],
                    num_inference_steps=30,
                    guidance_scale=7.5
                )
            
            image = result.images[0]
            image.save(cache_path, format=format.upper())
            
            logger.info(f"Generated AI image: {cache_path}")
            
            return {
                'success': True,
                'image_path': str(cache_path),
                'personality': personality,
                'type': 'ai_image',
                'prompt': prompt,
                'size': size,
                'file_size': cache_path.stat().st_size
            }
            
        except Exception as e:
            logger.error(f"AI image generation failed: {e}")
            # Fallback to placeholder
            return self._generate_placeholder_image(topic, personality, size, cache_path, format)
    
    def _generate_placeholder_image(self, topic: str, personality: str, 
                                   size: Tuple[int, int], cache_path: Path, 
                                   format: str) -> Dict:
        """
        Generate a placeholder image when AI generation is not available.
        
        Args:
            topic: Topic text
            personality: Personality
            size: Image size
            cache_path: Where to save
            format: Image format
            
        Returns:
            Dictionary with image info
        """
        theme = self.quote_card_themes[personality]
        
        # Create gradient background
        image = self._create_gradient_background(size, theme['bg_color'], 
                                                 tuple(max(0, c - 40) for c in theme['bg_color']))
        draw = ImageDraw.Draw(image)
        
        # Add topic text
        font_size = size[0] // 15
        font = self._get_font(font_size)
        
        text = f"🎭 {topic}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        # Draw with shadow
        draw.text((x + 3, y + 3), text, fill=(0, 0, 0, 128), font=font)
        draw.text((x, y), text, fill=theme['text_color'], font=font)
        
        # Add personality indicator
        small_font = self._get_font(font_size // 2)
        personality_text = f"Style: {personality.replace('_', ' ').title()}"
        bbox = draw.textbbox((0, 0), personality_text, font=small_font)
        small_width = bbox[2] - bbox[0]
        small_x = (size[0] - small_width) // 2
        small_y = y + text_height + 30
        
        draw.text((small_x, small_y), personality_text, 
                 fill=theme['accent_color'], font=small_font)
        
        # Save
        image.save(cache_path, format=format.upper())
        
        return {
            'success': True,
            'image_path': str(cache_path),
            'personality': personality,
            'type': 'placeholder_image',
            'size': size,
            'file_size': cache_path.stat().st_size,
            'note': 'Placeholder image - Stable Diffusion not available'
        }
    
    def generate_infographic(self,
                           data: Dict,
                           personality: Literal['john_cleese', 'c3po', 'robin_williams'],
                           title: str,
                           size: Tuple[int, int] = (1080, 1350),
                           format: str = 'png') -> Dict:
        """
        Generate an infographic with data visualization and personality commentary.
        
        Args:
            data: Data to visualize (key-value pairs)
            personality: Personality theme
            title: Infographic title
            size: Image size
            format: Image format
            
        Returns:
            Dictionary with image info
        """
        if personality not in self.PERSONALITIES:
            raise ValueError(f"Unknown personality: {personality}")
        
        theme = self.quote_card_themes[personality]
        
        # Generate cache path
        content_hash = hashlib.md5(f"{title}_{personality}".encode()).hexdigest()[:12]
        cache_path = self._get_cache_path(content_hash, f'infographic_{personality}', format)
        
        # Create background
        image = self._create_gradient_background(size, theme['bg_color'],
                                                 tuple(max(0, c - 40) for c in theme['bg_color']))
        draw = ImageDraw.Draw(image)
        
        margin = size[0] // 20
        
        # Draw title
        title_font = self._get_font(size[0] // 15)
        bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = bbox[2] - bbox[0]
        title_x = (size[0] - title_width) // 2
        title_y = margin
        
        draw.text((title_x, title_y), title, fill=theme['text_color'], font=title_font)
        
        # Draw data items
        data_font = self._get_font(size[0] // 25)
        current_y = title_y + 100
        
        for key, value in data.items():
            # Draw key
            draw.text((margin, current_y), f"{key}:", 
                     fill=theme['accent_color'], font=data_font)
            
            # Draw value
            draw.text((margin + 250, current_y), str(value), 
                     fill=theme['text_color'], font=data_font)
            
            current_y += 60
        
        # Save
        image.save(cache_path, format=format.upper())
        
        logger.info(f"Generated infographic: {cache_path}")
        
        return {
            'success': True,
            'image_path': str(cache_path),
            'personality': personality,
            'type': 'infographic',
            'size': size,
            'file_size': cache_path.stat().st_size
        }


# Example usage and testing
if __name__ == "__main__":
    generator = ImageGenerator()
    
    print("Image Generator Test")
    print("=" * 60)
    
    # Test quote card for each personality
    quotes = {
        'john_cleese': "The curious thing about pizza is that it's rather like the British railway system.",
        'c3po': "Oh my! This pizza presents precisely 2,479 possible interpretations!",
        'robin_williams': "So pizza walks into a bar... *laughs* This is comedy gold!"
    }
    
    for personality, quote in quotes.items():
        print(f"\nGenerating quote card for {personality}...")
        result = generator.generate_quote_card(quote, personality, 
                                               author_name=personality.replace('_', ' ').title())
        
        if result['success']:
            print(f"  ✓ Success: {result['image_path']}")
            print(f"  Size: {result['size']}")
            print(f"  File size: {result['file_size']} bytes")
