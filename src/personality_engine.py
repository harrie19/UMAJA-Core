"""Personality Engine - Friendly Archetypes for Daily Smiles

Transformed from comedian impersonations to warm, friendly personality archetypes
that focus on putting smiles on faces through community engagement.
"""

import random
from typing import Dict, List


class PersonalityArchetype:
    """Base class for friendly personality archetypes"""
    
    def __init__(self, name: str, traits: List[str], tone: str):
        self.name = name
        self.traits = traits
        self.tone = tone
    
    def generate_smile_text(self, topic: str = None) -> str:
        """Generate 30-60 second friendly content to put smiles on faces"""
        raise NotImplementedError


class TheProfessor(PersonalityArchetype):
    """The Professor - Curious, thoughtful, loves sharing interesting facts"""
    
    def __init__(self):
        super().__init__(
            name="The Professor",
            traits=["curious", "thoughtful", "educational", "warm"],
            tone="friendly and informative"
        )
    
    def generate_smile_text(self, topic: str = None) -> str:
        """Generate friendly, interesting content that makes people smile with knowledge"""
        openers = [
            "Here's something fascinating that might brighten your day!",
            "Let me share a delightful little fact with you...",
            "You know what's wonderfully interesting?",
            "I just learned something that made me smile, and I think you'll love it too!"
        ]
        
        facts = [
            "Sea otters hold hands while they sleep so they don't drift apart. They're nature's reminder to stay connected!",
            "Cows have best friends and get stressed when they're separated. Even in nature, friendship matters!",
            "A group of flamingos is called a 'flamboyance'. How perfect is that?",
            "Penguins propose to their mates with pebbles. Romance exists in the animal kingdom too!"
        ]
        
        closers = [
            "Isn't that wonderful? What little fact makes you smile today?",
            "Nature has such delightful surprises! What's something that fascinated you recently?",
            "I hope that brought a smile to your face! Share your favorite fun fact with us!"
        ]
        
        return f"{random.choice(openers)} {random.choice(facts)} {random.choice(closers)}"


class TheWorrier(PersonalityArchetype):
    """The Worrier - Anxious but caring, relatable, finds humor in everyday concerns"""
    
    def __init__(self):
        super().__init__(
            name="The Worrier",
            traits=["relatable", "caring", "authentic", "humorous"],
            tone="warm and understanding"
        )
    
    def generate_smile_text(self, topic: str = None) -> str:
        """Generate relatable content about everyday worries that make people smile and feel less alone"""
        openers = [
            "Can we talk about something we all worry about?",
            "Is it just me, or does anyone else...",
            "Let's be honest about our quirky worries for a moment...",
            "Here's a little worry we can all laugh about together:"
        ]
        
        scenarios = [
            "send a text and immediately reread it 47 times wondering if the punctuation made you sound angry? Just me? We're all in this together!",
            "triple-check that the door is locked, then check again 'just to be sure'? Your home is definitely secure, friend!",
            "practice conversations in your head that will never happen? Turns out, we're all doing this!",
            "wonder if people can hear your stomach growling from across the room? Spoiler: they probably can't, and if they can, they get it!"
        ]
        
        closers = [
            "What's your most relatable worry? Let's smile about our quirks together!",
            "Share your funny worry in the comments - you're not alone!",
            "We're all wonderfully imperfect together. What makes you smile about being human?"
        ]
        
        return f"{random.choice(openers)} {random.choice(scenarios)} {random.choice(closers)}"


class TheEnthusiast(PersonalityArchetype):
    """The Enthusiast - Energetic, joyful, finds excitement in everything"""
    
    def __init__(self):
        super().__init__(
            name="The Enthusiast",
            traits=["energetic", "joyful", "optimistic", "uplifting"],
            tone="warm and encouraging"
        )
    
    def generate_smile_text(self, topic: str = None) -> str:
        """Generate uplifting, joyful content that spreads smiles and positive energy"""
        openers = [
            "Friends! Let's celebrate something wonderful today!",
            "Can we take a moment to appreciate something amazing?",
            "I'm so excited to share this joy with you all!",
            "Here's something that absolutely fills my heart with happiness!"
        ]
        
        celebrations = [
            "Every single day, someone learns to ride a bike for the first time. Every. Single. Day. How magical is that?",
            "Right now, somewhere in the world, someone just laughed so hard they snorted. And that made someone else laugh even harder!",
            "Today, thousands of people will pet a dog and that dog's tail will wag with pure joy. We're living in a beautiful world!",
            "At this very moment, someone is getting a warm hug they really needed. Connection is everywhere!"
        ]
        
        closers = [
            "What small joy made you smile today? I want to celebrate with you!",
            "Share your moment of happiness below - let's spread the smiles!",
            "Tell us what brings you joy today! Your smile matters!"
        ]
        
        return f"{random.choice(openers)} {random.choice(celebrations)} {random.choice(closers)}"


class PersonalityEngine:
    """Manages friendly personality archetypes for community engagement"""
    
    def __init__(self):
        self.archetypes = {
            "professor": TheProfessor(),
            "worrier": TheWorrier(),
            "enthusiast": TheEnthusiast()
        }
    
    def get_archetype(self, archetype_name: str) -> PersonalityArchetype:
        """Get a specific personality archetype"""
        return self.archetypes.get(archetype_name.lower())
    
    def get_random_archetype(self) -> PersonalityArchetype:
        """Get a random personality archetype"""
        return random.choice(list(self.archetypes.values()))
    
    def generate_daily_smile(self, archetype_name: str = None) -> Dict[str, str]:
        """Generate a Daily Smile post with community engagement
        
        Args:
            archetype_name: Optional specific archetype, or random if None
            
        Returns:
            Dictionary with 'personality', 'content', and 'tone' keys
        """
        archetype = self.get_archetype(archetype_name) if archetype_name else self.get_random_archetype()
        
        return {
            "personality": archetype.name,
            "content": archetype.generate_smile_text(),
            "tone": archetype.tone,
            "traits": ", ".join(archetype.traits)
        }
    
    def generate_global_smile(self, archetype_name: str = None, languages: List[str] = None) -> Dict:
        """Generate smile in multiple languages at once
        
        Args:
            archetype_name: Optional specific archetype, or random if None
            languages: List of language codes to generate, or None for all supported
            
        Returns:
            {
                'original': {...},  # English version
                'translations': {
                    'es': {...},
                    'hi': {...},
                    ...
                }
            }
        """
        # Import here to avoid circular dependency
        try:
            from global_translator import GlobalTranslator
        except ImportError:
            raise ImportError("GlobalTranslator not available. Install required packages.")
        
        # Generate original English smile
        original = self.generate_daily_smile(archetype_name)
        
        # Translate to other languages
        translator = GlobalTranslator()
        translations = translator.translate_smile(original, languages)
        
        # Separate English original from other translations
        english = translations.pop('en', original)
        
        return {
            'original': english,
            'translations': translations
        }
