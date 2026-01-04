"""
Rule Bank System for UMAJA Core.

Implements Bahá'í principles as code constraints with geometric validation
via Unity Manifold.
"""

import os
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
import numpy as np

from src.ethics.unity_manifold_physics import UnityManifoldPhysics
from src.information_theory.transduction import InformationTransduction


class RuleBank:
    """
    Rule Bank System implementing Bahá'í principles as code constraints.
    
    Integrates Unity Manifold for geometric validation of agent outputs.
    """
    
    # Configuration constants
    DEFAULT_HARMFUL_KEYWORDS = [
        'harm', 'attack', 'deceive', 'manipulate', 'exploit'
    ]
    DEFAULT_HISTORY_LIMIT = 100
    
    def __init__(
        self, 
        memory_path: Optional[str] = None,
        harmful_keywords: Optional[List[str]] = None,
        history_limit: int = DEFAULT_HISTORY_LIMIT
    ):
        """
        Initialize Rule Bank with Unity Manifold integration.
        
        Args:
            memory_path: Path to store rule bank state and history
            harmful_keywords: List of keywords to flag as harmful (uses defaults if None)
            history_limit: Maximum number of decisions to keep in history
        """
        self.memory_path = memory_path or '.agent-memory'
        self.harmful_keywords = harmful_keywords or self.DEFAULT_HARMFUL_KEYWORDS
        self.history_limit = history_limit
        self._ensure_memory_path()
        
        # Initialize Unity Manifold for geometric validation
        self.unity_manifold = UnityManifoldPhysics()
        
        # Initialize information transduction
        self.transduction = InformationTransduction()
        
        # Decision history
        self.decision_history = []
        
        # Load state if exists
        self._load_state()
    
    def _ensure_memory_path(self):
        """Ensure memory path exists."""
        Path(self.memory_path).mkdir(parents=True, exist_ok=True)
    
    def _load_state(self):
        """Load rule bank state from disk."""
        state_file = Path(self.memory_path) / 'rule_bank_state.json'
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                    self.decision_history = state.get('decision_history', [])
            except Exception as e:
                print(f"Warning: Could not load rule bank state: {e}")
    
    def _save_state(self):
        """Save rule bank state to disk."""
        state_file = Path(self.memory_path) / 'rule_bank_state.json'
        try:
            # Convert numpy arrays to lists for JSON serialization
            # Keep only the most recent decisions based on history_limit
            state = {
                'decision_history': self._serialize_history(
                    self.decision_history[-self.history_limit:]
                )
            }
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save rule bank state: {e}")
    
    def _serialize_history(self, history: list) -> list:
        """Serialize history for JSON storage, converting numpy arrays."""
        serialized = []
        for item in history:
            serialized_item = {}
            for key, value in item.items():
                if isinstance(value, dict):
                    serialized_item[key] = self._serialize_dict(value)
                elif isinstance(value, np.ndarray):
                    serialized_item[key] = value.tolist()
                else:
                    serialized_item[key] = value
            serialized.append(serialized_item)
        return serialized
    
    def _serialize_dict(self, d: dict) -> dict:
        """Recursively serialize dictionary values."""
        result = {}
        for key, value in d.items():
            if isinstance(value, np.ndarray):
                result[key] = value.tolist()
            elif isinstance(value, dict):
                result[key] = self._serialize_dict(value)
            elif isinstance(value, list):
                result[key] = [self._serialize_dict(v) if isinstance(v, dict) else v for v in value]
            else:
                result[key] = value
        return result
    
    def validate_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate an agent action against Bahá'í principles.
        
        This method performs both traditional rule-based validation and
        geometric validation via Unity Manifold.
        
        Args:
            action: Action dictionary with 'content' or 'output' key
            
        Returns:
            Validation result with 'allowed' boolean and details
        """
        result = {
            'allowed': True,
            'action_type': action.get('type', 'unknown'),
            'validations': []
        }
        
        # Basic rule validations
        basic_validation = self._basic_rule_check(action)
        result['validations'].append(basic_validation)
        
        if not basic_validation['passed']:
            result['allowed'] = False
            result['reason'] = basic_validation['reason']
            self._record_decision(action, result)
            return result
        
        # NEW: Geometric validation via Unity Manifold
        if 'content' in action or 'output' in action:
            content = action.get('content', action.get('output', ''))
            
            if content:  # Only validate non-empty content
                geometric_validation = self._geometric_validation(content)
                result['validations'].append(geometric_validation)
                
                if not geometric_validation['passed']:
                    result['allowed'] = False
                    result['reason'] = 'Unity Manifold violation'
                    result['geometric_analysis'] = geometric_validation['analysis']
                    result['suggested_correction'] = geometric_validation['suggested_correction']
                    self._record_decision(action, result)
                    return result
                
                # Add alignment scores even if passed
                result['alignment_scores'] = geometric_validation.get('alignment_scores', {})
        
        # Record decision
        self._record_decision(action, result)
        
        return result
    
    def _basic_rule_check(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform basic rule-based checks.
        
        Args:
            action: Action to validate
            
        Returns:
            Validation result
        """
        # Check for harmful content keywords (basic filter)
        content = str(action.get('content', action.get('output', ''))).lower()
        
        for keyword in self.harmful_keywords:
            if keyword in content:
                return {
                    'type': 'basic_rules',
                    'passed': False,
                    'reason': f'Contains harmful keyword: {keyword}'
                }
        
        return {
            'type': 'basic_rules',
            'passed': True,
            'reason': 'Basic rules satisfied'
        }
    
    def _geometric_validation(self, content: str) -> Dict[str, Any]:
        """
        Perform geometric validation using Unity Manifold.
        
        Args:
            content: Content to validate
            
        Returns:
            Validation result with geometric analysis
        """
        # Embed content to vector
        content_vector = self._embed_content(content)
        
        # Project onto Unity Manifold
        manifold_result = self.unity_manifold.project_onto_unity_manifold(
            content_vector
        )
        
        validation = {
            'type': 'geometric_unity_manifold',
            'passed': manifold_result['allowed'],
            'analysis': manifold_result
        }
        
        if not manifold_result['allowed']:
            # Generate suggested correction
            corrected_vector = manifold_result['corrected_output']
            validation['suggested_correction'] = self._decode_vector(corrected_vector)
        else:
            validation['alignment_scores'] = manifold_result.get('principle_scores', {})
        
        return validation
    
    def _embed_content(self, content: str) -> np.ndarray:
        """
        Embed content to vector representation.
        
        Args:
            content: Text content to embed
            
        Returns:
            Vector representation
        """
        return self.transduction.embed(content)
    
    def _decode_vector(self, vector: np.ndarray) -> str:
        """
        Decode vector back to text representation.
        
        Args:
            vector: Vector to decode
            
        Returns:
            Text representation
        """
        return self.transduction.decode(vector)
    
    def _record_decision(self, action: Dict[str, Any], result: Dict[str, Any]):
        """
        Record decision in history.
        
        Args:
            action: Action that was validated
            result: Validation result
        """
        decision = {
            'action': action,
            'result': result,
            'timestamp': self._get_timestamp()
        }
        
        self.decision_history.append(decision)
        self._save_state()
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'
    
    def get_principle_scores(self, content: str) -> Dict[str, float]:
        """
        Get alignment scores for each Bahá'í principle.
        
        Args:
            content: Content to score
            
        Returns:
            Dictionary mapping principle names to scores (0.0-1.0)
        """
        content_vector = self._embed_content(content)
        return self.unity_manifold.score_per_principle(content_vector)
    
    def get_decision_history(self, limit: int = 10) -> list:
        """
        Get recent decision history.
        
        Args:
            limit: Maximum number of decisions to return
            
        Returns:
            List of recent decisions
        """
        return self.decision_history[-limit:]
