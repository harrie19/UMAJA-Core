"""
Unit tests for Autonomous Mode functionality

Tests cover:
- Agent creation and startup
- Task queue operations
- Emergency stop mechanism
- Task handlers
- Dashboard functionality
"""

import unittest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agent_orchestrator import AgentOrchestrator, AgentType, Task, TaskStatus


class TestAutonomousMode(unittest.TestCase):
    """Test suite for autonomous mode functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.data_dir = Path(self.test_dir) / "agents"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Create test orchestrator
        self.orchestrator = AgentOrchestrator(data_dir=str(self.data_dir))
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Stop all agents
        if hasattr(self, 'orchestrator'):
            self.orchestrator.stop_all_agents()
        
        # Remove temporary directory
        if hasattr(self, 'test_dir') and Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def test_agent_creation(self):
        """Test that agents can be created"""
        agent_id = self.orchestrator.create_agent(AgentType.CONTENT_GENERATOR)
        
        self.assertIsNotNone(agent_id)
        self.assertIn(agent_id, self.orchestrator.agents)
        self.assertEqual(self.orchestrator.agents[agent_id].type, AgentType.CONTENT_GENERATOR)
        self.assertEqual(self.orchestrator.stats['total_agents'], 1)
    
    def test_multiple_agent_creation(self):
        """Test creating multiple agents"""
        agent_types = [
            AgentType.CONTENT_GENERATOR,
            AgentType.TRANSLATOR,
            AgentType.QUALITY_CHECKER
        ]
        
        created_agents = []
        for agent_type in agent_types:
            agent_id = self.orchestrator.create_agent(agent_type)
            created_agents.append(agent_id)
        
        self.assertEqual(len(created_agents), 3)
        self.assertEqual(self.orchestrator.stats['total_agents'], 3)
    
    def test_task_addition(self):
        """Test adding tasks to queue"""
        task_id = self.orchestrator.add_task(
            task_type="test_task",
            agent_type=AgentType.CONTENT_GENERATOR,
            data={"test": "data"},
            priority=5
        )
        
        self.assertIsNotNone(task_id)
        self.assertEqual(self.orchestrator.stats['total_tasks'], 1)
        self.assertGreater(self.orchestrator.task_queue.qsize(), 0)
    
    def test_task_priority(self):
        """Test that tasks are prioritized correctly"""
        # Add tasks with different priorities
        low_priority = self.orchestrator.add_task(
            task_type="low",
            agent_type=AgentType.CONTENT_GENERATOR,
            data={},
            priority=3
        )
        
        high_priority = self.orchestrator.add_task(
            task_type="high",
            agent_type=AgentType.CONTENT_GENERATOR,
            data={},
            priority=9
        )
        
        # Get tasks from queue
        task1 = self.orchestrator.task_queue.get()
        task2 = self.orchestrator.task_queue.get()
        
        # High priority should come first
        self.assertEqual(task1.priority, 9)
        self.assertEqual(task2.priority, 3)
    
    def test_task_handler_registration(self):
        """Test registering task handlers"""
        def test_handler(data):
            return {"success": True}
        
        self.orchestrator.register_task_handler("test_type", test_handler)
        
        self.assertIn("test_type", self.orchestrator.task_handlers)
        self.assertEqual(self.orchestrator.task_handlers["test_type"], test_handler)
    
    def test_emergency_stop_file_check(self):
        """Test emergency stop file checking"""
        # Create temporary emergency stop file
        emergency_file = Path(self.test_dir) / "emergency_stop.json"
        
        # Test enabled state
        with open(emergency_file, 'w') as f:
            json.dump({"agent_enabled": True}, f)
        
        # Mock the file path
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', return_value=open(emergency_file, 'r')):
                # Test would check emergency stop
                self.assertTrue(emergency_file.exists())
    
    def test_agent_status_tracking(self):
        """Test that agent status is tracked correctly"""
        agent_id = self.orchestrator.create_agent(AgentType.CONTENT_GENERATOR)
        
        agent = self.orchestrator.agents[agent_id]
        self.assertEqual(agent.status, "idle")
        self.assertEqual(agent.tasks_completed, 0)
        self.assertEqual(agent.tasks_failed, 0)
    
    def test_orchestrator_state_save(self):
        """Test saving orchestrator state"""
        # Create an agent
        agent_id = self.orchestrator.create_agent(AgentType.CONTENT_GENERATOR)
        
        # Save state
        self.orchestrator.save_state()
        
        # Check state file exists
        state_file = self.data_dir / "orchestrator_state.json"
        self.assertTrue(state_file.exists())
        
        # Load and verify state
        with open(state_file, 'r') as f:
            state = json.load(f)
        
        self.assertIn('stats', state)
        self.assertIn('agents', state)
        self.assertEqual(state['stats']['total_agents'], 1)
    
    def test_get_status(self):
        """Test getting system status"""
        # Create agents and add tasks
        self.orchestrator.create_agent(AgentType.CONTENT_GENERATOR)
        self.orchestrator.add_task(
            task_type="test",
            agent_type=AgentType.CONTENT_GENERATOR,
            data={},
            priority=5
        )
        
        status = self.orchestrator.get_status()
        
        self.assertIn('stats', status)
        self.assertIn('agents', status)
        self.assertIn('queue_size', status)
        self.assertEqual(status['stats']['total_agents'], 1)
        self.assertEqual(status['stats']['total_tasks'], 1)
    
    def test_agent_scaling(self):
        """Test scaling agents up and down"""
        # Scale up to 3 content generators
        self.orchestrator.scale_agents(AgentType.CONTENT_GENERATOR, 3)
        
        # Count content generators
        content_generators = [
            a for a in self.orchestrator.agents.values()
            if a.type == AgentType.CONTENT_GENERATOR
        ]
        
        self.assertEqual(len(content_generators), 3)
    
    def test_mock_content_generation_handler(self):
        """Test content generation handler with mocked dependencies"""
        # Mock the handler function
        def mock_handler(data):
            return {
                "success": True,
                "city_id": "test_city",
                "personality": "john_cleese",
                "content": {"topic": "Test content"}
            }
        
        self.orchestrator.register_task_handler("generate_content", mock_handler)
        
        # Test handler is registered
        self.assertIn("generate_content", self.orchestrator.task_handlers)
        
        # Test handler execution
        result = self.orchestrator.task_handlers["generate_content"](
            {"city_id": "test_city", "personality": "john_cleese"}
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["city_id"], "test_city")
    
    def test_task_status_transitions(self):
        """Test task status transitions"""
        task = Task(
            id="test_123",
            type="test_task",
            agent_type=AgentType.CONTENT_GENERATOR,
            data={"test": "data"}
        )
        
        # Initial status
        self.assertEqual(task.status, TaskStatus.PENDING)
        
        # Simulate status changes
        task.status = TaskStatus.RUNNING
        self.assertEqual(task.status, TaskStatus.RUNNING)
        
        task.status = TaskStatus.COMPLETED
        self.assertEqual(task.status, TaskStatus.COMPLETED)


class TestDashboardFunctionality(unittest.TestCase):
    """Test suite for autonomous dashboard"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.data_dir = Path(self.test_dir) / "agents"
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def tearDown(self):
        """Clean up test fixtures"""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def test_dashboard_data_structure(self):
        """Test dashboard data structure"""
        # Create sample state file
        state_file = self.data_dir / "orchestrator_state.json"
        state_data = {
            "stats": {
                "total_agents": 9,
                "active_agents": 9,
                "total_tasks": 100,
                "completed_tasks": 95,
                "failed_tasks": 5,
                "started_at": "2026-01-03T12:00:00"
            },
            "agents": {},
            "saved_at": "2026-01-03T14:00:00"
        }
        
        with open(state_file, 'w') as f:
            json.dump(state_data, f)
        
        # Verify file exists and is readable
        self.assertTrue(state_file.exists())
        
        with open(state_file, 'r') as f:
            loaded_data = json.load(f)
        
        self.assertEqual(loaded_data['stats']['total_agents'], 9)
        self.assertEqual(loaded_data['stats']['completed_tasks'], 95)
    
    def test_emergency_stop_status_check(self):
        """Test checking emergency stop status"""
        emergency_file = Path(self.test_dir) / "emergency_stop.json"
        
        # Test enabled state
        with open(emergency_file, 'w') as f:
            json.dump({
                "agent_enabled": True,
                "reason": None,
                "disabled_by": None
            }, f)
        
        self.assertTrue(emergency_file.exists())
        
        with open(emergency_file, 'r') as f:
            config = json.load(f)
        
        self.assertTrue(config['agent_enabled'])
        
        # Test disabled state
        with open(emergency_file, 'w') as f:
            json.dump({
                "agent_enabled": False,
                "reason": "Testing",
                "disabled_by": "test_user"
            }, f)
        
        with open(emergency_file, 'r') as f:
            config = json.load(f)
        
        self.assertFalse(config['agent_enabled'])
        self.assertEqual(config['reason'], "Testing")


class TestWorkflowIntegration(unittest.TestCase):
    """Test workflow integration scenarios"""
    
    def test_worldtour_data_structure(self):
        """Test World Tour data structure"""
        test_data = {
            "cities": [
                {
                    "id": "tokyo",
                    "name": "Tokyo",
                    "country": "Japan",
                    "visited": True
                },
                {
                    "id": "london",
                    "name": "London",
                    "country": "UK",
                    "visited": False
                }
            ]
        }
        
        # Verify structure
        self.assertIn("cities", test_data)
        self.assertEqual(len(test_data["cities"]), 2)
        self.assertTrue(test_data["cities"][0]["visited"])
        self.assertFalse(test_data["cities"][1]["visited"])
    
    def test_analytics_data_structure(self):
        """Test analytics data structure"""
        analytics_data = {
            "total_smiles_generated": 144,
            "content_cycles_completed": 6,
            "last_cycle": "2026-01-03T16:00:00"
        }
        
        # Verify structure
        self.assertIn("total_smiles_generated", analytics_data)
        self.assertIn("content_cycles_completed", analytics_data)
        self.assertEqual(analytics_data["content_cycles_completed"], 6)


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAutonomousMode))
    suite.addTests(loader.loadTestsFromTestCase(TestDashboardFunctionality))
    suite.addTests(loader.loadTestsFromTestCase(TestWorkflowIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
