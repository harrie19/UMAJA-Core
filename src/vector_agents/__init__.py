"""
UMAJA Vector Agent System

Self-spawning, vector-based AI agents that navigate semantic space.

Philosophy from docs/VECTOR_AGENTS.md:
- All information exists as vectors in high-dimensional space
- Agents are vector entities searching for information in noise
- Signal + Noise = Creativity and Information
- Communication through vector similarity
- Energy-efficient (uses vectors, not LLMs)

Main Components:
- VectorAgent: Base agent class with vector-based intelligence
- Specialized Agents: Research, Code, Creative, Math, Teacher
- VectorAgentOrchestrator: Spawns and manages agents
"""

__version__ = "1.0.0"

from .base_agent import VectorAgent, VectorAgentState
from .specialized_agents import (
    ResearchAgent,
    CodeAgent,
    CreativeAgent,
    MathAgent,
    TeacherAgent,
    create_specialized_agent
)
from .orchestrator import VectorAgentOrchestrator, VectorTask

__all__ = [
    # Base classes
    'VectorAgent',
    'VectorAgentState',
    
    # Specialized agents
    'ResearchAgent',
    'CodeAgent',
    'CreativeAgent',
    'MathAgent',
    'TeacherAgent',
    'create_specialized_agent',
    
    # Orchestration
    'VectorAgentOrchestrator',
    'VectorTask',
]


def get_version():
    """Get the version of the vector agent system"""
    return __version__


def list_agent_types():
    """List all available specialized agent types"""
    return ['research', 'code', 'creative', 'math', 'teacher']


def quick_start():
    """
    Quick start guide for using vector agents
    
    Returns:
        String with quick start instructions
    """
    return """
    🌌 UMAJA Vector Agent System - Quick Start
    ==========================================
    
    1. Create an orchestrator:
       >>> from vector_agents import VectorAgentOrchestrator
       >>> orchestrator = VectorAgentOrchestrator()
    
    2. Spawn specialized agents:
       >>> research_id = orchestrator.spawn_agent('research')
       >>> code_id = orchestrator.spawn_agent('code')
       >>> creative_id = orchestrator.spawn_agent('creative')
    
    3. Add tasks:
       >>> task_id = orchestrator.add_task(
       ...     description="Find information about quantum computing",
       ...     priority=8
       ... )
    
    4. Start workers to process tasks:
       >>> orchestrator.start_workers(num_workers=3)
    
    5. Check status:
       >>> status = orchestrator.get_status()
       >>> print(status)
    
    6. Agent communication:
       >>> comm = orchestrator.enable_agent_communication(agent_id1, agent_id2)
       >>> print(f"Similarity: {comm['similarity']}")
    
    7. Clone and merge agents:
       >>> clone_id = orchestrator.clone_agent(agent_id)
       >>> merged_id = orchestrator.merge_agents(agent_id1, agent_id2)
    
    For more examples, see: src/vector_agents/README.md
    """


# Print welcome message when package is imported
import logging
logger = logging.getLogger(__name__)
logger.info(f"🌌 UMAJA Vector Agent System v{__version__} loaded")
