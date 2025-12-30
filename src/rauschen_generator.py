"""
UMAJA-Core: Rauschen Generator
Core text generation engine using sentence transformers, controlled noise variation,
and semantic coherence checking.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Literal, Optional
import numpy as np
from sentence_transformers import SentenceTransformer, util
import torch


class RauschenGenerator:
    """
    Core text generation engine that produces reflective text with controlled
    noise variation and semantic coherence checking.
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the Rauschen Generator.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model = SentenceTransformer(model_name)
        self.base_price_per_word = 0.01  # Base price per word in credits
        
        # Seed phrases for reflection generation
        self.reflection_templates = {
            'philosophical': [
                "Consider the deeper implications of {}",
                "What does it mean to truly understand {}?",
                "The essence of {} lies in its relationship to consciousness",
                "Through the lens of existence, {} reveals",
                "In contemplating {}, we discover layers of meaning"
            ],
            'analytical': [
                "Examining {} from multiple perspectives shows",
                "The systematic analysis of {} demonstrates",
                "Breaking down the components of {}, we observe",
                "A critical investigation into {} reveals",
                "The structural elements of {} indicate"
            ],
            'creative': [
                "Imagine {} as a tapestry of interconnected ideas",
                "The poetic nature of {} emerges when",
                "Dancing around the concept of {}, we find",
                "Like waves upon the shore, {} touches",
                "In the realm of possibility, {} becomes"
            ],
            'practical': [
                "The practical applications of {} extend to",
                "In everyday contexts, {} manifests as",
                "When we apply {} to real-world situations",
                "The tangible aspects of {} include",
                "From a pragmatic standpoint, {} offers"
            ]
        }
        
        self.continuation_phrases = [
            "Furthermore", "Additionally", "Moreover", "In this context",
            "Considering this", "From this perspective", "Building upon this",
            "It follows that", "Subsequently", "In relation to this",
            "This suggests that", "One might observe", "Consequently",
            "In essence", "Notably"
        ]
    
    def _apply_noise_variation(self, text: str, noise_level: float) -> str:
        """
        Apply controlled noise variation to text while maintaining coherence.
        
        Args:
            text: Input text
            noise_level: Level of noise to apply (0.0 to 1.0)
            
        Returns:
            Text with applied noise variation
        """
        words = text.split()
        if noise_level <= 0.0 or len(words) < 2:
            return text
        
        # Calculate number of variations to apply based on noise level
        num_variations = int(len(words) * noise_level * 0.3)
        
        # Apply variations: word reordering, synonym variation (simulated)
        varied_words = words.copy()
        indices = np.random.choice(len(words) - 1, 
                                   size=min(num_variations, len(words) - 1), 
                                   replace=False)
        
        for idx in indices:
            # Simulate variation by occasionally swapping adjacent words
            # or adding subtle modifications
            if idx < len(varied_words) - 1 and np.random.random() < 0.5:
                # Swap adjacent words (only if not at sentence boundaries)
                if not varied_words[idx].endswith(('.', '?', '!')):
                    varied_words[idx], varied_words[idx + 1] = \
                        varied_words[idx + 1], varied_words[idx]
        
        return ' '.join(varied_words)
    
    def _check_semantic_coherence(self, sentences: List[str], 
                                  threshold: float = 0.3) -> float:
        """
        Check semantic coherence between sentences using embeddings.
        
        Args:
            sentences: List of sentences to check
            threshold: Minimum similarity threshold
            
        Returns:
            Average coherence score
        """
        if len(sentences) < 2:
            return 1.0
        
        embeddings = self.model.encode(sentences, convert_to_tensor=True)
        
        # Calculate pairwise similarities
        coherence_scores = []
        for i in range(len(embeddings) - 1):
            similarity = util.cos_sim(embeddings[i], embeddings[i + 1])
            coherence_scores.append(similarity.item())
        
        avg_coherence = np.mean(coherence_scores)
        return max(avg_coherence, 0.0)
    
    def _generate_reflection_text(self, topic: str, target_words: int, 
                                  noise_level: float) -> str:
        """
        Generate reflective text about a topic.
        
        Args:
            topic: Topic to reflect upon
            target_words: Target word count
            noise_level: Noise level for variation
            
        Returns:
            Generated reflection text
        """
        # Select random style
        style = np.random.choice(list(self.reflection_templates.keys()))
        templates = self.reflection_templates[style]
        
        # Generate opening sentence
        opening_template = np.random.choice(templates)
        text = opening_template.format(topic) + ". "
        
        sentences = [text.strip()]
        current_words = len(text.split())
        
        # Generate additional sentences until target is reached
        while current_words < target_words:
            # Add continuation phrase
            continuation = np.random.choice(self.continuation_phrases)
            
            # Generate sentence with topic variation
            template = np.random.choice(templates)
            # Vary the topic reference
            topic_variations = [
                topic,
                f"this aspect of {topic}",
                f"the nature of {topic}",
                "these ideas",
                "this concept"
            ]
            varied_topic = np.random.choice(topic_variations)
            
            sentence = f"{continuation}, {template.format(varied_topic).lower()}. "
            sentences.append(sentence.strip())
            text += sentence
            current_words = len(text.split())
            
            # Check coherence periodically
            if len(sentences) % 3 == 0:
                coherence = self._check_semantic_coherence(sentences[-3:])
                # If coherence is too low, restart the last sentence
                if coherence < 0.2:
                    sentences.pop()
                    text = ' '.join(sentences) + ' '
                    current_words = len(text.split())
        
        # Apply noise variation
        text = self._apply_noise_variation(text, noise_level)
        
        return text.strip()
    
    def _calculate_price(self, word_count: int, noise_level: float, 
                        length_type: str) -> float:
        """
        Calculate price for generated text.
        
        Args:
            word_count: Number of words
            noise_level: Noise level applied
            length_type: Type of length (short/long)
            
        Returns:
            Price in credits
        """
        base_price = word_count * self.base_price_per_word
        
        # Apply modifiers
        noise_modifier = 1.0 + (noise_level * 0.5)  # Higher noise = higher price
        length_modifier = 1.2 if length_type == 'long' else 1.0
        
        return round(base_price * noise_modifier * length_modifier, 2)
    
    def generate_reflection(self, 
                          topic: str, 
                          length: Literal['short', 'long'] = 'short',
                          noise_level: float = 0.3) -> Dict:
        """
        Generate a reflection text with metadata.
        
        Args:
            topic: Topic to generate reflection about
            length: Length type - 'short' (50-150 words) or 'long' (200-500 words)
            noise_level: Noise variation level (0.0 to 1.0)
            
        Returns:
            Dictionary containing:
                - text: Generated reflection text
                - text_id: Unique identifier
                - word_count: Number of words
                - price: Price in credits
                - timestamp: Generation timestamp (ISO format)
                - metadata: Additional metadata (topic, length, noise_level, coherence_score)
        """
        # Validate inputs
        if not topic or not isinstance(topic, str):
            raise ValueError("Topic must be a non-empty string")
        
        if length not in ['short', 'long']:
            raise ValueError("Length must be 'short' or 'long'")
        
        noise_level = max(0.0, min(1.0, noise_level))  # Clamp to [0, 1]
        
        # Determine target word count
        if length == 'short':
            target_words = np.random.randint(50, 151)
        else:  # long
            target_words = np.random.randint(200, 501)
        
        # Generate text
        generated_text = self._generate_reflection_text(
            topic, target_words, noise_level
        )
        
        # Calculate actual word count
        word_count = len(generated_text.split())
        
        # Calculate coherence score
        sentences = [s.strip() + '.' for s in generated_text.split('.') if s.strip()]
        coherence_score = self._check_semantic_coherence(sentences)
        
        # Calculate price
        price = self._calculate_price(word_count, noise_level, length)
        
        # Generate unique ID
        text_id = str(uuid.uuid4())
        
        # Create timestamp
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        return {
            'text': generated_text,
            'text_id': text_id,
            'word_count': word_count,
            'price': price,
            'timestamp': timestamp,
            'metadata': {
                'topic': topic,
                'length': length,
                'noise_level': noise_level,
                'coherence_score': round(coherence_score, 3),
                'model': self.model.get_sentence_embedding_dimension()
            }
        }


# Example usage
if __name__ == "__main__":
    # Initialize generator
    generator = RauschenGenerator()
    
    # Generate short reflection
    result = generator.generate_reflection(
        topic="artificial intelligence",
        length="short",
        noise_level=0.4
    )
    
    print("Generated Reflection:")
    print(f"ID: {result['text_id']}")
    print(f"Word Count: {result['word_count']}")
    print(f"Price: ${result['price']}")
    print(f"Timestamp: {result['timestamp']}")
    print(f"Coherence Score: {result['metadata']['coherence_score']}")
    print(f"\nText:\n{result['text']}")
