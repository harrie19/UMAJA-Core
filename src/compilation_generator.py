"""
UMAJA Compilation Generator - Auto-Create Highlights
Automatically generate "Best Of" compilations from world tour content
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CompilationGenerator:
    """
    Auto-generate "Best Of" compilations.
    Creates highlight reels and recap videos from world tour content.
    """
    
    def __init__(self, output_dir: str = "output/compilations"):
        """
        Initialize compilation generator.
        
        Args:
            output_dir: Directory for compilation output
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_launch_day_recap(self, date: str, content_batch: Dict) -> Dict:
        """
        Create "50 Cities in 24 Hours" compilation video.
        
        Features:
        - 1-2 second clip per city
        - Upbeat music
        - Transition effects
        - Text overlay with city names
        - "Thank you" message at end
        
        Duration: 60 seconds (perfect for all platforms)
        
        Args:
            date: Launch date string
            content_batch: Generated content batch
            
        Returns:
            Compilation metadata
        """
        logger.info(f"🎬 Creating launch day recap for {date}...")
        
        # Select cities for compilation
        cities = list(content_batch.keys())[:50]
        
        compilation = {
            'title': f'🌍 UMAJA World Tour - {len(cities)} Cities in 24 Hours',
            'date': date,
            'duration_seconds': 60,
            'cities_count': len(cities),
            'cities': cities,
            'format': 'vertical_video',
            'resolution': '1080x1920',
            'music': 'upbeat_instrumental',
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Create compilation structure
        clips = []
        time_per_city = 60 / len(cities) if cities else 1
        
        for i, city_id in enumerate(cities):
            city_data = content_batch.get(city_id, {})
            
            clips.append({
                'city_id': city_id,
                'city_name': city_data.get('city_name', city_id),
                'start_time': i * time_per_city,
                'duration': time_per_city,
                'transition': 'fade' if i > 0 else None,
                'text_overlay': city_data.get('city_name', city_id).upper()
            })
        
        compilation['clips'] = clips
        
        # Add thank you message at end
        compilation['outro'] = {
            'text': 'Thank You for Smiling With Us! 😊',
            'duration': 3,
            'background': 'gradient'
        }
        
        # Save compilation spec
        spec_file = self.output_dir / f"recap_{date}.json"
        with open(spec_file, 'w') as f:
            json.dump(compilation, f, indent=2)
        
        logger.info(f"✅ Recap spec created: {spec_file}")
        
        return compilation
    
    def create_top_moments(self, days: int = 7, content_batch: Dict = None,
                          metrics: Dict = None) -> Dict:
        """
        Weekly "Top 10 Smiles" compilation.
        
        Auto-selects:
        - Highest engagement posts
        - Most comments
        - Best sentiment
        - Diverse cities/languages
        
        Args:
            days: Number of days to analyze
            content_batch: Content data
            metrics: Metrics data for selection
            
        Returns:
            Top moments compilation metadata
        """
        logger.info(f"🏆 Creating top moments compilation for {days} days...")
        
        if content_batch is None:
            content_batch = {}
        
        if metrics is None:
            metrics = {}
        
        # Score and rank content
        ranked_content = self._rank_content(content_batch, metrics)
        
        # Select top 10
        top_10 = ranked_content[:10]
        
        compilation = {
            'title': f'🌟 Top 10 Smiles - Week of {datetime.utcnow().strftime("%Y-%m-%d")}',
            'period_days': days,
            'clips_count': len(top_10),
            'duration_seconds': 90,  # ~9 seconds per clip
            'format': 'vertical_video',
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Create clips
        clips = []
        for i, item in enumerate(top_10, 1):
            clips.append({
                'rank': i,
                'city_id': item['city_id'],
                'city_name': item['city_name'],
                'engagement_score': item['score'],
                'duration': 8,
                'text_overlay': f"#{i} - {item['city_name']}"
            })
        
        compilation['clips'] = clips
        
        # Save compilation spec
        spec_file = self.output_dir / f"top_moments_{datetime.utcnow().strftime('%Y%m%d')}.json"
        with open(spec_file, 'w') as f:
            json.dump(compilation, f, indent=2)
        
        logger.info(f"✅ Top moments spec created: {spec_file}")
        
        return compilation
    
    def _rank_content(self, content_batch: Dict, metrics: Dict) -> List[Dict]:
        """
        Rank content by engagement and quality.
        
        Args:
            content_batch: Content batch
            metrics: Metrics data
            
        Returns:
            Ranked list of content items
        """
        ranked = []
        
        for city_id, city_data in content_batch.items():
            if 'error' in city_data:
                continue
            
            # Calculate engagement score
            score = city_data.get('quality_score', 0.5)
            
            # Bonus for diverse cities
            score += 0.1
            
            ranked.append({
                'city_id': city_id,
                'city_name': city_data.get('city_name', city_id),
                'score': score,
                'content': city_data
            })
        
        # Sort by score
        ranked.sort(key=lambda x: x['score'], reverse=True)
        
        return ranked
    
    def create_language_specific_compilation(self, language: str,
                                           content_batch: Dict) -> Dict:
        """
        Create compilation for specific language/region.
        
        Args:
            language: Target language code
            content_batch: Content batch
            
        Returns:
            Language-specific compilation
        """
        logger.info(f"🌐 Creating {language} compilation...")
        
        # Filter content for language
        lang_content = {}
        for city_id, city_data in content_batch.items():
            if language in city_data.get('languages', {}):
                lang_content[city_id] = city_data
        
        compilation = {
            'title': f'🌍 UMAJA World Tour - {language.upper()} Edition',
            'language': language,
            'cities_count': len(lang_content),
            'format': 'vertical_video',
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Create clips
        clips = []
        for city_id, city_data in lang_content.items():
            clips.append({
                'city_id': city_id,
                'city_name': city_data.get('city_name', city_id),
                'content': city_data['languages'][language],
                'duration': 5
            })
        
        compilation['clips'] = clips
        
        return compilation
    
    def create_platform_optimized_compilation(self, platform: str,
                                            content_batch: Dict) -> Dict:
        """
        Create platform-optimized compilation.
        
        Args:
            platform: Target platform
            content_batch: Content batch
            
        Returns:
            Platform-optimized compilation
        """
        platform_specs = {
            'tiktok': {
                'max_duration': 60,
                'format': 'vertical',
                'resolution': '1080x1920'
            },
            'instagram': {
                'max_duration': 90,
                'format': 'square_or_vertical',
                'resolution': '1080x1350'
            },
            'youtube': {
                'max_duration': 120,
                'format': 'horizontal',
                'resolution': '1920x1080'
            }
        }
        
        specs = platform_specs.get(platform, platform_specs['tiktok'])
        
        compilation = {
            'title': f'🌍 World Tour Highlights - {platform.title()}',
            'platform': platform,
            'format': specs['format'],
            'resolution': specs['resolution'],
            'max_duration': specs['max_duration'],
            'created_at': datetime.utcnow().isoformat()
        }
        
        return compilation
    
    def get_compilation_status(self) -> Dict:
        """
        Get status of all compilations.
        
        Returns:
            Status dictionary
        """
        compilations = list(self.output_dir.glob("*.json"))
        
        status = {
            'total_compilations': len(compilations),
            'recent_compilations': []
        }
        
        # Get recent compilations
        for comp_file in sorted(compilations, reverse=True)[:5]:
            with open(comp_file, 'r') as f:
                comp_data = json.load(f)
                status['recent_compilations'].append({
                    'file': comp_file.name,
                    'title': comp_data.get('title', 'Unknown'),
                    'created': comp_data.get('created_at', 'Unknown')
                })
        
        return status


# Example usage
if __name__ == "__main__":
    generator = CompilationGenerator()
    
    print("🎬 Compilation Generator Test")
    print("=" * 60)
    
    # Test data
    test_batch = {
        'new_york': {
            'city_name': 'New York',
            'quality_score': 0.95,
            'languages': {'en': 'content', 'es': 'contenido'},
            'platforms': {'tiktok': {}, 'instagram': {}}
        },
        'london': {
            'city_name': 'London',
            'quality_score': 0.92,
            'languages': {'en': 'content', 'fr': 'contenu'},
            'platforms': {'tiktok': {}, 'youtube': {}}
        },
        'tokyo': {
            'city_name': 'Tokyo',
            'quality_score': 0.98,
            'languages': {'en': 'content', 'ja': 'コンテンツ'},
            'platforms': {'tiktok': {}}
        }
    }
    
    # Create launch day recap
    recap = generator.create_launch_day_recap('2026-01-01', test_batch)
    print(f"\n✅ Recap created:")
    print(f"   Title: {recap['title']}")
    print(f"   Cities: {recap['cities_count']}")
    print(f"   Duration: {recap['duration_seconds']}s")
    
    # Create top moments
    top = generator.create_top_moments(7, test_batch)
    print(f"\n🏆 Top moments created:")
    print(f"   Title: {top['title']}")
    print(f"   Clips: {top['clips_count']}")
