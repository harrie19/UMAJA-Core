"""
Daily Smile World Tour Generator
Generates 60-second friendly content about cities
Goal: Make people smile, not perform stand-up
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.personality_engine import PersonalityEngine
from src.worldtour_manager import WorldtourManager
from src.voice_synthesizer import VoiceSynthesizer
import random


class DailySmileGenerator:
    def __init__(self):
        self.personality_engine = PersonalityEngine()
        self.worldtour = WorldtourManager()
        self.voice = None  # Initialize lazily if needed
        
    def generate_daily_smile(self) -> dict:
        """Generate today's smile content"""
        
        # Get next city
        city = self.worldtour.get_next_city()
        if not city:
            raise Exception("No unvisited cities available")
        
        # Rotate personalities daily
        personalities = ['the_professor', 'the_worrier', 'the_enthusiast']
        today_personality = personalities[self.worldtour.days_elapsed % 3]
        
        # Pick a topic from the city
        topic = random.choice(city['topics'])
        
        # Generate text (SHORT - 60 seconds max)
        text = self.personality_engine.generate_smile_text(
            city=city['name'],
            topic=topic,
            personality=today_personality,
            length='micro'  # 30-60 seconds only
        )
        
        # Add community question
        community_question = self.worldtour.get_community_question(city)
        text += f"\n\n{community_question}"
        
        # Generate audio (optional)
        audio_path = None
        try:
            if self.voice is None:
                self.voice = VoiceSynthesizer()
            audio = self.voice.synthesize(text, today_personality)
            audio_path = audio.get('audio_path')
        except Exception as e:
            print(f"Warning: Could not generate audio: {e}")
            audio_path = "audio_generation_skipped"
        
        return {
            'city': city,
            'personality': today_personality,
            'text': text,
            'audio_path': audio_path,
            'hashtags': [
                f"#DailySmileFrom{city['id'].title().replace('_', '')}",
                '#DailySmileWorldTour',
                '#TravelSmiles'
            ],
            'topic': topic
        }


if __name__ == '__main__':
    generator = DailySmileGenerator()
    smile = generator.generate_daily_smile()
    
    print(f"🌍 Today's Daily Smile: {smile['city']['name']}")
    print(f"🎭 Personality: {smile['personality']}")
    print(f"📝 Topic: {smile['topic']}")
    print(f"\n{smile['text']}")
    print(f"\n📱 Hashtags: {' '.join(smile['hashtags'])}")
    print(f"🎵 Audio: {smile['audio_path']}")
