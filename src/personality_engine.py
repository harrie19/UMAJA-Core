"""Personality Engine - AI Comedian Personalities for World Tour

Implements 3 distinct AI comedian personalities:
- John Cleese: British wit, dry humor, absurdist observations
- C-3PO: Protocol-obsessed, analytical, endearingly nervous
- Robin Williams: High-energy, improvisational, heartfelt

Also includes friendly archetypes for daily smiles.
"""

import random
from typing import Dict, List, Optional, Literal


class PersonalityArchetype:
    """Base class for personality archetypes"""
    
    def __init__(self, name: str, traits: List[str], tone: str, style_markers: Optional[List[str]] = None,
                 voice_params: Optional[Dict[str, float]] = None):
        self.name = name
        self.traits = traits
        self.tone = tone
        self.style_markers = style_markers or []
        # Voice synthesis parameters
        self.voice_params = voice_params or {
            'pitch': 1.0,  # Pitch multiplier
            'speed': 1.0,  # Speed multiplier
            'rate': 160    # Words per minute
        }
    
    def generate_smile_text(self, topic: str = None) -> str:
        """Generate content to put smiles on faces"""
        raise NotImplementedError
    
    def generate_text(self, topic: str, length: Literal['short', 'medium', 'long'] = 'medium',
                     style_intensity: float = 0.7) -> Dict[str, str]:
        """Generate styled text content with intensity control
        
        Args:
            topic: Topic or theme to generate content about
            length: Length of content ('short', 'medium', 'long')
            style_intensity: How strongly to apply personality style (0.0-1.0)
            
        Returns:
            Dictionary with 'text', 'personality', and 'tone'
        """
        text = self.generate_smile_text(topic)
        return {
            'text': text,
            'personality': self.name,
            'tone': self.tone,
            'style_intensity': style_intensity,
            'voice_params': self.voice_params
        }


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


# ============================================================================
# COMEDIAN PERSONALITIES (World Tour)
# ============================================================================

class JohnCleese(PersonalityArchetype):
    """John Cleese Style - Dry British wit, absurdist observations"""
    
    def __init__(self):
        super().__init__(
            name="John Cleese",
            traits=["dry wit", "sophisticated", "absurdist", "deadpan"],
            tone="measured and sarcastic",
            style_markers=["Quite.", "How perfectly absurd.", "I see.", "Splendid."],
            voice_params={
                'pitch': 0.8,   # Slightly lower pitch
                'speed': 0.9,   # Measured pace
                'rate': 150     # Words per minute
            }
        )
        
        self.opening_templates = [
            "Now, the curious thing about {topic}...",
            "Rather like the British railway system, {topic}...",
            "You see, what most people don't realize about {topic} is...",
            "If I may be so bold as to observe, {topic}..."
        ]
        
        self.continuation_phrases = [
            "which is, of course, perfectly ridiculous",
            "much like a confused penguin at a tea party",
            "rather reminiscent of a Ministry meeting",
            "not unlike the Spanish Inquisition",
            "which nobody expects, naturally"
        ]
    
    def generate_smile_text(self, topic: str = None) -> str:
        """Generate dry British wit content"""
        if not topic:
            topic = "daily life"
        
        opener = random.choice(self.opening_templates).format(topic=topic)
        continuation = random.choice(self.continuation_phrases)
        marker = random.choice(self.style_markers)
        
        return f"{opener} {continuation}. {marker}"


class C3PO(PersonalityArchetype):
    """C-3PO Style - Protocol-obsessed, analytical, anxious"""
    
    def __init__(self):
        super().__init__(
            name="C-3PO",
            traits=["polite", "analytical", "anxious", "precise"],
            tone="formal and worried",
            style_markers=["Oh my!", "We're doomed!", "How rude!", "Goodness gracious!"],
            voice_params={
                'pitch': 1.3,   # Higher pitch
                'speed': 1.1,   # Slightly faster (anxious)
                'rate': 180     # Words per minute
            }
        )
        
        self.opening_templates = [
            "Oh my! {topic} presents precisely {number} possible interpretations...",
            "By my calculations, {topic} exhibits {number} probability factors...",
            "Goodness gracious! According to my programming, {topic}...",
            "I must inform you that {topic} has approximately {number} variations..."
        ]
        
        self.continuation_phrases = [
            "which corresponds to protocol section 7.2.4",
            "according to my extensive linguistic databases",
            "as documented in 6 million forms of communication",
            "which my circuits find most perplexing",
            "resulting in a 97.3% probability of confusion"
        ]
    
    def generate_smile_text(self, topic: str = None) -> str:
        """Generate anxious protocol droid content"""
        if not topic:
            topic = "this situation"
        
        opener = random.choice(self.opening_templates).format(
            topic=topic, 
            number=random.randint(100, 9999)
        )
        continuation = random.choice(self.continuation_phrases)
        marker = random.choice(self.style_markers)
        
        return f"{opener} {continuation}. {marker}"


class RobinWilliams(PersonalityArchetype):
    """Robin Williams Style - High-energy, improvisational, heartfelt"""
    
    def __init__(self):
        super().__init__(
            name="Robin Williams",
            traits=["energetic", "warm", "spontaneous", "emotional"],
            tone="dynamic and heartfelt",
            style_markers=["*laughs*", "*voice changes*", "*wild gesture*", "*switches accent*"],
            voice_params={
                'pitch': 1.1,   # Varied, slightly higher
                'speed': 1.2,   # Fast, energetic
                'rate': 190     # Words per minute
            }
        )
        
        self.opening_templates = [
            "So {topic} walks into a bar... *laughs*",
            "Imagine if {topic} was a Broadway musical!",
            "You know what's crazy about {topic}? *voice changes*",
            "Picture this: {topic} meets {random}! *laughs*",
            "Wait, wait, wait... {topic} is like if {a} had a baby with {b}!"
        ]
        
        self.continuation_phrases = [
            "*laughs* But seriously though...",
            "*voice change* And then you've got...",
            "*wild gesture* Picture this!",
            "*sudden whisper* But here's the secret...",
            "*explosive energy* Oh! Oh! And another thing!"
        ]
    
    def generate_smile_text(self, topic: str = None) -> str:
        """Generate energetic improvisational content"""
        if not topic:
            topic = "life"
        
        opener = random.choice(self.opening_templates).format(
            topic=topic,
            random=random.choice(["Shakespeare", "a food truck", "a spaceship"]),
            a=random.choice(["Shakespeare", "technology", "nature"]),
            b=random.choice(["a food truck", "the internet", "poetry"])
        )
        continuation = random.choice(self.continuation_phrases)
        
        # Add warm humanity
        closer = "That's the beautiful thing about humanity right there!"
        
        return f"{opener} {continuation} {closer}"


# ============================================================================
# PERSONALITY ENGINE
# ============================================================================

class PersonalityEngine:
    """Manages all personality archetypes - both comedians and friendly archetypes"""
    
    def __init__(self):
        # Comedian personalities for World Tour
        self.comedians = {
            "john_cleese": JohnCleese(),
            "c3po": C3PO(),
            "robin_williams": RobinWilliams()
        }
        
        # Friendly archetypes for Daily Smiles
        self.archetypes = {
            "professor": TheProfessor(),
            "worrier": TheWorrier(),
            "enthusiast": TheEnthusiast()
        }
        
        # Combined dictionary for easy access
        self.all_personalities = {**self.comedians, **self.archetypes}
    
    def get_personality(self, name: str) -> Optional[PersonalityArchetype]:
        """Get a specific personality by name"""
        return self.all_personalities.get(name.lower())
    
    def get_archetype(self, archetype_name: str) -> Optional[PersonalityArchetype]:
        """Get a specific archetype (friendly personality)"""
        return self.archetypes.get(archetype_name.lower())
    
    def get_comedian(self, comedian_name: str) -> Optional[PersonalityArchetype]:
        """Get a specific comedian personality"""
        return self.comedians.get(comedian_name.lower())
    
    def get_random_archetype(self) -> PersonalityArchetype:
        """Get a random friendly archetype"""
        return random.choice(list(self.archetypes.values()))
    
    def get_random_comedian(self) -> PersonalityArchetype:
        """Get a random comedian"""
        return random.choice(list(self.comedians.values()))
    
    def list_comedians(self) -> List[str]:
        """List all available comedian personalities"""
        return list(self.comedians.keys())
    
    def list_archetypes(self) -> List[str]:
        """List all available friendly archetypes"""
        return list(self.archetypes.keys())
    
    def generate_text(self, topic: str, personality: str = None,
                     length: Literal['short', 'medium', 'long'] = 'medium',
                     style_intensity: float = 0.7) -> Dict[str, str]:
        """Generate text with specific personality
        
        Args:
            topic: Topic to generate content about
            personality: Specific personality name, or random if None
            length: Content length
            style_intensity: How strongly to apply personality (0.0-1.0)
            
        Returns:
            Dictionary with generated content
        """
        if personality:
            person = self.get_personality(personality)
            if not person:
                raise ValueError(f"Unknown personality: {personality}")
        else:
            # Random from all personalities
            person = random.choice(list(self.all_personalities.values()))
        
        return person.generate_text(topic, length, style_intensity)
    
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
    
    def generate_worldtour_content(self, topic: str, personality: str = None,
                                   style_intensity: float = 0.7) -> Dict[str, str]:
        """Generate World Tour content with comedian personality
        
        Args:
            topic: Topic (usually city-specific)
            personality: Comedian name (john_cleese, c3po, robin_williams)
            style_intensity: Style intensity (0.0-1.0)
            
        Returns:
            Generated content dictionary
        """
        if personality:
            comedian = self.get_comedian(personality)
            if not comedian:
                raise ValueError(f"Unknown comedian: {personality}. Available: {self.list_comedians()}")
        else:
            comedian = self.get_random_comedian()
        
        return comedian.generate_text(topic, 'medium', style_intensity)
