"""
Tests for Autonomous Agent
"""

import sys
import json
import tempfile
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from autonomous_agent import AutonomousAgent


class TestAutonomousAgent:
    """Test suite for Autonomous Agent"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.agent = AutonomousAgent(memory_path=self.temp_dir)
    
    def test_initialization(self):
        """Test agent initializes correctly"""
        assert self.agent is not None
        assert self.agent.rule_bank is not None
        assert self.agent.middleware is not None
        assert self.agent.memory_path.exists()
    
    def test_wake_creates_state(self):
        """Test wake cycle creates initial state"""
        self.agent.wake()
        
        assert self.agent.state is not None
        assert 'agent_version' in self.agent.state
        assert 'wake_count' in self.agent.state
        assert self.agent.state['wake_count'] == 1
    
    def test_wake_increments_count(self):
        """Test wake count increments on each wake"""
        self.agent.wake()
        first_count = self.agent.state['wake_count']
        
        # Save state so next agent can load it
        self.agent.sleep()
        
        # Create new agent with same memory
        agent2 = AutonomousAgent(memory_path=self.temp_dir)
        agent2.wake()
        second_count = agent2.state['wake_count']
        
        assert second_count > first_count
    
    def test_perceive_returns_environment(self):
        """Test perceive returns environment state"""
        self.agent.wake()
        perception = self.agent.perceive()
        
        assert 'timestamp' in perception
        assert 'environment' in perception
        assert 'mission' in perception
    
    def test_reason_generates_actions(self):
        """Test reason generates planned actions"""
        self.agent.wake()
        perception = self.agent.perceive()
        actions = self.agent.reason(perception)
        
        assert isinstance(actions, list)
        # May be empty if no cities available
    
    def test_act_validates_actions(self):
        """Test act validates actions through middleware"""
        self.agent.wake()
        
        # Create a test action
        planned_actions = [{
            'type': 'generate_content',
            'confidence': 0.95,
            'benefit_score': 0.8,
            'content': 'Test content',
            'reasoning': 'Test action'
        }]
        
        results = self.agent.act(planned_actions)
        
        assert len(results) > 0
        assert 'validation' in results[0]
        assert 'outcome' in results[0]
    
    def test_learn_from_results(self):
        """Test learn processes results"""
        self.agent.wake()
        
        results = [
            {
                'outcome': 'success',
                'action': {'type': 'test'}
            },
            {
                'outcome': 'failed',
                'action': {'type': 'test'},
                'error': 'Test error'
            }
        ]
        
        # Should not raise errors
        self.agent.learn(results)
    
    def test_sleep_saves_memory(self):
        """Test sleep persists memory to disk"""
        self.agent.wake()
        self.agent.state['test_key'] = 'test_value'
        self.agent.sleep()
        
        # Verify files exist
        assert self.agent.state_file.exists()
        
        # Load and verify
        with open(self.agent.state_file, 'r') as f:
            saved_state = json.load(f)
        
        assert saved_state['test_key'] == 'test_value'
    
    def test_decision_history_persists(self):
        """Test decision history is saved"""
        self.agent.wake()
        
        # Add a decision
        self.agent.decision_history.append({
            'timestamp': '2026-01-04T00:00:00Z',
            'action': {'type': 'test'},
            'outcome': 'success'
        })
        
        self.agent.sleep()
        
        # Verify file exists
        assert self.agent.decision_history_file.exists()
        
        # Load in new agent
        agent2 = AutonomousAgent(memory_path=self.temp_dir)
        agent2.wake()
        
        assert len(agent2.decision_history) > 0
    
    def test_state_tracking(self):
        """Test state tracks actions correctly"""
        self.agent.wake()
        initial_actions = self.agent.state.get('total_actions', 0)
        
        # Execute an action
        planned_actions = [{
            'type': 'test_action',
            'confidence': 0.95,
            'benefit_score': 0.8
        }]
        
        self.agent.act(planned_actions)
        
        # Check state updated
        assert self.agent.state['total_actions'] > initial_actions


def test_agent_complete_cycle():
    """Test complete agent cycle from wake to sleep"""
    with tempfile.TemporaryDirectory() as temp_dir:
        agent = AutonomousAgent(memory_path=temp_dir)
        
        # Run wake
        agent.wake()
        assert agent.state['wake_count'] == 1
        
        # Run perceive
        perception = agent.perceive()
        assert 'environment' in perception
        
        # Run reason
        actions = agent.reason(perception)
        assert isinstance(actions, list)
        
        # Run act (may have no actions if World Tour unavailable)
        if actions:
            results = agent.act(actions)
            assert len(results) > 0
        
            # Run learn
            agent.learn(results)
        
        # Run sleep
        agent.sleep()
        
        # Verify memory files exist
        state_file = Path(temp_dir) / "state.json"
        assert state_file.exists()


def test_agent_handles_rejection():
    """Test agent handles rejected actions correctly"""
    with tempfile.TemporaryDirectory() as temp_dir:
        agent = AutonomousAgent(memory_path=temp_dir)
        agent.wake()
        
        # Create action that will be rejected (low confidence)
        planned_actions = [{
            'type': 'generate_content',
            'confidence': 0.3,  # Too low
            'benefit_score': 0.5,
            'content': 'Test'
        }]
        
        results = agent.act(planned_actions)
        
        assert len(results) > 0
        assert results[0]['outcome'] == 'rejected'


if __name__ == "__main__":
    # Run basic smoke test
    print("=" * 60)
    print("🧪 Running Autonomous Agent Tests")
    print("=" * 60)
    
    test_agent_complete_cycle()
    print("✅ Complete agent cycle works")
    
    test_agent_handles_rejection()
    print("✅ Agent handles rejection correctly")
    
    test_suite = TestAutonomousAgent()
    test_suite.setup_method()
    
    test_suite.test_initialization()
    print("✅ Initialization works")
    
    test_suite.test_wake_creates_state()
    print("✅ Wake creates state")
    
    test_suite.test_perceive_returns_environment()
    print("✅ Perceive returns environment")
    
    test_suite.test_sleep_saves_memory()
    print("✅ Sleep saves memory")
    
    print()
    print("=" * 60)
    print("✅ ALL AUTONOMOUS AGENT TESTS PASSED")
    print("=" * 60)
