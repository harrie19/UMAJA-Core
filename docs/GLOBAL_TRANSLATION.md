# 🌍 Global Translation Guide

Transform UMAJA-Core content to reach 7+ billion people worldwide through automated translation into 8 major languages.

## Overview

The Global Translation Engine enables UMAJA-Core to automatically translate Daily Smile content into 8 major world languages, covering over 5 billion speakers. The system maintains personality, tone, and cultural appropriateness while expanding your reach from English-only (1.5B speakers) to global audiences.

## Supported Languages

| Language | Code | Speakers | Regions |
|----------|------|----------|---------|
| 🇬🇧 English | `en` | 1.5B | Global |
| 🇪🇸 Spanish | `es` | 550M | Spain, Latin America |
| 🇮🇳 Hindi | `hi` | 600M | India, South Asia |
| 🇸🇦 Arabic | `ar` | 420M | Middle East, North Africa |
| 🇨🇳 Chinese | `zh` | 1.3B | China, Taiwan, Singapore |
| 🇧🇷 Portuguese | `pt` | 260M | Brazil, Portugal, Africa |
| 🇫🇷 French | `fr` | 280M | France, Africa, Canada |
| 🇷🇺 Russian | `ru` | 260M | Russia, Central Asia |

**Total Reach: 5+ Billion People** 🌍

## Quick Start

### Basic Translation

```python
from src.personality_engine import PersonalityEngine
from src.global_translator import GlobalTranslator

# Generate English smile
engine = PersonalityEngine()
smile = engine.generate_daily_smile()

# Translate to all languages
translator = GlobalTranslator()
global_content = translator.translate_smile(smile)

# Access translations
spanish = global_content['es']
hindi = global_content['hi']
arabic = global_content['ar']
```

### Generate Multilingual Content at Once

```python
from src.personality_engine import PersonalityEngine

engine = PersonalityEngine()

# Generate in all supported languages
result = engine.generate_global_smile()

print(result['original'])  # English version
print(result['translations']['es'])  # Spanish version
print(result['translations']['hi'])  # Hindi version
```

### Command Line Usage

```bash
# Generate in all languages
python scripts/generate_multilingual_content.py

# Generate in specific languages only
python scripts/generate_multilingual_content.py --languages es,hi,ar

# Use specific archetype
python scripts/generate_multilingual_content.py --archetype professor

# Save output files
python scripts/generate_multilingual_content.py --save

# Export for platforms
python scripts/generate_multilingual_content.py --export-all
```

### Using Updated Daily Smile Script

```bash
# Generate in all languages
python scripts/generate_daily_smile.py --multilingual

# Generate in specific language
python scripts/generate_daily_smile.py --language es

# Export for platform
python scripts/generate_daily_smile.py --export-platform tiktok --language hi
```

## Features

### 1. Text Translation

Translates content while preserving:
- Personality and tone
- Formatting and structure
- Emoji and special characters
- Engaging questions and warmth

```python
translator = GlobalTranslator()
translated = translator.translate_text(
    "Hello, world!",
    target_language='es'
)
# Output: "¡Hola, mundo!"
```

### 2. Hashtag Localization

Automatically translates hashtags to target language while keeping brand hashtags in English:

```python
hashtags = ['#DailySmile', '#Joy', '#UMAJACore']
localized = translator.localize_hashtags(hashtags, 'es')
# Output: ['#SonrisaDiaria', '#Alegría', '#UMAJACore']
```

**Predefined Hashtag Translations:**
- `#DailySmile` → Spanish: `#SonrisaDiaria`, Hindi: `#दैनिकमुस्कान`
- `#Smile` → Arabic: `#ابتسامة`, Chinese: `#微笑`
- `#Joy` → Portuguese: `#Alegria`, French: `#Joie`
- Brand hashtags (`#UMAJACore`, `#UMAJA`) always remain in English

### 3. Subtitle Generation

Generate SRT subtitle files for video content:

```python
subtitles = translator.generate_subtitles(
    text="Your translated content here",
    language='es',
    duration=30  # seconds
)

# Save to file
with open('subtitles_es.srt', 'w', encoding='utf-8') as f:
    f.write(subtitles)
```

**Output format (SRT):**
```
1
00:00:00,000 --> 00:00:03,000
First subtitle line

2
00:00:03,000 --> 00:00:06,000
Second subtitle line
```

### 4. Language Detection

Automatically detect the best language for a country:

```python
lang = translator.detect_optimal_language('MX')  # Returns 'es'
lang = translator.detect_optimal_language('IN')  # Returns 'hi'
lang = translator.detect_optimal_language('BR')  # Returns 'pt'
```

## Cultural Adaptation

The Cultural Adapter ensures content is appropriate for different cultures:

```python
from src.cultural_adapter import CulturalAdapter

adapter = CulturalAdapter()

# Adapt content for culture
adapted = adapter.adapt_content(content, target_culture='ar')

# Get cultural guidelines
guidelines = adapter.get_cultural_guidelines('ar')
print(guidelines['guidelines'])
# ['Use formal greetings and closings', 'Avoid direct humor about religion', ...]
```

### Cultural Considerations by Language

#### Arabic (`ar`)
- **Formality:** High
- **Humor Style:** Subtle
- **Avoid:** Alcohol, pork, romantic relationships
- **Tips:** Use formal language, respect for elders, family values

#### Chinese (`zh`)
- **Formality:** Medium-High
- **Humor Style:** Indirect
- **Avoid:** Politics, religion
- **Tips:** Harmony and balance, indirect communication, lucky numbers (8)

#### Hindi (`hi`)
- **Formality:** Medium
- **Humor Style:** Warm
- **Avoid:** Beef, inter-religious conflicts
- **Tips:** Respect for elders, family-centric, spirituality important

#### Spanish (`es`)
- **Formality:** Low-Medium
- **Humor Style:** Direct
- **Tips:** Warm and expressive, family important, emotional expression welcome

#### Portuguese (`pt`)
- **Formality:** Low
- **Humor Style:** Warm
- **Tips:** Very friendly, physical affection common, joy and celebration valued

#### French (`fr`)
- **Formality:** Medium-High
- **Humor Style:** Subtle
- **Tips:** Intellectual discourse, subtlety appreciated, quality over quantity

#### Russian (`ru`)
- **Formality:** High
- **Humor Style:** Dark
- **Avoid:** Politics
- **Tips:** Direct communication, sincerity valued, formal initially

## Platform Export

Export translated content for social media platforms:

```python
from src.platform_exporter import PlatformExporter

exporter = PlatformExporter()

# Export for TikTok
tiktok_content = exporter.export_for_tiktok(translated_content, 'es')

# Export for Instagram
instagram_content = exporter.export_for_instagram(translated_content, 'hi')

# Export for YouTube
youtube_content = exporter.export_for_youtube(translated_content, 'ar')

# Export for all platforms
all_platforms = exporter.export_all_platforms(translated_content, 'zh')
```

### Platform Specifications

#### TikTok
- **Aspect Ratio:** 9:16
- **Max Caption:** 2200 characters
- **Max Hashtags:** 30
- **Subtitle Style:** Burned-in
- **Optimal Duration:** 30 seconds

#### Instagram Reels
- **Aspect Ratio:** 9:16
- **Max Caption:** 2200 characters
- **Max Hashtags:** 30
- **Subtitle Style:** Burned-in
- **Optimal Duration:** 30 seconds

#### YouTube Shorts
- **Aspect Ratio:** 9:16
- **Max Description:** 5000 characters
- **Max Hashtags:** 15
- **Subtitle Style:** Separate SRT track
- **Optimal Duration:** 60 seconds

## Best Practices

### Translation Quality

1. **Keep it Simple:** Use clear, straightforward language in original English content for better translation
2. **Avoid Idioms:** English idioms may not translate well; use universal concepts
3. **Test Translations:** Review translations with native speakers when possible
4. **Preserve Tone:** The system maintains personality, but review for cultural appropriateness

### Cultural Sensitivity

1. **Research Your Audience:** Understand cultural norms for target regions
2. **Use Cultural Adapter:** Always run content through cultural adaptation
3. **Avoid Sensitive Topics:** Politics, religion, and controversial subjects may not translate well
4. **Local Examples:** When possible, use examples relevant to the target culture

### Hashtag Strategy

1. **Mix Languages:** Use localized hashtags + brand hashtags in English
2. **Research Trends:** Check trending hashtags in target languages
3. **Keep it Relevant:** Ensure hashtags match the content and culture
4. **Don't Overuse:** Stick to 5-8 relevant hashtags per post

### Platform Optimization

1. **Match Platform Style:** Each platform has different norms and expectations
2. **Optimize Captions:** Keep captions concise and engaging
3. **Use Subtitles:** Always include subtitles for accessibility and engagement
4. **Test Aspect Ratios:** Ensure video content displays properly on each platform

## Troubleshooting

### Translation Quality Issues

**Problem:** Translation doesn't sound natural
- **Solution:** Simplify original English content, avoid idioms and complex sentence structures

**Problem:** Hashtags not translating
- **Solution:** Check if hashtag is in predefined list; add custom translations as needed

**Problem:** Special characters or emoji broken
- **Solution:** Ensure using UTF-8 encoding when saving files

### Rate Limiting

**Problem:** Translation API rate limits
- **Solution:** The system includes small delays (0.1s) between requests; for large batches, increase delay

### Cultural Issues

**Problem:** Content seems inappropriate for culture
- **Solution:** Review Cultural Adapter guidelines; adjust original content to be more universal

**Problem:** Humor not landing in target culture
- **Solution:** Check humor style preferences; some cultures prefer subtle vs direct humor

## Advanced Usage

### Batch Processing

```python
from src.personality_engine import PersonalityEngine
from src.global_translator import GlobalTranslator

engine = PersonalityEngine()
translator = GlobalTranslator()

# Generate multiple smiles
smiles = []
for i in range(10):
    smile = engine.generate_daily_smile()
    translations = translator.translate_smile(smile)
    smiles.append(translations)

# Save all translations
for i, smile_set in enumerate(smiles):
    for lang, content in smile_set.items():
        filename = f"smile_{i}_{lang}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content['text'])
```

### Custom Language Selection

```python
# Only translate to specific languages
languages = ['es', 'pt']  # Spanish and Portuguese only
translations = translator.translate_smile(smile, languages)
```

### Adding Subtitle Styling (Future Enhancement)

While the current system generates SRT files, future versions will support:
- Custom fonts and colors
- Position customization
- Background styling
- Automatic video burning

## Configuration

Environment variables in `.env`:

```env
# Default languages for translation
DEFAULT_TRANSLATION_LANGUAGES=es,hi,ar,zh,pt

# Translation service (currently 'free')
TRANSLATION_SERVICE=free

# Cultural sensitivity level
CULTURAL_SENSITIVITY=high

# Auto-detect language from location
AUTO_LANGUAGE_DETECTION=true

# Platform export formats
EXPORT_FORMATS=tiktok,instagram,youtube

# Subtitle styling
SUBTITLE_FONT=Arial
SUBTITLE_SIZE=48
SUBTITLE_COLOR=white
SUBTITLE_OUTLINE=black
```

## API Reference

### GlobalTranslator

#### `translate_smile(smile_content, target_languages=None)`
Translate Daily Smile to multiple languages.

#### `localize_hashtags(hashtags, language)`
Translate hashtags to target language.

#### `generate_subtitles(text, language, duration=30)`
Generate SRT subtitle file.

#### `detect_optimal_language(country_code)`
Auto-detect language for country.

### CulturalAdapter

#### `adapt_content(content, target_culture)`
Adapt content for cultural appropriateness.

#### `get_cultural_guidelines(country_or_language)`
Get cultural dos/don'ts.

#### `is_topic_sensitive(topic, culture=None)`
Check if topic is culturally sensitive.

### PlatformExporter

#### `export_for_tiktok(content, language)`
Format for TikTok.

#### `export_for_instagram(content, language)`
Format for Instagram Reels.

#### `export_for_youtube(content, language)`
Format for YouTube Shorts.

#### `export_all_platforms(content, language)`
Export for all platforms at once.

## Future Enhancements

The following features are planned for future releases:

- [ ] Professional translation API integration (DeepL)
- [ ] Video generation with burned-in subtitles
- [ ] Voice synthesis in multiple languages
- [ ] A/B testing for translation quality
- [ ] Community translation contributions
- [ ] Real-time translation API endpoint
- [ ] Advanced cultural adaptation using NLP
- [ ] Translation quality metrics and feedback

## Support

For issues or questions:
1. Check this documentation
2. Review examples in `examples/` directory
3. Open an issue on GitHub
4. Consult the Cultural Adapter guidelines

---

**Remember: Our mission is to put smiles on faces worldwide! 🌍😊**
