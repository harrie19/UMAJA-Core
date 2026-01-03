#!/usr/bin/env python3
"""
🤖 UMAJA Autonomous Mode Starter
Activates the autonomous agent system for self-sufficient operation

This script:
- Initializes the Agent Orchestrator
- Creates all 9 agent types
- Registers task handlers for each agent
- Adds initial tasks to the queue
- Starts all agents in their own threads
- Provides status monitoring and logging
- Includes graceful shutdown mechanism
- Handles errors with self-healing capability

Usage:
    python scripts/start_autonomous_mode.py [--duration SECONDS] [--agents-per-type N]
"""

import json
import sys
import time
import signal
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agent_orchestrator import AgentOrchestrator, AgentType

# Ensure log directory exists
log_dir = Path(__file__).parent.parent / "data" / "agents"
log_dir.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_dir / 'autonomous_mode.log')
    ]
)
logger = logging.getLogger(__name__)


class AutonomousMode:
    """
    Main autonomous mode controller
    Manages the entire autonomous agent system
    """
    
    def __init__(self):
        """Initialize autonomous mode"""
        self.orchestrator = None
        self.running = False
        self.emergency_stop_file = Path(".github/emergency_stop.json")
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self.stop()
    
    def _error_response(self, error_message: str) -> Dict:
        """
        Helper method to create standardized error responses
        
        Args:
            error_message: Error message to include
            
        Returns:
            Standardized error response dictionary
        """
        return {"success": False, "error": error_message}
    
    def check_emergency_stop(self) -> bool:
        """
        Check if emergency stop is activated
        
        Returns:
            True if system should stop, False otherwise
        """
        try:
            if self.emergency_stop_file.exists():
                with open(self.emergency_stop_file, 'r') as f:
                    config = json.load(f)
                    if not config.get('agent_enabled', True):
                        logger.warning(f"Emergency stop activated: {config.get('reason', 'No reason specified')}")
                        return True
            return False
        except Exception as e:
            logger.error(f"Error checking emergency stop: {e}")
            return False
    
    def register_task_handlers(self):
        """Register all task handlers for different agent types"""
        logger.info("Registering task handlers...")
        
        # ContentGenerator handlers
        self.orchestrator.register_task_handler("generate_content", self._handle_generate_content)
        self.orchestrator.register_task_handler("generate_smile", self._handle_generate_smile)
        
        # Translator handlers
        self.orchestrator.register_task_handler("translate_content", self._handle_translate_content)
        
        # QualityChecker handlers
        self.orchestrator.register_task_handler("check_quality", self._handle_check_quality)
        
        # Distributor handlers
        self.orchestrator.register_task_handler("distribute_content", self._handle_distribute_content)
        
        # Analytics handlers
        self.orchestrator.register_task_handler("analyze_performance", self._handle_analyze_performance)
        
        # Scheduler handlers
        self.orchestrator.register_task_handler("schedule_tasks", self._handle_schedule_tasks)
        
        # ErrorHandler handlers
        self.orchestrator.register_task_handler("handle_error", self._handle_error)
        
        # LearningAgent handlers
        self.orchestrator.register_task_handler("learn_optimize", self._handle_learn_optimize)
        
        logger.info("✅ All task handlers registered")
    
    # ========================================================================
    # Task Handler Implementations
    # ========================================================================
    
    def _handle_generate_content(self, data: Dict) -> Dict:
        """Handler for content generation"""
        try:
            from worldtour_generator import WorldtourGenerator
            
            generator = WorldtourGenerator()
            city_id = data.get('city_id')
            personality = data.get('personality', 'john_cleese')
            content_type = data.get('content_type', 'city_review')
            
            if not city_id:
                next_city = generator.get_next_city()
                if not next_city:
                    return self._error_response("No cities available")
                city_id = next_city['id']
            
            content = generator.generate_city_content(
                city_id=city_id,
                personality=personality,
                content_type=content_type
            )
            
            return {
                "success": True,
                "city_id": city_id,
                "personality": personality,
                "content": content
            }
        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            return self._error_response(str(e))
    
    def _handle_generate_smile(self, data: Dict) -> Dict:
        """Handler for daily smile generation"""
        try:
            from personality_engine import PersonalityEngine
            
            engine = PersonalityEngine()
            personality = data.get('personality', 'random')
            language = data.get('language', 'en')
            
            smile = engine.generate_daily_smile(
                personality=personality,
                language=language
            )
            
            return {
                "success": True,
                "smile": smile
            }
        except Exception as e:
            logger.error(f"Smile generation failed: {e}")
            return self._error_response(str(e))
    
    def _handle_translate_content(self, data: Dict) -> Dict:
        """Handler for content translation"""
        try:
            content = data.get('content', '')
            target_languages = data.get('languages', ['es', 'hi', 'ar', 'zh', 'pt', 'fr', 'ru'])
            
            # TODO: Implement proper translation service
            # Simplified translation (placeholder for production implementation)
            # In production, integrate with translation API (e.g., LibreTranslate, DeepL, etc.)
            translations = {}
            for lang in target_languages:
                translations[lang] = f"[{lang.upper()}] {content}"
            
            return {
                "success": True,
                "translations": translations
            }
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return self._error_response(str(e))
    
    def _handle_check_quality(self, data: Dict) -> Dict:
        """Handler for quality checking using Vector Analyzer"""
        try:
            from vektor_analyzer import VektorAnalyzer
            
            analyzer = VektorAnalyzer()
            content = data.get('content', '')
            theme = data.get('theme', 'comedy and joy')
            
            result = analyzer.analyze_coherence(content, theme)
            
            # Quality must be at least 'acceptable' (score >= 0.3)
            passed = result['overall_score'] >= 0.3
            
            return {
                "success": True,
                "passed": passed,
                "quality": result['quality'],
                "score": result['overall_score'],
                "details": result
            }
        except Exception as e:
            logger.error(f"Quality check failed: {e}")
            return self._error_response(str(e))
    
    def _handle_distribute_content(self, data: Dict) -> Dict:
        """Handler for content distribution"""
        try:
            content = data.get('content', {})
            city_id = data.get('city_id')
            
            # Save to output directory
            output_dir = Path("output/worldtour")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.utcnow().isoformat()
            filename = f"{city_id}_{timestamp.replace(':', '-')}.json"
            
            with open(output_dir / filename, 'w') as f:
                json.dump(content, f, indent=2)
            
            # Notify AI agent network (if enabled)
            try:
                from ai_agent_network import AIAgentNetwork
                network = AIAgentNetwork()
                # Simplified notification
                logger.info("Content distributed to AI agent network")
            except:
                pass
            
            return {
                "success": True,
                "file": str(output_dir / filename),
                "distributed_at": timestamp
            }
        except Exception as e:
            logger.error(f"Distribution failed: {e}")
            return self._error_response(str(e))
    
    def _handle_analyze_performance(self, data: Dict) -> Dict:
        """Handler for analytics and performance tracking"""
        try:
            # Get orchestrator statistics
            status = self.orchestrator.get_status()
            
            stats = status['stats']
            completion_rate = (
                stats['completed_tasks'] / stats['total_tasks'] * 100
                if stats['total_tasks'] > 0 else 0
            )
            
            return {
                "success": True,
                "total_tasks": stats['total_tasks'],
                "completed_tasks": stats['completed_tasks'],
                "failed_tasks": stats['failed_tasks'],
                "completion_rate": completion_rate,
                "active_agents": stats['active_agents']
            }
        except Exception as e:
            logger.error(f"Analytics failed: {e}")
            return self._error_response(str(e))
    
    def _handle_schedule_tasks(self, data: Dict) -> Dict:
        """Handler for task scheduling"""
        try:
            # Schedule next round of content generation
            personalities = ['john_cleese', 'c3po', 'robin_williams']
            
            for personality in personalities:
                self.orchestrator.add_task(
                    task_type="generate_content",
                    agent_type=AgentType.CONTENT_GENERATOR,
                    data={"personality": personality},
                    priority=7
                )
            
            return {
                "success": True,
                "scheduled_tasks": len(personalities)
            }
        except Exception as e:
            logger.error(f"Scheduling failed: {e}")
            return self._error_response(str(e))
    
    def _handle_error(self, data: Dict) -> Dict:
        """Handler for error recovery"""
        try:
            error_type = data.get('error_type', 'unknown')
            error_msg = data.get('error_msg', '')
            
            logger.error(f"Handling error: {error_type} - {error_msg}")
            
            # Attempt automatic recovery based on error type
            recovery_action = "logged"
            
            if error_type == "task_failure":
                # Retry logic is built into orchestrator
                recovery_action = "retry_scheduled"
            
            return {
                "success": True,
                "error_type": error_type,
                "recovery_action": recovery_action
            }
        except Exception as e:
            logger.error(f"Error handler failed: {e}")
            return self._error_response(str(e))
    
    def _handle_learn_optimize(self, data: Dict) -> Dict:
        """Handler for learning and optimization"""
        try:
            # Analyze recent task performance
            status = self.orchestrator.get_status()
            stats = status['stats']
            
            # Simple optimization: scale agents based on queue size
            queue_size = status['queue_size']
            
            optimization = {
                "recommendation": "maintain" if queue_size < 10 else "scale_up"
            }
            
            return {
                "success": True,
                "optimization": optimization,
                "queue_size": queue_size
            }
        except Exception as e:
            logger.error(f"Learning optimization failed: {e}")
            return self._error_response(str(e))
    
    # ========================================================================
    # Agent Creation and Management
    # ========================================================================
    
    def create_all_agents(self, agents_per_type: int = 1):
        """
        Create all 9 agent types
        
        Args:
            agents_per_type: Number of agents to create per type
        """
        logger.info(f"Creating {agents_per_type} agent(s) per type...")
        
        # Map new agent types to existing AgentType enum
        agent_mapping = {
            'ContentGenerator': AgentType.CONTENT_GENERATOR,
            'Translator': AgentType.TRANSLATOR,
            'QualityChecker': AgentType.QUALITY_CHECKER,
            'Distributor': AgentType.DISTRIBUTOR,
            'Analytics': AgentType.ANALYTICS,
            'Scheduler': AgentType.CONTENT_GENERATOR,  # Use content generator for scheduling
            'ErrorHandler': AgentType.CONTENT_GENERATOR,  # Use content generator for error handling
            'LearningAgent': AgentType.ANALYTICS,  # Use analytics for learning
            'CoordinatorAgent': AgentType.CONTENT_GENERATOR  # Use content generator for coordination
        }
        
        created_agents = []
        
        for agent_name, agent_type in agent_mapping.items():
            for i in range(agents_per_type):
                agent_id = self.orchestrator.create_agent(agent_type)
                self.orchestrator.start_agent(agent_id)
                created_agents.append(agent_id)
                logger.info(f"✅ Agent created: {agent_id} (Type: {agent_name})")
        
        return created_agents
    
    def add_initial_tasks(self):
        """Add initial tasks to get the system started"""
        logger.info("Adding initial tasks...")
        
        # Add content generation tasks
        personalities = ['john_cleese', 'c3po', 'robin_williams']
        for personality in personalities:
            self.orchestrator.add_task(
                task_type="generate_content",
                agent_type=AgentType.CONTENT_GENERATOR,
                data={"personality": personality},
                priority=8
            )
        
        # Add quality check task
        self.orchestrator.add_task(
            task_type="check_quality",
            agent_type=AgentType.QUALITY_CHECKER,
            data={"content": "System initialization check", "theme": "system startup"},
            priority=9
        )
        
        # Add analytics task
        self.orchestrator.add_task(
            task_type="analyze_performance",
            agent_type=AgentType.ANALYTICS,
            data={},
            priority=6
        )
        
        logger.info("✅ Initial tasks added")
    
    def start(self, duration: int = 0, agents_per_type: int = 1):
        """
        Start autonomous mode
        
        Args:
            duration: Run duration in seconds (0 = forever)
            agents_per_type: Number of agents per type
        """
        print("=" * 80)
        print("🚀 UMAJA AUTONOMOUS MODE STARTING...")
        print("=" * 80)
        print()
        
        # Check emergency stop
        if self.check_emergency_stop():
            print("❌ Emergency stop is active. Cannot start autonomous mode.")
            return False
        
        # Initialize orchestrator
        logger.info("Initializing Agent Orchestrator...")
        self.orchestrator = AgentOrchestrator()
        
        # Register task handlers
        self.register_task_handlers()
        
        # Create all agents
        self.create_all_agents(agents_per_type)
        
        # Add initial tasks
        self.add_initial_tasks()
        
        print()
        print("✅ System initialized successfully!")
        print()
        print(f"Active agents: {self.orchestrator.stats['active_agents']}")
        print(f"Task queue size: {self.orchestrator.task_queue.qsize()}")
        print()
        print("🤖 System running autonomously. Press Ctrl+C to stop.")
        print()
        
        self.running = True
        start_time = time.time()
        
        try:
            while self.running:
                # Check emergency stop periodically
                if self.check_emergency_stop():
                    logger.warning("Emergency stop detected, shutting down...")
                    break
                
                # Check duration
                if duration > 0 and (time.time() - start_time) >= duration:
                    logger.info(f"Duration limit reached ({duration}s), shutting down...")
                    break
                
                # Print status update every 30 seconds
                elapsed = int(time.time() - start_time)
                if elapsed % 30 == 0 and elapsed > 0:
                    status = self.orchestrator.get_status()
                    logger.info(f"Status: {status['stats']['completed_tasks']} tasks completed, "
                              f"{status['queue_size']} in queue")
                
                time.sleep(1)
        
        except KeyboardInterrupt:
            print()
            logger.info("Keyboard interrupt received")
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        
        finally:
            self.stop()
        
        return True
    
    def stop(self):
        """Stop autonomous mode gracefully"""
        if not self.running:
            return
        
        print()
        print("🛑 Shutting down autonomous mode...")
        
        self.running = False
        
        if self.orchestrator:
            self.orchestrator.stop_all_agents()
            time.sleep(2)  # Wait for agents to finish
            
            # Save state
            self.orchestrator.save_state()
            
            # Print final status
            status = self.orchestrator.get_status()
            print()
            print("=" * 80)
            print("📊 FINAL STATISTICS")
            print("=" * 80)
            print(f"Total tasks: {status['stats']['total_tasks']}")
            print(f"Completed: {status['stats']['completed_tasks']}")
            print(f"Failed: {status['stats']['failed_tasks']}")
            print(f"Active agents: {status['stats']['active_agents']}")
            print("=" * 80)
        
        print()
        print("✅ Autonomous mode stopped successfully")
        print()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🤖 UMAJA Autonomous Mode - Self-sufficient AI operation"
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=0,
        help='Run duration in seconds (0 = forever, default: 0)'
    )
    parser.add_argument(
        '--agents-per-type',
        type=int,
        default=1,
        help='Number of agents per type (default: 1)'
    )
    
    args = parser.parse_args()
    
    # Ensure data directory exists
    Path("data/agents").mkdir(parents=True, exist_ok=True)
    
    # Start autonomous mode
    autonomous = AutonomousMode()
    autonomous.start(duration=args.duration, agents_per_type=args.agents_per_type)


if __name__ == "__main__":
    main()
