"""
Transparency System - Full Decision Explainability

Every decision made by UMAJA must be explainable to humans.
This module provides tools to generate human-readable explanations
for all system decisions.

"If you can't explain it simply, you don't understand it well enough"
"""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class Decision:
    """Represents a decision made by the system"""
    decision_id: str
    action: str
    goal: str
    alternatives: List[str]
    rationale: str
    constitutional_checks: List[str]
    data_used: List[str]
    agents_involved: List[str]
    confidence: float
    timestamp: str
    impact_level: str
    logged_at: str


@dataclass
class Explanation:
    """Human-readable explanation of a decision"""
    decision_id: str
    summary: str
    reasoning: Dict[str, Any]
    human_explanation: str
    audit_trail: str
    reviewable_by: str
    alternatives_considered: List[Dict[str, str]]
    risks_identified: List[str]
    principles_applied: List[str]


class TransparencySystem:
    """
    Transparency System - Makes all decisions explainable
    
    This system ensures that every decision made by UMAJA can be
    explained to humans in clear, understandable language.
    """
    
    def __init__(self):
        self.decision_history = []
        self.explanation_cache = {}
        
    async def explain_decision(self, decision: Decision) -> Explanation:
        """
        Generate comprehensive explanation for a decision
        
        Args:
            decision: The decision to explain
            
        Returns:
            Explanation with human-readable details
        """
        # Check cache first
        if decision.decision_id in self.explanation_cache:
            return self.explanation_cache[decision.decision_id]
        
        # Generate explanation
        explanation = await self._generate_explanation(decision)
        
        # Cache it
        self.explanation_cache[decision.decision_id] = explanation
        
        # Store decision
        self.decision_history.append({
            'decision': decision,
            'explanation': explanation,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
        
        return explanation
    
    async def _generate_explanation(self, decision: Decision) -> Explanation:
        """Generate detailed explanation"""
        
        # Build reasoning structure
        reasoning = {
            'goal': decision.goal,
            'alternatives': decision.alternatives,
            'why_this_option': decision.rationale,
            'principles_applied': decision.constitutional_checks,
            'data_sources': decision.data_used,
            'agents_involved': decision.agents_involved,
            'confidence': decision.confidence,
            'impact_level': decision.impact_level
        }
        
        # Generate human explanation
        human_explanation = await self._generate_human_explanation(decision)
        
        # Format alternatives
        alternatives_considered = [
            {
                'option': alt,
                'why_not_chosen': await self._explain_alternative_rejection(alt, decision)
            }
            for alt in decision.alternatives
        ]
        
        # Identify risks
        risks = await self._identify_risks(decision)
        
        return Explanation(
            decision_id=decision.decision_id,
            summary=f"Decided to {decision.action} to achieve {decision.goal}",
            reasoning=reasoning,
            human_explanation=human_explanation,
            audit_trail=decision.logged_at,
            reviewable_by='anyone',
            alternatives_considered=alternatives_considered,
            risks_identified=risks,
            principles_applied=decision.constitutional_checks
        )
    
    async def _generate_human_explanation(self, decision: Decision) -> str:
        """Generate simple, human-readable explanation"""
        
        explanation_parts = []
        
        # Start with the goal
        explanation_parts.append(
            f"The goal was to {decision.goal.lower()}. "
        )
        
        # Explain the decision
        explanation_parts.append(
            f"I decided to {decision.action.lower()} because {decision.rationale.lower()}. "
        )
        
        # Mention alternatives
        if decision.alternatives:
            alt_text = ', '.join(decision.alternatives[:3])
            explanation_parts.append(
                f"I also considered {alt_text}, but chose this approach instead. "
            )
        
        # Mention principles
        if decision.constitutional_checks:
            principles = ', '.join(decision.constitutional_checks)
            explanation_parts.append(
                f"This decision aligns with our principles of {principles}. "
            )
        
        # Mention confidence
        confidence_word = self._confidence_to_word(decision.confidence)
        explanation_parts.append(
            f"I am {confidence_word} confident in this decision. "
        )
        
        # Mention data sources if available
        if decision.data_used:
            source_count = len(decision.data_used)
            explanation_parts.append(
                f"This is based on {source_count} data sources. "
            )
        
        return ''.join(explanation_parts)
    
    def _confidence_to_word(self, confidence: float) -> str:
        """Convert confidence score to human word"""
        if confidence >= 0.9:
            return "very"
        elif confidence >= 0.7:
            return "reasonably"
        elif confidence >= 0.5:
            return "moderately"
        else:
            return "somewhat"
    
    async def _explain_alternative_rejection(self, alternative: str, decision: Decision) -> str:
        """Explain why an alternative was not chosen"""
        # In production, this would use ML to generate nuanced explanations
        # For now, use template
        return f"While {alternative} was considered, {decision.action} better aligns with {decision.goal}"
    
    async def _identify_risks(self, decision: Decision) -> List[str]:
        """Identify potential risks in decision"""
        risks = []
        
        # Low confidence = risk
        if decision.confidence < 0.7:
            risks.append(f"Moderate confidence level ({decision.confidence:.2f})")
        
        # High impact = risk
        if decision.impact_level in ['high', 'critical']:
            risks.append(f"High impact decision - {decision.impact_level} level")
        
        # Few alternatives considered = risk
        if len(decision.alternatives) < 2:
            risks.append("Limited alternatives were considered")
        
        # Limited data = risk
        if len(decision.data_used) < 3:
            risks.append("Based on limited data sources")
        
        return risks
    
    async def explain_action_sequence(self, decisions: List[Decision]) -> str:
        """Explain a sequence of related decisions"""
        if not decisions:
            return "No decisions to explain"
        
        explanation_parts = [
            "Here's what happened:\n\n"
        ]
        
        for i, decision in enumerate(decisions, 1):
            explanation = await self.explain_decision(decision)
            explanation_parts.append(
                f"{i}. {explanation.summary}\n"
                f"   {explanation.human_explanation}\n\n"
            )
        
        return ''.join(explanation_parts)
    
    def get_decision_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent decision history"""
        return self.decision_history[-limit:]
    
    def search_decisions(
        self,
        agent_id: Optional[str] = None,
        impact_level: Optional[str] = None,
        confidence_min: Optional[float] = None,
        principle: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search decisions by criteria"""
        results = []
        
        for record in self.decision_history:
            decision = record['decision']
            
            # Filter by agent
            if agent_id and agent_id not in decision.agents_involved:
                continue
            
            # Filter by impact
            if impact_level and decision.impact_level != impact_level:
                continue
            
            # Filter by confidence
            if confidence_min and decision.confidence < confidence_min:
                continue
            
            # Filter by principle
            if principle and principle not in decision.constitutional_checks:
                continue
            
            results.append(record)
        
        return results
    
    def get_transparency_score(self) -> float:
        """Calculate transparency score (0.0-1.0)"""
        if not self.decision_history:
            return 1.0
        
        # All decisions have explanations
        explained = len(self.decision_history)
        total = len(self.decision_history)
        
        # Check explanation quality
        quality_sum = 0.0
        for record in self.decision_history:
            explanation = record['explanation']
            quality = self._assess_explanation_quality(explanation)
            quality_sum += quality
        
        avg_quality = quality_sum / total if total > 0 else 1.0
        
        return avg_quality
    
    def _assess_explanation_quality(self, explanation: Explanation) -> float:
        """Assess quality of explanation (0.0-1.0)"""
        score = 0.0
        
        # Has summary (0.2)
        if explanation.summary:
            score += 0.2
        
        # Has human explanation (0.3)
        if explanation.human_explanation and len(explanation.human_explanation) > 50:
            score += 0.3
        
        # Has alternatives (0.2)
        if explanation.alternatives_considered:
            score += 0.2
        
        # Has risks identified (0.15)
        if explanation.risks_identified:
            score += 0.15
        
        # Has principles (0.15)
        if explanation.principles_applied:
            score += 0.15
        
        return min(1.0, score)
    
    def generate_audit_report(self) -> Dict[str, Any]:
        """Generate audit report for transparency review"""
        total_decisions = len(self.decision_history)
        
        # Group by impact level
        by_impact = {}
        for record in self.decision_history:
            impact = record['decision'].impact_level
            by_impact[impact] = by_impact.get(impact, 0) + 1
        
        # Group by confidence
        high_confidence = sum(
            1 for r in self.decision_history
            if r['decision'].confidence >= 0.8
        )
        
        # Calculate average confidence
        avg_confidence = (
            sum(r['decision'].confidence for r in self.decision_history) / total_decisions
            if total_decisions > 0 else 0.0
        )
        
        return {
            'total_decisions': total_decisions,
            'transparency_score': self.get_transparency_score(),
            'by_impact_level': by_impact,
            'high_confidence_decisions': high_confidence,
            'average_confidence': avg_confidence,
            'all_decisions_explained': True,
            'audit_trail_available': True,
            'human_reviewable': True
        }
