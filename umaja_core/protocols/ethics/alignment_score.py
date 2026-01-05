"""
Alignment Score Utilities
Helper functions for computing and analyzing ethical alignment
"""

import numpy as np
from typing import List, Dict, Tuple, Optional


class AlignmentScorer:
    """
    Utilities for computing alignment scores between actions and values
    """
    
    @staticmethod
    def compute_aggregate_alignment(
        action_vector: np.ndarray,
        value_vectors: List[np.ndarray],
        aggregation: str = 'mean'
    ) -> float:
        """
        Compute aggregate alignment with multiple values
        
        Args:
            action_vector: Action embedding
            value_vectors: List of value embeddings
            aggregation: Method ('mean', 'min', 'weighted')
            
        Returns:
            Aggregate alignment score
        """
        if not value_vectors:
            return 0.0
        
        # Normalize vectors
        action_norm = action_vector / (np.linalg.norm(action_vector) + 1e-8)
        value_norms = [v / (np.linalg.norm(v) + 1e-8) for v in value_vectors]
        
        # Compute similarities
        similarities = [np.dot(action_norm, v) for v in value_norms]
        similarities = [(s + 1) / 2 for s in similarities]  # Map to [0, 1]
        
        if aggregation == 'mean':
            return float(np.mean(similarities))
        elif aggregation == 'min':
            return float(np.min(similarities))
        elif aggregation == 'max':
            return float(np.max(similarities))
        else:
            raise ValueError(f"Unknown aggregation: {aggregation}")
    
    @staticmethod
    def find_value_violations(
        action_vector: np.ndarray,
        value_vectors: Dict[str, np.ndarray],
        threshold: float = 0.3
    ) -> List[str]:
        """
        Find values that are violated by action
        
        Args:
            action_vector: Action embedding
            value_vectors: Dictionary of value name -> embedding
            threshold: Violation threshold
            
        Returns:
            List of violated value names
        """
        violations = []
        
        action_norm = action_vector / (np.linalg.norm(action_vector) + 1e-8)
        
        for name, value_vec in value_vectors.items():
            value_norm = value_vec / (np.linalg.norm(value_vec) + 1e-8)
            similarity = np.dot(action_norm, value_norm)
            alignment = (similarity + 1) / 2
            
            if alignment < threshold:
                violations.append(name)
        
        return violations
    
    @staticmethod
    def balance_values(
        value_vectors: List[np.ndarray],
        weights: Optional[List[float]] = None
    ) -> np.ndarray:
        """
        Create balanced value vector from multiple values
        
        Args:
            value_vectors: List of value embeddings
            weights: Optional weights for each value
            
        Returns:
            Balanced value vector
        """
        if not value_vectors:
            raise ValueError("Must provide at least one value")
        
        if weights is None:
            weights = [1.0] * len(value_vectors)
        
        # Normalize weights
        total = sum(weights)
        weights = [w / total for w in weights]
        
        # Weighted sum
        balanced = np.zeros_like(value_vectors[0])
        for vec, weight in zip(value_vectors, weights):
            balanced += weight * vec
        
        # Normalize
        balanced = balanced / (np.linalg.norm(balanced) + 1e-8)
        
        return balanced


class ValueJudgmentFunction:
    """
    Value judgment function for evaluating actions
    """
    
    def __init__(self, target_values: Dict[str, np.ndarray]):
        """
        Initialize with target values
        
        Args:
            target_values: Dictionary of value name -> embedding
        """
        self.target_values = target_values
    
    def judge(self, action_vector: np.ndarray) -> Dict[str, float]:
        """
        Judge action against all target values
        
        Args:
            action_vector: Action embedding
            
        Returns:
            Dictionary of value name -> alignment score
        """
        judgments = {}
        
        action_norm = action_vector / (np.linalg.norm(action_vector) + 1e-8)
        
        for name, value_vec in self.target_values.items():
            value_norm = value_vec / (np.linalg.norm(value_vec) + 1e-8)
            similarity = np.dot(action_norm, value_norm)
            alignment = (similarity + 1) / 2
            judgments[name] = float(alignment)
        
        return judgments
    
    def is_acceptable(
        self, 
        action_vector: np.ndarray,
        min_threshold: float = 0.3
    ) -> Tuple[bool, Dict[str, float]]:
        """
        Check if action is acceptable given value thresholds
        
        Args:
            action_vector: Action embedding
            min_threshold: Minimum acceptable alignment
            
        Returns:
            (is_acceptable, judgment_scores)
        """
        judgments = self.judge(action_vector)
        acceptable = all(score >= min_threshold for score in judgments.values())
        return acceptable, judgments


class NormPromotionFunction:
    """
    Function for promoting prosocial norms in agent behavior
    """
    
    def __init__(self, promoted_norms: List[np.ndarray]):
        """
        Initialize with norms to promote
        
        Args:
            promoted_norms: List of norm embeddings
        """
        self.promoted_norms = promoted_norms
    
    def evaluate_action(self, action_vector: np.ndarray) -> float:
        """
        Evaluate how well action promotes norms
        
        Args:
            action_vector: Action embedding
            
        Returns:
            Norm promotion score [0, 1]
        """
        scores = []
        
        action_norm = action_vector / (np.linalg.norm(action_vector) + 1e-8)
        
        for norm_vec in self.promoted_norms:
            norm_norm = norm_vec / (np.linalg.norm(norm_vec) + 1e-8)
            similarity = np.dot(action_norm, norm_norm)
            score = (similarity + 1) / 2
            scores.append(score)
        
        return float(np.mean(scores))
    
    def suggest_improvement(
        self,
        action_vector: np.ndarray,
        alpha: float = 0.2
    ) -> np.ndarray:
        """
        Suggest improved action that better promotes norms
        
        Args:
            action_vector: Original action
            alpha: Interpolation factor
            
        Returns:
            Improved action vector
        """
        # Average of promoted norms
        avg_norm = np.mean(self.promoted_norms, axis=0)
        avg_norm = avg_norm / (np.linalg.norm(avg_norm) + 1e-8)
        
        # Interpolate with action
        improved = (1 - alpha) * action_vector + alpha * avg_norm
        improved = improved / (np.linalg.norm(improved) + 1e-8)
        
        return improved
