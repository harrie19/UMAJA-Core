"""
Base Vector Agent - Foundation for self-spawning, vector-based AI agents

Implements the philosophy from docs/VECTOR_AGENTS.md:
- Agents as vectors navigating semantic space
- Signal/noise balance for creativity
- Vector-based communication
- Self-replication and merging capabilities
"""

import numpy as np
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import uuid

# Import existing UMAJA infrastructure
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from vektor_analyzer import VektorAnalyzer
from energy_monitor import get_energy_monitor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class VectorAgentState:
    """State of a vector agent in semantic space"""
    position: np.ndarray  # Current position in vector space
    velocity: np.ndarray  # Learning direction
    memory: List[np.ndarray] = field(default_factory=list)  # Past interaction vectors
    tasks_completed: int = 0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    last_active: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class VectorAgent:
    """
    Base Vector Agent - Navigates semantic space using vectors
    
    Philosophy (from VECTOR_AGENTS.md):
    - Agent is NOT a traditional program
    - Agent is a vector entity searching for information in noise
    - Communication happens through vector similarity
    - Creativity emerges from signal + noise balance
    """
    
    # Default signal/noise balance (70% signal, 30% noise for most agents)
    DEFAULT_SIGNAL_WEIGHT = 0.7
    DEFAULT_NOISE_WEIGHT = 0.3
    
    def __init__(
        self,
        agent_id: Optional[str] = None,
        core_vector: Optional[np.ndarray] = None,
        signal_weight: float = DEFAULT_SIGNAL_WEIGHT,
        noise_weight: float = DEFAULT_NOISE_WEIGHT,
        competence_description: str = "General purpose agent",
        analyzer: Optional[VektorAnalyzer] = None
    ):
        """
        Initialize a Vector Agent
        
        Args:
            agent_id: Unique identifier (auto-generated if None)
            core_vector: Base personality embedding (computed from competence_description if None)
            signal_weight: How much structure/order (0-1)
            noise_weight: How much creativity/chaos (0-1)
            competence_description: Text description of agent's competence
            analyzer: VektorAnalyzer instance (created if None)
        """
        self.agent_id = agent_id or f"vector_agent_{uuid.uuid4().hex[:8]}"
        
        # Initialize vector analyzer
        self.analyzer = analyzer or VektorAnalyzer()
        
        # Energy monitoring
        self.energy_monitor = get_energy_monitor()
        
        # Compute core vector from competence description
        if core_vector is None:
            core_vector = self.analyzer.encode_texts([competence_description])[0]
        
        self.competence_description = competence_description
        self.competence_vector = core_vector
        
        # Signal/noise weights
        self.signal_weight = signal_weight
        self.noise_weight = noise_weight
        
        # Initialize state
        self.state = VectorAgentState(
            position=core_vector.copy(),
            velocity=np.zeros_like(core_vector)
        )
        
        logger.info(
            f"🌌 VectorAgent '{self.agent_id}' spawned at position in semantic space "
            f"(signal: {signal_weight:.1%}, noise: {noise_weight:.1%})"
        )
        
        # Log energy-efficient creation
        self.energy_monitor.log_vector_operation(
            operation="agent_spawn",
            count=1,
            details={
                "agent_id": self.agent_id,
                "competence": competence_description
            }
        )
    
    def can_handle(self, task: str, threshold: float = 0.7) -> Tuple[bool, float]:
        """
        Determine if this agent can handle a task using cosine similarity
        
        Args:
            task: Task description as text
            threshold: Minimum similarity to handle task (0-1)
            
        Returns:
            Tuple of (can_handle, similarity_score)
        """
        # Encode task as vector
        task_vector = self.analyzer.encode_texts([task])[0]
        
        # Calculate similarity between task and agent's competence
        similarity = self.analyzer.cosine_similarity(
            self.competence_vector,
            task_vector
        )
        
        # Log energy-efficient vector operation
        self.energy_monitor.log_vector_operation(
            operation="can_handle_check",
            count=1,
            details={
                "agent_id": self.agent_id,
                "task": task[:50],
                "similarity": float(similarity)
            }
        )
        
        can_do = similarity >= threshold
        
        if can_do:
            logger.info(
                f"✅ Agent '{self.agent_id}' CAN handle task "
                f"(similarity: {similarity:.3f})"
            )
        else:
            logger.debug(
                f"❌ Agent '{self.agent_id}' cannot handle task "
                f"(similarity: {similarity:.3f} < {threshold})"
            )
        
        return can_do, float(similarity)
    
    def _generate_contextual_noise(self, creativity: float) -> np.ndarray:
        """
        Generate contextual noise vector for creativity
        
        Args:
            creativity: Noise level (0-1)
            
        Returns:
            Noise vector of same dimensionality as position
        """
        # Generate random noise with same shape as position
        noise = np.random.randn(*self.state.position.shape)
        
        # Normalize and scale by creativity
        noise = noise / (np.linalg.norm(noise) + 1e-10)
        noise = noise * creativity
        
        return noise
    
    def process_task(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a task using vector-based approach
        
        This is the core method where:
        1. Signal (task) is encoded
        2. Noise (creativity) is added
        3. Information emerges from signal + noise
        4. Result is validated
        
        Args:
            task: Task description
            context: Optional context dictionary
            
        Returns:
            Dictionary with result and metadata
        """
        # Step 1: Capture signal (task vector)
        signal_vector = self.analyzer.encode_texts([task])[0]
        
        # Step 2: Generate noise for creativity
        noise_vector = self._generate_contextual_noise(self.noise_weight)
        
        # Step 3: Combine signal and noise
        result_vector = (
            self.signal_weight * signal_vector +
            self.noise_weight * noise_vector
        )
        
        # Normalize result vector
        result_vector = result_vector / (np.linalg.norm(result_vector) + 1e-10)
        
        # Step 4: Update agent state (learning)
        self._update_state(signal_vector, result_vector)
        
        # Step 5: Validate quality (is it understandable?)
        quality_score = self.analyzer.cosine_similarity(
            result_vector,
            signal_vector
        )
        
        # Log the operation
        self.energy_monitor.log_vector_operation(
            operation="process_task",
            count=1,
            details={
                "agent_id": self.agent_id,
                "task": task[:50],
                "quality_score": float(quality_score)
            }
        )
        
        self.state.tasks_completed += 1
        self.state.last_active = datetime.utcnow().isoformat()
        
        return {
            "success": True,
            "agent_id": self.agent_id,
            "result_vector": result_vector,
            "quality_score": float(quality_score),
            "signal_weight": self.signal_weight,
            "noise_weight": self.noise_weight,
            "tasks_completed": self.state.tasks_completed
        }
    
    def _update_state(self, input_vector: np.ndarray, output_vector: np.ndarray):
        """
        Update agent state based on task processing (learning)
        
        Args:
            input_vector: Input task vector
            output_vector: Output result vector
        """
        # Calculate learning direction (velocity)
        learning_direction = output_vector - self.state.position
        
        # Update velocity (momentum-based learning)
        learning_rate = 0.1
        momentum = 0.9
        self.state.velocity = (
            momentum * self.state.velocity +
            learning_rate * learning_direction
        )
        
        # Update position (agent moves through semantic space)
        self.state.position += self.state.velocity
        
        # Normalize position to stay on unit sphere
        self.state.position = self.state.position / (
            np.linalg.norm(self.state.position) + 1e-10
        )
        
        # Add to memory (keep last 10 interactions)
        self.state.memory.append(input_vector)
        if len(self.state.memory) > 10:
            self.state.memory.pop(0)
    
    def communicate_with(self, other_agent: 'VectorAgent') -> Dict[str, Any]:
        """
        Communicate with another agent via vectors
        
        Communication = cosine similarity between agent positions
        
        Args:
            other_agent: Another VectorAgent instance
            
        Returns:
            Dictionary with communication metrics
        """
        # Calculate similarity between agent positions
        similarity = self.analyzer.cosine_similarity(
            self.state.position,
            other_agent.state.position
        )
        
        # Calculate alignment of competencies
        competence_similarity = self.analyzer.cosine_similarity(
            self.competence_vector,
            other_agent.competence_vector
        )
        
        # Log energy-efficient vector communication
        self.energy_monitor.log_vector_operation(
            operation="agent_communication",
            count=1,
            details={
                "agent1_id": self.agent_id,
                "agent2_id": other_agent.agent_id,
                "similarity": float(similarity),
                "competence_similarity": float(competence_similarity)
            }
        )
        
        logger.info(
            f"💬 Communication: '{self.agent_id}' <-> '{other_agent.agent_id}' "
            f"(similarity: {similarity:.3f})"
        )
        
        return {
            "similarity": float(similarity),
            "competence_similarity": float(competence_similarity),
            "aligned": similarity > 0.8,
            "complementary": competence_similarity < 0.3
        }
    
    def clone(self) -> 'VectorAgent':
        """
        Clone this agent (self-replication)
        
        Creates a new agent with similar but slightly varied characteristics
        
        Returns:
            New VectorAgent instance (child)
        """
        # Add small mutation to core vector for diversity
        mutation = np.random.randn(*self.competence_vector.shape) * 0.1
        mutated_vector = self.competence_vector + mutation
        mutated_vector = mutated_vector / (np.linalg.norm(mutated_vector) + 1e-10)
        
        # Create child agent
        child = VectorAgent(
            agent_id=f"{self.agent_id}_clone_{uuid.uuid4().hex[:4]}",
            core_vector=mutated_vector,
            signal_weight=self.signal_weight,
            noise_weight=self.noise_weight,
            competence_description=f"{self.competence_description} (cloned)",
            analyzer=self.analyzer
        )
        
        # Inherit some memory
        child.state.memory = self.state.memory[-3:].copy() if len(self.state.memory) >= 3 else []
        
        logger.info(f"🧬 Agent '{self.agent_id}' cloned -> '{child.agent_id}'")
        
        return child
    
    def merge_with(self, other_agent: 'VectorAgent') -> 'VectorAgent':
        """
        Merge with another agent to combine capabilities
        
        Creates a new agent that blends characteristics of both parents
        
        Args:
            other_agent: Another VectorAgent to merge with
            
        Returns:
            New VectorAgent instance (merged child)
        """
        # Blend competence vectors (weighted average)
        merged_vector = (
            0.5 * self.competence_vector +
            0.5 * other_agent.competence_vector
        )
        merged_vector = merged_vector / (np.linalg.norm(merged_vector) + 1e-10)
        
        # Blend signal/noise weights
        merged_signal = (self.signal_weight + other_agent.signal_weight) / 2
        merged_noise = (self.noise_weight + other_agent.noise_weight) / 2
        
        # Create merged agent
        merged = VectorAgent(
            agent_id=f"merged_{uuid.uuid4().hex[:8]}",
            core_vector=merged_vector,
            signal_weight=merged_signal,
            noise_weight=merged_noise,
            competence_description=f"Merged: {self.competence_description} + {other_agent.competence_description}",
            analyzer=self.analyzer
        )
        
        # Combine memories (take best from both)
        combined_memory = self.state.memory + other_agent.state.memory
        merged.state.memory = combined_memory[-10:]  # Keep last 10
        
        logger.info(
            f"🔀 Agents '{self.agent_id}' + '{other_agent.agent_id}' "
            f"merged -> '{merged.agent_id}'"
        )
        
        return merged
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current agent status
        
        Returns:
            Dictionary with agent status and metrics
        """
        return {
            "agent_id": self.agent_id,
            "competence": self.competence_description,
            "signal_weight": self.signal_weight,
            "noise_weight": self.noise_weight,
            "tasks_completed": self.state.tasks_completed,
            "memory_size": len(self.state.memory),
            "created_at": self.state.created_at,
            "last_active": self.state.last_active,
            "position_norm": float(np.linalg.norm(self.state.position)),
            "velocity_norm": float(np.linalg.norm(self.state.velocity))
        }


def main():
    """Example usage of VectorAgent"""
    print("=" * 70)
    print("🌌 UMAJA Vector Agent System - Base Agent Demo")
    print("=" * 70)
    print()
    
    # Create a general agent
    agent1 = VectorAgent(
        competence_description="General problem solving and task completion"
    )
    
    print(f"✅ Created agent: {agent1.agent_id}")
    print(f"   Competence: {agent1.competence_description}")
    print(f"   Signal/Noise: {agent1.signal_weight:.1%}/{agent1.noise_weight:.1%}")
    print()
    
    # Test can_handle
    print("Testing can_handle()...")
    tasks = [
        "Solve a complex mathematical problem",
        "Write creative poetry",
        "Debug a Python program",
        "Plan a marketing campaign"
    ]
    
    for task in tasks:
        can_do, similarity = agent1.can_handle(task)
        print(f"  Task: {task}")
        print(f"  -> Can handle: {can_do}, Similarity: {similarity:.3f}")
    
    print()
    
    # Process a task
    print("Processing task...")
    result = agent1.process_task("Solve a general problem")
    print(f"  Result: {result['success']}")
    print(f"  Quality: {result['quality_score']:.3f}")
    print(f"  Tasks completed: {result['tasks_completed']}")
    print()
    
    # Create another agent
    agent2 = VectorAgent(
        competence_description="Creative writing and content generation"
    )
    
    print(f"✅ Created agent: {agent2.agent_id}")
    print()
    
    # Test communication
    print("Testing agent communication...")
    comm_result = agent1.communicate_with(agent2)
    print(f"  Similarity: {comm_result['similarity']:.3f}")
    print(f"  Aligned: {comm_result['aligned']}")
    print(f"  Complementary: {comm_result['complementary']}")
    print()
    
    # Test cloning
    print("Testing cloning...")
    clone = agent1.clone()
    print(f"  Clone ID: {clone.agent_id}")
    print(f"  Parent tasks: {agent1.state.tasks_completed}")
    print(f"  Clone tasks: {clone.state.tasks_completed}")
    print()
    
    # Test merging
    print("Testing merging...")
    merged = agent1.merge_with(agent2)
    print(f"  Merged ID: {merged.agent_id}")
    print(f"  Competence: {merged.competence_description[:60]}...")
    print()
    
    # Show final status
    print("Final Status:")
    status = agent1.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
