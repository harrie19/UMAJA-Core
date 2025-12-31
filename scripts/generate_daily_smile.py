#!/usr/bin/env python3
"""Daily Smile Generator - Community Engagement Content Creator

Generates warm, friendly content focused on putting smiles on faces
and building community connections through engaging questions and relatable moments.

Usage:
    python scripts/generate_daily_smile.py [--archetype ARCHETYPE_NAME] [--count N]
    
Examples:
    python scripts/generate_daily_smile.py
    python scripts/generate_daily_smile.py --archetype professor
    python scripts/generate_daily_smile.py --count 5
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from personality_engine import PersonalityEngine


def generate_smile(archetype_name: str = None, output_format: str = "text") -> dict:
    """Generate a single Daily Smile post
    
    Args:
        archetype_name: Optional personality archetype (professor, worrier, enthusiast)
        output_format: Output format (text, json, markdown)
        
    Returns:
        Dictionary containing the generated smile content
    """
    engine = PersonalityEngine()
    smile_data = engine.generate_daily_smile(archetype_name)
    smile_data["timestamp"] = datetime.now(timezone.utc).isoformat()
    
    return smile_data


def format_output(smile_data: dict, format_type: str = "text") -> str:
    """Format the smile data for output
    
    Args:
        smile_data: Dictionary containing smile content
        format_type: Output format (text, json, markdown)
        
    Returns:
        Formatted string
    """
    if format_type == "json":
        return json.dumps(smile_data, indent=2)
    
    elif format_type == "markdown":
        return f"""# Daily Smile - {smile_data['timestamp']}

**Personality:** {smile_data['personality']}  
**Tone:** {smile_data['tone']}  
**Traits:** {smile_data['traits']}

## Content

{smile_data['content']}

---
*Generated with warmth and care by UMAJA-Core*
"""
    
    else:  # text format
        return f"""{'='*70}
DAILY SMILE GENERATOR
{'='*70}

Timestamp: {smile_data['timestamp']}
Personality: {smile_data['personality']}
Tone: {smile_data['tone']}
Traits: {smile_data['traits']}

{'-'*70}
CONTENT:
{'-'*70}

{smile_data['content']}

{'='*70}
Mission: Put smiles on faces 😊
{'='*70}
"""


def save_to_file(content: str, filename: str = None) -> str:
    """Save content to a file
    
    Args:
        content: Content to save
        filename: Optional filename, auto-generated if None
        
    Returns:
        Path to saved file
    """
    if filename is None:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"daily_smile_{timestamp}.txt"
    
    output_dir = Path("output/daily_smiles")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = output_dir / filename
    filepath.write_text(content)
    
    return str(filepath)


def main():
    """Main entry point for Daily Smile Generator"""
    parser = argparse.ArgumentParser(
        description="Generate Daily Smile content for community engagement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python scripts/generate_daily_smile.py
  python scripts/generate_daily_smile.py --archetype professor
  python scripts/generate_daily_smile.py --count 3 --format json
  python scripts/generate_daily_smile.py --save
  python scripts/generate_daily_smile.py --multilingual
  python scripts/generate_daily_smile.py --language es
  python scripts/generate_daily_smile.py --export-platform tiktok
        """
    )
    
    parser.add_argument(
        "--archetype",
        choices=["professor", "worrier", "enthusiast"],
        help="Specific personality archetype to use"
    )
    
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of smiles to generate (default: 1)"
    )
    
    parser.add_argument(
        "--format",
        choices=["text", "json", "markdown"],
        default="text",
        help="Output format (default: text)"
    )
    
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save output to file in output/daily_smiles/"
    )
    
    parser.add_argument(
        "--output",
        help="Specific output filename (implies --save)"
    )
    
    parser.add_argument(
        "--multilingual",
        action="store_true",
        help="Generate content in all supported languages"
    )
    
    parser.add_argument(
        "--language",
        help="Generate content in specific language (e.g., 'es', 'hi', 'ar')"
    )
    
    parser.add_argument(
        "--export-platform",
        choices=["tiktok", "instagram", "youtube"],
        help="Export content for specific platform"
    )
    
    args = parser.parse_args()
    
    # Handle multilingual or language-specific generation
    if args.multilingual or args.language:
        generate_multilingual(args)
        return
    
    # Handle platform export
    if args.export_platform:
        generate_with_platform_export(args)
        return
    
    # Standard generation (original behavior)
    # Generate smiles
    print(f"\n🌟 Generating {args.count} Daily Smile(s)...\n")
    
    for i in range(args.count):
        smile_data = generate_smile(args.archetype, args.format)
        output = format_output(smile_data, args.format)
        
        # Print to console
        print(output)
        
        if i < args.count - 1:
            print("\n" + "="*70 + "\n")
        
        # Save to file if requested
        if args.save or args.output:
            filename = args.output if args.output else None
            filepath = save_to_file(output, filename)
            print(f"\n✅ Saved to: {filepath}")
    
    print("\n😊 Mission accomplished: Putting smiles on faces!\n")


def generate_multilingual(args):
    """Generate content in multiple languages"""
    from global_translator import GlobalTranslator
    
    engine = PersonalityEngine()
    translator = GlobalTranslator()
    
    # Determine which languages to use
    if args.language:
        if not translator.is_language_supported(args.language):
            print(f"❌ Error: Unsupported language '{args.language}'")
            print(f"Supported: {', '.join(translator.supported_languages.keys())}")
            return
        languages = [args.language]
    else:
        languages = list(translator.supported_languages.keys())
    
    print(f"\n🌍 Generating multilingual content ({len(languages)} languages)...\n")
    
    # Generate original smile
    smile_data = engine.generate_daily_smile(args.archetype)
    
    # Translate
    translations = translator.translate_smile(smile_data, languages)
    
    # Display results
    for lang, content in translations.items():
        lang_name = translator.supported_languages[lang]
        print(f"\n{'='*70}")
        print(f"🌍 {lang_name} ({lang.upper()})")
        print(f"{'='*70}\n")
        print(content['text'])
        if content.get('hashtags'):
            print(f"\nHashtags: {' '.join(content['hashtags'])}")
        print()
    
    print("\n😊 Mission accomplished: Putting smiles on faces worldwide!\n")


def generate_with_platform_export(args):
    """Generate content with platform-specific export"""
    from global_translator import GlobalTranslator
    from platform_exporter import PlatformExporter
    
    engine = PersonalityEngine()
    translator = GlobalTranslator()
    exporter = PlatformExporter()
    
    print(f"\n📱 Generating content for {args.export_platform.upper()}...\n")
    
    # Generate original smile
    smile_data = engine.generate_daily_smile(args.archetype)
    
    # Get language
    language = args.language if args.language else 'en'
    
    # Translate if needed
    if language != 'en':
        translations = translator.translate_smile(smile_data, [language])
        content = translations[language]
    else:
        content = {
            'text': smile_data['content'],
            'hashtags': translator._extract_hashtags(smile_data['content']),
            'metadata': {
                'personality': smile_data['personality'],
                'tone': smile_data['tone'],
                'traits': smile_data['traits']
            }
        }
    
    # Export for platform
    if args.export_platform == 'tiktok':
        export = exporter.export_for_tiktok(content, language)
    elif args.export_platform == 'instagram':
        export = exporter.export_for_instagram(content, language)
    elif args.export_platform == 'youtube':
        export = exporter.export_for_youtube(content, language)
    
    # Display export
    print(f"Platform: {export['platform']}")
    print(f"Language: {export['language']}")
    print(f"\nCaption:\n{'-'*70}")
    print(export.get('caption') or export.get('description'))
    print(f"{'-'*70}\n")
    
    if 'title' in export:
        print(f"Title: {export['title']}\n")
    
    print(f"Video Specs: {export['video_specs']}\n")
    
    print("\n😊 Mission accomplished: Content ready for platform!\n")


if __name__ == "__main__":
    main()
