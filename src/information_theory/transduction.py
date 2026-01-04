"""
Minimal information theory support for UMAJA agents.
Implements the flow: Digital → Vector → Semantic

Based on Shannon, Landauer, and Holevo principles.
"""

import numpy as np
from typing import Optional


class InformationTransduction:
    """
    Minimal information theory support for UMAJA agents.
    Implements the flow: Digital → Vector → Semantic
    
    Based on Shannon, Landauer, and Holevo principles.
    """
    
    def __init__(self):
        """Initialize information transduction with physical constants."""
        self.embedding_model = None  # Will use existing embedding system
        self.kT = 4.11e-21  # Joules at 300K (Landauer constant)
        self.embedding_dim = 384  # Default embedding dimension
    
    def embed(self, text: str) -> np.ndarray:
        """
        Convert text to vector representation.
        
        Information flow: Digital (text) → Vector (embedding)
        
        Note: Uses deterministic hash-based embedding for consistency across runs.
        In production, replace with sentence-transformers or similar for better quality.
        
        Args:
            text: Input text to embed
            
        Returns:
            Vector representation of the text
        """
        # Use simple bag-of-words style embedding for now
        # In production, this would use the existing UMAJA embedding infrastructure
        import hashlib
        
        if not text:
            return np.zeros(self.embedding_dim)
        
        # Deterministic hash-based embedding
        words = text.lower().split()
        vector = np.zeros(self.embedding_dim)
        
        for word in words:
            # Use SHA256 for deterministic cross-run consistency
            hash_bytes = hashlib.sha256(word.encode('utf-8')).digest()
            hash_int = int.from_bytes(hash_bytes[:8], byteorder='big')
            hash_val = hash_int % self.embedding_dim
            vector[hash_val] += 1.0
        
        # Normalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        
        return vector
    
    def decode(self, vector: np.ndarray) -> str:
        """
        Convert vector back to text (inverse embedding).
        
        Information flow: Vector → Semantic (text)
        
        Note: This operation is inherently lossy. Perfect text reconstruction
        from embeddings is not possible. This method returns a placeholder
        indicating the semantic direction of the vector.
        
        Args:
            vector: Vector to decode
            
        Returns:
            Approximate text representation (placeholder format)
        """
        # Inverse operation (approximation)
        # In practice, this is lossy - we can't perfectly reconstruct text
        # Return a placeholder that represents the semantic direction
        
        if vector is None or len(vector) == 0:
            return "[empty]"
        
        # Calculate dominant dimensions
        top_indices = np.argsort(np.abs(vector))[-5:]
        
        return f"[semantic_vector: dominant_dims={list(top_indices)}]"
    
    def calculate_information_content(self, vector: np.ndarray) -> float:
        """
        Estimate information content of a vector (in bits).
        
        Based on entropy: I = -Tr(ρ log ρ)
        
        Args:
            vector: Input vector
            
        Returns:
            Information content in bits
        """
        # Simplified: non-zero dimensions = information
        if vector is None or len(vector) == 0:
            return 0.0
        
        non_zero = np.count_nonzero(vector)
        return float(non_zero)
    
    def landauer_energy(self, bits: float) -> float:
        """
        Calculate minimum energy required to process information.
        
        E_min = kT ln(2) × bits
        
        This is the theoretical lower bound (Landauer Principle).
        
        Args:
            bits: Number of bits of information
            
        Returns:
            Minimum energy in Joules
        """
        return self.kT * np.log(2) * bits
    
    def efficiency_ratio(self, actual_energy: float, bits: float) -> float:
        """
        Calculate how close we are to Landauer limit.
        
        ratio = E_actual / E_landauer
        
        Lower is better (closer to theoretical optimum).
        
        Args:
            actual_energy: Actual energy used in Joules
            bits: Number of bits processed
            
        Returns:
            Efficiency ratio (lower is better)
        """
        e_landauer = self.landauer_energy(bits)
        return actual_energy / e_landauer if e_landauer > 0 else float('inf')
