"""
Specialized Vector Agents - Experts in specific domains

Each agent has:
- Specialized position in semantic space
- Optimized signal/noise balance for their domain
- Unique competence vector
"""

import logging
from typing import Optional
import numpy as np

from .base_agent import VectorAgent
from vektor_analyzer import VektorAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResearchAgent(VectorAgent):
    """
    Research Agent - Information retrieval and analysis specialist
    
    Signal/Noise: 80/20 (high precision, low randomness)
    Optimized for: Finding accurate information, analyzing data, summarizing findings
    """
    
    def __init__(self, agent_id: Optional[str] = None, analyzer: Optional[VektorAnalyzer] = None):
        super().__init__(
            agent_id=agent_id or "research_agent",
            signal_weight=0.80,  # High signal for accuracy
            noise_weight=0.20,   # Some noise for creative connections
            competence_description=(
                "Expert in research, information retrieval, data analysis, "
                "fact-checking, literature review, academic writing, "
                "scientific methodology, and evidence-based conclusions"
            ),
            analyzer=analyzer
        )
        logger.info(f"🔬 ResearchAgent '{self.agent_id}' initialized (precision mode)")


class CodeAgent(VectorAgent):
    """
    Code Agent - Programming and debugging specialist
    
    Signal/Noise: 85/15 (very high precision, minimal randomness)
    Optimized for: Writing code, debugging, code review, refactoring, optimization
    """
    
    def __init__(self, agent_id: Optional[str] = None, analyzer: Optional[VektorAnalyzer] = None):
        super().__init__(
            agent_id=agent_id or "code_agent",
            signal_weight=0.85,  # Very high signal for correctness
            noise_weight=0.15,   # Minimal noise for creative solutions
            competence_description=(
                "Expert in software development, programming languages (Python, JavaScript, Java, C++), "
                "debugging, code review, algorithms, data structures, design patterns, "
                "software architecture, testing, and code optimization"
            ),
            analyzer=analyzer
        )
        logger.info(f"💻 CodeAgent '{self.agent_id}' initialized (precision mode)")


class CreativeAgent(VectorAgent):
    """
    Creative Agent - Art and content generation specialist
    
    Signal/Noise: 60/40 (lower signal, higher noise for creativity)
    Optimized for: Creative writing, art concepts, storytelling, novel ideas
    """
    
    def __init__(self, agent_id: Optional[str] = None, analyzer: Optional[VektorAnalyzer] = None):
        super().__init__(
            agent_id=agent_id or "creative_agent",
            signal_weight=0.60,  # Lower signal for exploration
            noise_weight=0.40,   # High noise for creativity
            competence_description=(
                "Expert in creative writing, storytelling, poetry, art concepts, "
                "content generation, comedy, humor, creative problem solving, "
                "brainstorming, innovation, and thinking outside the box"
            ),
            analyzer=analyzer
        )
        logger.info(f"🎨 CreativeAgent '{self.agent_id}' initialized (creative mode)")


class MathAgent(VectorAgent):
    """
    Math Agent - Calculations and mathematical analysis specialist
    
    Signal/Noise: 95/5 (extremely high precision, minimal noise)
    Optimized for: Mathematical calculations, proofs, statistical analysis, modeling
    """
    
    def __init__(self, agent_id: Optional[str] = None, analyzer: Optional[VektorAnalyzer] = None):
        super().__init__(
            agent_id=agent_id or "math_agent",
            signal_weight=0.95,  # Extremely high signal for accuracy
            noise_weight=0.05,   # Very minimal noise
            competence_description=(
                "Expert in mathematics, calculus, algebra, geometry, statistics, "
                "probability, mathematical proofs, numerical analysis, optimization, "
                "linear algebra, differential equations, and mathematical modeling"
            ),
            analyzer=analyzer
        )
        logger.info(f"🔢 MathAgent '{self.agent_id}' initialized (ultra-precision mode)")


class TeacherAgent(VectorAgent):
    """
    Teacher Agent - Explanation and education specialist
    
    Signal/Noise: 75/25 (high clarity, some creativity for engagement)
    Optimized for: Explaining concepts, teaching, tutoring, creating examples
    """
    
    def __init__(self, agent_id: Optional[str] = None, analyzer: Optional[VektorAnalyzer] = None):
        super().__init__(
            agent_id=agent_id or "teacher_agent",
            signal_weight=0.75,  # High signal for clarity
            noise_weight=0.25,   # Some noise for engaging examples
            competence_description=(
                "Expert in teaching, explaining complex concepts simply, "
                "creating educational content, tutoring, pedagogy, "
                "curriculum design, creating examples and analogies, "
                "student assessment, and adaptive learning strategies"
            ),
            analyzer=analyzer
        )
        logger.info(f"👨‍🏫 TeacherAgent '{self.agent_id}' initialized (education mode)")


def create_specialized_agent(agent_type: str, agent_id: Optional[str] = None, 
                            analyzer: Optional[VektorAnalyzer] = None) -> VectorAgent:
    """
    Factory function to create specialized agents
    
    Args:
        agent_type: Type of agent ('research', 'code', 'creative', 'math', 'teacher')
        agent_id: Optional custom agent ID
        analyzer: Optional VektorAnalyzer instance
        
    Returns:
        Specialized VectorAgent instance
        
    Raises:
        ValueError: If agent_type is unknown
    """
    agent_map = {
        'research': ResearchAgent,
        'code': CodeAgent,
        'creative': CreativeAgent,
        'math': MathAgent,
        'teacher': TeacherAgent
    }
    
    agent_type_lower = agent_type.lower()
    if agent_type_lower not in agent_map:
        raise ValueError(
            f"Unknown agent type '{agent_type}'. "
            f"Valid types: {', '.join(agent_map.keys())}"
        )
    
    agent_class = agent_map[agent_type_lower]
    return agent_class(agent_id=agent_id, analyzer=analyzer)


def main():
    """Demo of specialized agents"""
    print("=" * 70)
    print("🌌 UMAJA Vector Agent System - Specialized Agents Demo")
    print("=" * 70)
    print()
    
    # Create all specialized agents
    agents = {
        'research': ResearchAgent(),
        'code': CodeAgent(),
        'creative': CreativeAgent(),
        'math': MathAgent(),
        'teacher': TeacherAgent()
    }
    
    print("✅ Created specialized agents:")
    for agent_type, agent in agents.items():
        print(f"  {agent_type.upper()}: {agent.agent_id}")
        print(f"    Signal/Noise: {agent.signal_weight:.1%}/{agent.noise_weight:.1%}")
    
    print()
    
    # Test tasks with different agents
    test_tasks = [
        ("Find information about quantum computing", ['research', 'teacher']),
        ("Debug a Python function that's not working", ['code']),
        ("Write a creative story about AI", ['creative', 'teacher']),
        ("Calculate the derivative of x^2 + 3x + 2", ['math', 'teacher']),
        ("Explain machine learning to a beginner", ['teacher', 'research'])
    ]
    
    print("Testing which agents can handle which tasks:")
    print("-" * 70)
    
    for task, expected_handlers in test_tasks:
        print(f"\nTask: {task}")
        print("Agent responses:")
        
        best_agent = None
        best_similarity = 0.0
        
        for agent_type, agent in agents.items():
            can_do, similarity = agent.can_handle(task)
            symbol = "✅" if can_do else "❌"
            print(f"  {symbol} {agent_type.upper():10s}: {similarity:.3f}")
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_agent = agent_type
        
        print(f"  👉 Best match: {best_agent.upper()} ({best_similarity:.3f})")
    
    print()
    print("-" * 70)
    
    # Test agent communication (who works well together?)
    print()
    print("Testing agent collaboration (similarity scores):")
    print("-" * 70)
    
    agent_names = list(agents.keys())
    for i, name1 in enumerate(agent_names):
        for name2 in agent_names[i+1:]:
            agent1 = agents[name1]
            agent2 = agents[name2]
            comm = agent1.communicate_with(agent2)
            
            collaboration = "Good team" if comm['complementary'] else "Similar roles"
            print(f"  {name1.upper()} <-> {name2.upper()}: {comm['competence_similarity']:.3f} ({collaboration})")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
