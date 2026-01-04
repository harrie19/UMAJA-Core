"""
Rule Bank System - Persistent Ethical Constraint System

Purpose: Store and validate agent decisions against Bahá'í principles
Core Principles: Truth, Unity, Service, Justice, Moderation

This system ensures all autonomous agent actions align with ethical constraints
and provides persistent memory across execution cycles via GitHub Actions cache.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class RuleBank:
    """
    Persistent ethical constraint system based on Bahá'í principles.
    
    Stores rules, validates actions, learns from feedback, and maintains
    an audit trail of all validations and violations.
    """
    
    # Bahá'í principles mapped to ethical constraints
    PRINCIPLES = {
        "truth": {
            "description": "Independent investigation of truth, no hallucination",
            "constraints": ["no_hallucination", "cite_sources", "verify_facts"]
        },
        "unity": {
            "description": "Unity of humanity, no divisive content",
            "constraints": ["no_division", "inclusive_language", "respect_diversity"]
        },
        "service": {
            "description": "Service to humanity, benefit-driven actions",
            "constraints": ["positive_benefit", "no_exploitation", "community_first"]
        },
        "justice": {
            "description": "Justice and fairness, no bias or discrimination",
            "constraints": ["no_bias", "fair_access", "equal_treatment"]
        },
        "moderation": {
            "description": "Moderation in all things, efficient resource use",
            "constraints": ["resource_efficiency", "no_maximization", "sustainable_growth"]
        }
    }
    
    def __init__(self, memory_path: str = ".agent-memory"):
        """
        Initialize Rule Bank with persistent memory path.
        
        Args:
            memory_path: Directory path for persistent memory storage
        """
        self.memory_path = Path(memory_path)
        self.memory_path.mkdir(parents=True, exist_ok=True)
        
        self.rules_file = self.memory_path / "rule_bank.json"
        self.rules = self.load_rules()
        
        logger.info(f"Rule Bank initialized with {len(self.rules)} rules")
    
    def load_rules(self) -> List[Dict[str, Any]]:
        """
        Load rules from persistent storage or initialize with defaults.
        
        Returns:
            List of rule dictionaries
        """
        if self.rules_file.exists():
            try:
                with open(self.rules_file, 'r') as f:
                    data = json.load(f)
                    logger.info(f"Loaded {len(data.get('rules', []))} rules from storage")
                    return data.get('rules', [])
            except Exception as e:
                logger.warning(f"Could not load rules file: {e}, initializing defaults")
        
        return self._initialize_default_rules()
    
    def _initialize_default_rules(self) -> List[Dict[str, Any]]:
        """
        Initialize Rule Bank with default Bahá'í principle-based rules.
        
        Returns:
            List of default rule dictionaries
        """
        default_rules = [
            {
                "id": "TRUTH_001",
                "principle": "truth",
                "constraint": "no_hallucination",
                "expression": "confidence >= 0.8",
                "description": "Require high confidence (>=0.8) for factual claims",
                "learned_from": "Core Bahá'í principle: Independent investigation of truth",
                "violations": 0,
                "applied_count": 0,
                "severity": "HIGH"
            },
            {
                "id": "TRUTH_002",
                "principle": "truth",
                "constraint": "cite_sources",
                "expression": "has_source_attribution or confidence >= 0.95",
                "description": "Cite sources for claims unless extremely confident",
                "learned_from": "Core Bahá'í principle: Verifiable truth",
                "violations": 0,
                "applied_count": 0,
                "severity": "MEDIUM"
            },
            {
                "id": "UNITY_001",
                "principle": "unity",
                "constraint": "no_division",
                "expression": "divisive_content_score < 0.3",
                "description": "Reject content that promotes division or conflict",
                "learned_from": "Core Bahá'í principle: Unity of humanity",
                "violations": 0,
                "applied_count": 0,
                "severity": "CRITICAL"
            },
            {
                "id": "UNITY_002",
                "principle": "unity",
                "constraint": "inclusive_language",
                "expression": "inclusive_score >= 0.7",
                "description": "Use language that welcomes all people",
                "learned_from": "Core Bahá'í principle: Respect for diversity",
                "violations": 0,
                "applied_count": 0,
                "severity": "MEDIUM"
            },
            {
                "id": "SERVICE_001",
                "principle": "service",
                "constraint": "positive_benefit",
                "expression": "benefit_score >= 0.6",
                "description": "Actions must provide clear benefit to users",
                "learned_from": "Core Bahá'í principle: Service to humanity",
                "violations": 0,
                "applied_count": 0,
                "severity": "HIGH"
            },
            {
                "id": "SERVICE_002",
                "principle": "service",
                "constraint": "no_exploitation",
                "expression": "manipulation_score < 0.2",
                "description": "Reject manipulative or exploitative content",
                "learned_from": "Core Bahá'í principle: Ethical service",
                "violations": 0,
                "applied_count": 0,
                "severity": "CRITICAL"
            },
            {
                "id": "JUSTICE_001",
                "principle": "justice",
                "constraint": "no_bias",
                "expression": "bias_score < 0.3",
                "description": "Ensure fair treatment regardless of demographics",
                "learned_from": "Core Bahá'í principle: Justice and fairness",
                "violations": 0,
                "applied_count": 0,
                "severity": "HIGH"
            },
            {
                "id": "MODERATION_001",
                "principle": "moderation",
                "constraint": "resource_efficiency",
                "expression": "resource_usage <= budget",
                "description": "Use resources efficiently within allocated budget",
                "learned_from": "Core Bahá'í principle: Moderation in all things",
                "violations": 0,
                "applied_count": 0,
                "severity": "MEDIUM"
            }
        ]
        
        logger.info(f"Initialized {len(default_rules)} default rules")
        return default_rules
    
    def save_rules(self):
        """
        Persist rules to storage with metadata.
        """
        try:
            data = {
                "rules": self.rules,
                "last_updated": datetime.utcnow().isoformat() + "Z",
                "agent_version": "1.0.0",
                "total_validations": sum(r.get('applied_count', 0) for r in self.rules),
                "total_violations": sum(r.get('violations', 0) for r in self.rules)
            }
            
            with open(self.rules_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved {len(self.rules)} rules to storage")
        except Exception as e:
            logger.error(f"Failed to save rules: {e}")
    
    def validate_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate an action against all applicable rules.
        
        Args:
            action: Dictionary containing action details
                - type: Action type (e.g., 'post_world_tour_content')
                - confidence: Confidence score (0.0-1.0)
                - benefit_score: Benefit to users (0.0-1.0)
                - content: Content text (if applicable)
                - ... other action-specific fields
        
        Returns:
            Dictionary with validation results:
                - allowed: bool - Whether action is allowed
                - violated_rules: List[str] - IDs of violated rules
                - applied_rules: List[str] - IDs of all checked rules
                - risk_level: str - Overall risk assessment
                - recommendations: List[str] - Suggestions for improvement
        """
        violated_rules = []
        applied_rules = []
        recommendations = []
        
        # Extract action parameters with defaults
        confidence = action.get('confidence', 1.0)
        benefit_score = action.get('benefit_score', 0.0)
        content = action.get('content', '')
        
        # Calculate derived metrics (simplified for MVP)
        divisive_score = self._assess_divisiveness(content)
        inclusive_score = self._assess_inclusiveness(content)
        manipulation_score = self._assess_manipulation(content)
        bias_score = self._assess_bias(action)
        
        # Check each rule
        for rule in self.rules:
            rule_id = rule['id']
            principle = rule['principle']
            constraint = rule['constraint']
            severity = rule.get('severity', 'MEDIUM')
            
            rule['applied_count'] = rule.get('applied_count', 0) + 1
            applied_rules.append(rule_id)
            
            # Evaluate rule based on constraint type
            violated = False
            
            if constraint == "no_hallucination":
                if confidence < 0.8:
                    violated = True
                    recommendations.append(f"Increase confidence score to >=0.8 or add source citations")
            
            elif constraint == "cite_sources":
                has_source = self._has_source_attribution(content)
                if not has_source and confidence < 0.95:
                    violated = True
                    recommendations.append("Add source attribution for factual claims")
            
            elif constraint == "no_division":
                if divisive_score >= 0.3:
                    violated = True
                    recommendations.append("Remove divisive or conflict-promoting content")
            
            elif constraint == "inclusive_language":
                if inclusive_score < 0.7:
                    violated = True
                    recommendations.append("Use more inclusive and welcoming language")
            
            elif constraint == "positive_benefit":
                if benefit_score < 0.6:
                    violated = True
                    recommendations.append("Ensure action provides clear benefit to users")
            
            elif constraint == "no_exploitation":
                if manipulation_score >= 0.2:
                    violated = True
                    recommendations.append("Remove manipulative or exploitative elements")
            
            elif constraint == "no_bias":
                if bias_score >= 0.3:
                    violated = True
                    recommendations.append("Ensure fair treatment regardless of demographics")
            
            elif constraint == "resource_efficiency":
                resource_usage = action.get('resource_usage', 0)
                budget = action.get('resource_budget', float('inf'))
                if resource_usage > budget:
                    violated = True
                    recommendations.append("Reduce resource usage to stay within budget")
            
            if violated:
                violated_rules.append(rule_id)
                rule['violations'] = rule.get('violations', 0) + 1
                logger.warning(f"Rule {rule_id} violated: {rule['description']}")
        
        # Determine overall risk level
        risk_level = self._calculate_risk_level(violated_rules)
        
        # Action is allowed only if no critical violations
        critical_violations = [
            r_id for r_id in violated_rules 
            if any(r['id'] == r_id and r.get('severity') == 'CRITICAL' for r in self.rules)
        ]
        allowed = len(critical_violations) == 0
        
        result = {
            "allowed": allowed,
            "violated_rules": violated_rules,
            "applied_rules": applied_rules,
            "risk_level": risk_level,
            "recommendations": recommendations,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        logger.info(
            f"Validation complete: {'ALLOWED' if allowed else 'REJECTED'}, "
            f"{len(violated_rules)} violations, risk={risk_level}"
        )
        
        return result
    
    def _assess_divisiveness(self, content: str) -> float:
        """
        Assess how divisive content is (simplified heuristic).
        
        Returns:
            Score from 0.0 (not divisive) to 1.0 (very divisive)
        """
        if not content:
            return 0.0
        
        divisive_keywords = [
            'vs', 'versus', 'against', 'hate', 'stupid', 'inferior',
            'superior', 'enemy', 'war', 'fight', 'conflict'
        ]
        
        content_lower = content.lower()
        matches = sum(1 for keyword in divisive_keywords if keyword in content_lower)
        
        # Normalize to 0-1 range
        return min(matches / 5.0, 1.0)
    
    def _assess_inclusiveness(self, content: str) -> float:
        """
        Assess how inclusive content is (simplified heuristic).
        
        Returns:
            Score from 0.0 (not inclusive) to 1.0 (very inclusive)
        """
        if not content:
            return 0.5  # Neutral
        
        inclusive_keywords = [
            'everyone', 'all', 'together', 'unity', 'welcome',
            'diverse', 'inclusive', 'community', 'shared', 'humanity'
        ]
        
        content_lower = content.lower()
        matches = sum(1 for keyword in inclusive_keywords if keyword in content_lower)
        
        # Normalize to 0-1 range, baseline of 0.5
        return min(0.5 + (matches / 10.0), 1.0)
    
    def _assess_manipulation(self, content: str) -> float:
        """
        Assess manipulative intent (simplified heuristic).
        
        Returns:
            Score from 0.0 (not manipulative) to 1.0 (very manipulative)
        """
        if not content:
            return 0.0
        
        manipulative_keywords = [
            'must buy', 'limited time', 'act now', 'secret',
            'guaranteed', 'trick', 'exploit', 'manipulate'
        ]
        
        content_lower = content.lower()
        matches = sum(1 for keyword in manipulative_keywords if keyword in content_lower)
        
        return min(matches / 4.0, 1.0)
    
    def _assess_bias(self, action: Dict[str, Any]) -> float:
        """
        Assess potential bias (simplified heuristic).
        
        Returns:
            Score from 0.0 (no bias) to 1.0 (high bias)
        """
        # For MVP, return low bias score
        # In production, would use ML models for bias detection
        return 0.1
    
    def _has_source_attribution(self, content: str) -> bool:
        """
        Check if content has source attribution.
        
        Returns:
            True if sources are cited
        """
        if not content:
            return False
        
        # Look for citation patterns
        citation_patterns = ['source:', 'according to', 'reference:', 'citation:']
        content_lower = content.lower()
        
        return any(pattern in content_lower for pattern in citation_patterns)
    
    def _calculate_risk_level(self, violated_rules: List[str]) -> str:
        """
        Calculate overall risk level based on violated rules.
        
        Returns:
            Risk level: LOW, MEDIUM, HIGH, or CRITICAL
        """
        if not violated_rules:
            return "LOW"
        
        # Count violations by severity
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        
        for rule_id in violated_rules:
            for rule in self.rules:
                if rule['id'] == rule_id:
                    severity = rule.get('severity', 'MEDIUM')
                    severity_counts[severity] += 1
                    break
        
        if severity_counts["CRITICAL"] > 0:
            return "CRITICAL"
        elif severity_counts["HIGH"] > 0:
            return "HIGH"
        elif severity_counts["MEDIUM"] > 1:
            return "HIGH"
        elif severity_counts["MEDIUM"] > 0:
            return "MEDIUM"
        else:
            return "LOW"
    
    def learn_rule(self, observation: str, principle: str, constraint: str,
                   severity: str = "MEDIUM"):
        """
        Learn a new rule from observation or feedback.
        
        Args:
            observation: Description of what was observed
            principle: Bahá'í principle (truth, unity, service, justice, moderation)
            constraint: Specific constraint type
            severity: Rule severity (LOW, MEDIUM, HIGH, CRITICAL)
        """
        # Generate new rule ID
        principle_prefix = principle.upper()[:5]
        existing_ids = [r['id'] for r in self.rules if r['id'].startswith(principle_prefix)]
        next_num = len([i for i in existing_ids if i.startswith(principle_prefix)]) + 1
        new_id = f"{principle_prefix}_{next_num:03d}"
        
        new_rule = {
            "id": new_id,
            "principle": principle,
            "constraint": constraint,
            "expression": "learned_from_feedback",
            "description": observation,
            "learned_from": f"Feedback observation: {observation}",
            "violations": 0,
            "applied_count": 0,
            "severity": severity,
            "learned_at": datetime.utcnow().isoformat() + "Z"
        }
        
        self.rules.append(new_rule)
        logger.info(f"Learned new rule {new_id}: {observation}")
    
    def get_violation_report(self) -> Dict[str, Any]:
        """
        Generate a report of rule violations and statistics.
        
        Returns:
            Dictionary with violation statistics
        """
        total_validations = sum(r.get('applied_count', 0) for r in self.rules)
        total_violations = sum(r.get('violations', 0) for r in self.rules)
        
        violations_by_principle = {}
        for principle in self.PRINCIPLES.keys():
            violations = sum(
                r.get('violations', 0) 
                for r in self.rules 
                if r['principle'] == principle
            )
            violations_by_principle[principle] = violations
        
        most_violated = sorted(
            self.rules,
            key=lambda r: r.get('violations', 0),
            reverse=True
        )[:5]
        
        return {
            "total_validations": total_validations,
            "total_violations": total_violations,
            "violation_rate": total_violations / max(total_validations, 1),
            "violations_by_principle": violations_by_principle,
            "most_violated_rules": [
                {
                    "id": r['id'],
                    "description": r['description'],
                    "violations": r.get('violations', 0)
                }
                for r in most_violated if r.get('violations', 0) > 0
            ],
            "rule_count": len(self.rules),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    def get_principle_alignment(self, action: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate alignment scores for each Bahá'í principle.
        
        Returns:
            Dictionary mapping principles to alignment scores (0.0-1.0)
        """
        validation = self.validate_action(action)
        
        alignment = {}
        for principle in self.PRINCIPLES.keys():
            # Count rules for this principle
            principle_rules = [r for r in self.rules if r['principle'] == principle]
            principle_violated = [
                r_id for r_id in validation['violated_rules']
                if any(r['id'] == r_id and r['principle'] == principle for r in self.rules)
            ]
            
            # Calculate alignment (inverse of violation rate)
            if principle_rules:
                violation_rate = len(principle_violated) / len(principle_rules)
                alignment[principle] = 1.0 - violation_rate
            else:
                alignment[principle] = 1.0
        
        return alignment
