#!/usr/bin/env python3
"""
UMAJA WORLDTOUR - Daily Content Generation Script
Generates daily comedy content about a city for the worldtour campaign
"""

import os
import sys
import json
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


def get_next_personality(last_personality=None):
    """Rotate through personalities: John → C-3PO → Robin"""
    personalities = ['john_cleese', 'c3po', 'robin_williams']
    
    if not last_personality:
        return personalities[0]
    
    try:
        current_idx = personalities.index(last_personality)
        return personalities[(current_idx + 1) % len(personalities)]
    except ValueError:
        return personalities[0]


def load_last_state():
    """Load the last generated content state"""
    state_file = Path('data/worldtour_state.json')
    
    if state_file.exists():
        try:
            with open(state_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load state file: {e}")
    
    return {
        'last_personality': None,
        'last_city': None,
        'total_posts': 0
    }


def save_state(state):
    """Save the current state"""
    state_file = Path('data/worldtour_state.json')
    state_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        logger.error(f"Could not save state: {e}")


def generate_daily_content():
    """Main function to generate daily worldtour content"""
    
    print_header("🌍 UMAJA WORLDTOUR - Daily Content Generator")
    
    # Load last state
    state = load_last_state()
    print_info(f"Total posts generated: {state['total_posts']}")
    print_info(f"Last personality: {state['last_personality'] or 'None'}")
    
    # Initialize engines
    print_info("Initializing engines...")
    worldtour_gen = WorldtourGenerator()
    personality_engine = PersonalityEngine()
    voice_synth = VoiceSynthesizer()
    image_gen = ImageGenerator()
    video_gen = VideoGenerator()
    print_success("Engines initialized")
    
    # Get next city
    print_info("\nSelecting next city...")
    next_city = worldtour_gen.get_next_city()
    
    if not next_city:
        print_error("No unvisited cities remaining!")
        print_info("All 50+ cities have been visited. Consider resetting the database.")
        return 1
    
    city_id = next_city['id']
    city_name = next_city['name']
    print_success(f"Selected: {city_name} ({next_city['country']})")
    
    # Get next personality (rotate)
    personality = get_next_personality(state['last_personality'])
    print_success(f"Personality: {personality.replace('_', ' ').title()}")
    
    # Select content type (cycle through types)
    content_types = ['city_review', 'food_review', 'cultural_debate', 'language_lesson', 'tourist_trap']
    content_type = content_types[state['total_posts'] % len(content_types)]
    print_success(f"Content type: {content_type.replace('_', ' ').title()}")
    
    # Create output directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = Path(f'output/worldtour/{city_id}_{timestamp}')
    output_dir.mkdir(parents=True, exist_ok=True)
    print_success(f"Output directory: {output_dir}")
    
    # Generate city-specific content prompt
    print_info("\n" + "="*70)
    print_info("STEP 1: Generating City Content Prompt...")
    print_info("="*70)
    
    try:
        city_content = worldtour_gen.generate_city_content(
            city_id=city_id,
            personality=personality,
            content_type=content_type
        )
        print_success(f"Topic: {city_content['topic'][:80]}...")
        
        # Save city content info
        with open(output_dir / 'city_info.json', 'w') as f:
            json.dump(city_content, f, indent=2)
        
    except Exception as e:
        print_error(f"City content generation failed: {e}")
        return 1
    
    # Generate text
    print_info("\n" + "="*70)
    print_info("STEP 2: Generating Comedy Text...")
    print_info("="*70)
    
    try:
        text_result = personality_engine.generate_text(
            topic=city_content['topic'],
            personality=personality,
            length='medium',
            style_intensity=0.8
        )
        
        comedy_text = text_result['text']
        print_success(f"Generated {len(comedy_text)} characters")
        print_info(f"Preview: {comedy_text[:150]}...")
        
        # Save text
        with open(output_dir / 'comedy_text.txt', 'w') as f:
            f.write(comedy_text)
        
        with open(output_dir / 'text_metadata.json', 'w') as f:
            json.dump(text_result, f, indent=2)
        
    except Exception as e:
        print_error(f"Text generation failed: {e}")
        return 1
    
    # Generate audio
    print_info("\n" + "="*70)
    print_info("STEP 3: Synthesizing Voice...")
    print_info("="*70)
    
    try:
        audio_result = voice_synth.synthesize(
            text=comedy_text,
            personality=personality,
            format='mp3'
        )
        
        audio_path = audio_result.get('audio_path')
        if audio_path and Path(audio_path).exists():
            # Copy to output directory
            import shutil
            dest_audio = output_dir / 'voice.mp3'
            shutil.copy(audio_path, dest_audio)
            print_success(f"Audio saved: {dest_audio}")
        else:
            print_error("Audio file not generated")
            dest_audio = None
        
    except Exception as e:
        print_error(f"Audio generation failed: {e}")
        dest_audio = None
    
    # Generate image
    print_info("\n" + "="*70)
    print_info("STEP 4: Creating Quote Card...")
    print_info("="*70)
    
    try:
        # Use first sentence or first 150 chars for quote card
        quote_text = comedy_text.split('.')[0] + '.' if '.' in comedy_text else comedy_text[:150]
        
        image_result = image_gen.generate_quote_card(
            quote=quote_text,
            personality=personality,
            author_name=personality.replace('_', ' ').title()
        )
        
        image_path = image_result.get('image_path')
        if image_path and Path(image_path).exists():
            # Copy to output directory
            import shutil
            dest_image = output_dir / 'quote_card.png'
            shutil.copy(image_path, dest_image)
            print_success(f"Image saved: {dest_image}")
        else:
            print_error("Image file not generated")
            dest_image = None
        
    except Exception as e:
        print_error(f"Image generation failed: {e}")
        dest_image = None
    
    # Generate video (if audio and image available)
    if dest_audio and dest_image:
        print_info("\n" + "="*70)
        print_info("STEP 5: Creating Video...")
        print_info("="*70)
        
        try:
            video_result = video_gen.create_lyric_video(
                text=comedy_text,
                audio_path=str(dest_audio),
                personality=personality,
                background_image=str(dest_image)
            )
            
            video_path = video_result.get('video_path')
            if video_path and Path(video_path).exists():
                # Copy to output directory
                import shutil
                dest_video = output_dir / 'final_video.mp4'
                shutil.copy(video_path, dest_video)
                print_success(f"Video saved: {dest_video}")
            else:
                print_error("Video file not generated")
            
        except Exception as e:
            print_error(f"Video generation failed: {e}")
    else:
        print_info("\n" + "="*70)
        print_info("STEP 5: Skipping video (audio or image not available)")
        print_info("="*70)
    
    # Mark city as visited
    print_info("\nMarking city as visited...")
    worldtour_gen.mark_city_visited(city_id)
    print_success(f"{city_name} marked as visited")
    
    # Update state
    state['last_personality'] = personality
    state['last_city'] = city_id
    state['total_posts'] += 1
    save_state(state)
    
    # Print summary
    print_header("✅ GENERATION COMPLETE!")
    print(f"\n{Colors.BOLD}Content Summary:{Colors.ENDC}")
    print(f"  🌍 City: {city_name} ({next_city['country']})")
    print(f"  🎭 Personality: {personality.replace('_', ' ').title()}")
    print(f"  📝 Content Type: {content_type.replace('_', ' ').title()}")
    print(f"  📁 Output Directory: {output_dir}")
    print(f"  📊 Total Posts: {state['total_posts']}")
    
    # Print worldtour stats
    stats = worldtour_gen.get_stats()
    print(f"\n{Colors.BOLD}Worldtour Progress:{Colors.ENDC}")
    print(f"  ✓ Visited: {stats['visited_cities']} / {stats['total_cities']} cities")
    print(f"  ⏳ Remaining: {stats['remaining_cities']} cities")
    print(f"  📈 Completion: {stats['completion_percentage']}%")
    
    # Print next steps
    print(f"\n{Colors.BOLD}Next Steps:{Colors.ENDC}")
    print(f"  1. Review generated content in: {output_dir}")
    print(f"  2. Upload video to TikTok, YouTube Shorts, Instagram Reels")
    print(f"  3. Post teaser text on Twitter with link")
    print(f"  4. Use hashtags: #UMAJAWorldtour #AIComedy #{city_id}")
    print(f"  5. Create poll: 'Which city should we visit next?'")
    
    # Print file list
    print(f"\n{Colors.BOLD}Generated Files:{Colors.ENDC}")
    for file in sorted(output_dir.glob('*')):
        size = file.stat().st_size
        size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/1024/1024:.1f} MB"
        print(f"  📄 {file.name} ({size_str})")
    
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 Ready for social media upload! 🎉{Colors.ENDC}\n")
    
    return 0


if __name__ == '__main__':
    try:
        exit_code = generate_daily_content()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print_error("\n\nGeneration interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
