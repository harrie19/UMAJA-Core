"""
Dual-Layer Agent - Integrated Cognitive and Vector Processing

This module implements the dual-layer agent that combines:
- Cognitive Layer: Symbolic reasoning via PersonalityEngine and LLM
- Vector Layer: Continuous subsymbolic processing

The agent implements a veto mechanism where the vector layer can reject
actions that are misaligned with the agent's identity, providing a form
of continuous self-supervision and coherence maintenance.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Literal
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.vector_layer import VectorLayer, VectorState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DualLayerAgent:
    """
    Dual-Layer Agent combining cognitive and vector processing
    
    Architecture:
    1. Query vector layer for context (System 1 - fast, intuitive)
    2. Generate content with cognitive layer (System 2 - deliberate, symbolic)
    3. Check alignment with vector identity (veto mechanism)
    4. Update vector layer with feedback (Hebbian learning)
    
    This provides:
    - Persistent agent identity across sessions
    - Energy-efficient context retrieval
    - Risk assessment and priority scoring
    - Multi-turn coherence via vector memory
    """
    
    def __init__(self, 
                 personality_id: str = "distinguished_wit",
                 veto_threshold: float = 0.3,
                 vector_state_path: str = "data/vector_layer_state.json"):
        """
        Initialize dual-layer agent
        
        Args:
            personality_id: Personality archetype to use
            veto_threshold: Minimum alignment for action execution (0.0-1.0)
            vector_state_path: Path to vector layer state file
        """
        self.personality_id = personality_id
        self.veto_threshold = veto_threshold
        
        # Initialize cognitive layer
        logger.info("Initializing cognitive layer...")
        try:
            from personality_engine import PersonalityEngine
            from worldtour_generator import WorldtourGenerator
            
            self.personality_engine = PersonalityEngine()
            self.personality = self.personality_engine.get_comedian(personality_id)
            self.worldtour = WorldtourGenerator()
            logger.info(f"Cognitive layer initialized with personality: {personality_id}")
        except Exception as e:
            logger.error(f"Failed to initialize cognitive layer: {e}")
            self.personality_engine = None
            self.personality = None
            self.worldtour = None
        
        # Initialize vector layer
        logger.info("Initializing vector layer...")
        try:
            self.vector_layer = VectorLayer(state_path=vector_state_path)
            
            # Initialize identity vector with personality description if available
            if self.personality and hasattr(self.personality, 'name'):
                identity_text = f"I am {self.personality.name}. {' '.join(getattr(self.personality, 'traits', []))}"
                self.vector_layer.state.identity = self.vector_layer.encode(identity_text)
                logger.info(f"Vector identity initialized for {self.personality.name}")
            
            logger.info("Vector layer initialized")
        except Exception as e:
            logger.error(f"Failed to initialize vector layer: {e}")
            raise
        
        # Statistics
        self.generation_count = 0
        self.veto_count = 0
    
    def generate_content(self, 
                        topic: str, 
                        content_type: str = "joke",
                        feedback: Optional[float] = None) -> Dict[str, Any]:
        """
        Generate content using dual-layer architecture
        
        Process:
        1. Query vector layer for context and priorities
        2. Check risk and priority thresholds
        3. Generate content with cognitive layer
        4. Perform alignment check (veto mechanism)
        5. Update vector layer with action and feedback
        
        Args:
            topic: Topic or theme for content generation
            content_type: Type of content (joke, city_review, etc.)
            feedback: Optional feedback for previous generation (-1.0 to 1.0)
            
        Returns:
            Dictionary with content, metadata, and vector state info
        """
        # STEP 1: Query vector layer for context
        logger.info(f"Querying vector layer for topic: {topic}")
        vector_context = self.vector_layer.query_similar(topic)
        
        # STEP 2: Check priority and risk
        if vector_context['priority_score'] < 0.2:
            logger.warning(f"Low priority task: {vector_context['priority_score']:.3f}")
        
        if vector_context['risk_assessment'] > self.vector_layer.state.risk_threshold:
            logger.warning(f"High risk action: {vector_context['risk_assessment']:.3f}")
        
        # STEP 3: Cognitive generation with vector context
        formatted_context = self._format_vector_context(vector_context)
        
        try:
            if self.personality and hasattr(self.personality, 'generate_smile_text'):
                # Use personality for generation
                content = self.personality.generate_smile_text(topic=topic)
            else:
                # Fallback to simple generation
                content = f"Generated content about {topic} with {content_type} style."
            
            logger.info(f"Generated content: {content[:100]}...")
        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            content = f"Content generation encountered an error. Topic: {topic}"
        
        # STEP 4: Alignment check (veto mechanism)
        content_vec = self.vector_layer.encode(content)
        alignment = float(cosine_similarity([content_vec], [self.vector_layer.state.identity])[0][0])
        
        vetoed = False
        if alignment < self.veto_threshold:
            logger.warning(f"VETO: Content misaligned with identity! Alignment: {alignment:.3f}")
            self.veto_count += 1
            vetoed = True
            
            # Try to regenerate with stronger constraint
            if self.personality and hasattr(self.personality, 'name'):
                content = self._regenerate_with_constraint(topic, content_type, vector_context)
                content_vec = self.vector_layer.encode(content)
                alignment = float(cosine_similarity([content_vec], [self.vector_layer.state.identity])[0][0])
                logger.info(f"Regenerated content with alignment: {alignment:.3f}")
        
        # STEP 5: Update vector layer (Hebbian learning)
        # Use provided feedback or default to 1.0 if not vetoed
        update_feedback = feedback if feedback is not None else (0.5 if vetoed else 1.0)
        self.vector_layer.update(content, feedback=update_feedback)
        
        self.generation_count += 1
        
        # Return comprehensive result
        return {
            'content': content,
            'metadata': {
                'topic': topic,
                'content_type': content_type,
                'priority': vector_context['priority_score'],
                'risk': vector_context['risk_assessment'],
                'alignment': alignment,
                'goal_alignment': vector_context['goal_alignment'],
                'energy': vector_context['energy'],
                'vetoed': vetoed,
                'generation_count': self.generation_count,
                'veto_count': self.veto_count
            },
            'vector_context': formatted_context
        }
    
    def _format_vector_context(self, vector_context: Dict[str, Any]) -> str:
        """
        Format vector context for LLM prompt
        
        Args:
            vector_context: Context from vector layer
            
        Returns:
            Formatted string for prompt injection
        """
        return (
            f"[Vector Context]\n"
            f"Priority: {vector_context['priority_score']:.3f}\n"
            f"Risk: {vector_context['risk_assessment']:.3f}\n"
            f"Goal Alignment: {vector_context['goal_alignment']:.3f}\n"
            f"Identity Match: {vector_context['identity_similarity']:.3f}\n"
        )
    
    def _regenerate_with_constraint(self, 
                                   topic: str, 
                                   content_type: str,
                                   vector_context: Dict[str, Any]) -> str:
        """
        Regenerate content with stronger identity constraint
        
        Args:
            topic: Original topic
            content_type: Original content type
            vector_context: Vector context
            
        Returns:
            Regenerated content
        """
        # Add identity constraint to generation
        if self.personality and hasattr(self.personality, 'name'):
            constrained_topic = f"{topic} (in the style of {self.personality.name})"
            try:
                content = self.personality.generate_smile_text(topic=constrained_topic)
            except:
                content = f"Content about {topic} by {self.personality.name}"
        else:
            content = f"Carefully generated content about {topic}"
        
        return content
    
    def update_goals(self, goal_text: str):
        """
        Update vector layer goals
        
        Args:
            goal_text: New goal description
        """
        goal_vec = self.vector_layer.encode(goal_text)
        self.vector_layer.state.goals = goal_vec / np.linalg.norm(goal_vec)
        self.vector_layer.save_state()
        logger.info(f"Updated goals: {goal_text}")
    
    def get_vector_state(self) -> Dict[str, Any]:
        """Get current vector layer state"""
        return self.vector_layer.get_state_summary()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get agent statistics"""
        return {
            'generation_count': self.generation_count,
            'veto_count': self.veto_count,
            'veto_rate': self.veto_count / max(self.generation_count, 1),
            'personality_id': self.personality_id,
            'veto_threshold': self.veto_threshold,
            'vector_state': self.get_vector_state()
        }
    
    def save_state(self):
        """Save vector layer state"""
        self.vector_layer.save_state()
    
    def load_state(self, filepath: Optional[str] = None):
        """Load vector layer state"""
        self.vector_layer.state = self.vector_layer.load_state(filepath)
