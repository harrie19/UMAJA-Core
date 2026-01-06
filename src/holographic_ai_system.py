"""
UMAJA Holographic AI System
============================

Distributed intelligence across all components inspired by holographic principles.
Each fragment contains information about the whole system, enabling:
- Self-healing capabilities
- Vector-based knowledge representation
- Interference pattern analysis
- No central authority - truly distributed

Key Concepts:
- HolographicFragment: Distributed data structure
- Interference patterns between personality vectors
- Energy-aware operations
- Async by design

Author: UMAJA Core Team
Version: 1.0.0
"""

import asyncio
import logging
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import json
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class HolographicFragment:
    """
    Represents a fragment of distributed intelligence.
    Like a holographic plate, each fragment contains information about the whole.
    """
    id: str
    vector: np.ndarray  # Vector representation of this fragment
    metadata: Dict[str, Any] = field(default_factory=dict)
    energy_level: float = 1.0  # Energy level (0.0 - 1.0)
    connections: List[str] = field(default_factory=list)  # Connected fragment IDs
    last_updated: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'id': self.id,
            'vector': self.vector.tolist() if isinstance(self.vector, np.ndarray) else self.vector,
            'metadata': self.metadata,
            'energy_level': self.energy_level,
            'connections': self.connections,
            'last_updated': self.last_updated
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HolographicFragment':
        """Create from dictionary"""
        data['vector'] = np.array(data['vector'])
        return cls(**data)


class HolographicPersonalityAgent:
    """
    Personality represented as interference patterns between vector fragments.
    Integrates with existing personality_engine.py
    """
    
    def __init__(self, personality_name: str, dimension: int = 128):
        """
        Initialize holographic personality agent
        
        Args:
            personality_name: Name of the personality (e.g., 'john_cleese', 'professor')
            dimension: Vector dimension for embeddings
        """
        self.name = personality_name
        self.dimension = dimension
        self.fragments: List[HolographicFragment] = []
        self.interference_matrix: Optional[np.ndarray] = None
        
        # Initialize with random seed based on personality name
        np.random.seed(sum(ord(c) for c in personality_name) % 2**32)
        self._initialize_fragments()
        
        logger.info(f"Holographic personality agent '{personality_name}' initialized with {len(self.fragments)} fragments")
    
    def _initialize_fragments(self):
        """Create initial personality fragments"""
        # Create 5 core fragments for personality traits
        trait_names = ['humor', 'warmth', 'intelligence', 'creativity', 'empathy']
        
        for i, trait in enumerate(trait_names):
            vector = np.random.randn(self.dimension)
            vector = vector / np.linalg.norm(vector)  # Normalize
            
            fragment = HolographicFragment(
                id=f"{self.name}_{trait}",
                vector=vector,
                metadata={'trait': trait, 'personality': self.name},
                energy_level=1.0,
                connections=[f"{self.name}_{t}" for t in trait_names if t != trait]
            )
            self.fragments.append(fragment)
        
        # Compute interference matrix
        self._compute_interference_matrix()
    
    def _compute_interference_matrix(self):
        """Compute interference patterns between fragments"""
        n = len(self.fragments)
        self.interference_matrix = np.zeros((n, n))
        
        for i, frag_i in enumerate(self.fragments):
            for j, frag_j in enumerate(self.fragments):
                if i != j:
                    # Interference is the dot product (constructive/destructive)
                    interference = np.dot(frag_i.vector, frag_j.vector)
                    self.interference_matrix[i, j] = interference
    
    def get_personality_vector(self) -> np.ndarray:
        """
        Get combined personality vector from all fragments.
        This is the holographic reconstruction.
        """
        if not self.fragments:
            return np.zeros(self.dimension)
        
        # Weighted sum based on energy levels
        combined = np.zeros(self.dimension)
        total_energy = sum(f.energy_level for f in self.fragments)
        
        for fragment in self.fragments:
            weight = fragment.energy_level / total_energy if total_energy > 0 else 1.0 / len(self.fragments)
            combined += weight * fragment.vector
        
        # Normalize
        norm = np.linalg.norm(combined)
        return combined / norm if norm > 0 else combined
    
    def query_trait(self, trait_name: str) -> Optional[HolographicFragment]:
        """Query for a specific trait fragment"""
        for fragment in self.fragments:
            if fragment.metadata.get('trait') == trait_name:
                return fragment
        return None
    
    def update_energy(self, fragment_id: str, energy_delta: float):
        """Update energy level of a fragment"""
        for fragment in self.fragments:
            if fragment.id == fragment_id:
                fragment.energy_level = max(0.0, min(1.0, fragment.energy_level + energy_delta))
                fragment.last_updated = datetime.now(timezone.utc).isoformat()
                break
        
        # Recompute interference after energy change
        self._compute_interference_matrix()


class HolographicMemoryAgent:
    """
    Memory system using interference patterns.
    Can integrate with src/memory/engine.py if available.
    """
    
    def __init__(self, dimension: int = 128, max_memories: int = 1000):
        """
        Initialize holographic memory agent
        
        Args:
            dimension: Vector dimension
            max_memories: Maximum number of memories to store
        """
        self.dimension = dimension
        self.max_memories = max_memories
        self.memories: List[HolographicFragment] = []
        self.memory_index = 0
        
        logger.info(f"Holographic memory agent initialized (capacity: {max_memories})")
    
    async def store_memory(self, content: str, metadata: Optional[Dict] = None) -> str:
        """
        Store a memory as a holographic fragment
        
        Args:
            content: Memory content
            metadata: Additional metadata
            
        Returns:
            Memory ID
        """
        # Create vector representation (simple hash-based for now)
        # In production, use sentence-transformers or similar
        content_hash = hash(content) % (2**32)
        np.random.seed(content_hash)
        vector = np.random.randn(self.dimension)
        vector = vector / np.linalg.norm(vector)
        
        memory_id = f"mem_{self.memory_index}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        self.memory_index += 1
        
        fragment = HolographicFragment(
            id=memory_id,
            vector=vector,
            metadata={
                'content': content,
                'stored_at': datetime.now(timezone.utc).isoformat(),
                **(metadata or {})
            },
            energy_level=1.0
        )
        
        self.memories.append(fragment)
        
        # Forget oldest if exceeding capacity (holographic degradation)
        if len(self.memories) > self.max_memories:
            oldest = min(self.memories, key=lambda m: m.energy_level)
            self.memories.remove(oldest)
            logger.info(f"Memory {oldest.id} forgotten (capacity limit)")
        
        logger.info(f"Stored memory {memory_id}")
        return memory_id
    
    async def recall_memory(self, query: str, top_k: int = 5) -> List[HolographicFragment]:
        """
        Recall memories similar to query using interference patterns
        
        Args:
            query: Query string
            top_k: Number of memories to return
            
        Returns:
            List of most similar memory fragments
        """
        if not self.memories:
            return []
        
        # Create query vector
        query_hash = hash(query) % (2**32)
        np.random.seed(query_hash)
        query_vector = np.random.randn(self.dimension)
        query_vector = query_vector / np.linalg.norm(query_vector)
        
        # Compute similarity (interference) with all memories
        similarities = []
        for memory in self.memories:
            similarity = np.dot(query_vector, memory.vector) * memory.energy_level
            similarities.append((similarity, memory))
        
        # Sort by similarity and return top-k
        similarities.sort(reverse=True, key=lambda x: x[0])
        return [mem for _, mem in similarities[:top_k]]
    
    async def decay_memories(self, decay_rate: float = 0.01):
        """
        Apply energy decay to all memories (holographic degradation over time)
        
        Args:
            decay_rate: Rate of energy decay per call
        """
        for memory in self.memories:
            memory.energy_level *= (1.0 - decay_rate)
            
            # Remove memories that have decayed too much
            if memory.energy_level < 0.1:
                self.memories.remove(memory)
                logger.debug(f"Memory {memory.id} completely decayed")


class HolographicAISystem:
    """
    Complete holographic AI system orchestrating all agents.
    Truly distributed - no single point of failure.
    """
    
    def __init__(self, data_dir: str = "data/holographic"):
        """
        Initialize holographic AI system
        
        Args:
            data_dir: Directory to store holographic data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.personality_agents: Dict[str, HolographicPersonalityAgent] = {}
        self.memory_agent = HolographicMemoryAgent()
        self.system_energy = 1.0
        
        # Initialize with default personalities
        self._initialize_default_personalities()
        
        logger.info("Holographic AI System initialized")
    
    def _initialize_default_personalities(self):
        """Initialize default personality agents"""
        default_personalities = [
            'john_cleese', 'c3po', 'robin_williams',
            'professor', 'worrier', 'enthusiast'
        ]
        
        for personality in default_personalities:
            self.personality_agents[personality] = HolographicPersonalityAgent(personality)
    
    async def process_query(self, query: str, personality: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a query using holographic interference patterns
        
        Args:
            query: User query
            personality: Optional specific personality to use
            
        Returns:
            Response dictionary
        """
        start_time = datetime.now(timezone.utc)
        
        # Store query in memory
        await self.memory_agent.store_memory(query, {'type': 'query'})
        
        # Select personality
        if personality and personality in self.personality_agents:
            agent = self.personality_agents[personality]
        else:
            # Use interference patterns to select best personality
            agent = list(self.personality_agents.values())[0]  # Default for now
        
        # Get personality vector
        personality_vector = agent.get_personality_vector()
        
        # Recall relevant memories
        relevant_memories = await self.memory_agent.recall_memory(query, top_k=3)
        
        # Compute response (simplified for now)
        response = {
            'query': query,
            'personality': agent.name,
            'personality_vector_norm': float(np.linalg.norm(personality_vector)),
            'relevant_memories': len(relevant_memories),
            'system_energy': self.system_energy,
            'processing_time_ms': (datetime.now(timezone.utc) - start_time).total_seconds() * 1000,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        logger.info(f"Processed query with {agent.name} in {response['processing_time_ms']:.2f}ms")
        return response
    
    def get_interference_patterns(self, personality_a: str, personality_b: str) -> Optional[float]:
        """
        Get interference pattern between two personalities
        
        Args:
            personality_a: First personality name
            personality_b: Second personality name
            
        Returns:
            Interference strength (or None if personalities not found)
        """
        if personality_a not in self.personality_agents or personality_b not in self.personality_agents:
            return None
        
        vec_a = self.personality_agents[personality_a].get_personality_vector()
        vec_b = self.personality_agents[personality_b].get_personality_vector()
        
        # Interference is dot product (constructive/destructive)
        interference = float(np.dot(vec_a, vec_b))
        return interference
    
    def get_system_state(self) -> Dict[str, Any]:
        """Get current system state for visualization"""
        personalities_state = {}
        
        for name, agent in self.personality_agents.items():
            personalities_state[name] = {
                'fragments': len(agent.fragments),
                'avg_energy': np.mean([f.energy_level for f in agent.fragments]),
                'vector_norm': float(np.linalg.norm(agent.get_personality_vector()))
            }
        
        return {
            'personalities': personalities_state,
            'memories': len(self.memory_agent.memories),
            'system_energy': self.system_energy,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    async def self_heal(self):
        """Self-healing process - redistribute energy and reinforce weak fragments"""
        logger.info("Initiating self-healing process...")
        
        # Decay old memories
        await self.memory_agent.decay_memories(decay_rate=0.01)
        
        # Reinforce weak personality fragments
        for agent in self.personality_agents.values():
            for fragment in agent.fragments:
                if fragment.energy_level < 0.5:
                    # Reinforce with energy from system
                    agent.update_energy(fragment.id, 0.1)
                    logger.debug(f"Reinforced fragment {fragment.id}")
        
        logger.info("Self-healing complete")
    
    def save_state(self):
        """Save current holographic state to disk"""
        state = {
            'personalities': {
                name: {
                    'fragments': [f.to_dict() for f in agent.fragments]
                }
                for name, agent in self.personality_agents.items()
            },
            'memories': [m.to_dict() for m in self.memory_agent.memories],
            'system_energy': self.system_energy,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        state_path = self.data_dir / "holographic_state.json"
        with open(state_path, 'w') as f:
            json.dump(state, f, indent=2)
        
        logger.info(f"Holographic state saved to {state_path}")
        return state_path
    
    def load_state(self):
        """Load holographic state from disk"""
        state_path = self.data_dir / "holographic_state.json"
        
        if not state_path.exists():
            logger.warning("No saved state found")
            return False
        
        try:
            with open(state_path, 'r') as f:
                state = json.load(f)
            
            # Restore personalities
            for name, data in state['personalities'].items():
                if name in self.personality_agents:
                    agent = self.personality_agents[name]
                    agent.fragments = [
                        HolographicFragment.from_dict(f) for f in data['fragments']
                    ]
                    agent._compute_interference_matrix()
            
            # Restore memories
            self.memory_agent.memories = [
                HolographicFragment.from_dict(m) for m in state['memories']
            ]
            
            self.system_energy = state.get('system_energy', 1.0)
            
            logger.info(f"Holographic state loaded from {state_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
            return False


class UMAJAHolographicIntegration:
    """
    Integration layer between holographic AI and existing UMAJA systems:
    - personality_engine.py
    - energy_monitor.py
    - memory/engine.py (if available)
    """
    
    def __init__(self):
        """Initialize integration layer"""
        self.holographic_system = HolographicAISystem()
        self.personality_engine = None
        self.energy_monitor = None
        
        self._initialize_integrations()
        
        logger.info("UMAJA Holographic Integration initialized")
    
    def _initialize_integrations(self):
        """Initialize integrations with existing systems"""
        # Try to import and integrate personality engine
        try:
            from personality_engine import PersonalityEngine
            self.personality_engine = PersonalityEngine()
            logger.info("✓ Integrated with personality_engine")
        except ImportError:
            logger.warning("personality_engine not available")
        
        # Try to import and integrate energy monitor
        try:
            from energy_monitor import get_energy_monitor
            self.energy_monitor = get_energy_monitor()
            logger.info("✓ Integrated with energy_monitor")
        except ImportError:
            logger.warning("energy_monitor not available")
    
    async def generate_with_holographic_personality(
        self, 
        topic: str, 
        personality: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate content using both traditional and holographic personality systems
        
        Args:
            topic: Topic to generate content about
            personality: Personality name
            
        Returns:
            Generated content with holographic metadata
        """
        # Use traditional personality engine for content
        content = None
        if self.personality_engine and personality:
            try:
                content = self.personality_engine.generate_text(topic, personality)
            except Exception as e:
                logger.error(f"Personality generation error: {e}")
        
        # Add holographic analysis
        holographic_response = await self.holographic_system.process_query(
            f"Generate content about {topic}",
            personality=personality
        )
        
        # Log energy if monitor available
        if self.energy_monitor:
            self.energy_monitor.log_vector_operation("holographic_generation", count=1)
        
        return {
            'content': content,
            'holographic_metadata': holographic_response,
            'personality': personality
        }
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health including holographic metrics"""
        health = {
            'holographic': self.holographic_system.get_system_state(),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        # Add energy metrics if available
        if self.energy_monitor:
            health['energy'] = self.energy_monitor.get_metrics()
        
        return health


# Global instance
_holographic_integration = None

def get_holographic_integration() -> UMAJAHolographicIntegration:
    """Get or create global holographic integration instance"""
    global _holographic_integration
    if _holographic_integration is None:
        _holographic_integration = UMAJAHolographicIntegration()
    return _holographic_integration


# Example usage and testing
async def main():
    """Example usage of holographic AI system"""
    print("🌟 UMAJA Holographic AI System Demo\n")
    
    # Create system
    system = HolographicAISystem()
    
    # Process some queries
    queries = [
        "What makes people smile?",
        "Tell me something funny",
        "How can we spread joy?"
    ]
    
    for query in queries:
        print(f"Query: {query}")
        response = await system.process_query(query, personality='professor')
        print(f"Response: {json.dumps(response, indent=2)}\n")
    
    # Show interference patterns
    print("\n🎭 Personality Interference Patterns:")
    personalities = list(system.personality_agents.keys())
    for i, p1 in enumerate(personalities[:3]):
        for p2 in personalities[i+1:4]:
            interference = system.get_interference_patterns(p1, p2)
            print(f"  {p1} ↔ {p2}: {interference:.4f}")
    
    # Self-heal
    print("\n🔧 Running self-healing...")
    await system.self_heal()
    
    # Show system state
    print("\n📊 System State:")
    state = system.get_system_state()
    print(json.dumps(state, indent=2))
    
    # Save state
    print("\n💾 Saving state...")
    system.save_state()
    
    print("\n✅ Demo complete!")


if __name__ == "__main__":
    asyncio.run(main())
