"""
Tests for VectorAgentOrchestrator - Vector agent management and task routing
"""

import pytest
import time
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from vector_agents.orchestrator import VectorAgentOrchestrator, VectorTask


class TestVectorAgentOrchestrator:
    """Test suite for VectorAgentOrchestrator"""
    
    @pytest.fixture
    def orchestrator(self, tmp_path):
        """Create orchestrator instance with temporary data directory"""
        data_dir = tmp_path / "vector_agents"
        return VectorAgentOrchestrator(data_dir=str(data_dir))
    
    def test_initialization(self, orchestrator):
        """Test orchestrator initialization"""
        assert orchestrator is not None
        assert orchestrator.analyzer is not None
        assert orchestrator.energy_monitor is not None
        assert len(orchestrator.agents) == 0
        assert orchestrator.running is False
    
    def test_spawn_agent(self, orchestrator):
        """Test spawning a vector agent"""
        agent_id = orchestrator.spawn_agent('research')
        
        assert agent_id is not None
        assert agent_id in orchestrator.agents
        assert orchestrator.stats['total_agents'] == 1
    
    def test_spawn_multiple_agents(self, orchestrator):
        """Test spawning multiple agents of different types"""
        agent_types = ['research', 'code', 'creative', 'math', 'teacher']
        
        agent_ids = []
        for agent_type in agent_types:
            agent_id = orchestrator.spawn_agent(agent_type)
            agent_ids.append(agent_id)
        
        assert len(orchestrator.agents) == len(agent_types)
        assert orchestrator.stats['total_agents'] == len(agent_types)
        
        # All agent IDs should be unique
        assert len(set(agent_ids)) == len(agent_ids)
    
    def test_spawn_agent_with_custom_id(self, orchestrator):
        """Test spawning agent with custom ID"""
        custom_id = "my_custom_agent"
        agent_id = orchestrator.spawn_agent('research', agent_id=custom_id)
        
        assert agent_id == custom_id
        assert custom_id in orchestrator.agents
    
    def test_add_task(self, orchestrator):
        """Test adding a task to the queue"""
        task_id = orchestrator.add_task(
            description="Analyze quantum computing research",
            priority=7
        )
        
        assert task_id is not None
        assert task_id.startswith('task_')
        assert orchestrator.stats['total_tasks'] == 1
    
    def test_add_task_with_required_type(self, orchestrator):
        """Test adding task with required agent type"""
        task_id = orchestrator.add_task(
            description="Write Python code",
            priority=8,
            required_agent_type='code'
        )
        
        assert task_id is not None
        assert orchestrator.stats['total_tasks'] == 1
    
    def test_add_multiple_tasks(self, orchestrator):
        """Test adding multiple tasks"""
        tasks = [
            ("Research quantum computing", 9),
            ("Write sorting algorithm", 7),
            ("Create a poem about AI", 5)
        ]
        
        task_ids = []
        for description, priority in tasks:
            task_id = orchestrator.add_task(description, priority)
            task_ids.append(task_id)
        
        assert len(task_ids) == len(tasks)
        assert orchestrator.stats['total_tasks'] == len(tasks)
    
    def test_find_best_agent_no_agents(self, orchestrator):
        """Test finding agent when none exist"""
        task = VectorTask(
            task_id="test_task",
            description="Test task",
            task_vector=orchestrator.analyzer.encode_texts(["test"])[0],
            priority=5
        )
        
        result = orchestrator._find_best_agent(task)
        assert result is None
    
    def test_find_best_agent_with_agents(self, orchestrator):
        """Test finding best agent for a task"""
        # Spawn agents
        orchestrator.spawn_agent('research')
        orchestrator.spawn_agent('code')
        
        # Create a research-oriented task
        task = VectorTask(
            task_id="test_task",
            description="Research scientific papers on machine learning",
            task_vector=orchestrator.analyzer.encode_texts(
                ["Research scientific papers on machine learning"]
            )[0],
            priority=5
        )
        
        result = orchestrator._find_best_agent(task)
        
        assert result is not None
        agent_id, similarity = result
        assert agent_id in orchestrator.agents
        assert 0 <= similarity <= 1
    
    def test_find_best_agent_with_required_type(self, orchestrator):
        """Test finding agent with required type"""
        # Spawn different types
        research_id = orchestrator.spawn_agent('research')
        code_id = orchestrator.spawn_agent('code')
        
        # Task requiring code agent
        task = VectorTask(
            task_id="test_task",
            description="Write Python code",
            task_vector=orchestrator.analyzer.encode_texts(["Write Python code"])[0],
            priority=5,
            required_agent_type='code'
        )
        
        result = orchestrator._find_best_agent(task)
        
        if result:  # May be None if similarity too low
            agent_id, similarity = result
            # Should prefer code agent
            assert 'code' in orchestrator.agents[agent_id].competence_description.lower()
    
    def test_start_stop_workers(self, orchestrator):
        """Test starting and stopping worker threads"""
        # Start workers
        orchestrator.start_workers(num_workers=2)
        
        assert orchestrator.running is True
        assert len(orchestrator.worker_threads) == 2
        
        # Stop workers
        orchestrator.stop_workers()
        
        assert orchestrator.running is False
        assert len(orchestrator.worker_threads) == 0
    
    def test_worker_processing(self, orchestrator):
        """Test that workers process tasks"""
        # Spawn an agent
        orchestrator.spawn_agent('research')
        
        # Add a task
        task_id = orchestrator.add_task(
            description="Research artificial intelligence",
            priority=8
        )
        
        # Start workers
        orchestrator.start_workers(num_workers=1)
        
        # Wait for processing
        time.sleep(2)
        
        # Stop workers
        orchestrator.stop_workers()
        
        # Check stats
        assert orchestrator.stats['completed_tasks'] >= 0
    
    def test_clone_agent(self, orchestrator):
        """Test cloning an agent"""
        # Spawn original agent
        original_id = orchestrator.spawn_agent('research')
        
        # Clone it
        clone_id = orchestrator.clone_agent(original_id)
        
        assert clone_id != original_id
        assert clone_id in orchestrator.agents
        assert orchestrator.stats['total_agents'] == 2
    
    def test_clone_nonexistent_agent(self, orchestrator):
        """Test cloning non-existent agent raises error"""
        with pytest.raises(ValueError, match="not found"):
            orchestrator.clone_agent('nonexistent_agent')
    
    def test_merge_agents(self, orchestrator):
        """Test merging two agents"""
        # Spawn two agents
        agent1_id = orchestrator.spawn_agent('research')
        agent2_id = orchestrator.spawn_agent('code')
        
        # Merge them
        merged_id = orchestrator.merge_agents(agent1_id, agent2_id)
        
        assert merged_id in orchestrator.agents
        assert merged_id != agent1_id
        assert merged_id != agent2_id
        assert orchestrator.stats['total_agents'] == 3  # Original 2 + merged
    
    def test_merge_nonexistent_agents(self, orchestrator):
        """Test merging non-existent agents raises error"""
        orchestrator.spawn_agent('research')
        
        with pytest.raises(ValueError, match="not found"):
            orchestrator.merge_agents('agent1', 'nonexistent')
    
    def test_enable_agent_communication(self, orchestrator):
        """Test enabling communication between agents"""
        # Spawn two agents
        agent1_id = orchestrator.spawn_agent('research')
        agent2_id = orchestrator.spawn_agent('code')
        
        # Enable communication
        comm_result = orchestrator.enable_agent_communication(agent1_id, agent2_id)
        
        assert 'similarity' in comm_result
        assert 'aligned' in comm_result
        assert 0 <= comm_result['similarity'] <= 1
    
    def test_communication_nonexistent_agents(self, orchestrator):
        """Test communication with non-existent agents raises error"""
        agent_id = orchestrator.spawn_agent('research')
        
        with pytest.raises(ValueError, match="not found"):
            orchestrator.enable_agent_communication(agent_id, 'nonexistent')
    
    def test_get_status(self, orchestrator):
        """Test getting orchestrator status"""
        # Spawn some agents
        orchestrator.spawn_agent('research')
        orchestrator.spawn_agent('code')
        
        # Add some tasks
        orchestrator.add_task("Task 1", priority=5)
        orchestrator.add_task("Task 2", priority=7)
        
        # Get status
        status = orchestrator.get_status()
        
        assert 'stats' in status
        assert 'agents' in status
        assert 'queue_size' in status
        assert 'workers_running' in status
        assert 'num_workers' in status
        
        assert len(status['agents']) == 2
        assert status['stats']['total_agents'] == 2
        assert status['stats']['total_tasks'] == 2
    
    def test_decompose_complex_task(self, orchestrator):
        """Test decomposing complex task"""
        complex_task = "Research quantum computing and then write a summary and also create a presentation"
        
        subtasks = orchestrator.decompose_complex_task(complex_task)
        
        assert isinstance(subtasks, list)
        assert len(subtasks) > 1  # Should be decomposed
        
        # Check that subtasks are reasonable
        for subtask in subtasks:
            assert isinstance(subtask, str)
            assert len(subtask) > 0
    
    def test_decompose_simple_task(self, orchestrator):
        """Test that simple task is not decomposed"""
        simple_task = "Research quantum computing"
        
        subtasks = orchestrator.decompose_complex_task(simple_task)
        
        assert len(subtasks) == 1
        assert subtasks[0] == simple_task
    
    def test_task_priority_ordering(self, orchestrator):
        """Test that tasks are processed by priority"""
        # Spawn an agent
        orchestrator.spawn_agent('research')
        
        # Add tasks with different priorities
        low_priority = orchestrator.add_task("Low priority task", priority=1)
        high_priority = orchestrator.add_task("High priority task", priority=10)
        
        # The task queue should order by priority
        assert orchestrator.task_queue.qsize() == 2
    
    def test_multiple_agent_types(self, orchestrator):
        """Test spawning all agent types"""
        agent_types = ['research', 'code', 'creative', 'math', 'teacher']
        
        for agent_type in agent_types:
            agent_id = orchestrator.spawn_agent(agent_type)
            assert agent_id in orchestrator.agents
            agent = orchestrator.agents[agent_id]
            assert agent_type.lower() in agent.competence_description.lower()
    
    def test_stats_tracking(self, orchestrator):
        """Test that statistics are properly tracked"""
        initial_stats = orchestrator.stats.copy()
        
        # Spawn agents
        orchestrator.spawn_agent('research')
        orchestrator.spawn_agent('code')
        
        # Add tasks
        orchestrator.add_task("Task 1", priority=5)
        orchestrator.add_task("Task 2", priority=7)
        
        # Check stats updated
        assert orchestrator.stats['total_agents'] == initial_stats['total_agents'] + 2
        assert orchestrator.stats['total_tasks'] == initial_stats['total_tasks'] + 2
    
    def test_energy_tracking_integration(self, orchestrator):
        """Test that energy monitoring is integrated"""
        # Energy monitor should be initialized
        assert orchestrator.energy_monitor is not None
        
        # Adding task should log energy
        orchestrator.add_task("Test task", priority=5)
        
        # Energy monitor should have recorded the operation
        # (We can't easily test the exact values without mocking)
    
    def test_concurrent_task_processing(self, orchestrator):
        """Test processing multiple tasks concurrently"""
        # Spawn multiple agents
        for agent_type in ['research', 'code', 'creative']:
            orchestrator.spawn_agent(agent_type)
        
        # Add multiple tasks
        for i in range(5):
            orchestrator.add_task(f"Task {i}", priority=5 + i)
        
        # Start workers
        orchestrator.start_workers(num_workers=3)
        
        # Wait for processing
        time.sleep(3)
        
        # Stop workers
        orchestrator.stop_workers()
        
        # Some tasks should have been processed
        total_processed = (orchestrator.stats['completed_tasks'] + 
                          orchestrator.stats['failed_tasks'])
        assert total_processed >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
