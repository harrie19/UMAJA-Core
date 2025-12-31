"""Platform Exporter - Multi-Platform Content Export

Format content for different social media platforms with language support.
"""

from typing import Dict, List
import json


class PlatformExporter:
    """Export content for various social media platforms"""
    
    def __init__(self):
        """Initialize platform exporter with platform specifications"""
        
        self.platform_specs = {
            'tiktok': {
                'name': 'TikTok',
                'video_aspect_ratio': '9:16',
                'max_caption_length': 2200,
                'max_hashtags': 30,
                'subtitle_style': 'burned-in',
                'optimal_duration': 30
            },
            'instagram': {
                'name': 'Instagram Reels',
                'video_aspect_ratio': '9:16',
                'max_caption_length': 2200,
                'max_hashtags': 30,
                'subtitle_style': 'burned-in',
                'optimal_duration': 30
            },
            'youtube': {
                'name': 'YouTube Shorts',
                'video_aspect_ratio': '9:16',
                'max_caption_length': 5000,
                'max_hashtags': 15,
                'subtitle_style': 'separate-track',
                'optimal_duration': 60
            }
        }
    
    def export_for_tiktok(self, content: Dict, language: str) -> Dict:
        """Format content for TikTok with:
        - Burned-in subtitles
        - Hashtags optimized for region
        - Caption with translation
        - Aspect ratio 9:16
        
        Args:
            content: Translated content dictionary
            language: Language code
            
        Returns:
            Dictionary with TikTok-formatted content
        """
        specs = self.platform_specs['tiktok']
        
        # Format caption with text and hashtags
        text = content.get('text', '')
        hashtags = content.get('hashtags', [])
        
        # Ensure we don't exceed max hashtags
        hashtags = hashtags[:specs['max_hashtags']]
        
        # Build caption
        caption = text
        if hashtags:
            caption += '\n\n' + ' '.join(hashtags)
        
        # Truncate if needed
        if len(caption) > specs['max_caption_length']:
            caption = caption[:specs['max_caption_length'] - 3] + '...'
        
        return {
            'platform': 'TikTok',
            'language': language,
            'caption': caption,
            'text': text,
            'hashtags': hashtags,
            'video_specs': {
                'aspect_ratio': specs['video_aspect_ratio'],
                'duration': specs['optimal_duration'],
                'subtitle_style': specs['subtitle_style']
            },
            'metadata': content.get('metadata', {})
        }
    
    def export_for_instagram(self, content: Dict, language: str) -> Dict:
        """Format content for Instagram Reels
        
        Args:
            content: Translated content dictionary
            language: Language code
            
        Returns:
            Dictionary with Instagram-formatted content
        """
        specs = self.platform_specs['instagram']
        
        # Format caption with text and hashtags
        text = content.get('text', '')
        hashtags = content.get('hashtags', [])
        
        # Ensure we don't exceed max hashtags
        hashtags = hashtags[:specs['max_hashtags']]
        
        # Build caption
        caption = text
        if hashtags:
            caption += '\n\n' + ' '.join(hashtags)
        
        # Truncate if needed
        if len(caption) > specs['max_caption_length']:
            caption = caption[:specs['max_caption_length'] - 3] + '...'
        
        return {
            'platform': 'Instagram Reels',
            'language': language,
            'caption': caption,
            'text': text,
            'hashtags': hashtags,
            'video_specs': {
                'aspect_ratio': specs['video_aspect_ratio'],
                'duration': specs['optimal_duration'],
                'subtitle_style': specs['subtitle_style']
            },
            'metadata': content.get('metadata', {})
        }
    
    def export_for_youtube(self, content: Dict, language: str) -> Dict:
        """Format content for YouTube Shorts with:
        - Separate subtitle track (SRT)
        - Localized title and description
        - Tags in target language
        
        Args:
            content: Translated content dictionary
            language: Language code
            
        Returns:
            Dictionary with YouTube-formatted content
        """
        specs = self.platform_specs['youtube']
        
        # Format description with text
        text = content.get('text', '')
        hashtags = content.get('hashtags', [])
        metadata = content.get('metadata', {})
        
        # Ensure we don't exceed max hashtags
        hashtags = hashtags[:specs['max_hashtags']]
        
        # Build title (short, engaging)
        personality = metadata.get('personality', 'Daily Smile')
        title = f"{personality} - Daily Smile"
        
        # Build description
        description = text
        if hashtags:
            description += '\n\n' + ' '.join(hashtags)
        
        description += '\n\n---\n'
        description += 'Generated by UMAJA-Core\n'
        description += 'Mission: Put smiles on faces 😊\n'
        
        # Truncate if needed
        if len(description) > specs['max_caption_length']:
            description = description[:specs['max_caption_length'] - 3] + '...'
        
        # Extract tags (without # symbol)
        tags = [tag.replace('#', '') for tag in hashtags]
        
        return {
            'platform': 'YouTube Shorts',
            'language': language,
            'title': title,
            'description': description,
            'text': text,
            'hashtags': hashtags,
            'tags': tags,
            'video_specs': {
                'aspect_ratio': specs['video_aspect_ratio'],
                'duration': specs['optimal_duration'],
                'subtitle_style': specs['subtitle_style']
            },
            'metadata': metadata
        }
    
    def export_all_platforms(self, content: Dict, language: str) -> Dict[str, Dict]:
        """Export content for all supported platforms
        
        Args:
            content: Translated content dictionary
            language: Language code
            
        Returns:
            Dictionary with platform names as keys and formatted content as values
        """
        return {
            'tiktok': self.export_for_tiktok(content, language),
            'instagram': self.export_for_instagram(content, language),
            'youtube': self.export_for_youtube(content, language)
        }
    
    def get_platform_specs(self, platform: str) -> Dict:
        """Get specifications for a specific platform
        
        Args:
            platform: Platform name ('tiktok', 'instagram', 'youtube')
            
        Returns:
            Dictionary with platform specifications
        """
        return self.platform_specs.get(platform.lower(), {})
    
    def export_to_json(self, export_data: Dict, filepath: str = None) -> str:
        """Export data to JSON format
        
        Args:
            export_data: Data to export
            filepath: Optional file path to save JSON
            
        Returns:
            JSON string
        """
        json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_str)
        
        return json_str
