"""
Test Autonomous Agent System
=============================

Comprehensive tests for the autonomous agent system including:
- Natural language command processing
- GitHub operations
- Deployment operations
- Coding operations
- Master orchestrator
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
import asyncio


# =============================================================================
# NATURAL LANGUAGE COMMAND PROCESSOR TESTS
# =============================================================================

def test_nl_processor_initialization():
    """Test that NL command processor initializes correctly"""
    from autonomous.nl_command_processor import NLCommandProcessor
    
    processor = NLCommandProcessor()
    assert processor is not None
    assert processor.command_patterns is not None
    assert len(processor.command_patterns) > 0


def test_parse_merge_pr_command():
    """Test parsing merge PR command"""
    from autonomous.nl_command_processor import NLCommandProcessor
    
    processor = NLCommandProcessor()
    
    # Test English
    intent = processor.parse_command("Merge PR #90")
    assert intent is not None
    assert intent.action == "merge_pr"
    assert intent.parameters['pr_number'] == 90
    assert intent.confidence > 0.5
    
    # Test German
    intent = processor.parse_command("PR #90 mergen")
    assert intent is not None
    assert intent.action == "merge_pr"
    assert intent.parameters['pr_number'] == 90


def test_parse_deploy_command():
    """Test parsing deployment commands"""
    from autonomous.nl_command_processor import NLCommandProcessor
    
    processor = NLCommandProcessor()
    
    intent = processor.parse_command("Deploy to Railway")
    assert intent is not None
    assert intent.action == "deploy"
    assert intent.parameters['platform'] == "railway"


def test_parse_status_command():
    """Test parsing status commands"""
    from autonomous.nl_command_processor import NLCommandProcessor
    
    processor = NLCommandProcessor()
    
    intent = processor.parse_command("What's the status?")
    assert intent is not None
    assert intent.action == "status"


def test_parse_help_command():
    """Test parsing help commands"""
    from autonomous.nl_command_processor import NLCommandProcessor
    
    processor = NLCommandProcessor()
    
    # English
    intent = processor.parse_command("help")
    assert intent is not None
    assert intent.action == "help"
    
    # German
    intent = processor.parse_command("Hilfe")
    assert intent is not None
    assert intent.action == "help"


def test_get_help_text():
    """Test getting help text"""
    from autonomous.nl_command_processor import NLCommandProcessor
    
    processor = NLCommandProcessor()
    
    help_en = processor.get_help_text('en')
    assert len(help_en) > 0
    assert 'UMAJA' in help_en
    
    help_de = processor.get_help_text('de')
    assert len(help_de) > 0
    assert 'UMAJA' in help_de


# =============================================================================
# GITHUB OPERATIONS AGENT TESTS
# =============================================================================

@pytest.mark.asyncio
async def test_github_agent_initialization():
    """Test GitHub operations agent initializes"""
    from autonomous.github_operations_agent import GitHubOperationsAgent
    
    agent = GitHubOperationsAgent()
    assert agent is not None
    assert agent.owner is not None
    assert agent.repo is not None


@pytest.mark.asyncio
async def test_merge_pr_with_approval():
    """Test merging PR with approval required"""
    from autonomous.github_operations_agent import GitHubOperationsAgent
    
    agent = GitHubOperationsAgent()
    result = await agent.merge_pr(90, require_approval=True)
    
    assert result is not None
    assert 'action' in result
    assert result['action'] == 'merge_pr'
    assert 'status' in result
    # With approval, should be awaiting
    assert result['status'] == 'awaiting_approval'


@pytest.mark.asyncio
async def test_get_pr_status():
    """Test getting PR status"""
    from autonomous.github_operations_agent import GitHubOperationsAgent
    
    agent = GitHubOperationsAgent()
    status = await agent.get_pr_status(90)
    
    assert status is not None
    assert 'pr_number' in status
    assert status['pr_number'] == 90


@pytest.mark.asyncio
async def test_create_issue():
    """Test creating an issue"""
    from autonomous.github_operations_agent import GitHubOperationsAgent
    
    agent = GitHubOperationsAgent()
    result = await agent.create_issue("Test issue", "Test body")
    
    assert result is not None
    assert result['success'] == True
    assert 'issue_number' in result


# =============================================================================
# DEPLOYMENT AGENT TESTS
# =============================================================================

@pytest.mark.asyncio
async def test_deployment_agent_initialization():
    """Test deployment agent initializes"""
    from autonomous.deployment_agent import DeploymentAgent
    
    agent = DeploymentAgent()
    assert agent is not None


@pytest.mark.asyncio
async def test_deploy_to_railway():
    """Test Railway deployment"""
    from autonomous.deployment_agent import DeploymentAgent
    
    agent = DeploymentAgent()
    result = await agent.deploy_to_railway('production')
    
    assert result is not None
    assert 'platform' in result
    assert result['platform'] == 'railway'


@pytest.mark.asyncio
async def test_get_deployment_status():
    """Test getting deployment status"""
    from autonomous.deployment_agent import DeploymentAgent
    
    agent = DeploymentAgent()
    status = await agent.get_deployment_status('railway')
    
    assert status is not None
    assert 'platform' in status
    assert status['platform'] == 'railway'


# =============================================================================
# CODING AGENT TESTS
# =============================================================================

@pytest.mark.asyncio
async def test_coding_agent_initialization():
    """Test coding agent initializes"""
    from autonomous.coding_agent import CodingAgent
    
    agent = CodingAgent()
    assert agent is not None


@pytest.mark.asyncio
async def test_generate_feature():
    """Test feature generation"""
    from autonomous.coding_agent import CodingAgent
    
    agent = CodingAgent()
    result = await agent.generate_feature("Add user authentication")
    
    assert result is not None
    assert result['success'] == True
    assert 'files' in result


@pytest.mark.asyncio
async def test_write_tests():
    """Test test generation"""
    from autonomous.coding_agent import CodingAgent
    
    agent = CodingAgent()
    result = await agent.write_tests("src/example.py")
    
    assert result is not None
    assert result['success'] == True


# =============================================================================
# MASTER ORCHESTRATOR TESTS
# =============================================================================

@pytest.mark.asyncio
async def test_orchestrator_initialization():
    """Test master orchestrator initializes"""
    from autonomous.master_orchestrator import MasterOrchestrator
    
    orchestrator = MasterOrchestrator()
    assert orchestrator is not None
    assert orchestrator.nl_processor is not None
    assert orchestrator.github_agent is not None
    assert orchestrator.deployment_agent is not None
    assert orchestrator.coding_agent is not None


@pytest.mark.asyncio
async def test_process_status_command():
    """Test processing status command through orchestrator"""
    from autonomous.master_orchestrator import MasterOrchestrator
    
    orchestrator = MasterOrchestrator()
    result = await orchestrator.process_command("What's the status?")
    
    assert result is not None
    assert result['success'] == True
    assert 'intent' in result


@pytest.mark.asyncio
async def test_process_help_command():
    """Test processing help command"""
    from autonomous.master_orchestrator import MasterOrchestrator
    
    orchestrator = MasterOrchestrator()
    result = await orchestrator.process_command("help")
    
    assert result is not None
    assert result['success'] == True
    assert 'help_text' in result


@pytest.mark.asyncio
async def test_orchestrator_self_heal():
    """Test orchestrator self-healing"""
    from autonomous.master_orchestrator import MasterOrchestrator
    
    orchestrator = MasterOrchestrator()
    # Should not raise exception
    await orchestrator.self_heal()


@pytest.mark.asyncio
async def test_get_operation_history():
    """Test getting operation history"""
    from autonomous.master_orchestrator import MasterOrchestrator
    
    orchestrator = MasterOrchestrator()
    
    # Process a command first
    await orchestrator.process_command("help")
    
    # Get history
    history = orchestrator.get_operation_history(limit=10)
    
    assert history is not None
    assert isinstance(history, list)
    assert len(history) > 0


# =============================================================================
# CONFIGURATION TESTS
# =============================================================================

def test_config_loading():
    """Test configuration loading"""
    from autonomous.config import get_config, validate_config
    
    config = get_config()
    assert config is not None
    assert 'github' in config
    assert 'deployment' in config
    assert 'nlp' in config
    
    is_valid, errors = validate_config()
    # Should be valid even without tokens in test environment
    assert isinstance(is_valid, bool)
    assert isinstance(errors, list)


def test_command_patterns_exist():
    """Test command patterns file exists and is valid"""
    import json
    from pathlib import Path
    
    patterns_path = Path(__file__).parent.parent / "data" / "command_patterns.json"
    
    # File should exist
    assert patterns_path.exists()
    
    # Should be valid JSON
    with open(patterns_path, 'r') as f:
        patterns = json.load(f)
    
    assert patterns is not None
    assert len(patterns) > 0
    assert 'merge_pr' in patterns
    assert 'deploy' in patterns


def test_personality_vectors_exist():
    """Test personality vectors file exists and is valid"""
    import json
    from pathlib import Path
    
    vectors_path = Path(__file__).parent.parent / "data" / "personality_vectors.json"
    
    # File should exist
    assert vectors_path.exists()
    
    # Should be valid JSON
    with open(vectors_path, 'r') as f:
        vectors = json.load(f)
    
    assert vectors is not None
    assert 'personalities' in vectors
    assert len(vectors['personalities']) > 0


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

@pytest.mark.asyncio
async def test_end_to_end_status_query():
    """Test complete end-to-end status query"""
    from autonomous.master_orchestrator import MasterOrchestrator
    
    orchestrator = MasterOrchestrator()
    
    # User says "What's the status?"
    result = await orchestrator.process_command("What's the status?")
    
    # Should succeed
    assert result['success'] == True
    
    # Should have intent parsed
    assert 'intent' in result
    assert result['intent']['action'] == 'status'
    
    # Should have processing time
    assert 'processing_time_ms' in result
    assert result['processing_time_ms'] > 0


@pytest.mark.asyncio
async def test_low_confidence_command():
    """Test handling of low confidence commands"""
    from autonomous.master_orchestrator import MasterOrchestrator
    
    orchestrator = MasterOrchestrator()
    
    # Gibberish command
    result = await orchestrator.process_command("asdfghjkl qwerty")
    
    # Should fail gracefully
    assert result['success'] == False
    assert 'error' in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
