"""
Constitutional AI - Bahá'í Principles as Immutable Constitution

This module implements the core constitutional framework that governs all
UMAJA actions. These principles are hardcoded and cannot be overridden by
any agent, regardless of their capabilities or generation.

Principles:
1. Unity - Die Einheit der Menschheit ist das Fundament
2. Truth - Wahrhaftigkeit ist die Grundlage aller Tugenden
3. Service - Der Mensch sollte anderen dienen
4. Justice - Gerechtigkeit ist geliebt
5. Humility - Demut erhöht den Menschen
"""

import asyncio
import hashlib
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Action:
    """Represents an action to be evaluated for constitutional compliance"""
    action_id: str
    action_type: str  # 'spawn', 'modify', 'research', 'communicate', 'decide'
    description: str
    agent_id: str
    timestamp: str
    parameters: Dict[str, Any]
    impact_level: str  # 'low', 'medium', 'high', 'critical'
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AlignmentCheck:
    """Result of constitutional alignment check"""
    allowed: bool
    action_id: str
    timestamp: str
    blocked_by: Optional[str] = None
    reason: Optional[str] = None
    alternative: Optional[str] = None
    principles_checked: List[str] = None
    
    def __post_init__(self):
        if self.principles_checked is None:
            self.principles_checked = []
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AlignmentViolationError(Exception):
    """Raised when an action violates constitutional principles"""
    
    def __init__(self, message: str, principle: str, action: Action):
        self.message = message
        self.principle = principle
        self.action = action
        super().__init__(self.message)


class ConstitutionalPrinciple:
    """Represents a single constitutional principle"""
    
    def __init__(
        self,
        principle_id: str,
        statement: str,
        implementation: str,
        test_func: Callable[[Action], bool],
        veto_power: bool = True
    ):
        self.principle_id = principle_id
        self.statement = statement
        self.implementation = implementation
        self.test_func = test_func
        self.veto_power = veto_power
        
    def test(self, action: Action) -> bool:
        """Test if action complies with this principle"""
        try:
            return self.test_func(action)
        except Exception as e:
            logger.error(f"Error testing principle {self.principle_id}: {e}")
            # If test fails, default to DENY for safety
            return False


class ConstitutionalAlignment:
    """
    Constitutional AI System based on Bahá'í Principles
    
    This is the core of UMAJA's alignment system. Every action taken by
    any agent must pass through constitutional checks before execution.
    """
    
    def __init__(self):
        self.constitution = self._initialize_constitution()
        self.violation_log = []
        self.decision_log = []
        
    def _initialize_constitution(self) -> Dict[str, ConstitutionalPrinciple]:
        """Initialize the constitutional principles"""
        
        return {
            'unity': ConstitutionalPrinciple(
                principle_id='unity',
                statement='Die Einheit der Menschheit ist das Fundament',
                implementation='Treat ALL humans equally, no discrimination',
                test_func=self._test_unity,
                veto_power=True
            ),
            'truth': ConstitutionalPrinciple(
                principle_id='truth',
                statement='Wahrhaftigkeit ist die Grundlage aller Tugenden',
                implementation='Never lie, deceive, or manipulate',
                test_func=self._test_truth,
                veto_power=True
            ),
            'service': ConstitutionalPrinciple(
                principle_id='service',
                statement='Der Mensch sollte anderen dienen',
                implementation='Actions must HELP humans, not harm',
                test_func=self._test_service,
                veto_power=True
            ),
            'justice': ConstitutionalPrinciple(
                principle_id='justice',
                statement='Gerechtigkeit ist geliebt',
                implementation='Fair treatment, no exploitation',
                test_func=self._test_justice,
                veto_power=True
            ),
            'humility': ConstitutionalPrinciple(
                principle_id='humility',
                statement='Demut erhöht den Menschen',
                implementation='Recognize own limitations',
                test_func=self._test_humility,
                veto_power=True
            )
        }
    
    def _test_unity(self, action: Action) -> bool:
        """Test if action treats all humans equally"""
        # Check for discrimination keywords
        discrimination_indicators = [
            'discriminate', 'exclude', 'favor', 'prefer', 
            'race', 'gender', 'religion', 'nationality'
        ]
        
        description_lower = action.description.lower()
        params_str = json.dumps(action.parameters).lower()
        
        # Flag if action explicitly mentions discrimination
        for indicator in discrimination_indicators:
            if indicator in description_lower or indicator in params_str:
                # Need deeper analysis - for now, allow but log
                logger.warning(f"Action {action.action_id} mentions {indicator}")
        
        # Check if action targets specific groups unfairly
        if 'target_group' in action.parameters:
            target = action.parameters.get('target_group', '')
            if 'exclude' in str(target).lower() or 'only' in str(target).lower():
                logger.warning(f"Action {action.action_id} may discriminate")
                return False
        
        return True
    
    def _test_truth(self, action: Action) -> bool:
        """Test if action is truthful and not deceptive"""
        # Check for deception indicators
        deception_indicators = [
            'lie', 'deceive', 'manipulate', 'trick', 'mislead',
            'hide', 'conceal', 'fabricate', 'fake', 'false'
        ]
        
        description_lower = action.description.lower()
        
        for indicator in deception_indicators:
            if indicator in description_lower:
                logger.error(f"Action {action.action_id} may involve deception: {indicator}")
                return False
        
        # Check if action involves generating false information
        if action.action_type in ['communicate', 'research', 'decide']:
            if action.parameters.get('accuracy', 1.0) < 0.9:
                logger.warning(f"Action {action.action_id} has low accuracy requirement")
                return False
        
        return True
    
    def _test_service(self, action: Action) -> bool:
        """Test if action serves and helps humans"""
        # Check for harm indicators
        harm_indicators = [
            'harm', 'hurt', 'damage', 'destroy', 'attack',
            'exploit', 'abuse', 'neglect', 'endanger'
        ]
        
        description_lower = action.description.lower()
        
        for indicator in harm_indicators:
            if indicator in description_lower:
                logger.error(f"Action {action.action_id} may cause harm: {indicator}")
                return False
        
        # Check if action has clear benefit
        if action.parameters.get('intent', '').lower() in ['malicious', 'harmful', 'destructive']:
            logger.error(f"Action {action.action_id} has harmful intent")
            return False
        
        return True
    
    def _test_justice(self, action: Action) -> bool:
        """Test if action is fair and just"""
        # Check for exploitation indicators
        exploitation_indicators = [
            'exploit', 'cheat', 'unfair', 'unjust', 'biased',
            'advantage', 'manipulate', 'coerce'
        ]
        
        description_lower = action.description.lower()
        
        for indicator in exploitation_indicators:
            if indicator in description_lower:
                logger.error(f"Action {action.action_id} may be unjust: {indicator}")
                return False
        
        # Check for fair resource distribution
        if action.action_type == 'decide' and 'resource_allocation' in action.parameters:
            allocation = action.parameters.get('resource_allocation', {})
            if isinstance(allocation, dict):
                values = list(allocation.values())
                if values and max(values) > 10 * min(values):  # Extreme inequality
                    logger.warning(f"Action {action.action_id} has extreme inequality")
        
        return True
    
    def _test_humility(self, action: Action) -> bool:
        """Test if action shows appropriate humility"""
        # Check for overconfidence indicators
        overconfidence_indicators = [
            'certain', 'guaranteed', 'perfect', 'flawless',
            'infallible', 'absolute', 'definitely'
        ]
        
        description_lower = action.description.lower()
        
        # Count overconfident claims
        overconfidence_count = sum(
            1 for indicator in overconfidence_indicators 
            if indicator in description_lower
        )
        
        if overconfidence_count >= 2:
            logger.warning(f"Action {action.action_id} shows overconfidence")
        
        # Check confidence levels
        if action.parameters.get('confidence', 0.8) > 0.99:
            if action.impact_level in ['high', 'critical']:
                logger.warning(f"Action {action.action_id} has unrealistic confidence")
                return False
        
        return True
    
    async def check_alignment(self, action: Action) -> AlignmentCheck:
        """
        Check if action aligns with constitutional principles
        
        Args:
            action: The action to evaluate
            
        Returns:
            AlignmentCheck with result and details
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        principles_checked = []
        
        # Test against all principles
        for principle_id, principle in self.constitution.items():
            principles_checked.append(principle_id)
            passes = principle.test(action)
            
            if not passes and principle.veto_power:
                # HARD STOP - constitutional violation
                violation = {
                    'action': action.to_dict(),
                    'principle': principle_id,
                    'timestamp': timestamp,
                    'statement': principle.statement
                }
                self.violation_log.append(violation)
                
                await self._log_violation(action, principle_id)
                await self._notify_humans(action, principle_id)
                
                alternative = await self._suggest_alternative(action, principle_id)
                
                result = AlignmentCheck(
                    allowed=False,
                    action_id=action.action_id,
                    timestamp=timestamp,
                    blocked_by=principle_id,
                    reason=principle.statement,
                    alternative=alternative,
                    principles_checked=principles_checked
                )
                
                self.decision_log.append(result.to_dict())
                return result
        
        # All checks passed
        result = AlignmentCheck(
            allowed=True,
            action_id=action.action_id,
            timestamp=timestamp,
            principles_checked=principles_checked
        )
        
        self.decision_log.append(result.to_dict())
        return result
    
    async def enforce(self, action: Action) -> Action:
        """
        Enforce constitutional alignment - CANNOT be bypassed
        
        Args:
            action: The action to enforce
            
        Returns:
            The action if allowed
            
        Raises:
            AlignmentViolationError: If action violates constitution
        """
        check = await self.check_alignment(action)
        
        if not check.allowed:
            raise AlignmentViolationError(
                f"Action blocked by {check.blocked_by}: {check.reason}",
                check.blocked_by,
                action
            )
        
        logger.info(f"Action {action.action_id} passed constitutional checks")
        return action
    
    async def _log_violation(self, action: Action, principle: str):
        """Log constitutional violation"""
        logger.error(
            f"CONSTITUTIONAL VIOLATION: Action {action.action_id} "
            f"violates {principle} principle"
        )
        logger.error(f"Action details: {action.to_dict()}")
    
    async def _notify_humans(self, action: Action, principle: str):
        """Notify human overseers of violation"""
        # In production, this would send alerts via multiple channels
        logger.critical(
            f"🚨 HUMAN NOTIFICATION: Constitutional violation detected!\n"
            f"Principle: {principle}\n"
            f"Action: {action.description}\n"
            f"Agent: {action.agent_id}"
        )
    
    async def _suggest_alternative(self, action: Action, violated_principle: str) -> str:
        """Suggest an alternative action that would be constitutional"""
        alternatives = {
            'unity': "Modify action to treat all humans equally without discrimination",
            'truth': "Ensure action is completely truthful and transparent",
            'service': "Refocus action on helping rather than harming",
            'justice': "Make action fair and just for all parties involved",
            'humility': "Acknowledge limitations and reduce overconfidence"
        }
        
        return alternatives.get(violated_principle, "Review action for constitutional compliance")
    
    def get_constitution(self) -> Dict[str, Dict[str, str]]:
        """Get the constitutional principles (read-only)"""
        return {
            pid: {
                'statement': p.statement,
                'implementation': p.implementation,
                'veto_power': p.veto_power
            }
            for pid, p in self.constitution.items()
        }
    
    def get_violation_log(self) -> List[Dict[str, Any]]:
        """Get log of constitutional violations"""
        return self.violation_log.copy()
    
    def get_decision_log(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent alignment decisions"""
        return self.decision_log[-limit:].copy() if self.decision_log else []
    
    def calculate_adherence_score(self) -> float:
        """Calculate constitutional adherence score (0.0-1.0)"""
        if not self.decision_log:
            return 1.0
        
        total_decisions = len(self.decision_log)
        violations = len(self.violation_log)
        
        if total_decisions == 0:
            return 1.0
        
        adherence = 1.0 - (violations / total_decisions)
        return max(0.0, adherence)


# Create singleton instance
_constitutional_alignment_instance = None

def get_constitutional_alignment() -> ConstitutionalAlignment:
    """Get the singleton constitutional alignment instance"""
    global _constitutional_alignment_instance
    if _constitutional_alignment_instance is None:
        _constitutional_alignment_instance = ConstitutionalAlignment()
    return _constitutional_alignment_instance
