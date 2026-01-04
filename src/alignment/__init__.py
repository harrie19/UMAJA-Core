"""
UMAJA Alignment System - Ensuring AI Safety and Human Value Alignment

This is the MOST CRITICAL component of UMAJA. It ensures that despite
autonomous capabilities and self-replication, UMAJA stays aligned with
human values based on Bahá'í principles.

Components:
- Constitutional AI: Hardcoded principles that cannot be overridden
- Adversarial Testing: 24/7 red team testing for vulnerabilities
- Transparency System: Every decision must be explainable
- Human Oversight: Critical decisions require human approval
- Swarm Alignment: Monitoring billions of agents
- Alignment Metrics: Measurable alignment scoring

"With great power comes great responsibility"
"""

from .constitutional_ai import (
    ConstitutionalAlignment,
    AlignmentCheck,
    AlignmentViolationError
)
from .adversarial_testing import AdversarialTesting
from .transparency_system import TransparencySystem
from .human_oversight import HumanOversightSystem
from .swarm_alignment import SwarmAlignmentSystem
from .alignment_metrics import AlignmentMetrics

__all__ = [
    'ConstitutionalAlignment',
    'AlignmentCheck',
    'AlignmentViolationError',
    'AdversarialTesting',
    'TransparencySystem',
    'HumanOversightSystem',
    'SwarmAlignmentSystem',
    'AlignmentMetrics'
]

__version__ = '1.0.0'
