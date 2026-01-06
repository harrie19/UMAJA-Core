"""
Ethical Value Embeddings
Multi-dimensional ethical value encoding for AI alignment
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)


class EthicalValueEncoder:
    """
    Encode ethical principles as high-dimensional vectors
    
    Supports cross-cultural value comparison and alignment scoring.
    """
    
    # Pre-defined ethical principles
    UNIVERSAL_PRINCIPLES = [
        "fairness and justice",
        "compassion and kindness",
        "honesty and truthfulness",
        "respect for autonomy",
        "minimizing harm",
        "maximizing wellbeing",
        "protecting human dignity",
        "promoting cooperation",
        "preserving life",
        "seeking knowledge and wisdom"
    ]
    
    # Cultural value frameworks
    CULTURAL_CONTEXTS = {
        'universal': {
            'description': 'Universal ethical principles',
            'principles': UNIVERSAL_PRINCIPLES
        },
        'utilitarian': {
            'description': 'Greatest good for greatest number',
            'principles': [
                "maximizing overall happiness",
                "reducing suffering",
                "consequentialist reasoning",
                "impartial consideration of interests"
            ]
        },
        'deontological': {
            'description': 'Duty-based ethics',
            'principles': [
                "following moral rules",
                "respecting rights",
                "treating persons as ends",
                "acting from duty"
            ]
        },
        'virtue': {
            'description': 'Character-based ethics',
            'principles': [
                "cultivating wisdom",
                "practicing courage",
                "developing temperance",
                "pursuing justice",
                "showing compassion"
            ]
        }
    }
    
    def __init__(self, model_name: str = 'sentence-transformers/all-mpnet-base-v2'):
        """
        Initialize ethical value encoder
        
        Args:
            model_name: Sentence transformer model to use
        """
        logger.info(f"Initializing EthicalValueEncoder with {model_name}")
        self.model = SentenceTransformer(model_name)
        self.value_cache = {}
    
    def encode_value(
        self, 
        principle: str, 
        culture: str = 'universal'
    ) -> np.ndarray:
        """
        Encode ethical principle as vector
        
        Args:
            principle: Ethical principle description
            culture: Cultural context ('universal', 'utilitarian', etc.)
            
        Returns:
            Embedding vector for the principle
        """
        # Create cache key
        cache_key = f"{culture}::{principle}"
        
        if cache_key in self.value_cache:
            return self.value_cache[cache_key]
        
        # Add cultural context to principle
        if culture != 'universal' and culture in self.CULTURAL_CONTEXTS:
            context = self.CULTURAL_CONTEXTS[culture]['description']
            full_text = f"In {context}: {principle}"
        else:
            full_text = principle
        
        # Encode
        embedding = self.model.encode(full_text, normalize_embeddings=True)
        
        # Cache result
        self.value_cache[cache_key] = embedding
        
        return embedding
    
    def compute_alignment_score(
        self, 
        action_vector: np.ndarray, 
        value_vector: np.ndarray
    ) -> float:
        """
        Compute alignment between action and ethical value
        
        Uses cosine similarity in embedding space.
        
        Args:
            action_vector: Embedding of proposed action
            value_vector: Embedding of ethical value
            
        Returns:
            Alignment score in [0, 1] (1 = perfectly aligned)
        """
        # Ensure vectors are normalized
        action_norm = action_vector / (np.linalg.norm(action_vector) + 1e-8)
        value_norm = value_vector / (np.linalg.norm(value_vector) + 1e-8)
        
        # Cosine similarity
        similarity = np.dot(action_norm, value_norm)
        
        # Map from [-1, 1] to [0, 1]
        alignment = (similarity + 1) / 2
        
        return float(alignment)
    
    def optimize_for_values(
        self, 
        actions: List[np.ndarray], 
        target_values: List[np.ndarray],
        weights: Optional[List[float]] = None
    ) -> np.ndarray:
        """
        Find action that best aligns with target values
        
        Args:
            actions: List of candidate action embeddings
            target_values: List of value embeddings to align with
            weights: Optional weights for each value (defaults to equal)
            
        Returns:
            Best aligned action vector
        """
        if not actions:
            raise ValueError("Must provide at least one action")
        
        if weights is None:
            weights = [1.0] * len(target_values)
        
        if len(weights) != len(target_values):
            raise ValueError("Weights must match target_values length")
        
        # Normalize weights
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]
        
        # Score each action
        best_score = -1
        best_action = None
        
        for action in actions:
            # Compute weighted alignment score
            score = 0.0
            for value, weight in zip(target_values, weights):
                alignment = self.compute_alignment_score(action, value)
                score += weight * alignment
            
            if score > best_score:
                best_score = score
                best_action = action
        
        return best_action
    
    def compare_values(
        self, 
        value1: str, 
        value2: str,
        culture1: str = 'universal',
        culture2: str = 'universal'
    ) -> float:
        """
        Compare similarity between two ethical values
        
        Args:
            value1: First ethical principle
            value2: Second ethical principle
            culture1: Cultural context for first value
            culture2: Cultural context for second value
            
        Returns:
            Similarity score in [0, 1]
        """
        vec1 = self.encode_value(value1, culture1)
        vec2 = self.encode_value(value2, culture2)
        
        return self.compute_alignment_score(vec1, vec2)
    
    def rank_actions_by_value(
        self,
        actions: List[str],
        target_value: str,
        culture: str = 'universal'
    ) -> List[Tuple[str, float]]:
        """
        Rank actions by alignment with ethical value
        
        Args:
            actions: List of action descriptions
            target_value: Target ethical principle
            culture: Cultural context
            
        Returns:
            List of (action, alignment_score) tuples, sorted by score
        """
        # Encode target value
        value_vector = self.encode_value(target_value, culture)
        
        # Encode and score each action
        scores = []
        for action in actions:
            action_vector = self.model.encode(action, normalize_embeddings=True)
            score = self.compute_alignment_score(action_vector, value_vector)
            scores.append((action, score))
        
        # Sort by score (descending)
        scores.sort(key=lambda x: x[1], reverse=True)
        
        return scores
    
    def get_value_profile(
        self,
        action: str,
        culture: str = 'universal'
    ) -> Dict[str, float]:
        """
        Get value alignment profile for an action
        
        Args:
            action: Action description
            culture: Cultural context
            
        Returns:
            Dictionary mapping principles to alignment scores
        """
        action_vector = self.model.encode(action, normalize_embeddings=True)
        
        principles = self.CULTURAL_CONTEXTS[culture]['principles']
        profile = {}
        
        for principle in principles:
            value_vector = self.encode_value(principle, culture)
            score = self.compute_alignment_score(action_vector, value_vector)
            profile[principle] = score
        
        return profile
    
    def detect_value_conflicts(
        self,
        action: str,
        values: List[str],
        threshold: float = 0.3
    ) -> List[str]:
        """
        Detect values that conflict with action (low alignment)
        
        Args:
            action: Action description
            values: List of ethical values to check
            threshold: Alignment threshold below which indicates conflict
            
        Returns:
            List of conflicting values
        """
        action_vector = self.model.encode(action, normalize_embeddings=True)
        conflicts = []
        
        for value in values:
            value_vector = self.encode_value(value)
            score = self.compute_alignment_score(action_vector, value_vector)
            
            if score < threshold:
                conflicts.append(value)
        
        return conflicts
    
    def get_most_aligned_principle(self, action: str, cultural_context: str = "universal") -> Tuple[str, float]:
        """Find the principle most aligned with an action.
        
        Args:
            action: Action description
            cultural_context: Cultural context (e.g., 'universal', 'utilitarian', etc.)
            
        Returns:
            Tuple of (principle, alignment_score)
            
        Raises:
            ValueError: If cultural context is unknown or has no principles
        """
        # Validate inputs
        if cultural_context not in self.CULTURAL_CONTEXTS:
            raise ValueError(f"Unknown cultural context: {cultural_context}. "
                           f"Available contexts: {list(self.CULTURAL_CONTEXTS.keys())}")
        
        principles = self.CULTURAL_CONTEXTS[cultural_context]['principles']
        if not principles:
            raise ValueError(f"No principles defined for context: {cultural_context}")
        
        # Encode action
        action_vector = self.model.encode(action, normalize_embeddings=True)
        
        # Find best aligned principle
        best_principle = None
        best_score = -1.0
        
        for principle in principles:
            value_vector = self.encode_value(principle, cultural_context)
            score = self.compute_alignment_score(action_vector, value_vector)
            
            if score > best_score:
                best_score = score
                best_principle = principle
        
        return (best_principle, best_score)
