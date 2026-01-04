#!/usr/bin/env python3
"""
🌍 UMAJA World Tour Launcher
Starts the Live World Tour - visiting cities and generating content

This is IT! The moment we've been building towards!

Now with ethical validation via Rule Bank System.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from worldtour_generator import WorldtourGenerator
from rule_bank import RuleBank
from reasoning_middleware import ReasoningMiddleware

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
    
    # Initialize ethical systems
    print("🛡️  Initializing ethical governance systems...")
    rule_bank = RuleBank(memory_path='.agent-memory')
    middleware = ReasoningMiddleware(rule_bank)
    print("✅ Rule Bank loaded with Bahá'í principles")
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
    
    all_content_approved = True
    generated_contents = []
    
    for i, personality in enumerate(personalities):
        content_type = content_types[i % len(content_types)]
        
        print(f"{i+1}. {personality.replace('_', ' ').title()}")
        
        # Generate city content
        content = generator.generate_city_content(
            city_id=city_id,
            personality=personality,
            content_type=content_type
        )
        
        # Validate content with Rule Bank before posting
        action = {
            'type': 'post_world_tour_content',
            'city_id': city_id,
            'city_name': city_name,
            'personality': personality,
            'content_type': content_type,
            'content': content.get('topic', ''),
            'confidence': 0.85,  # Generated content confidence
            'benefit_score': 0.8,  # High benefit: bringing smiles to people
            'user_facing': True,
            'expected_reach': 1000,
        }
        
        validation_result = middleware.intercept(action)
        
        # Show preview and validation result
        topic = content.get('topic', '')
        if topic:
            preview = topic[:100] + "..." if len(topic) > 100 else topic
            print(f"   Topic: {preview}")
        
        print(f"   Type: {content_type}")
        print(f"   ✅ Ethical Check: {validation_result['status'].upper()}")
        
        if validation_result['status'] == 'approved':
            print(f"   🛡️  Bahá'í Alignment: ✓ Passed all principles")
            generated_contents.append(content)
        elif validation_result['status'] == 'rejected':
            print(f"   ⚠️  Ethical Violations: {len(validation_result['validation']['violated_rules'])} rules")
            print(f"   📝 Recommendations: {', '.join(validation_result['validation']['recommendations'][:2])}")
            all_content_approved = False
        else:  # requires_review
            print(f"   🔍 Requires Human Review: {validation_result['reasoning']}")
            all_content_approved = False
        
        print()
    
    # Save Rule Bank updates
    rule_bank.save_rules()
    
    print("-" * 70)
    print()
    
    if not all_content_approved:
        print("⚠️  Some content requires review or was rejected")
        print("   Not all content will be posted immediately")
        print()
    
    # Mark city as visited (if not dry run and content approved)
    if not dry_run and all_content_approved:
        success = generator.mark_city_visited(city_id)
        
        if success:
            print("✅ City marked as VISITED in database!")
            print()
            print(f"📊 Progress: {generator.get_progress()}")
            print()
        else:
            print("⚠️  Could not mark city as visited")
    elif dry_run:
        print("🔍 DRY RUN - City NOT marked as visited")
        print()
    else:
        print("⏸️  City NOT marked as visited (awaiting content review)")
        print()
    
    print("-" * 70)
    print()
    print("🎉 WORLD TOUR CYCLE COMPLETED!")
    print()
    print("Ethical Summary:")
    print(f"  ✅ Content validated against Bahá'í principles")
    print(f"  📊 Rule Bank: {len(rule_bank.rules)} active rules")
    
    # Get violation report
    report = rule_bank.get_violation_report()
    if report['total_violations'] > 0:
        print(f"  ⚠️  Total violations: {report['total_violations']}")
        print(f"  📈 Violation rate: {report['violation_rate']:.1%}")
    else:
        print(f"  🌟 Zero violations - perfect alignment!")
    
    print()
    print("Next steps:")
    if all_content_approved:
        print("1. Generate multimedia (audio, images, video)")
        print("2. Distribute via 215+ channels")
        print("3. Monitor engagement and feedback")
        print("4. Continue to next city!")
    else:
        print("1. Review flagged content")
        print("2. Apply recommended improvements")
        print("3. Re-validate with Rule Bank")
        print("4. Post approved content")
    print()
    print("=" * 70)
    print()
    print("'Die Erde ist nur ein Land, und alle Menschen sind seine Bürger'")
    print("- Bahá'u'lláh")
    print()
    print("Happy Landing! 🚀😊")
    print("=" * 70)
    
    return all_content_approved


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
