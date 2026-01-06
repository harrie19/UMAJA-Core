"""
UMAJA Autonomous Agent System
==============================

Fully autonomous agents that handle:
- Natural language commands
- GitHub operations
- Deployment
- Code generation
- System orchestration

The user just chats naturally and says "Accept" - AI does everything else.
"""

__version__ = "1.0.0"
__author__ = "UMAJA Core Team"

from .master_orchestrator import MasterOrchestrator
from .nl_command_processor import NLCommandProcessor
from .github_operations_agent import GitHubOperationsAgent
from .deployment_agent import DeploymentAgent
from .coding_agent import CodingAgent

__all__ = [
    'MasterOrchestrator',
    'NLCommandProcessor',
    'GitHubOperationsAgent',
    'DeploymentAgent',
    'CodingAgent',
]
