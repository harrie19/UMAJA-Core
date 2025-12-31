#!/usr/bin/env python3
"""Generate Daily Smile in all supported languages

Batch translation tool for generating content in multiple languages at once.

Usage:
    python scripts/generate_multilingual_content.py
    python scripts/generate_multilingual_content.py --languages es,hi,ar
    python scripts/generate_multilingual_content.py --archetype professor
    python scripts/generate_multilingual_content.py --export-all
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from personality_engine import PersonalityEngine
from global_translator import GlobalTranslator
from cultural_adapter import CulturalAdapter
from platform_exporter import PlatformExporter


def main():
    """Main entry point for multilingual content generation"""
    parser = argparse.ArgumentParser(
        description="Generate Daily Smile in multiple languages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  # Generate in all supported languages
  python scripts/generate_multilingual_content.py

  # Generate only in Spanish and Hindi
  python scripts/generate_multilingual_content.py --languages es,hi

  # Use specific archetype
  python scripts/generate_multilingual_content.py --archetype professor

  # Export for all platforms
  python scripts/generate_multilingual_content.py --export-all

  # Save output to file
  python scripts/generate_multilingual_content.py --save
        """
    )
    
    parser.add_argument(
        "--archetype",
        choices=["professor", "worrier", "enthusiast"],
        help="Specific personality archetype to use"
    )
    
    parser.add_argument(
        "--languages",
        help="Comma-separated list of language codes (e.g., 'es,hi,ar')"
    )
    
    parser.add_argument(
        "--export-all",
        action="store_true",
        help="Export for all platforms (TikTok, Instagram, YouTube)"
    )
    
    parser.add_argument(
        "--platform",
        choices=["tiktok", "instagram", "youtube"],
        help="Export for specific platform only"
    )
    
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save output to files in output/multilingual/"
    )
    
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)"
    )
    
    args = parser.parse_args()
    
    # Initialize engines
    print("🌍 Initializing Global Translation Engine...\n")
    engine = PersonalityEngine()
    translator = GlobalTranslator()
    adapter = CulturalAdapter()
    exporter = PlatformExporter()
    
    # Parse languages
    if args.languages:
        languages = [lang.strip() for lang in args.languages.split(',')]
        # Validate languages
        for lang in languages:
            if not translator.is_language_supported(lang):
                print(f"❌ Error: Unsupported language '{lang}'")
                print(f"Supported languages: {', '.join(translator.supported_languages.keys())}")
                return 1
    else:
        languages = list(translator.supported_languages.keys())
    
    # Step 1: Generate Daily Smile (English)
    print(f"📝 Step 1: Generating Daily Smile ({args.archetype or 'random'})...")
    smile_data = engine.generate_daily_smile(args.archetype)
    print(f"✓ Generated: {smile_data['personality']}\n")
    
    # Step 2: Translate to all languages
    print(f"🌐 Step 2: Translating to {len(languages)} languages...")
    translations = translator.translate_smile(smile_data, languages)
    print(f"✓ Translated to: {', '.join(languages)}\n")
    
    # Step 3: Apply cultural adaptation
    print("🎭 Step 3: Applying cultural adaptations...")
    for lang, content in translations.items():
        if lang != 'en':
            adapted_text = adapter.adapt_content(content['text'], lang)
            content['text'] = adapted_text
    print("✓ Cultural adaptations applied\n")
    
    # Step 4: Generate subtitles for each
    print("📑 Step 4: Generating subtitles...")
    for lang, content in translations.items():
        content['subtitles'] = translator.generate_subtitles(
            content['text'],
            lang,
            duration=30
        )
    print("✓ Subtitles generated\n")
    
    # Step 5: Export platform-specific formats
    platform_exports = {}
    
    if args.export_all or args.platform:
        print("📱 Step 5: Exporting platform-specific formats...")
        
        for lang, content in translations.items():
            platform_exports[lang] = {}
            
            if args.export_all:
                platform_exports[lang] = exporter.export_all_platforms(content, lang)
            elif args.platform:
                if args.platform == 'tiktok':
                    platform_exports[lang][args.platform] = exporter.export_for_tiktok(content, lang)
                elif args.platform == 'instagram':
                    platform_exports[lang][args.platform] = exporter.export_for_instagram(content, lang)
                elif args.platform == 'youtube':
                    platform_exports[lang][args.platform] = exporter.export_for_youtube(content, lang)
        
        print("✓ Platform exports ready\n")
    
    # Step 6: Display/Save results
    print("="*70)
    print("MULTILINGUAL CONTENT GENERATED")
    print("="*70)
    print()
    
    if args.format == "json":
        output_data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'original': smile_data,
            'translations': translations,
            'platform_exports': platform_exports if platform_exports else None
        }
        print(json.dumps(output_data, indent=2, ensure_ascii=False))
    else:
        # Text format
        for lang, content in translations.items():
            lang_name = translator.supported_languages[lang]
            print(f"\n{'='*70}")
            print(f"🌍 {lang_name} ({lang.upper()})")
            print(f"{'='*70}")
            print()
            print(content['text'])
            print()
            if content.get('hashtags'):
                print("Hashtags:", ' '.join(content['hashtags']))
            print()
    
    # Save to files if requested
    if args.save:
        print("\n💾 Saving to files...")
        output_dir = Path("output/multilingual")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        
        # Save translations
        for lang, content in translations.items():
            filename = f"daily_smile_{lang}_{timestamp}.txt"
            filepath = output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Language: {translator.supported_languages[lang]}\n")
                f.write(f"Personality: {content['metadata']['personality']}\n")
                f.write(f"Timestamp: {datetime.now(timezone.utc).isoformat()}\n")
                f.write("\n" + "="*70 + "\n\n")
                f.write(content['text'])
                f.write("\n\n")
                if content.get('hashtags'):
                    f.write("Hashtags: " + ' '.join(content['hashtags']))
                f.write("\n")
            
            print(f"  ✓ Saved: {filepath}")
            
            # Save subtitles
            if content.get('subtitles'):
                srt_filename = f"daily_smile_{lang}_{timestamp}.srt"
                srt_filepath = output_dir / srt_filename
                with open(srt_filepath, 'w', encoding='utf-8') as f:
                    f.write(content['subtitles'])
                print(f"  ✓ Saved: {srt_filepath}")
        
        # Save platform exports if available
        if platform_exports:
            exports_filename = f"platform_exports_{timestamp}.json"
            exports_filepath = output_dir / exports_filename
            with open(exports_filepath, 'w', encoding='utf-8') as f:
                json.dump(platform_exports, f, indent=2, ensure_ascii=False)
            print(f"  ✓ Saved: {exports_filepath}")
    
    print("\n" + "="*70)
    print("✨ Mission accomplished: Global content ready!")
    print(f"📊 Generated content in {len(languages)} languages")
    print("😊 Putting smiles on faces worldwide!")
    print("="*70 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
