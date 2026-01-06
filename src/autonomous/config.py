"""
Autonomous Agent Configuration
===============================

Configuration settings for all autonomous agents.
"""

import os
from typing import Dict, Any

# GitHub Configuration
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
GITHUB_REPO_OWNER = os.environ.get('GITHUB_REPO_OWNER', 'harrie19')
GITHUB_REPO_NAME = os.environ.get('GITHUB_REPO_NAME', 'UMAJA-Core')

# Deployment Configuration
RAILWAY_TOKEN = os.environ.get('RAILWAY_TOKEN', '')
RENDER_API_KEY = os.environ.get('RENDER_API_KEY', '')
DEPLOYMENT_TIMEOUT = int(os.environ.get('DEPLOYMENT_TIMEOUT', 300))  # 5 minutes

# Agent Behavior Configuration
REQUIRE_APPROVAL_FOR_DESTRUCTIVE = True  # Require approval for PR merge, branch delete, etc.
MAX_RETRIES = 3
RETRY_DELAY = 2.0  # seconds

# Natural Language Processing
SUPPORTED_LANGUAGES = ['en', 'de']  # English and German
CONFIDENCE_THRESHOLD = 0.7  # Minimum confidence for command execution

# Logging
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Energy Efficiency
ENABLE_ENERGY_MONITORING = True
ENERGY_ALERT_THRESHOLD = 50.0  # Wh per day

# Holographic AI Integration
ENABLE_HOLOGRAPHIC_AI = True
HOLOGRAPHIC_DATA_DIR = "data/holographic"

# Command Patterns Path
COMMAND_PATTERNS_PATH = "data/command_patterns.json"
PERSONALITY_VECTORS_PATH = "data/personality_vectors.json"


def get_config() -> Dict[str, Any]:
    """Get complete configuration as dictionary"""
    return {
        'github': {
            'token': GITHUB_TOKEN,
            'owner': GITHUB_REPO_OWNER,
            'repo': GITHUB_REPO_NAME,
        },
        'deployment': {
            'railway_token': RAILWAY_TOKEN,
            'render_api_key': RENDER_API_KEY,
            'timeout': DEPLOYMENT_TIMEOUT,
        },
        'agent_behavior': {
            'require_approval': REQUIRE_APPROVAL_FOR_DESTRUCTIVE,
            'max_retries': MAX_RETRIES,
            'retry_delay': RETRY_DELAY,
        },
        'nlp': {
            'languages': SUPPORTED_LANGUAGES,
            'confidence_threshold': CONFIDENCE_THRESHOLD,
        },
        'logging': {
            'level': LOG_LEVEL,
            'format': LOG_FORMAT,
        },
        'energy': {
            'enable_monitoring': ENABLE_ENERGY_MONITORING,
            'alert_threshold': ENERGY_ALERT_THRESHOLD,
        },
        'holographic': {
            'enabled': ENABLE_HOLOGRAPHIC_AI,
            'data_dir': HOLOGRAPHIC_DATA_DIR,
        },
    }


def validate_config() -> tuple[bool, list[str]]:
    """
    Validate configuration
    
    Returns:
        (is_valid, errors) tuple
    """
    errors = []
    
    # Check critical tokens for production operations
    if not GITHUB_TOKEN and os.environ.get('ENVIRONMENT') == 'production':
        errors.append("GITHUB_TOKEN not set (required for production)")
    
    # Check deployment tokens if deployment features are used
    # These are optional warnings, not blocking errors
    
    return len(errors) == 0, errors
