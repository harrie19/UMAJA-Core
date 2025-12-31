#!/usr/bin/env python3
"""
🌍 UMAJA World Tour Launcher
Starts the Live World Tour - visiting cities and generating content

This is IT! The moment we've been building towards!
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from worldtour_generator import WorldtourGenerator

def launch_world_tour(dry_run=False):
    """
    🚀 LAUNCH THE WORLD TOUR!
    
    Args:
        dry_run: If True, simulates without actually modifying files
    """
    print("=" * 70)
    print("🌍 UMAJA WORLD TOUR - LIVE LAUNCH")
    print("=" * 70)
    print()
    print("Mission: Bring smiles to all 8 billion people on Earth!")
    print("Method: Visit 50+ cities, 3 personalities, simultaneous distribution")
    print("Inspired by: Bahá'u'lláh's vision of unity")
    print()
    print("-" * 70)
    print()
    
    # Initialize generator
    generator = WorldtourGenerator()
    
    # Get next city
    next_city = generator.get_next_city()
    
    if not next_city:
        print("❌ No cities available to visit!")
        return False
    
    city_id = next_city['id']
    city_name = next_city['name']
    country = next_city['country']
    
    print(f"🎯 Next destination: {city_name}, {country}")
    print()
    print(f"Topics: {', '.join(next_city['topics'][:3])}")
    print(f"Stereotypes: {', '.join(next_city['stereotypes'][:2])}")
    print(f"Fun fact: {next_city['fun_facts'][0]}")
    print()
    print("-" * 70)
    print()
    
    # Generate content for each personality
    personalities = ['john_cleese', 'c3po', 'robin_williams']
    content_types = ['city_review', 'food_review', 'cultural_debate']
    
    print("🎭 Generating content from our 3 comedians:")
    print()
    
    for i, personality in enumerate(personalities):
        content_type = content_types[i % len(content_types)]
        
        print(f"{i+1}. {personality.replace('_', ' ').title()}")
        
        # Generate city content
        content = generator.generate_city_content(
            city_id=city_id,
            personality=personality,
            content_type=content_type
        )
        
        # Show preview
        topic = content.get('topic', '')
        if topic:
            preview = topic[:100] + "..." if len(topic) > 100 else topic
            print(f"   Topic: {preview}")
        
        print(f"   Type: {content_type}")
        print()
    
    # Mark city as visited (if not dry run)
    if not dry_run:
        success = generator.mark_city_visited(city_id)
        
        if success:
            print("✅ City marked as VISITED in database!")
            print()
            print(f"📊 Progress: {generator.get_progress()}")
            print()
        else:
            print("⚠️  Could not mark city as visited")
    else:
        print("🔍 DRY RUN - City NOT marked as visited")
        print()
    
    print("-" * 70)
    print()
    print("🎉 WORLD TOUR SUCCESSFULLY LAUNCHED!")
    print()
    print("Next steps:")
    print("1. Generate multimedia (audio, images, video)")
    print("2. Distribute via 215+ channels")
    print("3. Monitor engagement and feedback")
    print("4. Continue to next city!")
    print()
    print("=" * 70)
    print()
    print("'Die Erde ist nur ein Land, und alle Menschen sind seine Bürger'")
    print("- Bahá'u'lláh")
    print()
    print("Happy Landing! 🚀😊")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🌍 Launch the UMAJA World Tour - Visit cities and generate content"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate without modifying files"
    )
    
    args = parser.parse_args()
    
    success = launch_world_tour(dry_run=args.dry_run)
    
    sys.exit(0 if success else 1)
