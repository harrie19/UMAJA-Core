"""
VectorComm Encoder
Tiered embedding system for efficient AI-to-AI communication

Implements three-tier architecture:
- Tier 1 (Fast): 384D embeddings using all-MiniLM-L6-v2 (~16ms latency)
- Tier 2 (Core): 768D embeddings using all-mpnet-base-v2 (~45ms latency)
- Tier 3 (Deep): 1024D embeddings using all-roberta-large-v1 (~120ms latency)
"""

import numpy as np
from typing import Union, List, Optional
from sentence_transformers import SentenceTransformer
import logging
from sklearn.decomposition import PCA

logger = logging.getLogger(__name__)


class VectorCommEncoder:
    """
    Multi-tier vector encoder for AI-to-AI communication
    
    Supports dynamic tier selection based on latency/accuracy tradeoffs.
    """
    
    # Model configurations
    TIER_CONFIGS = {
        1: {
            'model': 'sentence-transformers/all-MiniLM-L6-v2',
            'dim': 384,
            'latency_ms': 16,
            'description': 'Fast tier - quick responses'
        },
        2: {
            'model': 'sentence-transformers/all-mpnet-base-v2',
            'dim': 768,
            'latency_ms': 45,
            'description': 'Core tier - balanced performance'
        },
        3: {
            'model': 'sentence-transformers/all-roberta-large-v1',
            'dim': 1024,
            'latency_ms': 120,
            'description': 'Deep tier - maximum accuracy'
        }
    }
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize VectorComm encoder with all tiers
        
        Args:
            cache_dir: Optional directory to cache downloaded models
        """
        self.cache_dir = cache_dir
        self.models = {}
        self.pca_projectors = {}
        
        logger.info("Initializing VectorComm Encoder")
        
    def _load_model(self, tier: int) -> SentenceTransformer:
        """Lazy load model for specified tier"""
        if tier not in self.models:
            if tier not in self.TIER_CONFIGS:
                raise ValueError(f"Invalid tier {tier}. Must be 1, 2, or 3.")
            
            config = self.TIER_CONFIGS[tier]
            logger.info(f"Loading Tier {tier} model: {config['model']}")
            
            self.models[tier] = SentenceTransformer(
                config['model'],
                cache_folder=self.cache_dir
            )
            
        return self.models[tier]
    
    def encode(
        self, 
        message: Union[str, List[str]], 
        tier: int = 2,
        normalize: bool = True
    ) -> np.ndarray:
        """
        Encode message(s) into vector representation
        
        Args:
            message: Text message or list of messages to encode
            tier: Tier level (1=fast, 2=core, 3=deep)
            normalize: Whether to L2-normalize the embeddings
            
        Returns:
            numpy array of shape (embedding_dim,) or (n_messages, embedding_dim)
        """
        model = self._load_model(tier)
        
        # Encode
        embeddings = model.encode(
            message,
            normalize_embeddings=normalize,
            show_progress_bar=False
        )
        
        return embeddings
    
    def decode(
        self, 
        vector: np.ndarray, 
        tier: int = 2,
        candidates: Optional[List[str]] = None,
        top_k: int = 5
    ) -> str:
        """
        Decode vector back to nearest message (approximate)
        
        Note: This is an approximate decode using similarity search.
        For exact decode, store a mapping of vectors to messages.
        
        Args:
            vector: Embedding vector to decode
            tier: Tier level used for encoding
            candidates: Optional list of candidate messages to search
            top_k: Number of top candidates to return
            
        Returns:
            Most likely decoded message string
        """
        if candidates is None:
            # Without candidates, return a description of the vector
            return f"<Vector: dim={len(vector)}, norm={np.linalg.norm(vector):.3f}>"
        
        # Encode candidates and find nearest
        model = self._load_model(tier)
        candidate_embeddings = model.encode(candidates, show_progress_bar=False)
        
        # Compute similarities
        if vector.ndim == 1:
            vector = vector.reshape(1, -1)
        
        similarities = np.dot(candidate_embeddings, vector.T).flatten()
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Return top match
        return candidates[top_indices[0]]
    
    def compress_to_tier(
        self, 
        vector: np.ndarray, 
        source_tier: int, 
        target_tier: int
    ) -> np.ndarray:
        """
        Compress embedding from higher tier to lower tier
        
        Uses PCA projection to reduce dimensionality while preserving
        maximum variance.
        
        Args:
            vector: Source embedding vector
            source_tier: Original tier (higher dimension)
            target_tier: Target tier (lower dimension)
            
        Returns:
            Compressed vector at target tier dimension
        """
        if source_tier not in self.TIER_CONFIGS or target_tier not in self.TIER_CONFIGS:
            raise ValueError("Invalid tier specification")
        
        source_dim = self.TIER_CONFIGS[source_tier]['dim']
        target_dim = self.TIER_CONFIGS[target_tier]['dim']
        
        if source_dim <= target_dim:
            logger.warning(
                f"Source tier {source_tier} (dim={source_dim}) is not higher than "
                f"target tier {target_tier} (dim={target_dim}). Returning as-is."
            )
            return vector
        
        # Create or retrieve PCA projector
        key = f"{source_tier}_to_{target_tier}"
        if key not in self.pca_projectors:
            self.pca_projectors[key] = PCA(n_components=target_dim)
            # Fit on random samples (in production, use representative data)
            random_samples = np.random.randn(1000, source_dim)
            self.pca_projectors[key].fit(random_samples)
        
        # Project
        if vector.ndim == 1:
            vector = vector.reshape(1, -1)
        
        compressed = self.pca_projectors[key].transform(vector)
        
        return compressed.flatten() if compressed.shape[0] == 1 else compressed
    
    def get_tier_info(self, tier: int) -> dict:
        """Get information about a specific tier"""
        if tier not in self.TIER_CONFIGS:
            raise ValueError(f"Invalid tier {tier}")
        return self.TIER_CONFIGS[tier].copy()
    
    def list_tiers(self) -> dict:
        """List all available tiers and their configurations"""
        return {
            tier: {
                'dimension': config['dim'],
                'latency_ms': config['latency_ms'],
                'description': config['description']
            }
            for tier, config in self.TIER_CONFIGS.items()
        }
