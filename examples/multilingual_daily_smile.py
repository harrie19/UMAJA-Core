#!/usr/bin/env python3
"""Complete Multilingual Daily Smile Example

This example demonstrates the full workflow of the Global Translation Engine:
1. Generate English Daily Smile
2. Translate to all supported languages
3. Apply cultural adaptations
4. Export for TikTok with subtitles
5. Export for Instagram
6. Export for YouTube

Usage:
    python examples/multilingual_daily_smile.py
"""

import sys
from pathlib import Path
from datetime import datetime
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from personality_engine import PersonalityEngine
from global_translator import GlobalTranslator
from cultural_adapter import CulturalAdapter
from platform_exporter import PlatformExporter


def main():
    """Run the complete multilingual content generation workflow"""
    
    print("="*70)
    print("🌍 UMAJA-Core Global Translation Engine Demo")
    print("="*70)
    print()
    
    # Initialize all components
    print("🔧 Initializing engines...\n")
    engine = PersonalityEngine()
    translator = GlobalTranslator()
    adapter = CulturalAdapter()
    exporter = PlatformExporter()
    
    # Step 1: Generate English Daily Smile
    print("="*70)
    print("STEP 1: Generate Daily Smile (English)")
    print("="*70)
    print()
    
    smile = engine.generate_daily_smile('professor')
    print(f"Personality: {smile['personality']}")
    print(f"Tone: {smile['tone']}")
    print(f"\nContent:\n{smile['content']}\n")
    
    # Step 2: Translate to all languages
    print("="*70)
    print("STEP 2: Translate to All Languages")
    print("="*70)
    print()
    
    translations = translator.translate_smile(smile)
    print(f"✓ Translated to {len(translations)} languages")
    print(f"  Languages: {', '.join(translations.keys())}\n")
    
    # Show some example translations
    examples = ['es', 'hi', 'ar']
    for lang in examples:
        if lang in translations:
            lang_name = translator.supported_languages[lang]
            print(f"\n{lang_name} ({lang.upper()}):")
            print("-" * 70)
            print(translations[lang]['text'][:150] + "..." if len(translations[lang]['text']) > 150 else translations[lang]['text'])
    
    print()
    
    # Step 3: Apply Cultural Adaptations
    print("="*70)
    print("STEP 3: Cultural Adaptation")
    print("="*70)
    print()
    
    for lang in translations:
        if lang != 'en':
            # Get cultural guidelines
            guidelines = adapter.get_cultural_guidelines(lang)
            print(f"\n{translator.supported_languages[lang]} Cultural Guidelines:")
            print(f"  - Formality: {guidelines.get('formality', 'N/A')}")
            print(f"  - Humor Style: {guidelines.get('humor_style', 'N/A')}")
            print(f"  - Text Direction: {adapter.get_text_direction(lang)}")
            
            # Adapt content
            adapted = adapter.adapt_content(translations[lang]['text'], lang)
            translations[lang]['text'] = adapted
    
    print("\n✓ Cultural adaptations applied\n")
    
    # Step 4: Generate Subtitles
    print("="*70)
    print("STEP 4: Generate Subtitles")
    print("="*70)
    print()
    
    # Generate subtitles for a few languages
    subtitle_langs = ['en', 'es', 'hi']
    for lang in subtitle_langs:
        if lang in translations:
            srt = translator.generate_subtitles(
                translations[lang]['text'],
                lang,
                duration=30
            )
            translations[lang]['subtitles'] = srt
            print(f"✓ Generated subtitles for {translator.supported_languages[lang]}")
    
    # Show example subtitle
    print(f"\nExample SRT (English):")
    print("-" * 70)
    print(translations['en']['subtitles'][:300] + "...")
    print()
    
    # Step 5: Export for TikTok
    print("="*70)
    print("STEP 5: Export for TikTok")
    print("="*70)
    print()
    
    tiktok_exports = {}
    for lang in ['en', 'es', 'hi']:
        if lang in translations:
            tiktok = exporter.export_for_tiktok(translations[lang], lang)
            tiktok_exports[lang] = tiktok
            
            lang_name = translator.supported_languages[lang]
            print(f"\n{lang_name} TikTok Export:")
            print("-" * 70)
            print(f"Caption: {tiktok['caption'][:100]}...")
            print(f"Hashtags: {len(tiktok['hashtags'])} tags")
            print(f"Video: {tiktok['video_specs']['aspect_ratio']}, {tiktok['video_specs']['duration']}s")
    
    print()
    
    # Step 6: Export for Instagram
    print("="*70)
    print("STEP 6: Export for Instagram Reels")
    print("="*70)
    print()
    
    instagram_exports = {}
    for lang in ['en', 'pt', 'fr']:
        if lang in translations:
            instagram = exporter.export_for_instagram(translations[lang], lang)
            instagram_exports[lang] = instagram
            
            lang_name = translator.supported_languages[lang]
            print(f"✓ {lang_name} Instagram Reel ready")
    
    print()
    
    # Step 7: Export for YouTube
    print("="*70)
    print("STEP 7: Export for YouTube Shorts")
    print("="*70)
    print()
    
    youtube_exports = {}
    for lang in ['en', 'ar', 'zh']:
        if lang in translations:
            youtube = exporter.export_for_youtube(translations[lang], lang)
            youtube_exports[lang] = youtube
            
            lang_name = translator.supported_languages[lang]
            print(f"\n{lang_name} YouTube Short:")
            print("-" * 70)
            print(f"Title: {youtube['title']}")
            print(f"Tags: {', '.join(youtube['tags'][:5])}...")
            print(f"Description: {youtube['description'][:100]}...")
    
    print()
    
    # Summary
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print()
    print(f"✨ Generated content in {len(translations)} languages")
    print(f"📱 Exported for 3 social media platforms")
    print(f"🎬 Created subtitles for 3 languages")
    print(f"🌍 Total potential reach: 5+ billion people")
    print()
    print("Files created (in memory):")
    print(f"  - Translations: {len(translations)} text files")
    print(f"  - Subtitles: {len(subtitle_langs)} SRT files")
    print(f"  - TikTok exports: {len(tiktok_exports)} formats")
    print(f"  - Instagram exports: {len(instagram_exports)} formats")
    print(f"  - YouTube exports: {len(youtube_exports)} formats")
    print()
    
    # Optional: Save to files
    print("="*70)
    print("SAVING TO FILES")
    print("="*70)
    print()
    
    output_dir = Path("output/multilingual_example")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    
    # Save all translations
    for lang, content in translations.items():
        filename = f"smile_{lang}_{timestamp}.txt"
        filepath = output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Language: {translator.supported_languages[lang]}\n")
            f.write(f"Code: {lang}\n")
            f.write(f"Personality: {content['metadata']['personality']}\n")
            f.write(f"Generated: {datetime.utcnow().isoformat()}\n")
            f.write("\n" + "="*70 + "\n\n")
            f.write(content['text'])
            f.write("\n\n")
            if content.get('hashtags'):
                f.write("Hashtags: " + ' '.join(content['hashtags']))
            f.write("\n")
        
        print(f"✓ Saved {translator.supported_languages[lang]}: {filepath}")
        
        # Save subtitles if available
        if content.get('subtitles'):
            srt_filename = f"subtitles_{lang}_{timestamp}.srt"
            srt_filepath = output_dir / srt_filename
            with open(srt_filepath, 'w', encoding='utf-8') as f:
                f.write(content['subtitles'])
            print(f"  + Subtitles: {srt_filepath}")
    
    # Save platform exports
    platform_data = {
        'tiktok': tiktok_exports,
        'instagram': instagram_exports,
        'youtube': youtube_exports
    }
    
    exports_file = output_dir / f"platform_exports_{timestamp}.json"
    with open(exports_file, 'w', encoding='utf-8') as f:
        json.dump(platform_data, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Saved platform exports: {exports_file}")
    
    print()
    print("="*70)
    print("✅ Demo Complete!")
    print("="*70)
    print()
    print("🌍 UMAJA-Core is now ready to reach billions worldwide!")
    print("😊 Mission: Put smiles on faces globally!")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
