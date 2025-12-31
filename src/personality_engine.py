"""
UMAJA WORLDTOUR - Personality Engine
Generates friendly, warm content in distinct personality archetypes
"""

import random
from typing import Dict, List, Literal
import numpy as np


class PersonalityEngine:
    """
    Generates text in friendly personality archetypes designed to bring smiles.
    No impersonations - just warm, relatable characters.
    """
    
    PERSONALITIES = ['the_professor', 'the_worrier', 'the_enthusiast']
    
    def __init__(self):
        """Initialize the personality engine with templates and markers."""
        self.personality_templates = {
            'the_professor': {
                'name': 'The Professor',
                'description': 'Curious academic who studies everyday life',
                'tone': 'Friendly, inquisitive, slightly naive',
                'style': 'Asks innocent questions, finds wonder in mundane',
                'voice_desc': 'Warm, thoughtful, curious',
                'opening_templates': [
                    "I've been studying {} for exactly 3 days now...",
                    "According to my research, {} is fascinating because...",
                    "You know what surprises me about {}?",
                    "In my observations of {}, I've noticed...",
                    "The interesting thing about {} that nobody mentions...",
                    "After careful consideration, {} turns out to be...",
                    "My field notes on {} reveal something wonderful...",
                    "Here's what I learned about {} this week..."
                ],
                'continuation_phrases': [
                    "which made me wonder about everyday life",
                    "and that's what makes it so charming",
                    "in the most delightful way",
                    "which brings a smile to my face",
                    "and I find that genuinely fascinating",
                    "which teaches us something about ourselves",
                    "in ways I never expected",
                    "and that's the beauty of it"
                ],
                'catchphrases': [
                    "Fascinating!",
                    "How wonderful!",
                    "That's curious!",
                    "I wonder...",
                    "How delightful!",
                    "That's amazing!"
                ],
                'humor_markers': [
                    "innocent curiosity",
                    "warm observations",
                    "finding wonder in mundane"
                ]
            },
            'the_worrier': {
                'name': 'The Worrier',
                'description': 'Lovably anxious overthinker',
                'tone': 'Cautious, considerate, endearingly paranoid',
                'style': 'Finds "concerns" everywhere, but charming about it',
                'voice_desc': 'Gentle, concerned, caring',
                'opening_templates': [
                    "Okay but what if {} is actually dangerous?",
                    "I've been worrying about {} for hours...",
                    "Does anyone else get nervous about {}?",
                    "Can we talk about the risks of {}?",
                    "I'm probably overthinking {}, but...",
                    "Something about {} keeps me up at night...",
                    "Is it just me, or is {} concerning?",
                    "I need to share my concerns about {}..."
                ],
                'continuation_phrases': [
                    "but in a caring way",
                    "because I want everyone to be safe",
                    "though I might be overthinking it",
                    "but that's what friends do, right?",
                    "because preparation is important",
                    "though hopefully I'm wrong",
                    "but better safe than sorry",
                    "and I just want people to be aware"
                ],
                'catchphrases': [
                    "Just to be safe...",
                    "I worry about this...",
                    "We should be careful...",
                    "Does that concern anyone else?",
                    "Maybe I'm paranoid, but...",
                    "Let's think this through..."
                ],
                'humor_markers': [
                    "lovable anxiety",
                    "caring overthinking",
                    "endearing caution"
                ]
            },
            'the_enthusiast': {
                'name': 'The Enthusiast',
                'description': 'Eternally optimistic cheerleader',
                'tone': 'Warm, excited, unconditionally positive',
                'style': 'Finds joy in everything, infectious positivity',
                'voice_desc': 'Bright, energetic, joyful',
                'opening_templates': [
                    "Can we talk about how AMAZING {} is?!",
                    "{} might just be the best thing ever!",
                    "Okay so {} just made my entire day!",
                    "I'm SO excited to tell you about {}!",
                    "{} brings me pure joy and here's why...",
                    "You know what's absolutely wonderful? {}!",
                    "I can't stop thinking about how great {} is!",
                    "Let me share why {} is fantastic..."
                ],
                'continuation_phrases': [
                    "and that makes life beautiful",
                    "which fills my heart with joy",
                    "and I just love that so much",
                    "which is why I'm smiling right now",
                    "and that's the best part",
                    "which makes everything better",
                    "and I'm so grateful for it",
                    "which is simply wonderful"
                ],
                'catchphrases': [
                    "How amazing!",
                    "I love it!",
                    "That's wonderful!",
                    "So exciting!",
                    "Best thing ever!",
                    "Pure joy!"
                ],
                'humor_markers': [
                    "infectious positivity",
                    "genuine enthusiasm",
                    "finding joy everywhere"
                ]
            }
        }
        
        # Add smile templates for community-focused content
        self.SMILE_TEMPLATES = {
            'the_professor': {
                'opening': lambda topic: f"I've been studying {topic} for exactly 3 days now..."
            },
            'the_worrier': {
                'opening': lambda topic: f"Okay but what if {topic} is actually dangerous?"
            },
            'the_enthusiast': {
                'opening': lambda topic: f"Can we talk about how AMAZING {topic} is?!"
            }
        }
        
        # Topic-specific comedy angles
        self.comedy_angles = {
            'food': ['taste', 'preparation', 'cultural significance', 'eating etiquette'],
            'city': ['traffic', 'people', 'architecture', 'stereotypes', 'weather'],
            'culture': ['traditions', 'language', 'social norms', 'history'],
            'technology': ['complexity', 'user experience', 'evolution', 'absurdity'],
            'travel': ['airports', 'tourists', 'language barriers', 'cultural shocks']
        }
    
    def load_personality_templates(self, personality: str) -> Dict:
        """
        Load templates for a specific personality.
        
        Args:
            personality: One of 'the_professor', 'the_worrier', 'the_enthusiast'
            
        Returns:
            Dictionary of templates and markers
        """
        if personality not in self.PERSONALITIES:
            raise ValueError(f"Unknown personality: {personality}. Must be one of {self.PERSONALITIES}")
        
        return self.personality_templates[personality]
    
    def inject_personality_markers(self, text: str, personality: str, intensity: float = 0.7) -> str:
        """
        Inject personality-specific markers, catchphrases, and humor patterns.
        
        Args:
            text: Base text to enhance
            personality: Personality to apply
            intensity: How strongly to apply markers (0.0 to 1.0)
            
        Returns:
            Text enhanced with personality markers
        """
        templates = self.load_personality_templates(personality)
        
        # Split into sentences
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        enhanced_sentences = []
        
        for i, sentence in enumerate(sentences):
            enhanced = sentence
            
            # Add catchphrases randomly based on intensity
            if random.random() < intensity * 0.3 and i > 0:
                catchphrase = random.choice(templates['catchphrases'])
                enhanced = f"{catchphrase} {enhanced}"
            
            # Add continuation phrases
            if random.random() < intensity * 0.4 and i > 0:
                continuation = random.choice(templates['continuation_phrases'])
                enhanced = f"{enhanced}, {continuation}"
            
            enhanced_sentences.append(enhanced)
        
        # Join back together
        result = '. '.join(enhanced_sentences)
        if not result.endswith('.'):
            result += '.'
        
        return result
    
    def _generate_professor_text(self, topic: str, length: int, intensity: float) -> str:
        """Generate text in The Professor style."""
        templates = self.personality_templates['the_professor']
        
        # Opening
        opening = random.choice(templates['opening_templates']).format(topic)
        
        # Build paragraphs with curious observations
        paragraphs = [opening]
        current_length = len(opening.split())
        
        observations = [
            f"What strikes me most about {topic} is how universal it feels",
            f"Every time I explore {topic}, I discover something new and charming",
            f"The lovely thing about {topic} is how it connects people",
            f"In studying {topic}, I've found so many reasons to smile",
            f"There's something wonderfully human about {topic}",
            f"The beauty of {topic} lies in its everyday magic"
        ]
        
        while current_length < length:
            if random.random() < intensity:
                obs = random.choice(observations)
                continuation = random.choice(templates['continuation_phrases'])
                sentence = f"{obs}, {continuation}."
            else:
                sentence = f"The more I learn about {topic}, the more I appreciate its simple joys."
            
            paragraphs.append(sentence)
            current_length += len(sentence.split())
        
        text = ' '.join(paragraphs)
        return self.inject_personality_markers(text, 'the_professor', intensity)
    
    def _generate_worrier_text(self, topic: str, length: int, intensity: float) -> str:
        """Generate text in The Worrier style."""
        templates = self.personality_templates['the_worrier']
        
        # Opening
        opening = random.choice(templates['opening_templates']).format(topic)
        
        paragraphs = [opening]
        current_length = len(opening.split())
        
        observations = [
            f"I just want everyone to enjoy {topic} safely",
            f"Has anyone else thought deeply about {topic}? Just checking!",
            f"Maybe I'm overthinking {topic}, but I care about the details",
            f"I've prepared a mental checklist for {topic}, in case it helps",
            f"The thing about {topic} is we should approach it thoughtfully",
            f"I know I worry too much about {topic}, but that's who I am"
        ]
        
        while current_length < length:
            if random.random() < intensity:
                obs = random.choice(observations)
                continuation = random.choice(templates['continuation_phrases'])
                sentence = f"{obs}, {continuation}."
            else:
                sentence = f"Just want to make sure everyone's thinking about {topic} carefully!"
            
            paragraphs.append(sentence)
            current_length += len(sentence.split())
        
        text = ' '.join(paragraphs)
        return self.inject_personality_markers(text, 'the_worrier', intensity)
    
    def _generate_enthusiast_text(self, topic: str, length: int, intensity: float) -> str:
        """Generate text in The Enthusiast style."""
        templates = self.personality_templates['the_enthusiast']
        
        # Opening with energy
        opening = random.choice(templates['opening_templates']).format(topic)
        
        paragraphs = [opening]
        current_length = len(opening.split())
        
        # Enthusiastic observations
        observations = [
            f"Every single thing about {topic} brings me happiness!",
            f"I could talk about {topic} for hours because it's just that wonderful!",
            f"The world needs more {topic} - it's pure positivity!",
            f"{topic} reminds me why life is so amazing!",
            f"Honestly, {topic} is one of my favorite things ever!",
            f"I get so excited just thinking about {topic}!"
        ]
        
        while current_length < length:
            if random.random() < intensity:
                obs = random.choice(observations)
                continuation = random.choice(templates['continuation_phrases'])
                sentence = f"{obs} {continuation}!"
            else:
                sentence = f"And that's what makes {topic} so incredibly special!"
            
            paragraphs.append(sentence)
            current_length += len(sentence.split())
        
        text = ' '.join(paragraphs)
        return self.inject_personality_markers(text, 'the_enthusiast', intensity)
    
    def generate_text(self, 
                     topic: str,
                     personality: Literal['the_professor', 'the_worrier', 'the_enthusiast'],
                     length: Literal['short', 'medium', 'long'] = 'medium',
                     style_intensity: float = 0.7) -> Dict:
        """
        Generate text in a specific friendly personality style.
        
        Args:
            topic: Topic to write about
            personality: Personality archetype to use
            length: Text length - 'short' (50-100 words), 'medium' (150-250), 'long' (300-500)
            style_intensity: How strongly to apply personality (0.0 to 1.0)
            
        Returns:
            Dictionary containing:
                - text: Generated text
                - personality: Personality used
                - word_count: Number of words
                - style_intensity: Intensity applied
                - humor_markers: List of humor techniques used
        """
        # Validate inputs
        if personality not in self.PERSONALITIES:
            raise ValueError(f"Unknown personality: {personality}")
        
        if length not in ['short', 'medium', 'long']:
            raise ValueError("Length must be 'short', 'medium', or 'long'")
        
        style_intensity = max(0.0, min(1.0, style_intensity))
        
        # Determine target word count
        length_ranges = {
            'short': (50, 100),
            'medium': (150, 250),
            'long': (300, 500)
        }
        target_min, target_max = length_ranges[length]
        target_words = random.randint(target_min, target_max)
        
        # Generate text based on personality
        if personality == 'the_professor':
            text = self._generate_professor_text(topic, target_words, style_intensity)
        elif personality == 'the_worrier':
            text = self._generate_worrier_text(topic, target_words, style_intensity)
        else:  # the_enthusiast
            text = self._generate_enthusiast_text(topic, target_words, style_intensity)
        
        # Get humor markers
        templates = self.personality_templates[personality]
        
        return {
            'text': text,
            'personality': personality,
            'topic': topic,
            'word_count': len(text.split()),
            'style_intensity': style_intensity,
            'humor_markers': templates['humor_markers'],
            'voice_description': templates['voice_desc']
        }
    
    def generate_smile_text(self, city: str, topic: str, 
                           personality: str, length: str = 'micro') -> str:
        """
        Generate short, friendly, smile-inducing text
        
        Rules:
        - 30-60 seconds when spoken (75-150 words for 'micro')
        - Warm, not edgy
        - Relatable, not performative
        - Inclusive, not divisive
        - Ends with community question
        
        Args:
            city: City name
            topic: Topic to discuss
            personality: Personality to use
            length: 'micro' (30-60 sec), 'short' (60-90 sec)
            
        Returns:
            Smile-inducing text ready for posting
        """
        if personality not in self.PERSONALITIES:
            raise ValueError(f"Unknown personality: {personality}")
        
        # Determine word count based on length
        # 150 words per minute speaking rate = 2.5 words per second
        # 30-60 seconds = 75-150 words
        length_ranges = {
            'micro': (75, 150),
            'short': (150, 225)
        }
        target_min, target_max = length_ranges.get(length, (75, 150))
        target_words = random.randint(target_min, target_max)
        
        # Use lower intensity for friendlier, less extreme content
        intensity = 0.6
        
        # Generate observation
        observation = self._generate_observation(city, topic, personality)
        
        # Generate relatable comparison
        comparison = self._generate_comparison(topic, personality)
        
        # Get opening template
        template = self.personality_templates[personality]
        opening = random.choice(template['opening_templates']).format(topic)
        
        # Construct smile
        smile = f"🌍 Daily Smile from {city}!\n\n{opening}\n\n{observation}\n\n{comparison}"
        
        # Trim if too long
        words = smile.split()
        if len(words) > target_max:
            smile = ' '.join(words[:target_max]) + '...'
        
        return smile.strip()
    
    def _generate_observation(self, city: str, topic: str, personality: str) -> str:
        """Generate a warm observation about a topic in a city."""
        observations = {
            'the_professor': [
                f"What fascinates me about {topic} in {city} is how it brings people together.",
                f"I've noticed that {topic} here has a unique charm that makes everyone smile.",
                f"The wonderful thing about {city}'s {topic} is how welcoming it feels.",
                f"After studying {topic} in {city}, I've discovered it's full of delightful surprises."
            ],
            'the_worrier': [
                f"I want to make sure everyone experiences {topic} in {city} safely and happily!",
                f"I've been thinking about the best way to enjoy {topic} here, and I have some tips!",
                f"Does anyone else feel a bit overwhelmed by {city}'s {topic}? Let's help each other out!",
                f"I care about everyone having a good time with {topic} in {city}."
            ],
            'the_enthusiast': [
                f"{city}'s {topic} is absolutely INCREDIBLE and everyone needs to experience it!",
                f"I'm so excited about {topic} here - it's pure happiness!",
                f"The energy around {topic} in {city} is contagious and amazing!",
                f"I can't get enough of {city}'s {topic} - it's the best thing ever!"
            ]
        }
        return random.choice(observations[personality])
    
    def _generate_comparison(self, topic: str, personality: str) -> str:
        """Generate a relatable comparison."""
        comparisons = {
            'the_professor': [
                f"It reminds me that everyday life is full of wonder.",
                f"It's like discovering a new favorite book - you just want to share it.",
                f"Think of it as a small gift that brightens your day.",
                f"It's proof that simple pleasures are often the best."
            ],
            'the_worrier': [
                f"Just remember to take your time and enjoy it at your own pace!",
                f"It's okay to feel a bit nervous - we're all in this together!",
                f"I promise it's worth the initial worry - trust me on this!",
                f"Take care of yourself while exploring - that's what matters most!"
            ],
            'the_enthusiast': [
                f"It's like sunshine in everyday form - pure joy!",
                f"This is what happiness looks like, friends!",
                f"Life is too short not to celebrate wonderful things like this!",
                f"This is the kind of positivity we all need more of!"
            ]
        }
        return random.choice(comparisons[personality])
    
    def maintain_coherence(self, text: str, personality: str) -> str:
        """
        Check and improve coherence while maintaining humor.
        
        Args:
            text: Text to check
            personality: Personality style
            
        Returns:
            Improved text
        """
        # Basic coherence: ensure sentences flow logically
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        # Add transitions if needed
        templates = self.personality_templates[personality]
        improved = []
        
        for i, sentence in enumerate(sentences):
            if i > 0 and random.random() < 0.3:
                # Add a transition
                transitions = ['However', 'Nevertheless', 'Furthermore', 'Indeed', 'Naturally']
                sentence = f"{random.choice(transitions)}, {sentence.lower()}"
            improved.append(sentence)
        
        return '. '.join(improved) + '.'


# Example usage and testing
if __name__ == "__main__":
    engine = PersonalityEngine()
    
    # Test each personality
    for personality in ['the_professor', 'the_worrier', 'the_enthusiast']:
        print(f"\n{'='*60}")
        print(f"Testing {personality.upper().replace('_', ' ')}")
        print('='*60)
        
        result = engine.generate_text(
            topic="New York pizza",
            personality=personality,
            length='medium',
            style_intensity=0.8
        )
        
        print(f"\nTopic: {result['topic']}")
        print(f"Word Count: {result['word_count']}")
        print(f"Style Intensity: {result['style_intensity']}")
        print(f"Humor Markers: {', '.join(result['humor_markers'])}")
        print(f"\nGenerated Text:")
        print(result['text'])
    
    # Test smile generation
    print(f"\n{'='*60}")
    print("Testing Daily Smile Generation")
    print('='*60)
    
    for personality in ['the_professor', 'the_worrier', 'the_enthusiast']:
        smile = engine.generate_smile_text(
            city="Tokyo",
            topic="sushi",
            personality=personality,
            length='micro'
        )
        print(f"\n{personality}:")
        print(smile)
