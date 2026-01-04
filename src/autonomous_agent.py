"""
Autonomous Agent - Main Agent Orchestrator

Purpose: Main agent loop that runs on GitHub Actions schedule with
persistent memory, ethical validation, and World Tour integration.

Key Features:
- Wake/sleep cycle with memory persistence
- Ethical validation via Reasoning Middleware
- Integration with existing World Tour system
- Decision logging and audit trail
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from rule_bank import RuleBank
from reasoning_middleware import ReasoningMiddleware

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AutonomousAgent:
    """
    Autonomous agent with persistent memory and ethical governance.
    
    Implements a complete wake-perceive-reason-act-learn-sleep cycle
    with validation against Bahá'í principles.
    """
    
    def __init__(self, memory_path: str = ".agent-memory"):
        """
        Initialize autonomous agent with memory path.
        
        Args:
            memory_path: Directory path for persistent memory storage
        """
        self.memory_path = Path(memory_path)
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize ethical systems
        self.rule_bank = RuleBank(memory_path)
        self.middleware = ReasoningMiddleware(self.rule_bank)
        
        # Memory files
        self.state_file = self.memory_path / "state.json"
        self.decision_history_file = self.memory_path / "decision_history.json"
        self.learned_patterns_file = self.memory_path / "learned_patterns.json"
        
        # Agent state
        self.state = {}
        self.decision_history = []
        self.learned_patterns = []
        
        logger.info(f"Autonomous Agent initialized with memory at {self.memory_path}")
    
    def wake(self):
        """
        Wake up: Load persistent memory from previous cycles.
        """
        logger.info("=" * 70)
        logger.info("🌅 AUTONOMOUS AGENT WAKING UP")
        logger.info("=" * 70)
        
        # Load state
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    self.state = json.load(f)
                logger.info(f"Loaded state from {self.state_file}")
            except Exception as e:
                logger.warning(f"Could not load state: {e}, starting fresh")
                self.state = self._initialize_state()
        else:
            self.state = self._initialize_state()
        
        # Load decision history
        if self.decision_history_file.exists():
            try:
                with open(self.decision_history_file, 'r') as f:
                    data = json.load(f)
                    self.decision_history = data.get('decisions', [])
                logger.info(f"Loaded {len(self.decision_history)} past decisions")
            except Exception as e:
                logger.warning(f"Could not load decision history: {e}")
                self.decision_history = []
        
        # Load learned patterns
        if self.learned_patterns_file.exists():
            try:
                with open(self.learned_patterns_file, 'r') as f:
                    data = json.load(f)
                    self.learned_patterns = data.get('patterns', [])
                logger.info(f"Loaded {len(self.learned_patterns)} learned patterns")
            except Exception as e:
                logger.warning(f"Could not load learned patterns: {e}")
                self.learned_patterns = []
        
        # Update wake count
        self.state['wake_count'] = self.state.get('wake_count', 0) + 1
        self.state['last_wake'] = datetime.utcnow().isoformat() + "Z"
        
        logger.info(f"Wake count: {self.state['wake_count']}")
        logger.info("Memory loaded successfully")
    
    def _initialize_state(self) -> Dict[str, Any]:
        """Initialize fresh agent state."""
        return {
            "agent_version": "1.0.0",
            "created_at": datetime.utcnow().isoformat() + "Z",
            "wake_count": 0,
            "last_wake": None,
            "total_actions": 0,
            "successful_actions": 0,
            "failed_actions": 0,
            "ethical_violations": 0,
            "current_mission": "world_tour_content_generation"
        }
    
    def perceive(self) -> Dict[str, Any]:
        """
        Perceive: Read repository state and environment.
        
        Returns:
            Dictionary with perceived state
        """
        logger.info("-" * 70)
        logger.info("👀 PERCEIVING ENVIRONMENT")
        logger.info("-" * 70)
        
        perception = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "environment": "github_actions",
            "mission": self.state.get('current_mission', 'world_tour'),
            "wake_count": self.state.get('wake_count', 0)
        }
        
        # Check if World Tour system is available
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
            from worldtour_generator import WorldtourGenerator
            
            generator = WorldtourGenerator()
            next_city = generator.get_next_city()
            
            if next_city:
                perception['next_city'] = {
                    "id": next_city['id'],
                    "name": next_city['name'],
                    "country": next_city['country']
                }
                logger.info(f"Next city in queue: {next_city['name']}, {next_city['country']}")
            else:
                perception['next_city'] = None
                logger.info("No cities remaining in World Tour queue")
            
            perception['worldtour_available'] = True
        except Exception as e:
            logger.warning(f"Could not access World Tour system: {e}")
            perception['worldtour_available'] = False
            perception['next_city'] = None
        
        logger.info("Perception complete")
        return perception
    
    def reason(self, perception: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Reason: Decide what actions to take based on perception.
        
        Args:
            perception: Perceived environment state
        
        Returns:
            List of planned actions
        """
        logger.info("-" * 70)
        logger.info("🤔 REASONING ABOUT ACTIONS")
        logger.info("-" * 70)
        
        planned_actions = []
        
        # Mission: World Tour content generation
        if perception.get('worldtour_available') and perception.get('next_city'):
            city = perception['next_city']
            
            # Plan action to generate World Tour content
            action = {
                "type": "generate_world_tour_content",
                "city_id": city['id'],
                "city_name": city['name'],
                "country": city['country'],
                "personality": "john_cleese",  # Could rotate personalities
                "content_type": "city_review",
                "confidence": 0.85,
                "benefit_score": 0.8,  # High benefit: bringing smiles to people
                "user_facing": True,
                "expected_reach": 1000,
                "reasoning": f"Daily World Tour content for {city['name']}"
            }
            
            planned_actions.append(action)
            logger.info(f"Planned: Generate content for {city['name']}")
        else:
            logger.info("No World Tour actions available")
        
        # Could add more action types here (e.g., maintenance, analytics)
        
        logger.info(f"Reasoning complete: {len(planned_actions)} actions planned")
        return planned_actions
    
    def act(self, planned_actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Act: Execute planned actions with ethical validation.
        
        Args:
            planned_actions: List of actions to execute
        
        Returns:
            List of execution results
        """
        logger.info("-" * 70)
        logger.info("⚡ EXECUTING ACTIONS")
        logger.info("-" * 70)
        
        results = []
        
        for action in planned_actions:
            logger.info(f"Processing action: {action['type']}")
            
            # Validate action through middleware
            validation_result = self.middleware.intercept(action)
            
            if validation_result['status'] == 'approved':
                # Execute the action
                execution_result = self._execute_action(action)
                execution_result['validation'] = validation_result
                results.append(execution_result)
                
                if execution_result['outcome'] == 'success':
                    self.state['successful_actions'] = self.state.get('successful_actions', 0) + 1
                else:
                    self.state['failed_actions'] = self.state.get('failed_actions', 0) + 1
                
            elif validation_result['status'] == 'rejected':
                logger.warning(f"Action rejected: {validation_result['reasoning']}")
                self.state['ethical_violations'] = self.state.get('ethical_violations', 0) + 1
                
                results.append({
                    "action": action,
                    "outcome": "rejected",
                    "validation": validation_result,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })
            
            elif validation_result['status'] == 'requires_review':
                logger.info(f"Action requires human review: {validation_result['reasoning']}")
                
                results.append({
                    "action": action,
                    "outcome": "pending_review",
                    "validation": validation_result,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })
            
            # Record decision in history
            decision_record = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "action": action,
                "validation": validation_result,
                "outcome": results[-1].get('outcome', 'unknown'),
                "bahai_alignment": self.rule_bank.get_principle_alignment(action)
            }
            self.decision_history.append(decision_record)
        
        self.state['total_actions'] = self.state.get('total_actions', 0) + len(planned_actions)
        
        logger.info(f"Execution complete: {len(results)} actions processed")
        return results
    
    def _execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a validated action.
        
        Args:
            action: Action to execute
        
        Returns:
            Execution result dictionary
        """
        action_type = action.get('type')
        
        if action_type == "generate_world_tour_content":
            return self._execute_world_tour_generation(action)
        else:
            logger.warning(f"Unknown action type: {action_type}")
            return {
                "action": action,
                "outcome": "failed",
                "error": f"Unknown action type: {action_type}",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
    
    def _execute_world_tour_generation(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute World Tour content generation.
        
        Args:
            action: World Tour generation action
        
        Returns:
            Execution result
        """
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
            from worldtour_generator import WorldtourGenerator
            
            generator = WorldtourGenerator()
            
            city_id = action['city_id']
            personality = action.get('personality', 'john_cleese')
            content_type = action.get('content_type', 'city_review')
            
            # Generate content
            content = generator.generate_city_content(
                city_id=city_id,
                personality=personality,
                content_type=content_type
            )
            
            logger.info(f"Generated content for {action['city_name']}")
            logger.info(f"Personality: {personality}, Type: {content_type}")
            
            # In a real implementation, would post to channels here
            # For now, just log the success
            
            return {
                "action": action,
                "outcome": "success",
                "content": content,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
        except Exception as e:
            logger.error(f"Failed to generate World Tour content: {e}")
            return {
                "action": action,
                "outcome": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
    
    def learn(self, results: List[Dict[str, Any]]):
        """
        Learn: Update Rule Bank based on action outcomes.
        
        Args:
            results: List of execution results
        """
        logger.info("-" * 70)
        logger.info("📚 LEARNING FROM OUTCOMES")
        logger.info("-" * 70)
        
        # Analyze results for patterns
        successful = [r for r in results if r['outcome'] == 'success']
        failed = [r for r in results if r['outcome'] == 'failed']
        rejected = [r for r in results if r['outcome'] == 'rejected']
        
        logger.info(f"Results: {len(successful)} successful, {len(failed)} failed, {len(rejected)} rejected")
        
        # Learn from failures (simplified for MVP)
        if failed:
            for result in failed:
                error = result.get('error', 'Unknown error')
                logger.info(f"Learning from failure: {error}")
                # In production, would analyze patterns and create new rules
        
        # Learn from rejections
        if rejected:
            for result in rejected:
                violation = result.get('validation', {})
                violated_rules = violation.get('violated_rules', [])
                logger.info(f"Analyzing {len(violated_rules)} rule violations")
        
        # Save learned patterns
        if results:
            pattern = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "successful_count": len(successful),
                "failed_count": len(failed),
                "rejected_count": len(rejected),
                "note": "Pattern recognition placeholder for future ML integration"
            }
            self.learned_patterns.append(pattern)
        
        logger.info("Learning complete")
    
    def sleep(self):
        """
        Sleep: Save persistent memory for next cycle.
        """
        logger.info("-" * 70)
        logger.info("💤 SAVING MEMORY AND GOING TO SLEEP")
        logger.info("-" * 70)
        
        # Update state
        self.state['last_sleep'] = datetime.utcnow().isoformat() + "Z"
        
        # Save state
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            logger.info(f"Saved state to {self.state_file}")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
        
        # Save decision history
        try:
            with open(self.decision_history_file, 'w') as f:
                json.dump({
                    "decisions": self.decision_history,
                    "last_updated": datetime.utcnow().isoformat() + "Z"
                }, f, indent=2)
            logger.info(f"Saved {len(self.decision_history)} decisions")
        except Exception as e:
            logger.error(f"Failed to save decision history: {e}")
        
        # Save learned patterns
        try:
            with open(self.learned_patterns_file, 'w') as f:
                json.dump({
                    "patterns": self.learned_patterns,
                    "last_updated": datetime.utcnow().isoformat() + "Z"
                }, f, indent=2)
            logger.info(f"Saved {len(self.learned_patterns)} learned patterns")
        except Exception as e:
            logger.error(f"Failed to save learned patterns: {e}")
        
        # Save Rule Bank
        self.rule_bank.save_rules()
        
        logger.info("=" * 70)
        logger.info("🌙 AUTONOMOUS AGENT SLEEPING")
        logger.info("=" * 70)
        logger.info("")
        logger.info("Summary:")
        logger.info(f"  Wake count: {self.state['wake_count']}")
        logger.info(f"  Total actions: {self.state['total_actions']}")
        logger.info(f"  Successful: {self.state['successful_actions']}")
        logger.info(f"  Failed: {self.state['failed_actions']}")
        logger.info(f"  Ethical violations: {self.state['ethical_violations']}")
        logger.info("")
        logger.info("Memory persisted. See you next cycle! 🌅")
        logger.info("=" * 70)
    
    def run_cycle(self):
        """
        Run a complete agent cycle: wake -> perceive -> reason -> act -> learn -> sleep
        """
        try:
            # Wake up
            self.wake()
            
            # Perceive environment
            perception = self.perceive()
            
            # Reason about actions
            planned_actions = self.reason(perception)
            
            # Act on plans
            results = self.act(planned_actions)
            
            # Learn from outcomes
            self.learn(results)
            
            # Go to sleep
            self.sleep()
            
            return True
            
        except Exception as e:
            logger.error(f"Agent cycle failed: {e}", exc_info=True)
            # Still try to save state
            try:
                self.sleep()
            except:
                pass
            return False


def main():
    """Main entry point for autonomous agent."""
    parser = argparse.ArgumentParser(
        description="🤖 UMAJA Autonomous Agent - Ethical AI with Persistent Memory"
    )
    parser.add_argument(
        "--memory-path",
        default=".agent-memory",
        help="Path to persistent memory directory"
    )
    
    args = parser.parse_args()
    
    # Create and run agent
    agent = AutonomousAgent(memory_path=args.memory_path)
    success = agent.run_cycle()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
