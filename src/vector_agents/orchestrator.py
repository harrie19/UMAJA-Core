"""
Vector Agent Orchestrator - Manages spawning and coordination of vector agents

Uses vector similarity for:
- Task decomposition
- Agent selection
- Parallel execution
- Agent communication

Does NOT modify existing agent_orchestrator.py - this is a new vector-based system
"""

import logging
import threading
import queue
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import uuid

from .base_agent import VectorAgent
from .specialized_agents import create_specialized_agent
from vektor_analyzer import VektorAnalyzer
from energy_monitor import get_energy_monitor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class VectorTask:
    """A task to be processed by vector agents"""
    task_id: str
    description: str
    task_vector: Any  # numpy array
    priority: int = 5  # 1-10
    required_agent_type: Optional[str] = None
    status: str = "pending"  # pending, assigned, running, completed, failed
    assigned_agent_id: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    def __lt__(self, other):
        """For priority queue ordering"""
        return self.priority > other.priority


class VectorAgentOrchestrator:
    """
    Orchestrates vector agents using semantic similarity
    
    Features:
    - Spawns agents on demand
    - Routes tasks using vector similarity
    - Enables agent communication
    - Parallel task execution
    - Energy-efficient (uses vectors, not LLMs)
    """
    
    def __init__(self, data_dir: str = "data/vector_agents"):
        """
        Initialize Vector Agent Orchestrator
        
        Args:
            data_dir: Directory for storing agent data
        """
        from pathlib import Path
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Vector analyzer (shared across all agents)
        self.analyzer = VektorAnalyzer()
        
        # Energy monitoring
        self.energy_monitor = get_energy_monitor()
        
        # Agent pool
        self.agents: Dict[str, VectorAgent] = {}
        
        # Task queue (priority queue)
        self.task_queue = queue.PriorityQueue()
        
        # Worker threads
        self.worker_threads: List[threading.Thread] = []
        self.running = False
        
        # Statistics
        self.stats = {
            "total_agents": 0,
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "started_at": datetime.utcnow().isoformat()
        }
        
        logger.info("🌌 VectorAgentOrchestrator initialized")
    
    def spawn_agent(
        self,
        agent_type: str,
        agent_id: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Spawn a new vector agent
        
        Args:
            agent_type: Type of agent ('research', 'code', 'creative', 'math', 'teacher')
            agent_id: Optional custom agent ID
            **kwargs: Additional arguments for agent creation
            
        Returns:
            Agent ID
        """
        try:
            agent = create_specialized_agent(
                agent_type=agent_type,
                agent_id=agent_id,
                analyzer=self.analyzer
            )
            
            self.agents[agent.agent_id] = agent
            self.stats["total_agents"] += 1
            
            logger.info(f"✨ Spawned agent: {agent.agent_id} (type: {agent_type})")
            
            return agent.agent_id
        
        except Exception as e:
            logger.error(f"Failed to spawn agent: {e}")
            raise
    
    def add_task(
        self,
        description: str,
        priority: int = 5,
        required_agent_type: Optional[str] = None
    ) -> str:
        """
        Add a task to the queue
        
        Args:
            description: Task description
            priority: Task priority (1-10, higher = more important)
            required_agent_type: Optional specific agent type required
            
        Returns:
            Task ID
        """
        # Encode task as vector
        task_vector = self.analyzer.encode_texts([description])[0]
        
        # Create task
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        task = VectorTask(
            task_id=task_id,
            description=description,
            task_vector=task_vector,
            priority=priority,
            required_agent_type=required_agent_type
        )
        
        # Add to queue
        self.task_queue.put(task)
        self.stats["total_tasks"] += 1
        
        logger.info(f"📝 Task added: {task_id} (priority: {priority})")
        
        # Log energy-efficient operation
        self.energy_monitor.log_vector_operation(
            operation="task_encode",
            count=1,
            details={"task_id": task_id, "description": description[:50]}
        )
        
        return task_id
    
    def _find_best_agent(self, task: VectorTask) -> Optional[Tuple[str, float]]:
        """
        Find the best agent for a task using vector similarity
        
        Args:
            task: VectorTask to assign
            
        Returns:
            Tuple of (agent_id, similarity_score) or None if no suitable agent
        """
        if not self.agents:
            return None
        
        # If specific agent type required, filter
        if task.required_agent_type:
            eligible_agents = {
                aid: agent for aid, agent in self.agents.items()
                if task.required_agent_type.lower() in agent.competence_description.lower()
            }
            if not eligible_agents:
                return None
        else:
            eligible_agents = self.agents
        
        # Find agent with highest similarity to task
        best_agent_id = None
        best_similarity = 0.0
        
        for agent_id, agent in eligible_agents.items():
            similarity = self.analyzer.cosine_similarity(
                agent.competence_vector,
                task.task_vector
            )
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_agent_id = agent_id
        
        if best_agent_id and best_similarity > 0.5:  # Minimum threshold
            return (best_agent_id, best_similarity)
        
        return None
    
    def _worker(self):
        """Worker thread that processes tasks"""
        while self.running:
            try:
                # Get task from queue (with timeout)
                try:
                    task = self.task_queue.get(timeout=1.0)
                except queue.Empty:
                    continue
                
                # Find best agent for task
                agent_match = self._find_best_agent(task)
                
                if not agent_match:
                    # No suitable agent, put back in queue
                    logger.warning(f"No suitable agent for task {task.task_id}")
                    task.status = "failed"
                    task.result = {"error": "No suitable agent available"}
                    self.stats["failed_tasks"] += 1
                    continue
                
                agent_id, similarity = agent_match
                agent = self.agents[agent_id]
                
                # Assign and process task
                task.status = "running"
                task.assigned_agent_id = agent_id
                task.started_at = datetime.utcnow().isoformat()
                
                logger.info(
                    f"▶️  Processing task {task.task_id} with agent {agent_id} "
                    f"(similarity: {similarity:.3f})"
                )
                
                try:
                    # Process task
                    result = agent.process_task(task.description)
                    
                    task.status = "completed"
                    task.result = result
                    task.completed_at = datetime.utcnow().isoformat()
                    self.stats["completed_tasks"] += 1
                    
                    logger.info(f"✅ Task {task.task_id} completed")
                
                except Exception as e:
                    logger.error(f"❌ Task {task.task_id} failed: {e}")
                    task.status = "failed"
                    task.result = {"error": str(e)}
                    task.completed_at = datetime.utcnow().isoformat()
                    self.stats["failed_tasks"] += 1
            
            except Exception as e:
                logger.error(f"Worker error: {e}")
                time.sleep(1)
    
    def start_workers(self, num_workers: int = 3):
        """
        Start worker threads for parallel task processing
        
        Args:
            num_workers: Number of worker threads
        """
        if self.running:
            logger.warning("Workers already running")
            return
        
        self.running = True
        
        for i in range(num_workers):
            worker = threading.Thread(
                target=self._worker,
                name=f"VectorWorker-{i}",
                daemon=True
            )
            worker.start()
            self.worker_threads.append(worker)
        
        logger.info(f"🚀 Started {num_workers} worker threads")
    
    def stop_workers(self):
        """Stop all worker threads"""
        self.running = False
        
        # Wait for workers to finish
        for worker in self.worker_threads:
            worker.join(timeout=5.0)
        
        self.worker_threads = []
        logger.info("🛑 Stopped all worker threads")
    
    def enable_agent_communication(self, agent_id1: str, agent_id2: str) -> Dict[str, Any]:
        """
        Enable communication between two agents
        
        Args:
            agent_id1: First agent ID
            agent_id2: Second agent ID
            
        Returns:
            Communication metrics
        """
        if agent_id1 not in self.agents or agent_id2 not in self.agents:
            raise ValueError("One or both agents not found")
        
        agent1 = self.agents[agent_id1]
        agent2 = self.agents[agent_id2]
        
        return agent1.communicate_with(agent2)
    
    def clone_agent(self, agent_id: str) -> str:
        """
        Clone an existing agent
        
        Args:
            agent_id: ID of agent to clone
            
        Returns:
            New agent ID
        """
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")
        
        parent = self.agents[agent_id]
        child = parent.clone()
        
        self.agents[child.agent_id] = child
        self.stats["total_agents"] += 1
        
        return child.agent_id
    
    def merge_agents(self, agent_id1: str, agent_id2: str) -> str:
        """
        Merge two agents into a new agent
        
        Args:
            agent_id1: First agent ID
            agent_id2: Second agent ID
            
        Returns:
            Merged agent ID
        """
        if agent_id1 not in self.agents or agent_id2 not in self.agents:
            raise ValueError("One or both agents not found")
        
        agent1 = self.agents[agent_id1]
        agent2 = self.agents[agent_id2]
        
        merged = agent1.merge_with(agent2)
        
        self.agents[merged.agent_id] = merged
        self.stats["total_agents"] += 1
        
        return merged.agent_id
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get orchestrator status
        
        Returns:
            Status dictionary
        """
        return {
            "stats": self.stats,
            "agents": {
                agent_id: agent.get_status()
                for agent_id, agent in self.agents.items()
            },
            "queue_size": self.task_queue.qsize(),
            "workers_running": self.running,
            "num_workers": len(self.worker_threads)
        }
    
    def decompose_complex_task(self, complex_task: str) -> List[str]:
        """
        Decompose a complex task into subtasks
        
        Uses vector space to identify logical components
        
        Args:
            complex_task: Complex task description
            
        Returns:
            List of subtask descriptions
        """
        # For now, use simple heuristic decomposition
        # In production, this could use more sophisticated NLP
        
        # Split by "and", "then", "also", etc.
        import re
        
        separators = r'\s+and\s+|\s+then\s+|\s+also\s+|\s+plus\s+|\.\s+'
        subtasks = re.split(separators, complex_task, flags=re.IGNORECASE)
        
        # Clean up subtasks
        subtasks = [s.strip() for s in subtasks if s.strip()]
        
        if len(subtasks) <= 1:
            # Task is not complex, return as-is
            return [complex_task]
        
        logger.info(f"📊 Decomposed complex task into {len(subtasks)} subtasks")
        
        return subtasks


def main():
    """Demo of VectorAgentOrchestrator"""
    print("=" * 70)
    print("🌌 UMAJA Vector Agent Orchestrator - Demo")
    print("=" * 70)
    print()
    
    # Create orchestrator
    orchestrator = VectorAgentOrchestrator()
    
    # Spawn various specialized agents
    print("Spawning agents...")
    agents = []
    for agent_type in ['research', 'code', 'creative', 'math', 'teacher']:
        agent_id = orchestrator.spawn_agent(agent_type)
        agents.append(agent_id)
        print(f"  ✅ {agent_type}: {agent_id}")
    
    print()
    
    # Add various tasks
    print("Adding tasks...")
    tasks = [
        ("Find information about quantum computing", 8, None),
        ("Write a Python function to sort a list", 7, None),
        ("Create a short poem about AI", 6, None),
        ("Calculate the integral of x^2 from 0 to 5", 9, None),
        ("Explain neural networks to a beginner", 7, None)
    ]
    
    task_ids = []
    for description, priority, agent_type in tasks:
        task_id = orchestrator.add_task(description, priority, agent_type)
        task_ids.append(task_id)
        print(f"  📝 {task_id}: {description[:50]}...")
    
    print()
    
    # Start workers
    print("Starting workers...")
    orchestrator.start_workers(num_workers=3)
    
    # Wait for tasks to complete
    print("Processing tasks...")
    time.sleep(5)  # Give time for tasks to process
    
    # Stop workers
    orchestrator.stop_workers()
    
    print()
    
    # Show status
    print("Final Status:")
    print("-" * 70)
    status = orchestrator.get_status()
    print(f"Total agents: {status['stats']['total_agents']}")
    print(f"Total tasks: {status['stats']['total_tasks']}")
    print(f"Completed: {status['stats']['completed_tasks']}")
    print(f"Failed: {status['stats']['failed_tasks']}")
    print(f"Queue size: {status['queue_size']}")
    
    print()
    
    # Test agent communication
    print("Testing agent communication...")
    if len(agents) >= 2:
        comm = orchestrator.enable_agent_communication(agents[0], agents[1])
        print(f"  {agents[0]} <-> {agents[1]}")
        print(f"  Similarity: {comm['similarity']:.3f}")
        print(f"  Aligned: {comm['aligned']}")
    
    print()
    
    # Test cloning
    print("Testing agent cloning...")
    if agents:
        clone_id = orchestrator.clone_agent(agents[0])
        print(f"  Cloned {agents[0]} -> {clone_id}")
    
    print()
    
    # Test task decomposition
    print("Testing task decomposition...")
    complex_task = "Research quantum computing and then write a summary and also create a presentation"
    subtasks = orchestrator.decompose_complex_task(complex_task)
    print(f"  Complex task: {complex_task}")
    print(f"  Decomposed into {len(subtasks)} subtasks:")
    for i, subtask in enumerate(subtasks, 1):
        print(f"    {i}. {subtask}")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
