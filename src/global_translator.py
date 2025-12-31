"""Global Translation Engine - Translate UMAJA content to 8 major languages

Transform UMAJA-Core from English-only to globally accessible content,
enabling reach to 7+ billion people worldwide.
"""

from typing import Dict, List, Optional
from deep_translator import GoogleTranslator
from langdetect import detect
import pycountry
import time
import re


class GlobalTranslator:
    """Main translation engine supporting 8 major world languages"""
    
    def __init__(self):
        """Initialize translator with 8 major languages covering 5+ billion speakers"""
        self.supported_languages = {
            'en': 'English',      # 1.5B speakers
            'es': 'Spanish',      # 550M speakers
            'hi': 'Hindi',        # 600M speakers
            'ar': 'Arabic',       # 420M speakers
            'zh': 'Chinese',      # 1.3B speakers
            'pt': 'Portuguese',   # 260M speakers
            'fr': 'French',       # 280M speakers
            'ru': 'Russian'       # 260M speakers
        }
        
        # Brand hashtags that should remain in English
        self.brand_hashtags = ['#UMAJACore', '#UMAJA']
        
        # Country to language mapping
        self.country_language_map = {
            'US': 'en', 'GB': 'en', 'CA': 'en', 'AU': 'en', 'NZ': 'en', 'IE': 'en',
            'ES': 'es', 'MX': 'es', 'AR': 'es', 'CO': 'es', 'CL': 'es', 'PE': 'es',
            'IN': 'hi',
            'SA': 'ar', 'EG': 'ar', 'AE': 'ar', 'IQ': 'ar', 'JO': 'ar', 'LB': 'ar',
            'CN': 'zh', 'TW': 'zh', 'HK': 'zh', 'SG': 'zh',
            'BR': 'pt', 'PT': 'pt', 'AO': 'pt', 'MZ': 'pt',
            'FR': 'fr', 'BE': 'fr', 'CH': 'fr', 'CA': 'fr', 'DZ': 'fr', 'MA': 'fr',
            'RU': 'ru', 'BY': 'ru', 'KZ': 'ru', 'UA': 'ru'
        }
    
    def translate_text(self, text: str, target_language: str, source_language: str = 'en') -> str:
        """Translate text while preserving tone and personality
        
        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'es', 'hi')
            source_language: Source language code (default: 'en')
            
        Returns:
            Translated text
        """
        if target_language == source_language:
            return text
        
        if target_language not in self.supported_languages:
            raise ValueError(f"Unsupported language: {target_language}")
        
        try:
            # Map our language codes to Google Translator codes
            lang_map = {
                'zh': 'zh-CN',  # Chinese Simplified
                'ar': 'ar',
                'en': 'en',
                'es': 'es',
                'fr': 'fr',
                'hi': 'hi',
                'pt': 'pt',
                'ru': 'ru'
            }
            
            target_lang_code = lang_map.get(target_language, target_language)
            source_lang_code = lang_map.get(source_language, source_language)
            
            # Use Google Translator (free, no API key needed)
            translator = GoogleTranslator(source=source_lang_code, target=target_lang_code)
            
            # Split into sentences to preserve formatting
            sentences = text.split('\n')
            translated_sentences = []
            
            for sentence in sentences:
                if sentence.strip():
                    # Add small delay to avoid rate limiting
                    time.sleep(0.1)
                    translated = translator.translate(sentence)
                    translated_sentences.append(translated)
                else:
                    translated_sentences.append('')
            
            return '\n'.join(translated_sentences)
        
        except Exception as e:
            print(f"Translation error for {target_language}: {e}")
            return text  # Return original text on error
    
    def translate_smile(self, smile_content: Dict, target_languages: List[str] = None) -> Dict:
        """Translate Daily Smile content to multiple languages
        
        Args:
            smile_content: Output from PersonalityEngine.generate_daily_smile()
            target_languages: List of language codes, defaults to all supported
            
        Returns:
            Dictionary with translations for each language:
            {
                'en': {'text': '...', 'hashtags': [...], 'metadata': {...}},
                'es': {'text': '...', 'hashtags': [...], 'metadata': {...}},
                ...
            }
        """
        if target_languages is None:
            target_languages = list(self.supported_languages.keys())
        
        # Validate languages
        for lang in target_languages:
            if lang not in self.supported_languages:
                raise ValueError(f"Unsupported language: {lang}")
        
        results = {}
        
        # Always include English original
        results['en'] = {
            'text': smile_content.get('content', ''),
            'hashtags': self._extract_hashtags(smile_content.get('content', '')),
            'metadata': {
                'personality': smile_content.get('personality', ''),
                'tone': smile_content.get('tone', ''),
                'traits': smile_content.get('traits', ''),
                'language': 'en',
                'language_name': 'English'
            }
        }
        
        # Translate to other languages
        for lang in target_languages:
            if lang == 'en':
                continue
            
            print(f"Translating to {self.supported_languages[lang]}...")
            
            translated_text = self.translate_text(
                smile_content.get('content', ''),
                lang
            )
            
            results[lang] = {
                'text': translated_text,
                'hashtags': self.localize_hashtags(results['en']['hashtags'], lang),
                'metadata': {
                    'personality': smile_content.get('personality', ''),
                    'tone': smile_content.get('tone', ''),
                    'traits': smile_content.get('traits', ''),
                    'language': lang,
                    'language_name': self.supported_languages[lang]
                }
            }
        
        return results
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text"""
        return re.findall(r'#\w+', text)
    
    def localize_hashtags(self, hashtags: List[str], language: str) -> List[str]:
        """Translate and localize hashtags for target language/culture
        
        Args:
            hashtags: List of hashtags to localize
            language: Target language code
            
        Returns:
            List of localized hashtags
        
        Examples:
            - #DailySmile → #SonrisaDiaria (Spanish)
            - #DailySmile → #दैनिकमुस्कान (Hindi)
            - Keep brand hashtags in English (#UMAJACore)
        """
        if language == 'en':
            return hashtags
        
        localized = []
        
        # Predefined localized hashtags for common tags
        hashtag_translations = {
            'es': {
                '#DailySmile': '#SonrisaDiaria',
                '#Smile': '#Sonrisa',
                '#Joy': '#Alegría',
                '#Happiness': '#Felicidad',
                '#Community': '#Comunidad',
                '#Connection': '#Conexión'
            },
            'hi': {
                '#DailySmile': '#दैनिकमुस्कान',
                '#Smile': '#मुस्कान',
                '#Joy': '#खुशी',
                '#Happiness': '#खुशी',
                '#Community': '#समुदाय',
                '#Connection': '#संबंध'
            },
            'ar': {
                '#DailySmile': '#ابتسامة_يومية',
                '#Smile': '#ابتسامة',
                '#Joy': '#فرح',
                '#Happiness': '#سعادة',
                '#Community': '#مجتمع',
                '#Connection': '#اتصال'
            },
            'zh': {
                '#DailySmile': '#每日微笑',
                '#Smile': '#微笑',
                '#Joy': '#喜悦',
                '#Happiness': '#幸福',
                '#Community': '#社区',
                '#Connection': '#连接'
            },
            'pt': {
                '#DailySmile': '#SorrisoDiário',
                '#Smile': '#Sorriso',
                '#Joy': '#Alegria',
                '#Happiness': '#Felicidade',
                '#Community': '#Comunidade',
                '#Connection': '#Conexão'
            },
            'fr': {
                '#DailySmile': '#SourireQuotidien',
                '#Smile': '#Sourire',
                '#Joy': '#Joie',
                '#Happiness': '#Bonheur',
                '#Community': '#Communauté',
                '#Connection': '#Connexion'
            },
            'ru': {
                '#DailySmile': '#ЕжедневнаяУлыбка',
                '#Smile': '#Улыбка',
                '#Joy': '#Радость',
                '#Happiness': '#Счастье',
                '#Community': '#Сообщество',
                '#Connection': '#Связь'
            }
        }
        
        for hashtag in hashtags:
            # Keep brand hashtags in English
            if hashtag in self.brand_hashtags:
                localized.append(hashtag)
            # Use predefined translation if available
            elif language in hashtag_translations and hashtag in hashtag_translations[language]:
                localized.append(hashtag_translations[language][hashtag])
            # Otherwise keep original
            else:
                localized.append(hashtag)
        
        return localized
    
    def generate_subtitles(self, text: str, language: str, duration: int = 30) -> str:
        """Generate SRT subtitle file for video content
        
        Args:
            text: Translated text
            language: Target language code
            duration: Video duration in seconds
            
        Returns:
            SRT-formatted string ready for video overlay
        """
        # Split text into subtitle chunks (max ~40 chars per line)
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        max_chars_per_line = 40
        
        for word in words:
            if current_length + len(word) + 1 > max_chars_per_line:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        # Generate SRT format
        srt_content = []
        time_per_chunk = duration / len(chunks) if chunks else duration
        
        for i, chunk in enumerate(chunks):
            start_time = i * time_per_chunk
            end_time = (i + 1) * time_per_chunk
            
            start_formatted = self._format_srt_time(start_time)
            end_formatted = self._format_srt_time(end_time)
            
            srt_content.append(f"{i + 1}")
            srt_content.append(f"{start_formatted} --> {end_formatted}")
            srt_content.append(chunk)
            srt_content.append("")  # Blank line between subtitles
        
        return '\n'.join(srt_content)
    
    def _format_srt_time(self, seconds: float) -> str:
        """Format time for SRT subtitle format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def detect_optimal_language(self, country_code: str) -> str:
        """Auto-detect best language for a country
        
        Args:
            country_code: ISO 3166-1 alpha-2 country code (e.g., 'US', 'MX', 'IN')
            
        Returns:
            Language code (e.g., 'en', 'es', 'hi')
        
        Examples:
            - 'US' → 'en'
            - 'MX' → 'es'
            - 'IN' → 'hi'
            - 'BR' → 'pt'
        """
        country_code = country_code.upper()
        return self.country_language_map.get(country_code, 'en')
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get dictionary of supported languages"""
        return self.supported_languages.copy()
    
    def is_language_supported(self, language_code: str) -> bool:
        """Check if a language is supported"""
        return language_code in self.supported_languages
