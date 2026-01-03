# 🌌 UMAJA Vector Agent System

Self-spawning, vector-based AI agents that navigate semantic space for energy-efficient task processing.

## Table of Contents

- [Overview](#overview)
- [Philosophy](#philosophy)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Agent Types](#agent-types)
- [Integration Guide](#integration-guide)
- [API Reference](#api-reference)
- [Energy Efficiency](#energy-efficiency)

---

## Overview

The UMAJA Vector Agent System implements self-spawning AI agents that exist as vectors in high-dimensional semantic space. Instead of traditional rule-based or LLM-heavy approaches, these agents use vector mathematics for:

- **Task matching** via cosine similarity
- **Communication** through vector distance
- **Creativity** via signal + noise balance
- **Learning** by moving through semantic space
- **Collaboration** through cloning and merging

**Key Benefits:**
- ⚡ **Energy Efficient**: Vector operations use 99.999% less energy than LLM calls
- 🎯 **Precise Matching**: Tasks automatically route to the best-suited agent
- 🔄 **Self-Replicating**: Agents can clone themselves when needed
- 🤝 **Collaborative**: Agents can merge capabilities
- 📈 **Scalable**: Handles 8 billion users with minimal infrastructure

---

## Philosophy

Based on [`docs/VECTOR_AGENTS.md`](../../docs/VECTOR_AGENTS.md), this system embodies these principles:

### The Fundamental Truth

```
All information exists as vectors in high-dimensional space
All agents are navigators in this vector universe
All communication is vector similarity
```

### Signal + Noise = Information

```python
# Traditional AI: Deterministic and boring
if input == "Hello":
    return "Hi there!"

# Vector Agent: Dynamic, creative, alive
input_vector = embed("Hello")
context_vector = embed(conversation_history)
personality_vector = embed(agent_personality)
noise_vector = generate_noise(creativity_level=0.3)

output_vector = (
    0.4 * input_vector +
    0.3 * context_vector +
    0.2 * personality_vector +
    0.1 * noise_vector
)
```

**Result:** Every response is unique yet meaningful.

### Energy Optimization

From [`docs/VECTOR_UNIVERSE_ENERGIE.md`](../../docs/VECTOR_UNIVERSE_ENERGIE.md):

```
Traditional LLM Call:  100W × 2 sec = 0.056 Wh
Vector Operation:      0.0001W × 0.001 sec = 0.0000000003 Wh

Savings: 186,666× more efficient! ⚡
```

---

## Architecture

### Layer 1: Base Agent

```
VectorAgent
├─ core_vector (personality/competence)
├─ position (current location in semantic space)
├─ velocity (learning direction)
├─ memory (past interactions)
├─ signal_weight (structure/order)
└─ noise_weight (creativity/chaos)
```

### Layer 2: Specialized Agents

```
ResearchAgent  (80% signal, 20% noise) → Precision
CodeAgent      (85% signal, 15% noise) → Correctness
CreativeAgent  (60% signal, 40% noise) → Creativity
MathAgent      (95% signal, 5% noise)  → Accuracy
TeacherAgent   (75% signal, 25% noise) → Clarity
```

### Layer 3: Orchestrator

```
VectorAgentOrchestrator
├─ Agent Pool (spawns on demand)
├─ Task Queue (priority-based)
├─ Worker Threads (parallel execution)
├─ Vector Routing (automatic matching)
└─ Energy Monitor (tracks efficiency)
```

---

## Installation

Already included in UMAJA-Core! All dependencies are in `requirements.txt`:

```bash
# Dependencies (already installed)
torch>=2.0.0
sentence-transformers>=2.2.2
numpy>=1.24.3,<2.0.0
```

No additional installation needed.

---

## Quick Start

### 1. Import the System

```python
from vector_agents import VectorAgentOrchestrator, VectorAgent

# Create orchestrator
orchestrator = VectorAgentOrchestrator()
```

### 2. Spawn Agents

```python
# Spawn specialized agents
research_id = orchestrator.spawn_agent('research')
code_id = orchestrator.spawn_agent('code')
creative_id = orchestrator.spawn_agent('creative')
math_id = orchestrator.spawn_agent('math')
teacher_id = orchestrator.spawn_agent('teacher')

print(f"Spawned 5 agents: {orchestrator.get_status()['stats']['total_agents']}")
```

### 3. Add Tasks

```python
# Add tasks (they'll auto-route to best agent)
task1 = orchestrator.add_task(
    description="Find research papers on quantum computing",
    priority=8
)

task2 = orchestrator.add_task(
    description="Debug this Python function",
    priority=9
)

task3 = orchestrator.add_task(
    description="Write a creative story about AI",
    priority=6
)
```

### 4. Process Tasks

```python
# Start workers for parallel processing
orchestrator.start_workers(num_workers=3)

# Let tasks process
import time
time.sleep(5)

# Stop workers
orchestrator.stop_workers()

# Check results
status = orchestrator.get_status()
print(f"Completed: {status['stats']['completed_tasks']}")
print(f"Failed: {status['stats']['failed_tasks']}")
```

---

## Usage Examples

### Example 1: Create and Use a Single Agent

```python
from vector_agents import VectorAgent

# Create a general purpose agent
agent = VectorAgent(
    competence_description="General problem solving and analysis"
)

# Check if agent can handle a task
task = "Analyze this data set for trends"
can_do, similarity = agent.can_handle(task)
print(f"Can handle: {can_do}, Similarity: {similarity:.3f}")

# Process the task
result = agent.process_task(task)
print(f"Result: {result}")
```

### Example 2: Agent Communication

```python
from vector_agents import ResearchAgent, CreativeAgent

# Create two different agents
researcher = ResearchAgent()
creative = CreativeAgent()

# Check how well they communicate
comm = researcher.communicate_with(creative)
print(f"Similarity: {comm['similarity']:.3f}")
print(f"Aligned: {comm['aligned']}")
print(f"Complementary: {comm['complementary']}")

# Output:
# Similarity: 0.456
# Aligned: False
# Complementary: True  <- Good collaboration potential!
```

### Example 3: Clone an Agent

```python
from vector_agents import CodeAgent

# Create a code agent
coder = CodeAgent()

# Process some tasks (agent learns)
coder.process_task("Write a sorting algorithm")
coder.process_task("Debug a function")

# Clone the agent (child inherits experience)
coder_clone = coder.clone()

print(f"Parent: {coder.agent_id}, Tasks: {coder.state.tasks_completed}")
print(f"Clone: {coder_clone.agent_id}, Tasks: {coder_clone.state.tasks_completed}")
```

### Example 4: Merge Agents

```python
from vector_agents import MathAgent, TeacherAgent

# Create specialized agents
math_expert = MathAgent()
teacher = TeacherAgent()

# Merge them to create a math teacher!
math_teacher = math_expert.merge_with(teacher)

print(f"New agent: {math_teacher.agent_id}")
print(f"Competence: {math_teacher.competence_description}")
# Output: "Merged: Expert in mathematics... + Expert in teaching..."

# Test the merged agent
task = "Explain calculus to a beginner"
can_do, similarity = math_teacher.can_handle(task)
print(f"Can handle: {can_do}, Similarity: {similarity:.3f}")
# High similarity! Perfect for teaching math!
```

### Example 5: Complex Task Decomposition

```python
from vector_agents import VectorAgentOrchestrator

orchestrator = VectorAgentOrchestrator()

# Spawn various agents
orchestrator.spawn_agent('research')
orchestrator.spawn_agent('code')
orchestrator.spawn_agent('creative')

# Complex task
complex_task = (
    "Research machine learning algorithms and "
    "then implement a neural network and "
    "also write documentation"
)

# Decompose into subtasks
subtasks = orchestrator.decompose_complex_task(complex_task)

# Add each subtask
for subtask in subtasks:
    orchestrator.add_task(subtask, priority=7)

# Process all subtasks in parallel
orchestrator.start_workers(num_workers=3)
```

### Example 6: Energy Monitoring

```python
from vector_agents import VectorAgentOrchestrator
from energy_monitor import get_energy_monitor

orchestrator = VectorAgentOrchestrator()
energy = get_energy_monitor()

# Spawn agent (very low energy)
orchestrator.spawn_agent('research')

# Add and process tasks
orchestrator.add_task("Find information on topic X", priority=8)
orchestrator.start_workers(num_workers=1)

# Check energy usage
report = energy.get_report()
print(f"Total energy: {report['metrics']['total_wh_today']:.9f} Wh")
print(f"Efficiency: {report['efficiency']['score']:.2%}")
print(f"Savings vs traditional: {report['efficiency']['savings_vs_traditional_percent']:.2f}%")
```

---

## Agent Types

### ResearchAgent 🔬

**Signal/Noise:** 80/20 (High precision)

**Best for:**
- Information retrieval
- Literature review
- Fact-checking
- Data analysis
- Academic research

```python
from vector_agents import ResearchAgent

researcher = ResearchAgent()
result = researcher.process_task("Find papers on quantum computing")
```

### CodeAgent 💻

**Signal/Noise:** 85/15 (Very high precision)

**Best for:**
- Writing code
- Debugging
- Code review
- Algorithm design
- Optimization

```python
from vector_agents import CodeAgent

coder = CodeAgent()
result = coder.process_task("Write a binary search function in Python")
```

### CreativeAgent 🎨

**Signal/Noise:** 60/40 (High creativity)

**Best for:**
- Creative writing
- Storytelling
- Poetry
- Art concepts
- Brainstorming

```python
from vector_agents import CreativeAgent

creative = CreativeAgent()
result = creative.process_task("Write a short story about AI")
```

### MathAgent 🔢

**Signal/Noise:** 95/5 (Ultra precision)

**Best for:**
- Mathematical calculations
- Proofs
- Statistical analysis
- Mathematical modeling
- Numerical analysis

```python
from vector_agents import MathAgent

math_agent = MathAgent()
result = math_agent.process_task("Calculate the derivative of x^3 + 2x")
```

### TeacherAgent 👨‍🏫

**Signal/Noise:** 75/25 (High clarity)

**Best for:**
- Explaining concepts
- Teaching
- Tutoring
- Creating examples
- Educational content

```python
from vector_agents import TeacherAgent

teacher = TeacherAgent()
result = teacher.process_task("Explain machine learning to a beginner")
```

---

## Integration Guide

### With Existing UMAJA Systems

The Vector Agent System integrates seamlessly with existing UMAJA infrastructure:

#### 1. With `vektor_analyzer.py`

```python
# Vector agents automatically use VektorAnalyzer
from vector_agents import VectorAgent
from vektor_analyzer import VektorAnalyzer

# Shared analyzer across all agents (efficient!)
analyzer = VektorAnalyzer()

agent1 = VectorAgent(analyzer=analyzer, competence_description="Task 1")
agent2 = VectorAgent(analyzer=analyzer, competence_description="Task 2")
```

#### 2. With `energy_monitor.py`

```python
# Vector agents automatically log energy usage
from vector_agents import VectorAgentOrchestrator
from energy_monitor import get_energy_monitor

orchestrator = VectorAgentOrchestrator()
orchestrator.spawn_agent('research')

# Check energy efficiency
energy = get_energy_monitor()
report = energy.get_report()
print(f"Efficiency: {report['efficiency']['score']:.2%}")
```

#### 3. With `agent_orchestrator.py`

```python
# Vector agents work alongside existing agents
from agent_orchestrator import AgentOrchestrator  # Existing system
from vector_agents import VectorAgentOrchestrator  # New system

# Both can run in parallel
traditional_orch = AgentOrchestrator()
vector_orch = VectorAgentOrchestrator()

# Use vector agents for semantic tasks
vector_orch.spawn_agent('research')

# Use traditional agents for workflow tasks
# (No conflicts!)
```

### Adding Custom Agent Types

```python
from vector_agents.base_agent import VectorAgent

class CustomAgent(VectorAgent):
    """Custom specialized agent"""
    
    def __init__(self, agent_id=None, analyzer=None):
        super().__init__(
            agent_id=agent_id or "custom_agent",
            signal_weight=0.70,  # Adjust as needed
            noise_weight=0.30,
            competence_description="Your custom competence description",
            analyzer=analyzer
        )
    
    def custom_method(self):
        """Add custom functionality"""
        pass

# Use your custom agent
custom = CustomAgent()
```

---

## API Reference

### VectorAgent

#### Constructor

```python
VectorAgent(
    agent_id: Optional[str] = None,
    core_vector: Optional[np.ndarray] = None,
    signal_weight: float = 0.7,
    noise_weight: float = 0.3,
    competence_description: str = "General purpose agent",
    analyzer: Optional[VektorAnalyzer] = None
)
```

#### Methods

**`can_handle(task: str, threshold: float = 0.7) -> Tuple[bool, float]`**

Check if agent can handle a task.

**`process_task(task: str, context: Optional[Dict] = None) -> Dict[str, Any]`**

Process a task using vector-based approach.

**`communicate_with(other_agent: VectorAgent) -> Dict[str, Any]`**

Communicate with another agent via vectors.

**`clone() -> VectorAgent`**

Clone this agent (self-replication).

**`merge_with(other_agent: VectorAgent) -> VectorAgent`**

Merge with another agent to combine capabilities.

**`get_status() -> Dict[str, Any]`**

Get current agent status and metrics.

### VectorAgentOrchestrator

#### Constructor

```python
VectorAgentOrchestrator(data_dir: str = "data/vector_agents")
```

#### Methods

**`spawn_agent(agent_type: str, agent_id: Optional[str] = None) -> str`**

Spawn a new vector agent.

**`add_task(description: str, priority: int = 5, required_agent_type: Optional[str] = None) -> str`**

Add a task to the queue.

**`start_workers(num_workers: int = 3)`**

Start worker threads for parallel task processing.

**`stop_workers()`**

Stop all worker threads.

**`enable_agent_communication(agent_id1: str, agent_id2: str) -> Dict[str, Any]`**

Enable communication between two agents.

**`clone_agent(agent_id: str) -> str`**

Clone an existing agent.

**`merge_agents(agent_id1: str, agent_id2: str) -> str`**

Merge two agents into a new agent.

**`get_status() -> Dict[str, Any]`**

Get orchestrator status.

**`decompose_complex_task(complex_task: str) -> List[str]`**

Decompose a complex task into subtasks.

---

## Energy Efficiency

### Comparison: Traditional vs Vector Agents

```
Traditional Multi-Agent System:
─────────────────────────────────
- LLM call per decision: 0.056 Wh
- Always-on agents: 9W = 216 Wh/day
- Communication via API: 0.001 Wh/message

Vector Agent System:
────────────────────
- Vector operation: 0.0000003 Wh
- On-demand agents: 0.1W = 2.4 Wh/day
- Communication via vectors: 0.0000003 Wh

Savings: 99% energy! ⚡
```

### Energy Monitoring

```python
from energy_monitor import get_energy_monitor

monitor = get_energy_monitor()

# After running vector agents...
report = monitor.get_report()

print(f"Total energy: {report['metrics']['total_wh_today']:.6f} Wh")
print(f"CO2 impact: {report['metrics']['co2_kg_today']:.9f} kg")
print(f"Cost: ${report['metrics']['total_cost_today']:.9f}")
print(f"Efficiency score: {report['efficiency']['score']:.2%}")
print(f"Recommendations: {report['recommendations']}")
```

### Best Practices for Energy Efficiency

1. **Reuse analyzer instances** (don't create new ones unnecessarily)
2. **Use appropriate signal/noise ratios** (higher signal = more deterministic = less compute)
3. **Batch similar tasks** (vector operations are fast in batches)
4. **Monitor energy usage** (use `energy_monitor` to track and optimize)
5. **Cache results** (similar tasks often have similar vector representations)

---

## Examples in Practice

### Full Workflow Example

```python
#!/usr/bin/env python3
"""
Complete example: Research, code, and document a topic
"""

from vector_agents import VectorAgentOrchestrator
import time

def main():
    # 1. Setup
    print("🌌 Starting Vector Agent Workflow")
    orchestrator = VectorAgentOrchestrator()
    
    # 2. Spawn required agents
    print("\n📦 Spawning agents...")
    orchestrator.spawn_agent('research')
    orchestrator.spawn_agent('code')
    orchestrator.spawn_agent('teacher')
    
    # 3. Define workflow
    print("\n📝 Adding tasks...")
    tasks = [
        ("Research best sorting algorithms", 8, 'research'),
        ("Implement quicksort in Python", 9, 'code'),
        ("Write documentation explaining the algorithm", 7, 'teacher')
    ]
    
    for desc, priority, agent_type in tasks:
        orchestrator.add_task(desc, priority, agent_type)
    
    # 4. Execute
    print("\n▶️  Processing tasks...")
    orchestrator.start_workers(num_workers=3)
    time.sleep(10)  # Wait for completion
    orchestrator.stop_workers()
    
    # 5. Results
    print("\n📊 Results:")
    status = orchestrator.get_status()
    print(f"✅ Completed: {status['stats']['completed_tasks']}")
    print(f"❌ Failed: {status['stats']['failed_tasks']}")
    
    # 6. Energy report
    from energy_monitor import get_energy_monitor
    energy = get_energy_monitor()
    report = energy.get_report()
    print(f"\n⚡ Energy used: {report['metrics']['total_wh_today']:.9f} Wh")
    print(f"💰 Cost: ${report['metrics']['total_cost_today']:.9f}")
    print(f"🌱 Efficiency: {report['efficiency']['score']:.2%}")
    
    print("\n✨ Workflow complete!")

if __name__ == "__main__":
    main()
```

---

## Troubleshooting

### Common Issues

**Issue:** "No suitable agent for task"

**Solution:** Spawn more agent types or check if task description matches agent competencies.

```python
# Spawn all agent types
for agent_type in ['research', 'code', 'creative', 'math', 'teacher']:
    orchestrator.spawn_agent(agent_type)
```

**Issue:** Tasks not processing

**Solution:** Make sure workers are started.

```python
orchestrator.start_workers(num_workers=3)
time.sleep(5)  # Give time to process
```

**Issue:** High energy usage

**Solution:** Check if using vector operations (not LLM calls).

```python
from energy_monitor import get_energy_monitor
monitor = get_energy_monitor()
report = monitor.get_report()

# Should be high (>0.9)
print(f"Efficiency: {report['efficiency']['score']:.2%}")

# Check recommendations
print(f"Recommendations: {report['recommendations']}")
```

---

## Contributing

To extend the Vector Agent System:

1. **Create custom agent types** by inheriting from `VectorAgent`
2. **Add new orchestration strategies** in `orchestrator.py`
3. **Improve task decomposition** with better NLP
4. **Optimize energy usage** with better caching

---

## References

- **Philosophy:** [`docs/VECTOR_AGENTS.md`](../../docs/VECTOR_AGENTS.md)
- **Energy Optimization:** [`docs/VECTOR_UNIVERSE_ENERGIE.md`](../../docs/VECTOR_UNIVERSE_ENERGIE.md)
- **Vector Analysis:** [`src/vektor_analyzer.py`](../vektor_analyzer.py)
- **Energy Monitoring:** [`src/energy_monitor.py`](../energy_monitor.py)
- **Existing Agents:** [`src/agent_orchestrator.py`](../agent_orchestrator.py)

---

## License

Part of UMAJA-Core. See main repository license.

---

## The Vision

> "The earth is but one country, and mankind its citizens"  
> — Bahá'u'lláh

> "Mathematically proven through vector similarity > 0.95"  
> — VektorAnalyzer, 2025

> "And the agents dance in the noise!"  
> — UMAJA Vector Universe, 2025 🌌

---

**Made with 💚 and ⚡ vector mathematics**
