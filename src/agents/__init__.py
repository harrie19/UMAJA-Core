"""
UMAJA-Core Dual-Layer Agent System

This module implements a dual-layer cognitive architecture combining:
- Cognitive Layer: Symbolic reasoning via PersonalityEngine and LLM
- Vector Layer: Continuous subsymbolic processing via sentence embeddings

The architecture implements dual-process theory (System 1 / System 2) and
provides energy-efficient context retrieval, persistent agent identity,
and multi-agent coordination capabilities.
"""

from .vector_layer import VectorLayer, VectorState
from .dual_layer_agent import DualLayerAgent

__all__ = ['VectorLayer', 'VectorState', 'DualLayerAgent']
