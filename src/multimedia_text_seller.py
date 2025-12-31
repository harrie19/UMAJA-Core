"""
UMAJA WORLDTOUR - Multimedia Text Seller
Extended seller for all content types (text, audio, image, video)
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Literal, Optional
import zipfile
import logging

# Import core modules
from .personality_engine import PersonalityEngine
from .voice_synthesizer import VoiceSynthesizer
from .image_generator import ImageGenerator
from .video_generator import VideoGenerator
from .bundle_builder import BundleBuilder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultimediaTextSeller:
    """
    Extended seller for all multimedia content types.
    Handles creation, packaging, and delivery of text, audio, images, and videos.
    """
    
    def __init__(self, 
                 output_dir: str = "static/purchases",
                 data_dir: str = "data"):
        """
        Initialize the multimedia seller.
        
        Args:
            output_dir: Directory to save purchase packages
            data_dir: Directory for data files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize engines
        self.personality_engine = PersonalityEngine()
        self.voice_synthesizer = VoiceSynthesizer()
        self.image_generator = ImageGenerator()
        self.video_generator = VideoGenerator()
        self.bundle_builder = BundleBuilder()
        
        # Sales tracking
        self.sales_file = self.data_dir / "sales.json"
        self.sales = self._load_sales()
    
    def _load_sales(self) -> List[Dict]:
        """Load sales history from file."""
        if self.sales_file.exists():
            try:
                with open(self.sales_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load sales file: {e}")
        return []
    
    def _save_sales(self):
        """Save sales history to file."""
        try:
            with open(self.sales_file, 'w') as f:
                json.dump(self.sales, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save sales file: {e}")
    
    def create_multimedia_purchase(self,
                                  email: str,
                                  topic: str,
                                  personality: Literal['john_cleese', 'c3po', 'robin_williams'],
                                  content_types: List[Literal['text', 'audio', 'image', 'video']],
                                  extras: List[str] = None,
                                  length: Literal['short', 'medium', 'long'] = 'medium',
                                  style_intensity: float = 0.7) -> Dict:
        """
        Create a multimedia purchase with all requested content types.
        
        Args:
            email: Customer email
            topic: Topic for content
            personality: Comedian personality
            content_types: List of content types to generate
            extras: List of extra add-ons
            length: Content length
            style_intensity: Style intensity for personality
            
        Returns:
            Dictionary with purchase information and file paths
        """
        if extras is None:
            extras = []
        
        # Generate unique purchase ID
        purchase_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().isoformat()
        
        logger.info(f"Creating multimedia purchase {purchase_id} for {email}")
        
        # Create purchase directory
        purchase_dir = self.output_dir / purchase_id
        purchase_dir.mkdir(parents=True, exist_ok=True)
        
        generated_files = {}
        generation_errors = []
        
        # Generate text (base for all other content)
        text_content = None
        if 'text' in content_types:
            try:
                logger.info(f"Generating text for {personality}...")
                text_result = self.personality_engine.generate_text(
                    topic=topic,
                    personality=personality,
                    length=length,
                    style_intensity=style_intensity
                )
                
                text_content = text_result['text']
                
                # Save text file
                text_path = purchase_dir / f"{personality}_text.txt"
                with open(text_path, 'w', encoding='utf-8') as f:
                    f.write(f"Topic: {topic}\n")
                    f.write(f"Personality: {personality.replace('_', ' ').title()}\n")
                    f.write(f"Generated: {timestamp}\n")
                    f.write(f"\n{'='*60}\n\n")
                    f.write(text_content)
                
                generated_files['text'] = {
                    'path': str(text_path),
                    'word_count': text_result['word_count'],
                    'personality': personality
                }
                
                logger.info(f"✓ Text generated: {text_result['word_count']} words")
                
            except Exception as e:
                error_msg = f"Text generation failed: {e}"
                logger.error(error_msg)
                generation_errors.append(error_msg)
        
        # Generate audio
        if 'audio' in content_types:
            try:
                if text_content is None:
                    # Generate text for audio even if not requested
                    text_result = self.personality_engine.generate_text(
                        topic=topic,
                        personality=personality,
                        length=length,
                        style_intensity=style_intensity
                    )
                    text_content = text_result['text']
                
                logger.info(f"Generating audio for {personality}...")
                audio_result = self.voice_synthesizer.synthesize(
                    text=text_content,
                    personality=personality,
                    format='mp3'
                )
                
                if audio_result['success']:
                    # Copy audio to purchase directory
                    import shutil
                    audio_dest = purchase_dir / f"{personality}_audio.mp3"
                    shutil.copy2(audio_result['audio_path'], audio_dest)
                    
                    generated_files['audio'] = {
                        'path': str(audio_dest),
                        'duration': audio_result['duration_estimate'],
                        'backend': audio_result['backend'],
                        'personality': personality
                    }
                    
                    logger.info(f"✓ Audio generated: {audio_result['duration_estimate']:.1f}s")
                else:
                    error_msg = f"Audio generation failed: {audio_result.get('error', 'Unknown error')}"
                    logger.error(error_msg)
                    generation_errors.append(error_msg)
                
            except Exception as e:
                error_msg = f"Audio generation failed: {e}"
                logger.error(error_msg)
                generation_errors.append(error_msg)
        
        # Generate image
        if 'image' in content_types:
            try:
                if text_content is None:
                    # Generate text for image
                    text_result = self.personality_engine.generate_text(
                        topic=topic,
                        personality=personality,
                        length='short',
                        style_intensity=style_intensity
                    )
                    text_content = text_result['text']
                
                logger.info(f"Generating image for {personality}...")
                
                # Generate quote card with excerpt
                quote = text_content[:200] + "..." if len(text_content) > 200 else text_content
                image_result = self.image_generator.generate_quote_card(
                    quote=quote,
                    personality=personality,
                    author_name=personality.replace('_', ' ').title()
                )
                
                if image_result['success']:
                    # Copy image to purchase directory
                    import shutil
                    image_dest = purchase_dir / f"{personality}_image.png"
                    shutil.copy2(image_result['image_path'], image_dest)
                    
                    generated_files['image'] = {
                        'path': str(image_dest),
                        'type': image_result['type'],
                        'size': image_result['size'],
                        'personality': personality
                    }
                    
                    logger.info(f"✓ Image generated")
                else:
                    error_msg = "Image generation failed"
                    logger.error(error_msg)
                    generation_errors.append(error_msg)
                
            except Exception as e:
                error_msg = f"Image generation failed: {e}"
                logger.error(error_msg)
                generation_errors.append(error_msg)
        
        # Generate video
        if 'video' in content_types:
            try:
                if text_content is None:
                    # Generate text for video
                    text_result = self.personality_engine.generate_text(
                        topic=topic,
                        personality=personality,
                        length=length,
                        style_intensity=style_intensity
                    )
                    text_content = text_result['text']
                
                # Need audio for video
                audio_path = generated_files.get('audio', {}).get('path')
                if not audio_path:
                    # Generate audio
                    audio_result = self.voice_synthesizer.synthesize(
                        text=text_content,
                        personality=personality,
                        format='mp3'
                    )
                    if audio_result['success']:
                        audio_path = audio_result['audio_path']
                
                if audio_path:
                    logger.info(f"Generating video for {personality}...")
                    
                    # Get background image if available
                    background_image = generated_files.get('image', {}).get('path')
                    
                    video_result = self.video_generator.create_lyric_video(
                        text=text_content,
                        audio_path=audio_path,
                        personality=personality,
                        background_image=background_image
                    )
                    
                    if video_result['success']:
                        # Copy video to purchase directory
                        import shutil
                        video_dest = purchase_dir / f"{personality}_video.mp4"
                        shutil.copy2(video_result['video_path'], video_dest)
                        
                        generated_files['video'] = {
                            'path': str(video_dest),
                            'duration': video_result['duration'],
                            'backend': video_result['backend'],
                            'personality': personality
                        }
                        
                        logger.info(f"✓ Video generated: {video_result['duration']:.1f}s")
                    else:
                        error_msg = f"Video generation failed: {video_result.get('error', 'Unknown error')}"
                        logger.error(error_msg)
                        generation_errors.append(error_msg)
                else:
                    error_msg = "Cannot generate video without audio"
                    logger.error(error_msg)
                    generation_errors.append(error_msg)
                
            except Exception as e:
                error_msg = f"Video generation failed: {e}"
                logger.error(error_msg)
                generation_errors.append(error_msg)
        
        # Create info file
        info = {
            'purchase_id': purchase_id,
            'customer_email': email,
            'topic': topic,
            'personality': personality,
            'content_types': content_types,
            'extras': extras,
            'length': length,
            'style_intensity': style_intensity,
            'timestamp': timestamp,
            'generated_files': generated_files,
            'errors': generation_errors
        }
        
        info_path = purchase_dir / 'purchase_info.json'
        with open(info_path, 'w') as f:
            json.dump(info, f, indent=2)
        
        # Create ZIP package
        zip_path = self.output_dir / f"{purchase_id}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_type, file_info in generated_files.items():
                file_path = Path(file_info['path'])
                if file_path.exists():
                    zipf.write(file_path, file_path.name)
            
            # Add info file
            zipf.write(info_path, 'purchase_info.json')
        
        logger.info(f"✓ Package created: {zip_path}")
        
        # Calculate pricing
        tier_id = self.bundle_builder.create_custom_bundle(content_types, extras)
        pricing = self.bundle_builder.calculate_bundle_price([tier_id], extras=extras)
        
        # Record sale
        sale_record = {
            'purchase_id': purchase_id,
            'email': email,
            'topic': topic,
            'personality': personality,
            'content_types': content_types,
            'extras': extras,
            'pricing': pricing,
            'timestamp': timestamp,
            'success': len(generation_errors) == 0
        }
        
        self.sales.append(sale_record)
        self._save_sales()
        
        return {
            'success': len(generated_files) > 0,
            'purchase_id': purchase_id,
            'package_path': str(zip_path),
            'generated_files': generated_files,
            'pricing': pricing,
            'errors': generation_errors,
            'download_url': f"/download/{purchase_id}.zip"
        }
    
    def get_purchase(self, purchase_id: str) -> Optional[Dict]:
        """Get purchase information by ID."""
        for sale in self.sales:
            if sale['purchase_id'] == purchase_id:
                return sale
        return None
    
    def get_sales_stats(self) -> Dict:
        """Get sales statistics."""
        total_sales = len(self.sales)
        total_revenue = sum(sale['pricing']['total'] for sale in self.sales)
        total_charity = sum(sale['pricing']['charity_amount'] for sale in self.sales)
        
        # Content type popularity
        content_type_counts = {}
        for sale in self.sales:
            for ct in sale['content_types']:
                content_type_counts[ct] = content_type_counts.get(ct, 0) + 1
        
        # Personality popularity
        personality_counts = {}
        for sale in self.sales:
            p = sale['personality']
            personality_counts[p] = personality_counts.get(p, 0) + 1
        
        return {
            'total_sales': total_sales,
            'total_revenue': round(total_revenue, 2),
            'total_charity': round(total_charity, 2),
            'average_order_value': round(total_revenue / total_sales, 2) if total_sales > 0 else 0,
            'content_type_popularity': content_type_counts,
            'personality_popularity': personality_counts,
            'currency': 'EUR'
        }


# Example usage and testing
if __name__ == "__main__":
    seller = MultimediaTextSeller()
    
    print("Multimedia Text Seller Test")
    print("=" * 60)
    
    # Test purchase creation
    print("\nCreating test purchase...")
    result = seller.create_multimedia_purchase(
        email="test@example.com",
        topic="New York pizza",
        personality="john_cleese",
        content_types=['text', 'audio', 'image'],
        length='medium'
    )
    
    if result['success']:
        print(f"✓ Purchase created: {result['purchase_id']}")
        print(f"  Package: {result['package_path']}")
        print(f"  Price: €{result['pricing']['total']:.2f}")
        print(f"  To charity: €{result['pricing']['charity_amount']:.2f}")
        
        print("\n  Generated files:")
        for file_type, file_info in result['generated_files'].items():
            print(f"    - {file_type}: {file_info['path']}")
    else:
        print("✗ Purchase failed")
        for error in result['errors']:
            print(f"  Error: {error}")
    
    # Get stats
    print("\n" + "="*60)
    stats = seller.get_sales_stats()
    print(f"Sales Stats:")
    print(f"  Total sales: {stats['total_sales']}")
    print(f"  Total revenue: €{stats['total_revenue']:.2f}")
    print(f"  To charity: €{stats['total_charity']:.2f}")
