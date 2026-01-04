"""
Language Model Network (LMNet) Utilities
Helper functions for embedding-based agent networks
"""

import numpy as np
from typing import List, Tuple, Optional
from sklearn.metrics.pairwise import cosine_similarity


class LMNet:
    """
    Language Model Network utilities
    Provides helper functions for vector-based agent communication
    """
    
    @staticmethod
    def compute_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Compute cosine similarity between two vectors
        
        Args:
            vec1: First embedding vector
            vec2: Second embedding vector
            
        Returns:
            Similarity score in [0, 1]
        """
        if vec1.ndim == 1:
            vec1 = vec1.reshape(1, -1)
        if vec2.ndim == 1:
            vec2 = vec2.reshape(1, -1)
        
        similarity = cosine_similarity(vec1, vec2)[0, 0]
        # Normalize to [0, 1]
        return (similarity + 1) / 2
    
    @staticmethod
    def find_nearest_agents(
        query_vector: np.ndarray,
        agent_vectors: List[np.ndarray],
        agent_ids: List[str],
        top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Find k nearest agents based on vector similarity
        
        Args:
            query_vector: Query embedding
            agent_vectors: List of agent embeddings
            agent_ids: List of agent IDs
            top_k: Number of nearest agents to return
            
        Returns:
            List of (agent_id, similarity_score) tuples
        """
        if len(agent_vectors) != len(agent_ids):
            raise ValueError("agent_vectors and agent_ids must have same length")
        
        similarities = []
        for agent_vec, agent_id in zip(agent_vectors, agent_ids):
            sim = LMNet.compute_similarity(query_vector, agent_vec)
            similarities.append((agent_id, sim))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    @staticmethod
    def aggregate_vectors(
        vectors: List[np.ndarray],
        method: str = 'mean',
        weights: Optional[List[float]] = None
    ) -> np.ndarray:
        """
        Aggregate multiple vectors into a single representation
        
        Args:
            vectors: List of embedding vectors
            method: Aggregation method ('mean', 'max', 'weighted')
            weights: Optional weights for weighted aggregation
            
        Returns:
            Aggregated vector
        """
        if not vectors:
            raise ValueError("vectors list cannot be empty")
        
        vectors = np.array(vectors)
        
        if method == 'mean':
            return np.mean(vectors, axis=0)
        elif method == 'max':
            return np.max(vectors, axis=0)
        elif method == 'weighted':
            if weights is None:
                raise ValueError("weights required for weighted aggregation")
            if len(weights) != len(vectors):
                raise ValueError("weights must match vectors length")
            weights = np.array(weights).reshape(-1, 1)
            return np.sum(vectors * weights, axis=0) / np.sum(weights)
        else:
            raise ValueError(f"Unknown aggregation method: {method}")
    
    @staticmethod
    def interpolate_vectors(
        vec1: np.ndarray,
        vec2: np.ndarray,
        alpha: float = 0.5
    ) -> np.ndarray:
        """
        Interpolate between two vectors
        
        Args:
            vec1: First vector
            vec2: Second vector
            alpha: Interpolation factor (0=vec1, 1=vec2)
            
        Returns:
            Interpolated vector
        """
        return (1 - alpha) * vec1 + alpha * vec2
    
    @staticmethod
    def compute_diversity(vectors: List[np.ndarray]) -> float:
        """
        Compute diversity score for a set of vectors
        Higher score means more diverse
        
        Args:
            vectors: List of embedding vectors
            
        Returns:
            Diversity score
        """
        if len(vectors) < 2:
            return 0.0
        
        # Compute pairwise similarities
        similarities = []
        for i in range(len(vectors)):
            for j in range(i + 1, len(vectors)):
                sim = LMNet.compute_similarity(vectors[i], vectors[j])
                similarities.append(sim)
        
        # Diversity is inverse of average similarity
        avg_similarity = np.mean(similarities)
        diversity = 1.0 - avg_similarity
        
        return diversity
