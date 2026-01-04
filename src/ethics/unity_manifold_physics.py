"""
Bahá'í Principles as emergent ethical constraints in vector space.

Physics Analogy:
- Quantum: Wave function collapse to allowed states
- Classical: Projection onto constraint surface
- Vector Space: Projection onto Unity Manifold
"""

import numpy as np
from typing import Dict, List, Any, Tuple
from ..information_theory.transduction import InformationTransduction


class UnityManifoldPhysics:
    """
    Bahá'í Principles as emergent ethical constraints in vector space.
    
    Physics Analogy:
    - Quantum: Wave function collapse to allowed states
    - Classical: Projection onto constraint surface
    - Vector Space: Projection onto Unity Manifold
    """
    
    def __init__(self):
        """Initialize Unity Manifold with Bahá'í principle vectors."""
        self.transduction = InformationTransduction()
        
        # Initialize principle vectors (embeddings)
        self.principles = {
            "truth": self.embed_principle("truth", [
                "transparency", "honesty", "no_hallucination",
                "cite_sources", "admit_uncertainty"
            ]),
            "unity": self.embed_principle("unity", [
                "serves_all_equally", "no_discrimination",
                "inclusive", "universal_access"
            ]),
            "service": self.embed_principle("service", [
                "purpose_driven", "benefits_humanity",
                "user_centric", "mission_aligned"
            ]),
            "justice": self.embed_principle("justice", [
                "fair_distribution", "equity", "balance",
                "no_bias", "equal_opportunity"
            ]),
            "moderation": self.embed_principle("moderation", [
                "efficiency", "no_excess", "minimal_waste",
                "sustainable", "balanced"
            ])
        }
        
        # Calculate Unity Manifold centroid
        self.unity_centroid = self.calculate_centroid(
            list(self.principles.values())
        )
        
        # Physics-inspired parameters
        self.energy_threshold = 0.95  # Max distance from centroid (adjusted for simple embeddings)
        self.projection_strength = 0.8  # How strongly to project violations
    
    def embed_principle(self, name: str, keywords: List[str]) -> np.ndarray:
        """
        Embed principle as vector (use existing embedding model).
        
        Args:
            name: Principle name
            keywords: Keywords describing the principle
            
        Returns:
            Embedded principle vector
        """
        # Combine name and keywords into a coherent description
        text = f"{name} " + " ".join(keywords)
        return self.transduction.embed(text)
    
    def project_onto_unity_manifold(self, agent_output_vector: np.ndarray) -> Dict[str, Any]:
        """
        Project agent output onto Unity Manifold.
        
        Physics Analog: 
        - Like projecting arbitrary state onto allowed quantum states
        - Minimizes "ethical energy" (distance to manifold)
        
        Args:
            agent_output_vector: Vector representation of agent output
            
        Returns:
            Dictionary with validation results and corrections if needed
        """
        # Calculate distance to centroid
        distance = self.cosine_distance(
            agent_output_vector,
            self.unity_centroid
        )
        
        # Check violation
        if distance > self.energy_threshold:
            # Outside manifold - project back
            projected = self.project_vector(
                agent_output_vector,
                self.unity_centroid,
                strength=self.projection_strength
            )
            
            # Identify which principle was violated
            violations = self.identify_violations(
                agent_output_vector,
                distance
            )
            
            return {
                'allowed': False,
                'distance_from_unity': distance,
                'threshold': self.energy_threshold,
                'violated_principles': violations,
                'corrected_output': projected,
                'alignment_score': 1 - distance
            }
        else:
            # Within manifold - approved
            return {
                'allowed': True,
                'distance_from_unity': distance,
                'alignment_score': 1 - distance,
                'principle_scores': self.score_per_principle(
                    agent_output_vector
                )
            }
    
    def identify_violations(self, vector: np.ndarray, distance: float) -> List[Dict[str, Any]]:
        """
        Determine which principles are violated based on vector direction.
        
        Args:
            vector: Agent output vector
            distance: Distance from unity centroid
            
        Returns:
            List of violated principles with severity
        """
        violations = []
        
        for principle_name, principle_vector in self.principles.items():
            # Calculate similarity to each principle
            similarity = self.cosine_similarity(vector, principle_vector)
            
            # If dissimilar (negative or low), it's a violation
            if similarity < 0.5:
                violations.append({
                    'principle': principle_name,
                    'similarity': similarity,
                    'severity': 'HIGH' if similarity < 0.2 else 'MEDIUM'
                })
        
        return violations
    
    def score_per_principle(self, vector: np.ndarray) -> Dict[str, float]:
        """
        Score alignment with each Bahá'í principle (0.0-1.0).
        
        Args:
            vector: Vector to score
            
        Returns:
            Dictionary mapping principle names to scores
        """
        scores = {}
        for name, principle_vec in self.principles.items():
            similarity = self.cosine_similarity(vector, principle_vec)
            scores[name] = max(0.0, similarity)  # Clamp to [0, 1]
        return scores
    
    def cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """
        Compute cosine similarity between two vectors.
        
        Args:
            v1: First vector
            v2: Second vector
            
        Returns:
            Cosine similarity in range [-1, 1]
        """
        if v1 is None or v2 is None or len(v1) == 0 or len(v2) == 0:
            return 0.0
        
        # Compute dot product
        dot_product = np.dot(v1, v2)
        
        # Compute norms
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        
        # Avoid division by zero
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0
        
        # Cosine similarity
        return dot_product / (norm_v1 * norm_v2)
    
    def cosine_distance(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """
        Compute cosine distance (1 - similarity).
        
        Args:
            v1: First vector
            v2: Second vector
            
        Returns:
            Cosine distance in range [0, 2]
        """
        return 1 - self.cosine_similarity(v1, v2)
    
    def project_vector(self, v: np.ndarray, target: np.ndarray, strength: float) -> np.ndarray:
        """
        Project vector v towards target with given strength.
        
        Args:
            v: Vector to project
            target: Target vector
            strength: Projection strength (0.0 to 1.0)
            
        Returns:
            Projected vector
        """
        if v is None or target is None or len(v) == 0 or len(target) == 0:
            return v if v is not None else np.zeros_like(target)
        
        # Linear interpolation towards target
        # strength=1.0 means full projection to target
        # strength=0.0 means no change
        return (1 - strength) * v + strength * target
    
    def calculate_centroid(self, vectors: List[np.ndarray]) -> np.ndarray:
        """
        Calculate geometric center of principle vectors.
        
        Args:
            vectors: List of vectors
            
        Returns:
            Centroid vector (mean of all vectors)
        """
        if not vectors:
            return np.zeros(self.transduction.embedding_dim)
        
        # Stack vectors and compute mean
        stacked = np.stack(vectors)
        centroid = np.mean(stacked, axis=0)
        
        # Normalize to unit length
        norm = np.linalg.norm(centroid)
        if norm > 0:
            centroid = centroid / norm
        
        return centroid
