"""
UMAJA WORLDTOUR - Personality Engine
Generates text in specific comedian styles (John Cleese, C-3PO, Robin Williams)
"""

import random
from typing import Dict, List, Literal
import numpy as np


class PersonalityEngine:
    """
    Generates text in specific comedian styles with personality markers,
    catchphrases, and humor patterns.
    """
    
    PERSONALITIES = ['john_cleese', 'c3po', 'robin_williams']
    
    def __init__(self):
        """Initialize the personality engine with templates and markers."""
        self.personality_templates = {
            'john_cleese': {
                'style': 'Dry British wit, Monty Python humor',
                'voice_desc': 'Deep, measured, sarcastic',
                'opening_templates': [
                    "Now, the curious thing about {}...",
                    "Rather like the British railway system, {}...",
                    "You see, what most people don't realize about {} is...",
                    "If I may be so bold as to observe, {}...",
                    "In my considerable experience with {}, I've found...",
                    "It's rather peculiar how {}...",
                    "One might reasonably argue that {}...",
                    "The essential absurdity of {} becomes clear when..."
                ],
                'continuation_phrases': [
                    "which is, of course, perfectly ridiculous",
                    "much like a confused penguin at a tea party",
                    "rather reminiscent of a Ministry meeting",
                    "not unlike the Spanish Inquisition",
                    "which nobody expects, naturally",
                    "in the most British way possible",
                    "with all the subtlety of a Flying Circus",
                    "as sensible as arguing with a parrot"
                ],
                'catchphrases': [
                    "Quite.",
                    "How perfectly absurd.",
                    "I see.",
                    "Splendid.",
                    "Marvelous.",
                    "How frightfully odd."
                ],
                'humor_markers': [
                    "ironic understatement",
                    "deadpan delivery",
                    "absurdist comparisons"
                ]
            },
            'c3po': {
                'style': 'Overly polite protocol droid, statistical obsession',
                'voice_desc': 'Higher pitch, robotic cadence, anxious',
                'opening_templates': [
                    "Oh my! {} presents precisely 2,479 possible interpretations...",
                    "By my calculations, {} exhibits {} probability factors...",
                    "Goodness gracious! According to my programming, {}...",
                    "I must inform you that {} has approximately {} variations...",
                    "Begging your pardon, but {} suggests {} outcomes...",
                    "How remarkable! My databanks indicate that {}...",
                    "Oh dear, oh dear! {} shows {} distinct patterns...",
                    "If I may be so presumptuous, {} registers {} on my sensors..."
                ],
                'continuation_phrases': [
                    "which corresponds to protocol section 7.2.4",
                    "according to my extensive linguistic databases",
                    "as documented in 6 million forms of communication",
                    "which my circuits find most perplexing",
                    "resulting in a 97.3% probability of confusion",
                    "creating exactly 1,458 potential misunderstandings",
                    "violating approximately 42 known protocols",
                    "causing my probability matrix to fluctuate wildly"
                ],
                'catchphrases': [
                    "Oh my!",
                    "We're doomed!",
                    "How rude!",
                    "I should be most grateful...",
                    "Goodness gracious!",
                    "Thank the Maker!"
                ],
                'humor_markers': [
                    "excessive politeness",
                    "unnecessary statistics",
                    "anxious observations"
                ]
            },
            'robin_williams': {
                'style': 'Energetic improv, rapid topic changes, warm',
                'voice_desc': 'Dynamic, varied pitch, lots of laughs',
                'opening_templates': [
                    "So {} walks into a bar... *laughs*",
                    "Imagine if {} was a Broadway musical!",
                    "You know what's crazy about {}? *voice changes*",
                    "Picture this: {} meets {}! *laughs*",
                    "So I'm thinking about {}, right? And suddenly...",
                    "Wait, wait, wait... {} is like if {} had a baby with {}!",
                    "Here's the thing about {}: *switches accent*",
                    "You ever notice how {}? *laughs* No? Just me?"
                ],
                'continuation_phrases': [
                    "*laughs* But seriously though...",
                    "*voice change* And then you've got...",
                    "*wild gesture* Picture this!",
                    "*sudden whisper* But here's the secret...",
                    "*explosive energy* Oh! Oh! And another thing!",
                    "*different accent* Now imagine...",
                    "*tender moment* But you know what's beautiful?",
                    "*back to comedy* BOOM! Plot twist!"
                ],
                'catchphrases': [
                    "*laughs*",
                    "Nanu nanu!",
                    "Good morning, Vietnam!",
                    "*switches voice*",
                    "Carpe diem!",
                    "*wild improvisation*"
                ],
                'humor_markers': [
                    "rapid-fire delivery",
                    "voice changes",
                    "warm humanity",
                    "improvisation"
                ]
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
            personality: One of 'john_cleese', 'c3po', 'robin_williams'
            
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
    
    def _generate_cleese_text(self, topic: str, length: int, intensity: float) -> str:
        """Generate text in John Cleese style."""
        templates = self.personality_templates['john_cleese']
        
        # Opening
        opening = random.choice(templates['opening_templates']).format(topic)
        
        # Build paragraphs with dry wit
        paragraphs = [opening]
        current_length = len(opening.split())
        
        observations = [
            f"One observes that {topic} exhibits all the charm of a wet Sunday in Basingstoke",
            f"The average person's understanding of {topic} rivals that of a confused hamster",
            f"If {topic} were a person, it would definitely wear a bowler hat. Badly",
            f"The Ministry of Silly Walks has officially classified {topic} as 'moderately absurd'",
            f"In my extensive research, {topic} proves to be as logical as a Monty Python sketch",
            f"The British approach to {topic} involves tea, queuing, and mild disappointment"
        ]
        
        while current_length < length:
            if random.random() < intensity:
                obs = random.choice(observations)
                continuation = random.choice(templates['continuation_phrases'])
                sentence = f"{obs}, {continuation}."
            else:
                sentence = f"Furthermore, one might observe that {topic} demonstrates remarkable similarities to other forms of organized chaos."
            
            paragraphs.append(sentence)
            current_length += len(sentence.split())
        
        text = ' '.join(paragraphs)
        return self.inject_personality_markers(text, 'john_cleese', intensity)
    
    def _generate_c3po_text(self, topic: str, length: int, intensity: float) -> str:
        """Generate text in C-3PO style."""
        templates = self.personality_templates['c3po']
        
        # Generate random statistics
        def random_stat():
            return random.randint(100, 9999)
        
        # Opening with statistics
        opening = random.choice(templates['opening_templates']).format(
            topic, 
            random_stat()
        )
        
        paragraphs = [opening]
        current_length = len(opening.split())
        
        observations = [
            f"My databanks reveal {random_stat()} entries related to {topic}, oh my!",
            f"According to protocol {random.randint(1,9)}.{random.randint(1,9)}.{random.randint(1,9)}, {topic} requires {random_stat()} steps",
            f"I calculate a {random.randint(60,99)}.{random.randint(1,9)}% probability that {topic} will cause confusion",
            f"Goodness! {topic} violates approximately {random_stat()} known communication protocols",
            f"My circuits indicate that {topic} presents {random_stat()} unique challenges, how distressing!",
            f"If I may be so bold, {topic} exhibits {random_stat()} characteristics worthy of analysis"
        ]
        
        while current_length < length:
            if random.random() < intensity:
                obs = random.choice(observations)
                continuation = random.choice(templates['continuation_phrases'])
                sentence = f"{obs}, {continuation}."
            else:
                sentence = f"Additionally, my programming suggests that {topic} warrants further computational analysis with {random_stat()} variables."
            
            paragraphs.append(sentence)
            current_length += len(sentence.split())
        
        text = ' '.join(paragraphs)
        return self.inject_personality_markers(text, 'c3po', intensity)
    
    def _generate_williams_text(self, topic: str, length: int, intensity: float) -> str:
        """Generate text in Robin Williams style."""
        templates = self.personality_templates['robin_williams']
        
        # Random combination topics for improvisation
        random_topics = ['Shakespeare', 'a food truck', 'your grandmother', 'a tech startup', 
                        'reality TV', 'a yoga class', 'quantum physics', 'a disco ball']
        
        # Opening with energy
        opening_template = random.choice(templates['opening_templates'])
        if '{}' in opening_template:
            # Count placeholders
            count = opening_template.count('{}')
            if count == 1:
                opening = opening_template.format(topic)
            elif count == 2:
                opening = opening_template.format(topic, random.choice(random_topics))
            else:
                opening = opening_template.format(topic, random.choice(random_topics), random.choice(random_topics))
        else:
            opening = opening_template.replace('{}', topic)
        
        paragraphs = [opening]
        current_length = len(opening.split())
        
        # High-energy improvisations
        improvisations = [
            f"*laughs* So {topic} is sitting there, right? And I'm thinking, this is EXACTLY like {random.choice(random_topics)}!",
            f"*voice changes* Now, if {topic} was a movie, it would star {random.choice(['Marlon Brando', 'Meryl Streep', 'a confused llama'])}",
            f"Picture this: {topic} meets {random.choice(random_topics)} at a party. *dramatic pause* CHAOS! Beautiful chaos!",
            f"*switches accent* You know what {topic} reminds me of? *laughs* Everything! And nothing! That's the beauty!",
            f"BOOM! *explosive energy* {topic} just became the most interesting thing since {random.choice(random_topics)} invented {random.choice(['sliced bread', 'the internet', 'confusion'])}!",
            f"*tender moment* But here's the thing about {topic}... *pause* ...it's human. It's beautiful. It's us."
        ]
        
        while current_length < length:
            if random.random() < intensity:
                improv = random.choice(improvisations)
                continuation = random.choice(templates['continuation_phrases'])
                sentence = f"{improv} {continuation}"
            else:
                sentence = f"And that's what makes {topic} so incredible - it's spontaneous, it's alive, it's *laughs* totally unpredictable!"
            
            paragraphs.append(sentence)
            current_length += len(sentence.split())
        
        text = ' '.join(paragraphs)
        return self.inject_personality_markers(text, 'robin_williams', intensity)
    
    def generate_text(self, 
                     topic: str,
                     personality: Literal['john_cleese', 'c3po', 'robin_williams'],
                     length: Literal['short', 'medium', 'long'] = 'medium',
                     style_intensity: float = 0.7) -> Dict:
        """
        Generate text in a specific comedian style.
        
        Args:
            topic: Topic to write about
            personality: Comedian personality to use
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
        if personality == 'john_cleese':
            text = self._generate_cleese_text(topic, target_words, style_intensity)
        elif personality == 'c3po':
            text = self._generate_c3po_text(topic, target_words, style_intensity)
        else:  # robin_williams
            text = self._generate_williams_text(topic, target_words, style_intensity)
        
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
    for personality in ['john_cleese', 'c3po', 'robin_williams']:
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
