"""
UMAJA Batch Content Generator - Mass Production
Generate content for multiple cities simultaneously with parallel processing
"""

import logging
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BatchContentGenerator:
    """
    Generate content for multiple cities simultaneously.
    Supports parallel processing for speed and multiple personality variations.
    """
    
    def __init__(self, max_workers: int = 10):
        """
        Initialize batch content generator.
        
        Args:
            max_workers: Maximum number of parallel workers
        """
        self.max_workers = max_workers
        
        # Lazy-load to avoid circular imports
        self._worldtour_gen = None
        self._personality_engine = None
    
    @property
    def worldtour_gen(self):
        """Lazy-load worldtour generator"""
        if self._worldtour_gen is None:
            from worldtour_generator import WorldtourGenerator
            self._worldtour_gen = WorldtourGenerator()
        return self._worldtour_gen
    
    @property
    def personality_engine(self):
        """Lazy-load personality engine"""
        if self._personality_engine is None:
            from personality_engine import PersonalityEngine
            self._personality_engine = PersonalityEngine()
        return self._personality_engine
    
    def generate_city_batch(self, 
                           cities: List[str],
                           languages: List[str] = None,
                           platforms: List[str] = None,
                           parallel: bool = True) -> Dict:
        """
        Generate Daily Smiles for multiple cities at once.
        
        Args:
            cities: List of city IDs
            languages: List of language codes (default: ['en'])
            platforms: List of platforms (default: ['tiktok', 'instagram', 'youtube'])
            parallel: Use multiprocessing for speed (default: True)
            
        Returns:
            {
                'city_id': {
                    'content': {...},
                    'variations': 3,
                    'languages': {...},
                    'platforms': {...},
                    'generated_at': '...',
                    'quality_score': 0.95
                }
            }
        """
        if languages is None:
            languages = ['en']
        
        if platforms is None:
            platforms = ['tiktok', 'instagram', 'youtube']
        
        logger.info(f"📦 Generating content batch for {len(cities)} cities...")
        
        if parallel and len(cities) > 1:
            return self._generate_parallel(cities, languages, platforms)
        else:
            return self._generate_sequential(cities, languages, platforms)
    
    def _generate_sequential(self, cities: List[str], 
                            languages: List[str],
                            platforms: List[str]) -> Dict:
        """Generate content sequentially (slower but simpler)"""
        batch = {}
        
        for city_id in cities:
            logger.info(f"  Generating for {city_id}...")
            batch[city_id] = self._generate_city_content(
                city_id, languages, platforms
            )
        
        return batch
    
    def _generate_parallel(self, cities: List[str],
                          languages: List[str],
                          platforms: List[str]) -> Dict:
        """Generate content in parallel (10x faster)"""
        batch = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_city = {
                executor.submit(
                    self._generate_city_content, 
                    city_id, 
                    languages, 
                    platforms
                ): city_id
                for city_id in cities
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_city):
                city_id = future_to_city[future]
                try:
                    batch[city_id] = future.result()
                    logger.info(f"  ✓ Completed {city_id}")
                except Exception as e:
                    logger.error(f"  ✗ Failed {city_id}: {e}")
                    batch[city_id] = {'error': str(e)}
        
        return batch
    
    def _generate_city_content(self, 
                              city_id: str,
                              languages: List[str],
                              platforms: List[str]) -> Dict:
        """
        Generate content for a single city with all variations.
        
        Args:
            city_id: City identifier
            languages: Languages to generate
            platforms: Platforms to target
            
        Returns:
            Content dictionary for the city
        """
        # Get city data
        city = self.worldtour_gen.get_city(city_id)
        if not city:
            raise ValueError(f"Unknown city: {city_id}")
        
        # Generate base content for each archetype
        variations = self.generate_with_variations(city_id, count=3)
        
        # Generate translations for each language
        languages_content = {}
        for lang in languages:
            languages_content[lang] = self._translate_content(
                variations, lang
            )
        
        # Adapt for each platform
        platforms_content = {}
        for platform in platforms:
            platforms_content[platform] = self._adapt_for_platform(
                variations, platform
            )
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(variations)
        
        return {
            'city_id': city_id,
            'city_name': city['name'],
            'country': city['country'],
            'content': variations[0],  # Best variation
            'variations': variations,
            'languages': languages_content,
            'platforms': platforms_content,
            'generated_at': datetime.utcnow().isoformat(),
            'quality_score': quality_score
        }
    
    def generate_with_variations(self, city: str, count: int = 3) -> List[Dict]:
        """
        Generate multiple variations for A/B testing.
        
        Creates:
        - Professor version (educational angle)
        - Worrier version (relatable angle)
        - Enthusiast version (celebratory angle)
        
        Auto-selects best based on predicted engagement.
        
        Args:
            city: City ID
            count: Number of variations (default: 3)
            
        Returns:
            List of content variations, sorted by predicted engagement
        """
        archetypes = ['professor', 'worrier', 'enthusiast'][:count]
        variations = []
        
        for archetype in archetypes:
            # Generate base smile content
            smile = self.personality_engine.generate_daily_smile(archetype)
            
            # Get city-specific content
            city_content = self.worldtour_gen.generate_city_content(
                city,
                personality=self._map_archetype_to_personality(archetype),
                content_type='city_review'
            )
            
            # Combine city content with smile personality
            combined_content = self._combine_content(smile, city_content)
            
            # Predict engagement score
            engagement_score = self._predict_engagement(combined_content)
            
            variations.append({
                'archetype': archetype,
                'content': combined_content,
                'engagement_score': engagement_score,
                'city_content': city_content,
                'smile_data': smile
            })
        
        # Sort by engagement score (highest first)
        variations.sort(key=lambda x: x['engagement_score'], reverse=True)
        
        return variations
    
    def _map_archetype_to_personality(self, archetype: str) -> str:
        """Map personality archetype to worldtour personality"""
        mapping = {
            'professor': 'john_cleese',
            'worrier': 'c3po',
            'enthusiast': 'robin_williams'
        }
        return mapping.get(archetype, 'john_cleese')
    
    def _combine_content(self, smile: Dict, city_content: Dict) -> str:
        """
        Combine smile personality with city-specific content.
        
        Args:
            smile: Smile data from personality engine
            city_content: City content from worldtour generator
            
        Returns:
            Combined content string
        """
        # Create engaging content that combines both
        content = f"{city_content['topic']}\n\n"
        content += f"Fun fact: {city_content['fun_facts'][0]}\n\n"
        content += f"What do you think about {city_content['city_name']}? "
        content += "Share your experiences in the comments!"
        
        return content
    
    def _translate_content(self, variations: List[Dict], language: str) -> Dict:
        """
        Translate content to target language.
        
        Args:
            variations: Content variations
            language: Target language code
            
        Returns:
            Translated content dictionary
        """
        # For MVP, we'll return a placeholder structure
        # In production, this would use deep-translator
        
        if language == 'en':
            # No translation needed
            return variations[0]['content']
        
        # Placeholder for translation
        return {
            'language': language,
            'original': variations[0]['content'],
            'translated': f"[{language.upper()}] {variations[0]['content']}",
            'translation_note': 'Translation would be performed here in production'
        }
    
    def _adapt_for_platform(self, variations: List[Dict], platform: str) -> Dict:
        """
        Adapt content for specific platform requirements.
        
        Args:
            variations: Content variations
            platform: Target platform
            
        Returns:
            Platform-adapted content
        """
        base_content = variations[0]['content']
        
        adaptations = {
            'tiktok': {
                'max_length': 150,
                'hashtags': ['#DailySmile', '#TikTokTravel', '#WorldTour'],
                'duration': '30-60 seconds',
                'format': 'vertical_video'
            },
            'instagram': {
                'max_length': 2200,
                'hashtags': ['#DailySmile', '#TravelGram', '#WorldTour', '#SmileMore'],
                'format': 'reel_or_post'
            },
            'youtube': {
                'max_length': 5000,
                'hashtags': ['#DailySmile', '#WorldTour', '#Travel'],
                'format': 'short_or_video'
            }
        }
        
        adaptation = adaptations.get(platform, adaptations['tiktok'])
        
        # Trim content if needed
        content = base_content[:adaptation['max_length']]
        
        return {
            'platform': platform,
            'content': content,
            'hashtags': adaptation['hashtags'],
            **adaptation
        }
    
    def _predict_engagement(self, content: str) -> float:
        """
        Predict engagement score for content.
        
        Args:
            content: Content string
            
        Returns:
            Engagement score (0.0 - 1.0)
        """
        # Simple heuristic-based scoring
        score = 0.5  # Base score
        
        # Length scoring
        if 100 <= len(content) <= 500:
            score += 0.2
        
        # Question scoring (engagement hooks)
        if '?' in content:
            score += 0.1
        
        # Excitement scoring
        if '!' in content:
            score += 0.1
        
        # Emoji scoring
        if any(emoji in content for emoji in ['😊', '🌍', '✨', '🎉']):
            score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_quality_score(self, variations: List[Dict]) -> float:
        """
        Calculate overall quality score for generated content.
        
        Args:
            variations: Content variations
            
        Returns:
            Quality score (0.0 - 1.0)
        """
        if not variations:
            return 0.0
        
        # Average engagement scores across variations
        avg_engagement = sum(v['engagement_score'] for v in variations) / len(variations)
        
        # Bonus for having multiple variations
        variation_bonus = min(len(variations) / 3, 0.1)
        
        return min(avg_engagement + variation_bonus, 1.0)


# Example usage
if __name__ == "__main__":
    generator = BatchContentGenerator()
    
    print("🏭 Batch Content Generator Test")
    print("=" * 60)
    
    # Test with 3 cities
    cities = ['new_york', 'london', 'tokyo']
    languages = ['en', 'es']
    platforms = ['tiktok', 'instagram']
    
    print(f"\nGenerating batch for {len(cities)} cities...")
    batch = generator.generate_city_batch(
        cities=cities,
        languages=languages,
        platforms=platforms,
        parallel=True
    )
    
    print(f"\n✨ Batch Generation Complete!")
    for city_id, data in batch.items():
        if 'error' not in data:
            print(f"\n{data['city_name']}:")
            print(f"  Variations: {len(data['variations'])}")
            print(f"  Languages: {list(data['languages'].keys())}")
            print(f"  Platforms: {list(data['platforms'].keys())}")
            print(f"  Quality Score: {data['quality_score']:.2f}")
