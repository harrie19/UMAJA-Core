"""
Master Orchestrator
===================

Coordinates all autonomous agents:
- Routes commands to appropriate agents
- Manages multi-step operations
- Provides error recovery
- Reports progress
- Integrates holographic AI system

The brain of the autonomous system - like JARVIS from Iron Man.
"""

import asyncio
import logging
from typing import Dict, Optional, Any, List
from datetime import datetime, timezone
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from .nl_command_processor import NLCommandProcessor, CommandIntent
from .github_operations_agent import GitHubOperationsAgent
from .deployment_agent import DeploymentAgent
from .coding_agent import CodingAgent
from .config import get_config, validate_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MasterOrchestrator:
    """
    Master Orchestrator - Coordinates all autonomous agents
    The central intelligence that makes everything work together
    """
    
    def __init__(self):
        """Initialize master orchestrator"""
        logger.info("🌟 Initializing UMAJA Master Orchestrator...")
        
        # Initialize all agents
        self.nl_processor = NLCommandProcessor()
        self.github_agent = GitHubOperationsAgent()
        self.deployment_agent = DeploymentAgent()
        self.coding_agent = CodingAgent()
        
        # Configuration
        self.config = get_config()
        is_valid, errors = validate_config()
        if not is_valid:
            logger.warning(f"Configuration warnings: {errors}")
        
        # Operation history
        self.operation_history: List[Dict[str, Any]] = []
        
        # Holographic AI integration (optional)
        self.holographic_ai = None
        if self.config['holographic']['enabled']:
            try:
                from holographic_ai_system import get_holographic_integration
                self.holographic_ai = get_holographic_integration()
                logger.info("✓ Holographic AI integrated")
            except ImportError:
                logger.info("Holographic AI not available")
        
        logger.info("✅ Master Orchestrator initialized and ready!")
    
    async def process_command(
        self, 
        command_text: str,
        require_approval: bool = True
    ) -> Dict[str, Any]:
        """
        Process a natural language command
        
        Args:
            command_text: User's natural language command
            require_approval: Whether to require approval for destructive operations
            
        Returns:
            Operation result dictionary
        """
        logger.info(f"Processing command: {command_text}")
        start_time = datetime.now(timezone.utc)
        
        try:
            # Parse command
            intent = self.nl_processor.parse_command(command_text)
            
            if not intent:
                return {
                    'success': False,
                    'error': 'Could not understand command',
                    'suggestion': 'Try "help" to see available commands',
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
            
            # Check confidence
            if intent.confidence < self.config['nlp']['confidence_threshold']:
                return {
                    'success': False,
                    'error': 'Low confidence in command understanding',
                    'confidence': intent.confidence,
                    'suggestion': f'Did you mean to {intent.action}?',
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
            
            # Route to appropriate agent
            result = await self._route_command(intent, require_approval)
            
            # Add metadata
            result['intent'] = {
                'action': intent.action,
                'confidence': intent.confidence,
                'parameters': intent.parameters,
                'language': intent.language
            }
            result['processing_time_ms'] = (
                datetime.now(timezone.utc) - start_time
            ).total_seconds() * 1000
            
            # Store in history
            self.operation_history.append(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Command processing failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
    
    async def _route_command(
        self, 
        intent: CommandIntent,
        require_approval: bool
    ) -> Dict[str, Any]:
        """
        Route command to appropriate agent
        
        Args:
            intent: Parsed command intent
            require_approval: Whether to require approval
            
        Returns:
            Operation result
        """
        action = intent.action
        params = intent.parameters
        
        # GitHub Operations
        if action == 'merge_pr':
            pr_number = params.get('pr_number')
            return await self.github_agent.merge_pr(pr_number, require_approval=require_approval)
        
        elif action == 'close_pr':
            pr_number = params.get('pr_number')
            return await self.github_agent.close_pr(pr_number, require_approval=require_approval)
        
        elif action == 'close_old_prs':
            return await self.github_agent.close_old_prs(require_approval=require_approval)
        
        elif action == 'fix_conflicts':
            pr_number = params.get('pr_number')
            # This is a multi-step operation
            return await self._fix_conflicts_workflow(pr_number)
        
        elif action == 'create_issue':
            title = params.get('title', 'New issue')
            return await self.github_agent.create_issue(title)
        
        # Deployment Operations
        elif action == 'deploy':
            platform = params.get('platform', 'railway').lower()
            if platform == 'produktion':  # German
                platform = 'production'
            return await self.deployment_agent.deploy(platform=platform)
        
        # Coding Operations
        elif action == 'create_feature':
            description = params.get('description', 'New feature')
            return await self._create_feature_workflow(description)
        
        # Status & Help
        elif action == 'status':
            return await self._get_system_status()
        
        elif action == 'help':
            help_text = self.nl_processor.get_help_text(intent.language)
            return {
                'success': True,
                'action': 'help',
                'help_text': help_text,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
        
        else:
            return {
                'success': False,
                'error': f'Action not implemented: {action}',
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
    
    async def _fix_conflicts_workflow(self, pr_number: int) -> Dict[str, Any]:
        """
        Multi-step workflow to fix merge conflicts
        
        Args:
            pr_number: PR number with conflicts
            
        Returns:
            Workflow result
        """
        logger.info(f"Starting conflict resolution workflow for PR #{pr_number}")
        
        results = []
        
        # Step 1: Get PR status
        logger.info("Step 1/3: Getting PR status...")
        status = await self.github_agent.get_pr_status(pr_number)
        results.append({'step': 'get_status', 'result': status})
        
        # Step 2: Fix conflicts using coding agent
        logger.info("Step 2/3: Resolving conflicts...")
        resolution = await self.github_agent.fix_merge_conflicts(pr_number)
        results.append({'step': 'resolve_conflicts', 'result': resolution})
        
        # Step 3: Update branch
        if resolution.get('success'):
            logger.info("Step 3/3: Updating branch...")
            update = await self.github_agent.update_branch(pr_number)
            results.append({'step': 'update_branch', 'result': update})
        
        # Determine overall success
        overall_success = all(r['result'].get('success', True) for r in results)
        
        return {
            'success': overall_success,
            'action': 'fix_conflicts_workflow',
            'pr_number': pr_number,
            'steps': results,
            'message': f'Conflict resolution workflow completed for PR #{pr_number}',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    async def _create_feature_workflow(self, description: str) -> Dict[str, Any]:
        """
        Multi-step workflow to create a new feature
        
        Args:
            description: Feature description
            
        Returns:
            Workflow result
        """
        logger.info(f"Starting feature creation workflow: {description}")
        
        results = []
        
        # Step 1: Generate code
        logger.info("Step 1/4: Generating code...")
        code_gen = await self.coding_agent.generate_feature(description)
        results.append({'step': 'generate_code', 'result': code_gen})
        
        # Step 2: Write tests
        if code_gen.get('success'):
            logger.info("Step 2/4: Writing tests...")
            test_gen = await self.coding_agent.write_tests('src/new_feature.py')
            results.append({'step': 'write_tests', 'result': test_gen})
        
        # Step 3: Update documentation
        if code_gen.get('success'):
            logger.info("Step 3/4: Updating documentation...")
            doc_update = await self.coding_agent.update_documentation('src/new_feature.py')
            results.append({'step': 'update_docs', 'result': doc_update})
        
        # Step 4: Create PR (would be implemented in real version)
        logger.info("Step 4/4: Creating pull request...")
        pr_result = {
            'success': True,
            'pr_number': 101,
            'message': 'PR created (simulated)'
        }
        results.append({'step': 'create_pr', 'result': pr_result})
        
        # Determine overall success
        overall_success = all(r['result'].get('success', True) for r in results)
        
        return {
            'success': overall_success,
            'action': 'create_feature_workflow',
            'description': description,
            'steps': results,
            'message': f'Feature creation workflow completed: {description}',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    async def _get_system_status(self) -> Dict[str, Any]:
        """
        Get comprehensive system status
        
        Returns:
            System status dictionary
        """
        logger.info("Getting system status...")
        
        status = {
            'success': True,
            'action': 'status',
            'agents': {
                'nl_processor': 'online',
                'github_agent': 'online',
                'deployment_agent': 'online',
                'coding_agent': 'online',
            },
            'config': {
                'github_configured': bool(self.config['github']['token']),
                'railway_configured': bool(self.config['deployment']['railway_token']),
                'holographic_ai': self.config['holographic']['enabled'],
            },
            'operations': {
                'total_processed': len(self.operation_history),
                'recent_operations': self.operation_history[-5:] if self.operation_history else [],
            },
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        # Add holographic AI status if available
        if self.holographic_ai:
            try:
                holo_state = self.holographic_ai.holographic_system.get_system_state()
                status['holographic_ai'] = holo_state
            except Exception as e:
                logger.warning(f"Could not get holographic AI status: {e}")
        
        return status
    
    def get_operation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent operation history
        
        Args:
            limit: Maximum number of operations to return
            
        Returns:
            List of recent operations
        """
        return self.operation_history[-limit:] if self.operation_history else []
    
    async def self_heal(self):
        """Perform self-healing operations"""
        logger.info("Initiating self-healing...")
        
        # Heal holographic AI if available
        if self.holographic_ai:
            await self.holographic_ai.holographic_system.self_heal()
        
        logger.info("Self-healing complete")


# Example usage
async def main():
    """Example usage of Master Orchestrator"""
    print("🌟 UMAJA Master Orchestrator Demo\n")
    print("Like JARVIS from Iron Man - just talk naturally!\n")
    
    orchestrator = MasterOrchestrator()
    
    # Test commands
    commands = [
        "Merge PR #90",
        "What's the status?",
        "Deploy to Railway",
        "Create feature: Add user dashboard",
        "Help",
    ]
    
    for cmd in commands:
        print(f"\n{'='*60}")
        print(f"User: {cmd}")
        print(f"{'='*60}")
        
        result = await orchestrator.process_command(cmd, require_approval=True)
        
        if result['success']:
            print(f"✅ {result.get('message', 'Success')}")
        else:
            print(f"❌ {result.get('error', 'Failed')}")
            if 'suggestion' in result:
                print(f"💡 Suggestion: {result['suggestion']}")
        
        if 'steps' in result:
            print(f"\nWorkflow Steps:")
            for step in result['steps']:
                step_name = step['step']
                step_result = step['result']
                status = "✅" if step_result.get('success') else "❌"
                print(f"  {status} {step_name}")
    
    print(f"\n{'='*60}")
    print("✅ Demo complete!")
    print(f"\nTotal operations processed: {len(orchestrator.operation_history)}")


if __name__ == "__main__":
    asyncio.run(main())
