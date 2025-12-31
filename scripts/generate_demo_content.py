#!/usr/bin/env python3
"""
UMAJA WORLDTOUR - Demo Content Generator
Quickly generates 3-5 sample videos to prepare for launch
"""

import os
import sys
import json
import shutil
import traceback
from pathlib import Path
from datetime import datetime
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from personality_engine import PersonalityEngine
from voice_synthesizer import VoiceSynthesizer
from image_generator import ImageGenerator
from video_generator import VideoGenerator
from worldtour_generator import WorldtourGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Color output for console
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKBLUE}→ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


# Demo configurations - one per personality, different cities
DEMO_CONFIGS = [
    {
        'city_id': 'new_york',
        'personality': 'john_cleese',
        'content_type': 'city_review'
    },
    {
        'city_id': 'tokyo',
        'personality': 'c3po',
        'content_type': 'food_review'
    },
    {
        'city_id': 'paris',
        'personality': 'robin_williams',
        'content_type': 'tourist_trap'
    },
    {
        'city_id': 'london',
        'personality': 'john_cleese',
        'content_type': 'cultural_debate'
    },
    {
        'city_id': 'berlin',
        'personality': 'robin_williams',
        'content_type': 'language_lesson'
    }
]


def generate_demo_video(config, demo_num, output_base_dir):
    """Generate a single demo video"""
    
    city_id = config['city_id']
    personality = config['personality']
    content_type = config['content_type']
    
    print_header(f"Demo {demo_num}: {city_id.upper()} - {personality.replace('_', ' ').title()}")
    
    # Initialize engines
    worldtour_gen = WorldtourGenerator()
    personality_engine = PersonalityEngine()
    voice_synth = VoiceSynthesizer()
    image_gen = ImageGenerator()
    video_gen = VideoGenerator()
    
    # Get city info
    city = worldtour_gen.get_city(city_id)
    if not city:
        print_error(f"City {city_id} not found")
        return False
    
    city_name = city['name']
    print_info(f"City: {city_name} ({city['country']})")
    print_info(f"Personality: {personality}")
    print_info(f"Content Type: {content_type}")
    
    # Create output directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = output_base_dir / f"demo_{demo_num}_{city_id}_{personality}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Step 1: Generate city content prompt
        print_info("Generating city content...")
        city_content = worldtour_gen.generate_city_content(
            city_id=city_id,
            personality=personality,
            content_type=content_type
        )
        print_success(f"Topic: {city_content['topic'][:60]}...")
        
        # Step 2: Generate comedy text
        print_info("Generating comedy text...")
        text_result = personality_engine.generate_text(
            topic=city_content['topic'],
            personality=personality,
            length='short',  # Keep demos short
            style_intensity=0.8
        )
        comedy_text = text_result['text']
        print_success(f"Generated {len(comedy_text)} characters")
        
        # Save text
        with open(output_dir / 'comedy_text.txt', 'w') as f:
            f.write(comedy_text)
        
        # Step 3: Generate audio
        print_info("Synthesizing voice...")
        audio_result = voice_synth.synthesize(
            text=comedy_text,
            personality=personality,
            format='mp3'
        )
        
        audio_path = audio_result.get('audio_path')
        if audio_path and Path(audio_path).exists():
            dest_audio = output_dir / 'voice.mp3'
            shutil.copy(audio_path, dest_audio)
            print_success("Audio generated")
        else:
            print_error("Audio generation failed")
            return False
        
        # Step 4: Generate image
        print_info("Creating quote card...")
        quote_text = comedy_text.split('.')[0] + '.' if '.' in comedy_text else comedy_text[:150]
        
        image_result = image_gen.generate_quote_card(
            quote=quote_text,
            personality=personality,
            author_name=personality.replace('_', ' ').title()
        )
        
        image_path = image_result.get('image_path')
        if image_path and Path(image_path).exists():
            dest_image = output_dir / 'quote_card.png'
            shutil.copy(image_path, dest_image)
            print_success("Image generated")
        else:
            print_error("Image generation failed")
            return False
        
        # Step 5: Create video
        print_info("Creating video...")
        video_result = video_gen.create_lyric_video(
            text=comedy_text,
            audio_path=str(dest_audio),
            personality=personality,
            background_image=str(dest_image)
        )
        
        video_path = video_result.get('video_path')
        if video_path and Path(video_path).exists():
            dest_video = output_dir / 'demo_video.mp4'
            shutil.copy(video_path, dest_video)
            print_success(f"Video saved: {dest_video}")
        else:
            print_error("Video generation failed")
            return False
        
        # Save metadata
        metadata = {
            'city_id': city_id,
            'city_name': city_name,
            'country': city['country'],
            'personality': personality,
            'content_type': content_type,
            'generated_at': timestamp,
            'text_length': len(comedy_text),
            'files': {
                'text': 'comedy_text.txt',
                'audio': 'voice.mp3',
                'image': 'quote_card.png',
                'video': 'demo_video.mp4'
            }
        }
        
        with open(output_dir / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print_success(f"Demo {demo_num} complete!\n")
        return True
        
    except Exception as e:
        print_error(f"Demo generation failed: {e}")
        traceback.print_exc()
        return False


def generate_demo_content(num_demos=5):
    """Main function to generate demo content"""
    
    print_header("🎬 UMAJA WORLDTOUR - Demo Content Generator")
    
    print_info(f"Generating {num_demos} demo videos...")
    print_info(f"One video per personality, different cities")
    print_info(f"Output: output/demos/\n")
    
    # Create output directory
    output_base_dir = Path('output/demos')
    output_base_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate demos
    successful = 0
    failed = 0
    
    for i in range(min(num_demos, len(DEMO_CONFIGS))):
        config = DEMO_CONFIGS[i]
        
        if generate_demo_video(config, i + 1, output_base_dir):
            successful += 1
        else:
            failed += 1
        
        print("")  # Blank line between demos
    
    # Print summary
    print_header("✅ DEMO GENERATION COMPLETE!")
    
    print(f"\n{Colors.BOLD}Summary:{Colors.ENDC}")
    print(f"  ✅ Successful: {successful} demos")
    if failed > 0:
        print(f"  ❌ Failed: {failed} demos")
    print(f"  📁 Output Directory: {output_base_dir}")
    
    print(f"\n{Colors.BOLD}Demo Videos:{Colors.ENDC}")
    for i, config in enumerate(DEMO_CONFIGS[:num_demos], 1):
        demo_dir = output_base_dir / f"demo_{i}_{config['city_id']}_{config['personality']}"
        if demo_dir.exists():
            video_file = demo_dir / 'demo_video.mp4'
            if video_file.exists():
                size = video_file.stat().st_size
                size_str = f"{size/1024/1024:.1f} MB"
                print(f"  🎬 Demo {i}: {config['city_id']} - {config['personality']} ({size_str})")
    
    print(f"\n{Colors.BOLD}Next Steps:{Colors.ENDC}")
    print(f"  1. Review all demo videos in: {output_base_dir}")
    print(f"  2. Test upload to social media platforms")
    print(f"  3. Check video quality and audio sync")
    print(f"  4. Use best demos for launch campaign")
    print(f"  5. Share with team for feedback")
    
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 Demo content ready for preview! 🎉{Colors.ENDC}\n")
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate demo worldtour videos')
    parser.add_argument(
        '--count',
        type=int,
        default=5,
        help='Number of demo videos to generate (default: 5, max: 5)'
    )
    
    args = parser.parse_args()
    
    try:
        exit_code = generate_demo_content(args.count)
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print_error("\n\nGeneration interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\nUnexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)
