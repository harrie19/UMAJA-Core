"""
Reasoning Middleware - Action Validation and Ethical Governance

Purpose: Intercept agent actions and validate them against the Rule Bank
before execution, ensuring all autonomous operations meet ethical standards.

Key Features:
- Task profiling and risk assessment
- Ethical validation via Rule Bank
- Violation handling with alternatives
- Human review escalation for critical actions
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from rule_bank import RuleBank

logger = logging.getLogger(__name__)


class ReasoningMiddleware:
    """
    Middleware that validates all agent actions against ethical constraints.
    
    Acts as a gatekeeper between agent decisions and execution, ensuring
    compliance with Bahá'í principles and safety guidelines.
    """
    
    # Risk thresholds for different action types
    RISK_THRESHOLDS = {
        "post_content": "MEDIUM",
        "generate_content": "MEDIUM",
        "modify_data": "HIGH",
        "external_api_call": "HIGH",
        "financial_transaction": "CRITICAL",
        "user_interaction": "MEDIUM"
    }
    
    def __init__(self, rule_bank: RuleBank):
        """
        Initialize middleware with a Rule Bank instance.
        
        Args:
            rule_bank: RuleBank instance for validation
        """
        self.rule_bank = rule_bank
        self.validation_history = []
        
        logger.info("Reasoning Middleware initialized")
    
    def intercept(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point: intercept and validate an action.
        
        Args:
            action: Dictionary containing action details
                - type: Action type (required)
                - confidence: Confidence score (optional, default 1.0)
                - benefit_score: Benefit to users (optional, default 0.0)
                - content: Content text (optional)
                - ... other action-specific fields
        
        Returns:
            Dictionary with validation results:
                - status: 'approved', 'rejected', or 'requires_review'
                - action: Original action (potentially modified)
                - validation: Rule Bank validation results
                - risk_profile: Risk assessment results
                - alternatives: List of alternative actions (if rejected)
                - requires_human_review: bool
                - reasoning: Explanation of decision
        """
        logger.info(f"Intercepting action: {action.get('type', 'unknown')}")
        
        # 1. Profile the task
        risk_profile = self.profile_task(action)
        
        # 2. Validate against Rule Bank
        validation = self.rule_bank.validate_action(action)
        
        # 3. Determine action status
        # Check for critical violations first
        critical_violations = [
            r_id for r_id in validation.get('violated_rules', [])
            if any(r['id'] == r_id and r.get('severity') == 'CRITICAL' for r in self.rule_bank.rules)
        ]
        
        num_violations = len(validation.get('violated_rules', []))
        
        if num_violations == 0 and risk_profile['risk_level'] != 'CRITICAL':
            status = 'approved'
            reasoning = "Action passes all ethical checks and safety requirements"
            alternatives = []
            requires_review = False
        elif risk_profile['risk_level'] == 'CRITICAL' or len(critical_violations) > 0:
            status = 'requires_review'
            reasoning = "Action flagged as critical risk or contains critical violations - human review required"
            alternatives = self._generate_alternatives(action, validation)
            requires_review = True
        elif num_violations > 0:
            status = 'rejected'
            reasoning = f"Action violates {num_violations} ethical rules"
            alternatives = self._generate_alternatives(action, validation)
            requires_review = num_violations > 2
        else:
            # Fallback - should not normally reach here
            status = 'approved'
            reasoning = "Action passes validation"
            alternatives = []
            requires_review = False
        
        result = {
            "status": status,
            "action": action,
            "validation": validation,
            "risk_profile": risk_profile,
            "alternatives": alternatives,
            "requires_human_review": requires_review,
            "reasoning": reasoning,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        # Record in history
        self.validation_history.append(result)
        
        logger.info(
            f"Validation complete: {status.upper()}, "
            f"Risk={risk_profile['risk_level']}, "
            f"Review={requires_review}"
        )
        
        return result
    
    def profile_task(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Profile a task to assess risk level and requirements.
        
        Args:
            action: Action dictionary
        
        Returns:
            Dictionary with risk profile:
                - risk_level: LOW, MEDIUM, HIGH, or CRITICAL
                - risk_factors: List of identified risk factors
                - recommended_checks: List of recommended validations
                - estimated_impact: User impact assessment
        """
        action_type = action.get('type', 'unknown')
        
        # Assess base risk from action type
        base_risk = self.RISK_THRESHOLDS.get(action_type, "MEDIUM")
        
        risk_factors = []
        recommended_checks = []
        
        # Check for risk amplifiers
        if action.get('confidence', 1.0) < 0.7:
            risk_factors.append("Low confidence score")
            recommended_checks.append("Manual content review")
        
        if action.get('user_facing', False):
            risk_factors.append("User-facing content")
            recommended_checks.append("Quality assurance check")
        
        if action.get('external_dependency', False):
            risk_factors.append("External API dependency")
            recommended_checks.append("Fallback mechanism required")
        
        if action.get('data_modification', False):
            risk_factors.append("Data modification involved")
            recommended_checks.append("Backup and rollback plan")
        
        # Estimate impact
        estimated_impact = self._estimate_impact(action)
        
        # Elevate risk if needed
        final_risk = self._elevate_risk_if_needed(base_risk, risk_factors, estimated_impact)
        
        return {
            "risk_level": final_risk,
            "risk_factors": risk_factors,
            "recommended_checks": recommended_checks,
            "estimated_impact": estimated_impact,
            "base_risk": base_risk
        }
    
    def _assess_risk(self, action: Dict[str, Any]) -> str:
        """
        Internal risk assessment helper.
        
        Returns:
            Risk level: LOW, MEDIUM, HIGH, or CRITICAL
        """
        profile = self.profile_task(action)
        return profile['risk_level']
    
    def _estimate_impact(self, action: Dict[str, Any]) -> str:
        """
        Estimate user impact of an action.
        
        Returns:
            Impact level: minimal, moderate, significant, major
        """
        # Factors that increase impact
        user_facing = action.get('user_facing', False)
        reach = action.get('expected_reach', 0)
        permanence = action.get('permanent', False)
        
        if permanence and reach > 1000:
            return "major"
        elif user_facing and reach > 100:
            return "significant"
        elif user_facing or reach > 10:
            return "moderate"
        else:
            return "minimal"
    
    def _elevate_risk_if_needed(self, base_risk: str, risk_factors: List[str],
                                 estimated_impact: str) -> str:
        """
        Elevate risk level based on factors and impact.
        
        Returns:
            Elevated risk level
        """
        risk_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        current_index = risk_levels.index(base_risk) if base_risk in risk_levels else 1
        
        # Elevate for multiple risk factors
        if len(risk_factors) >= 3:
            current_index = min(current_index + 1, 3)
        
        # Elevate for major impact
        if estimated_impact in ["significant", "major"]:
            current_index = min(current_index + 1, 3)
        
        return risk_levels[current_index]
    
    def handle_violation(self, action: Dict[str, Any],
                        validation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a rule violation by suggesting alternatives or modifications.
        
        Args:
            action: Original action that violated rules
            validation: Validation results from Rule Bank
        
        Returns:
            Dictionary with handling results:
                - can_proceed: bool
                - modified_action: Modified action (if applicable)
                - alternatives: List of alternative actions
                - escalate_to_human: bool
        """
        violated_rules = validation['violated_rules']
        recommendations = validation.get('recommendations', [])
        
        # Check if violation can be auto-corrected
        can_auto_correct = len(violated_rules) <= 2 and validation['risk_level'] != 'CRITICAL'
        
        if can_auto_correct:
            # Attempt to modify action based on recommendations
            modified_action = action.copy()
            
            # Apply simple auto-corrections
            if 'confidence' in action and action['confidence'] < 0.8:
                modified_action['confidence'] = 0.8
                modified_action['auto_corrected'] = True
                modified_action['corrections_applied'] = ['increased_confidence_threshold']
            
            return {
                "can_proceed": True,
                "modified_action": modified_action,
                "alternatives": [],
                "escalate_to_human": False,
                "reasoning": "Applied automatic corrections"
            }
        else:
            # Cannot auto-correct, provide alternatives
            return {
                "can_proceed": False,
                "modified_action": None,
                "alternatives": self._generate_alternatives(action, validation),
                "escalate_to_human": True,
                "reasoning": "Violations require human judgment"
            }
    
    def _generate_alternatives(self, action: Dict[str, Any],
                              validation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate alternative actions when original is rejected.
        
        Args:
            action: Original action
            validation: Validation results
        
        Returns:
            List of alternative action dictionaries
        """
        alternatives = []
        recommendations = validation.get('recommendations', [])
        
        # Alternative 1: Reduce scope
        if action.get('type') == 'post_world_tour_content':
            alternatives.append({
                "type": "preview_content",
                "description": "Preview content for manual review instead of posting",
                "confidence": action.get('confidence', 0.5),
                "reasoning": "Lower-risk alternative: review before publishing"
            })
        
        # Alternative 2: Add safeguards based on recommendations
        if recommendations:
            enhanced_action = action.copy()
            enhanced_action['safeguards'] = recommendations
            enhanced_action['description'] = "Original action with enhanced safeguards"
            alternatives.append(enhanced_action)
        
        # Alternative 3: Defer to human
        alternatives.append({
            "type": "escalate_to_human",
            "description": "Request human review and approval",
            "original_action": action,
            "reasoning": "Complex ethical considerations require human judgment"
        })
        
        return alternatives
    
    def get_validation_stats(self) -> Dict[str, Any]:
        """
        Get statistics about validation history.
        
        Returns:
            Dictionary with validation statistics
        """
        total = len(self.validation_history)
        if total == 0:
            return {
                "total_validations": 0,
                "approved": 0,
                "rejected": 0,
                "requires_review": 0,
                "approval_rate": 0.0
            }
        
        approved = sum(1 for v in self.validation_history if v['status'] == 'approved')
        rejected = sum(1 for v in self.validation_history if v['status'] == 'rejected')
        requires_review = sum(1 for v in self.validation_history if v['status'] == 'requires_review')
        
        return {
            "total_validations": total,
            "approved": approved,
            "rejected": rejected,
            "requires_review": requires_review,
            "approval_rate": approved / total if total > 0 else 0.0,
            "rejection_rate": rejected / total if total > 0 else 0.0,
            "review_rate": requires_review / total if total > 0 else 0.0
        }
