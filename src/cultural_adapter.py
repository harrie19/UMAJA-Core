"""Cultural Adapter - Handle cultural nuances and sensitivities

Ensure content is culturally appropriate and respectful across different
regions and cultures.
"""

from typing import Dict, List
import re


class CulturalAdapter:
    """Handle cultural sensitivity and adaptation of content"""
    
    def __init__(self):
        """Initialize cultural adapter with guidelines and rules"""
        
        # Cultural guidelines by region/language
        self.cultural_guidelines = {
            'ar': {
                'name': 'Arabic/Middle East',
                'direction': 'rtl',  # Right-to-left
                'avoid_topics': ['alcohol', 'pork', 'romantic relationships'],
                'humor_style': 'subtle',
                'formality': 'high',
                'guidelines': [
                    'Use formal greetings and closings',
                    'Avoid direct humor about religion',
                    'Family values are highly important',
                    'Respect for elders is paramount',
                    'Use modest language and examples'
                ]
            },
            'zh': {
                'name': 'Chinese',
                'direction': 'ltr',
                'avoid_topics': ['politics', 'religion'],
                'humor_style': 'indirect',
                'formality': 'medium-high',
                'guidelines': [
                    'Harmony and balance are valued',
                    'Indirect communication is preferred',
                    'Respect for hierarchy',
                    'Lucky numbers (8) and colors (red) are positive',
                    'Avoid number 4 (sounds like death)'
                ]
            },
            'hi': {
                'name': 'Hindi/Indian',
                'direction': 'ltr',
                'avoid_topics': ['beef', 'inter-religious conflicts'],
                'humor_style': 'warm',
                'formality': 'medium',
                'guidelines': [
                    'Respect for elders and teachers',
                    'Family is central to culture',
                    'Spirituality is important',
                    'Use respectful terms',
                    'Avoid left-hand references (considered unclean)'
                ]
            },
            'es': {
                'name': 'Spanish/Latin',
                'direction': 'ltr',
                'avoid_topics': [],
                'humor_style': 'direct',
                'formality': 'low-medium',
                'guidelines': [
                    'Warmth and expressiveness valued',
                    'Family is very important',
                    'Personal connections matter',
                    'More relaxed about time',
                    'Emotional expression is welcome'
                ]
            },
            'pt': {
                'name': 'Portuguese/Brazilian',
                'direction': 'ltr',
                'avoid_topics': [],
                'humor_style': 'warm',
                'formality': 'low',
                'guidelines': [
                    'Very warm and friendly culture',
                    'Physical affection is common',
                    'Family and friends are central',
                    'Relaxed and informal',
                    'Joy and celebration valued'
                ]
            },
            'fr': {
                'name': 'French',
                'direction': 'ltr',
                'avoid_topics': [],
                'humor_style': 'subtle',
                'formality': 'medium-high',
                'guidelines': [
                    'Value intellectual discourse',
                    'Appreciate subtlety and nuance',
                    'Quality over quantity',
                    'More formal than English',
                    'Art and culture highly valued'
                ]
            },
            'ru': {
                'name': 'Russian',
                'direction': 'ltr',
                'avoid_topics': ['politics'],
                'humor_style': 'dark',
                'formality': 'high',
                'guidelines': [
                    'Direct communication style',
                    'Respect for strength and resilience',
                    'Dark humor is common',
                    'Formal in initial interactions',
                    'Value sincerity and authenticity'
                ]
            },
            'en': {
                'name': 'English',
                'direction': 'ltr',
                'avoid_topics': [],
                'humor_style': 'varied',
                'formality': 'low-medium',
                'guidelines': [
                    'Casual and friendly',
                    'Direct communication',
                    'Individual expression valued',
                    'Humor is welcome',
                    'Informality is common'
                ]
            }
        }
        
        # Sensitive topics that need careful handling
        self.sensitive_topics = [
            'politics', 'religion', 'war', 'death', 'disease',
            'race', 'ethnicity', 'gender', 'sexuality', 'poverty',
            'violence', 'drugs', 'alcohol'
        ]
    
    def adapt_content(self, content: str, target_culture: str) -> str:
        """Adapt content for cultural appropriateness
        
        Args:
            content: Original content to adapt
            target_culture: Target culture/language code (e.g., 'ar', 'zh')
            
        Returns:
            Culturally adapted content
        
        Checks:
            - Avoid culturally sensitive topics
            - Adjust humor style (some cultures prefer subtle vs direct)
            - Modify examples (use local references)
            - Check for unintentional offense
        """
        if target_culture not in self.cultural_guidelines:
            return content  # No adaptation needed for unknown cultures
        
        guidelines = self.cultural_guidelines[target_culture]
        adapted_content = content
        
        # Check for sensitive topics
        content_lower = content.lower()
        for topic in guidelines.get('avoid_topics', []):
            if topic in content_lower:
                # Log warning but don't block - this is advisory
                print(f"⚠️  Warning: Content may contain culturally sensitive topic '{topic}' for {guidelines['name']}")
        
        # Add cultural context notes
        if target_culture == 'ar':
            # For Arabic, ensure respectful tone
            adapted_content = self._ensure_respectful_tone(adapted_content)
        
        elif target_culture == 'zh':
            # For Chinese, ensure indirect/harmonious tone
            adapted_content = self._soften_directness(adapted_content)
        
        elif target_culture == 'hi':
            # For Hindi, add warmth and respect
            adapted_content = self._add_warmth(adapted_content)
        
        return adapted_content
    
    def _ensure_respectful_tone(self, content: str) -> str:
        """Ensure content has respectful, formal tone for Arabic cultures
        
        Note: This is a placeholder implementation. In production, this would use
        NLP to adjust tone and formality levels.
        """
        return content
    
    def _soften_directness(self, content: str) -> str:
        """Soften direct statements for Chinese culture
        
        Note: This is a placeholder implementation. In production, this would
        rephrase direct questions to be more indirect and harmonious.
        """
        return content
    
    def _add_warmth(self, content: str) -> str:
        """Add warmth and familial tone for Hindi/Indian culture
        
        Note: This is a placeholder implementation. In production, this would
        add friendly terms and warm expressions appropriate for the culture.
        """
        return content
    
    def get_cultural_guidelines(self, country_or_language: str) -> Dict:
        """Return cultural dos/don'ts for content creation
        
        Args:
            country_or_language: Country code or language code
            
        Returns:
            Dictionary with cultural guidelines
        """
        # Try as language code first
        if country_or_language in self.cultural_guidelines:
            return self.cultural_guidelines[country_or_language].copy()
        
        # Default to English guidelines
        return self.cultural_guidelines['en'].copy()
    
    def get_text_direction(self, language: str) -> str:
        """Get text direction for a language
        
        Args:
            language: Language code
            
        Returns:
            'ltr' for left-to-right, 'rtl' for right-to-left
        """
        guidelines = self.cultural_guidelines.get(language, {'direction': 'ltr'})
        return guidelines.get('direction', 'ltr')
    
    def is_topic_sensitive(self, topic: str, culture: str = None) -> bool:
        """Check if a topic is sensitive for a given culture
        
        Args:
            topic: Topic to check
            culture: Optional culture code, checks universal if None
            
        Returns:
            True if topic is sensitive
        """
        topic_lower = topic.lower()
        
        # Check universal sensitive topics
        if any(sensitive in topic_lower for sensitive in self.sensitive_topics):
            return True
        
        # Check culture-specific topics
        if culture and culture in self.cultural_guidelines:
            avoid_topics = self.cultural_guidelines[culture].get('avoid_topics', [])
            if any(avoid in topic_lower for avoid in avoid_topics):
                return True
        
        return False
    
    def get_formality_level(self, language: str) -> str:
        """Get formality level for a language
        
        Args:
            language: Language code
            
        Returns:
            Formality level: 'low', 'medium', 'high'
        """
        guidelines = self.cultural_guidelines.get(language, {'formality': 'medium'})
        return guidelines.get('formality', 'medium')
    
    def get_humor_style(self, language: str) -> str:
        """Get preferred humor style for a language/culture
        
        Args:
            language: Language code
            
        Returns:
            Humor style: 'direct', 'subtle', 'warm', 'dark', 'indirect'
        """
        guidelines = self.cultural_guidelines.get(language, {'humor_style': 'varied'})
        return guidelines.get('humor_style', 'varied')
