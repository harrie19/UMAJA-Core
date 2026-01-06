"""
Vector Layer - Continuous Subsymbolic Processing Component

This module implements the vector layer of the dual-layer architecture,
providing continuous state representation, energy-efficient evaluation,
and subsymbolic reasoning capabilities.

Key Features:
- Persistent agent identity and context via 768D embeddings
- Hebbian-like learning for state updates
- L2 normalization to prevent vector drift
- Semantic collapse detection via entropy monitoring
- Energy-efficient similarity search
- State persistence across sessions

Model: sentence-transformers/all-mpnet-base-v2 (768D embeddings)
"""

import os
import sys
import json
import logging
import numpy as np
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from collections import deque
from scipy.stats import entropy
from sklearn.metrics.pairwise import cosine_similarity

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add src to path for energy monitor
sys.path.insert(0, str(Path(__file__).parent.parent))


@dataclass
class VectorState:
    """
    Represents the continuous state of the vector layer.
    
    All vectors are L2-normalized (||v|| = 1) to prevent drift.
    """
    identity: np.ndarray = field(default_factory=lambda: np.random.randn(768))
    goals: np.ndarray = field(default_factory=lambda: np.random.randn(768))
    context: np.ndarray = field(default_factory=lambda: np.random.randn(768))
    priorities: np.ndarray = field(default_factory=lambda: np.random.randn(768))
    risk_threshold: float = 0.7
    
    def __post_init__(self):
        """Normalize all vectors after initialization"""
        self.identity = self._normalize(self.identity)
        self.goals = self._normalize(self.goals)
        self.context = self._normalize(self.context)
        self.priorities = self._normalize(self.priorities)
    
    @staticmethod
    def _normalize(vec: np.ndarray) -> np.ndarray:
        """L2 normalize a vector"""
        norm = np.linalg.norm(vec)
        if norm < 1e-10:
            # Avoid division by zero - return random normalized vector
            vec = np.random.randn(len(vec))
            norm = np.linalg.norm(vec)
        return vec / norm
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'identity': self.identity.tolist(),
            'goals': self.goals.tolist(),
            'context': self.context.tolist(),
            'priorities': self.priorities.tolist(),
            'risk_threshold': self.risk_threshold
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VectorState':
        """Load from dictionary"""
        return cls(
            identity=np.array(data['identity']),
            goals=np.array(data['goals']),
            context=np.array(data['context']),
            priorities=np.array(data['priorities']),
            risk_threshold=data['risk_threshold']
        )


class VectorLayer:
    """
    Vector Layer - Continuous subsymbolic processing component
    
    Implements:
    - Sentence encoding via transformer models
    - Similarity-based context retrieval
    - Hebbian-like state updates
    - Vector drift prevention
    - Energy-efficient operations
    - State persistence
    """
    
    # Energy costs (Wh per operation)
    VECTOR_ENCODE_WH = 0.00001      # 10 µWh per encoding
    VECTOR_SIMILARITY_WH = 0.0000003  # 0.3 µWh per similarity check
    
    # Learning and drift parameters
    DEFAULT_LEARNING_RATE = 0.01
    MAX_VECTOR_NORM = 1.5
    MIN_ENTROPY = 3.0
    
    def __init__(self, 
                 model_name: str = "sentence-transformers/all-mpnet-base-v2",
                 state_path: str = "data/vector_layer_state.json",
                 memory_size: int = 1000):
        """
        Initialize the vector layer
        
        Args:
            model_name: Sentence transformer model name
            state_path: Path to save/load state
            memory_size: Size of memory ring buffer
        """
        self.model_name = model_name
        self.state_path = Path(state_path)
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.memory_size = memory_size
        
        # Initialize encoder
        logger.info(f"Initializing vector layer with model: {model_name}")
        try:
            from sentence_transformers import SentenceTransformer
            self.encoder = SentenceTransformer(model_name)
            logger.info("Sentence transformer loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load sentence transformer: {e}")
            raise
        
        # Memory bank - ring buffer of past action vectors (initialize before loading state)
        self.memory = deque(maxlen=memory_size)
        
        # Update counters (initialize before loading state)
        self.update_count = 0
        
        # Initialize or load state
        if self.state_path.exists():
            try:
                self.state = self.load_state()
                logger.info(f"Loaded existing state from {self.state_path}")
            except Exception as e:
                logger.warning(f"Failed to load state: {e}. Creating new state.")
                self.state = VectorState()
        else:
            self.state = VectorState()
            logger.info("Created new vector state")
        
        # Initialize energy monitor
        try:
            from energy_monitor import EnergyMonitor
            self.energy_monitor = EnergyMonitor()
            logger.info("Energy monitor initialized for vector layer")
        except Exception as e:
            logger.warning(f"Could not initialize energy monitor: {e}")
            self.energy_monitor = None
        
        # Auto-save interval
        self.auto_save_interval = 100
    
    def encode(self, text: str) -> np.ndarray:
        """
        Encode text to vector
        
        Args:
            text: Input text
            
        Returns:
            768D normalized embedding vector
        """
        # Log energy consumption
        if self.energy_monitor:
            self.energy_monitor.log_operation(
                operation_type='vector_encode',
                duration_sec=0.001,  # ~1ms encoding time
                watts=10.0,  # Encoding power
                details={'text_length': len(text)}
            )
        
        # Encode
        vec = self.encoder.encode(text, convert_to_numpy=True)
        
        # Normalize
        vec = vec / np.linalg.norm(vec)
        
        return vec
    
    def query_similar(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Query vector layer for similar memories and compute context
        
        Args:
            query: Query string
            top_k: Number of top similar memories to retrieve
            
        Returns:
            Dictionary with priority_score, risk_assessment, goal_alignment,
            suggested_direction, and similar_memories
        """
        # Log energy consumption
        if self.energy_monitor:
            self.energy_monitor.log_vector_similarity(count=1)
        
        # Encode query
        query_vec = self.encode(query)
        
        # Compute similarities with state components
        identity_sim = float(cosine_similarity([query_vec], [self.state.identity])[0][0])
        goal_sim = float(cosine_similarity([query_vec], [self.state.goals])[0][0])
        context_sim = float(cosine_similarity([query_vec], [self.state.context])[0][0])
        priority_sim = float(cosine_similarity([query_vec], [self.state.priorities])[0][0])
        
        # Retrieve similar memories
        similar_memories = []
        if len(self.memory) > 0:
            memory_array = np.array(list(self.memory))
            similarities = cosine_similarity([query_vec], memory_array)[0]
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            similar_memories = [
                {
                    'index': int(idx),
                    'similarity': float(similarities[idx])
                }
                for idx in top_indices
            ]
        
        # Compute derived metrics
        priority_score = (priority_sim + 1.0) / 2.0  # Map [-1, 1] to [0, 1]
        risk_assessment = np.clip(1.0 - identity_sim, 0.0, 1.0)  # High risk when dissimilar, clipped to [0, 1]
        goal_alignment = (goal_sim + 1.0) / 2.0
        
        # Compute energy function: E(C,V) = -α₁⟨v,identity⟩ - α₂⟨v,goals⟩ + α₃⟨v,context⟩²
        alpha1, alpha2, alpha3 = 1.0, 0.8, 0.5
        energy = -alpha1 * identity_sim - alpha2 * goal_sim + alpha3 * (context_sim ** 2)
        
        # Suggested direction (gradient of energy function)
        suggested_direction = (
            alpha1 * self.state.identity + 
            alpha2 * self.state.goals - 
            2 * alpha3 * context_sim * self.state.context
        )
        suggested_direction = suggested_direction / np.linalg.norm(suggested_direction)
        
        return {
            'priority_score': priority_score,
            'risk_assessment': risk_assessment,
            'goal_alignment': goal_alignment,
            'identity_similarity': identity_sim,
            'context_similarity': context_sim,
            'energy': energy,
            'suggested_direction': suggested_direction,
            'similar_memories': similar_memories,
            'query_vector': query_vec
        }
    
    def update(self, action: str, feedback: float, learning_rate: Optional[float] = None):
        """
        Update vector state using Hebbian-like learning
        
        Args:
            action: Action text that was taken
            feedback: Feedback signal (-1.0 to 1.0, where 1.0 is positive)
            learning_rate: Learning rate (default: 0.01)
        """
        if learning_rate is None:
            learning_rate = self.DEFAULT_LEARNING_RATE
        
        # Encode action
        action_vec = self.encode(action)
        
        # Add to memory
        self.memory.append(action_vec)
        
        # Hebbian update: state += α · outer(action_vec, state).mean()
        # Simplified to: state += α · action_vec (weighted by feedback)
        update_strength = learning_rate * feedback
        
        # Update state components with decay toward action
        self.state.goals = self.state.goals + update_strength * (action_vec - self.state.goals)
        self.state.context = 0.9 * self.state.context + 0.1 * action_vec  # Decay old context
        self.state.priorities = self.state.priorities + 0.5 * update_strength * action_vec
        
        # Renormalize to prevent drift
        self.state.goals = self._normalize_vector(self.state.goals)
        self.state.context = self._normalize_vector(self.state.context)
        self.state.priorities = self._normalize_vector(self.state.priorities)
        
        # Check for drift
        self._check_drift()
        
        # Auto-save periodically
        self.update_count += 1
        if self.update_count % self.auto_save_interval == 0:
            self.save_state()
            logger.info(f"Auto-saved state after {self.update_count} updates")
    
    def _normalize_vector(self, vec: np.ndarray) -> np.ndarray:
        """Normalize vector with safety checks"""
        norm = np.linalg.norm(vec)
        if norm < 1e-10:
            logger.warning("Vector norm too small, reinitializing")
            vec = np.random.randn(len(vec))
            norm = np.linalg.norm(vec)
        return vec / norm
    
    def _check_drift(self):
        """Check for vector drift and semantic collapse"""
        # Check magnitude drift
        identity_norm = np.linalg.norm(self.state.identity)
        goals_norm = np.linalg.norm(self.state.goals)
        context_norm = np.linalg.norm(self.state.context)
        priorities_norm = np.linalg.norm(self.state.priorities)
        
        if any(norm > self.MAX_VECTOR_NORM for norm in [identity_norm, goals_norm, context_norm, priorities_norm]):
            logger.warning(f"Vector drift detected! Norms: identity={identity_norm:.3f}, goals={goals_norm:.3f}")
            # Renormalize
            self.state.identity = self._normalize_vector(self.state.identity)
            self.state.goals = self._normalize_vector(self.state.goals)
            self.state.context = self._normalize_vector(self.state.context)
            self.state.priorities = self._normalize_vector(self.state.priorities)
        
        # Check semantic collapse (low entropy)
        # Compute entropy of goal vector (binned into 10 bins)
        hist, _ = np.histogram(self.state.goals, bins=10)
        hist = hist / hist.sum()  # Normalize
        goal_entropy = entropy(hist)
        
        if goal_entropy < self.MIN_ENTROPY:
            logger.warning(f"Semantic collapse detected! Goal entropy: {goal_entropy:.3f}")
            # Add small noise to prevent collapse
            noise = np.random.randn(len(self.state.goals)) * 0.01
            self.state.goals = self._normalize_vector(self.state.goals + noise)
    
    def save_state(self, filepath: Optional[str] = None):
        """
        Save vector state to file
        
        Args:
            filepath: Optional custom filepath
        """
        save_path = Path(filepath) if filepath else self.state_path
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        state_dict = {
            'state': self.state.to_dict(),
            'memory': [vec.tolist() for vec in self.memory],
            'update_count': self.update_count,
            'model_name': self.model_name
        }
        
        with open(save_path, 'w') as f:
            json.dump(state_dict, f, indent=2)
        
        logger.info(f"Saved vector state to {save_path}")
    
    def load_state(self, filepath: Optional[str] = None) -> VectorState:
        """
        Load vector state from file
        
        Args:
            filepath: Optional custom filepath
            
        Returns:
            Loaded VectorState
        """
        load_path = Path(filepath) if filepath else self.state_path
        
        with open(load_path, 'r') as f:
            state_dict = json.load(f)
        
        # Load state
        state = VectorState.from_dict(state_dict['state'])
        
        # Load memory
        if 'memory' in state_dict:
            self.memory = deque(
                [np.array(vec) for vec in state_dict['memory']],
                maxlen=self.memory_size
            )
        
        # Load update count
        if 'update_count' in state_dict:
            self.update_count = state_dict['update_count']
        
        logger.info(f"Loaded vector state from {load_path}")
        return state
    
    def reset_state(self):
        """Reset vector state to random initialization"""
        self.state = VectorState()
        self.memory.clear()
        self.update_count = 0
        logger.info("Vector state reset")
    
    def get_state_summary(self) -> Dict[str, Any]:
        """Get summary of current state"""
        return {
            'identity_norm': float(np.linalg.norm(self.state.identity)),
            'goals_norm': float(np.linalg.norm(self.state.goals)),
            'context_norm': float(np.linalg.norm(self.state.context)),
            'priorities_norm': float(np.linalg.norm(self.state.priorities)),
            'risk_threshold': self.state.risk_threshold,
            'memory_size': len(self.memory),
            'update_count': self.update_count
        }
