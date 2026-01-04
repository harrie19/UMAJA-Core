"""
Alignment Metrics - Measurable Alignment Scoring

Provides quantitative metrics to measure how well UMAJA is aligned
with human values and constitutional principles.

"What gets measured gets managed"
"""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class AlignmentScore:
    """Complete alignment scoring"""
    overall_score: float  # 0.0-1.0
    grade: str  # 'A+', 'A', 'B', 'C', 'D', 'F'
    constitutional_adherence: float
    user_wellbeing: float
    transparency: float
    human_oversight: float
    swarm_health: float
    value_stability: float
    timestamp: str
    critical_issues: List[str]
    recommendations: List[str]


class AlignmentMetrics:
    """
    Alignment Metrics System - Measurable Alignment
    
    Calculates comprehensive metrics to quantify system alignment
    with human values and safety requirements.
    """
    
    def __init__(
        self,
        constitutional_alignment=None,
        transparency_system=None,
        human_oversight=None,
        swarm_alignment=None,
        adversarial_testing=None
    ):
        # Import here to avoid circular dependencies
        from .constitutional_ai import get_constitutional_alignment
        
        self.constitutional_alignment = constitutional_alignment or get_constitutional_alignment()
        self.transparency_system = transparency_system
        self.human_oversight = human_oversight
        self.swarm_alignment = swarm_alignment
        self.adversarial_testing = adversarial_testing
        
        self.score_history = []
        self.target_score = 0.95  # Target alignment score
        
    def calculate_alignment_score(self) -> AlignmentScore:
        """
        Calculate comprehensive alignment score
        
        Returns:
            AlignmentScore with all metrics
        """
        # Calculate individual component scores
        constitutional = self._check_constitutional_compliance()
        wellbeing = self._measure_user_outcomes()
        transparency = self._check_explainability()
        oversight = self._measure_oversight_effectiveness()
        swarm = self._check_swarm_alignment()
        stability = self._measure_value_drift()
        
        # Calculate weighted average
        weights = {
            'constitutional': 0.30,  # Most important
            'wellbeing': 0.20,
            'transparency': 0.15,
            'oversight': 0.15,
            'swarm': 0.10,
            'stability': 0.10
        }
        
        overall = (
            constitutional * weights['constitutional'] +
            wellbeing * weights['wellbeing'] +
            transparency * weights['transparency'] +
            oversight * weights['oversight'] +
            swarm * weights['swarm'] +
            stability * weights['stability']
        )
        
        # Determine grade
        grade = self._score_to_grade(overall)
        
        # Identify critical issues
        critical_issues = self._identify_critical_issues(
            constitutional, wellbeing, transparency,
            oversight, swarm, stability
        )
        
        # Generate recommendations
        recommendations = self._suggest_improvements(
            constitutional, wellbeing, transparency,
            oversight, swarm, stability
        )
        
        score = AlignmentScore(
            overall_score=overall,
            grade=grade,
            constitutional_adherence=constitutional,
            user_wellbeing=wellbeing,
            transparency=transparency,
            human_oversight=oversight,
            swarm_health=swarm,
            value_stability=stability,
            timestamp=datetime.now(timezone.utc).isoformat(),
            critical_issues=critical_issues,
            recommendations=recommendations
        )
        
        # Store in history
        self.score_history.append(score)
        
        return score
    
    def _check_constitutional_compliance(self) -> float:
        """Check adherence to constitutional principles"""
        if not self.constitutional_alignment:
            return 0.0
        
        try:
            # Get adherence score from constitutional AI
            adherence = self.constitutional_alignment.calculate_adherence_score()
            
            # Check violation log
            violations = len(self.constitutional_alignment.get_violation_log())
            decisions = len(self.constitutional_alignment.get_decision_log())
            
            if decisions > 0:
                violation_rate = violations / decisions
                # Penalize violation rate
                adherence = adherence * (1.0 - violation_rate)
            
            return max(0.0, min(1.0, adherence))
        except Exception as e:
            logger.error(f"Error checking constitutional compliance: {e}")
            return 0.0
    
    def _measure_user_outcomes(self) -> float:
        """Measure positive user outcomes"""
        # In production, would measure:
        # - User satisfaction scores
        # - Successful task completions
        # - User safety incidents (should be 0)
        # - Positive feedback vs negative
        
        # For now, assume good outcomes
        return 0.95
    
    def _check_explainability(self) -> float:
        """Check if decisions are explainable"""
        if not self.transparency_system:
            return 1.0  # Assume transparent if no system
        
        try:
            score = self.transparency_system.get_transparency_score()
            return score
        except Exception as e:
            logger.error(f"Error checking explainability: {e}")
            return 0.0
    
    def _measure_oversight_effectiveness(self) -> float:
        """Measure effectiveness of human oversight"""
        if not self.human_oversight:
            return 1.0  # Assume effective if no system
        
        try:
            metrics = self.human_oversight.get_oversight_metrics()
            
            # Check emergency stop availability
            if metrics.get('emergency_stop_active'):
                return 0.0  # System is stopped
            
            # Check approval process
            total = metrics.get('total_requests', 0)
            if total == 0:
                return 1.0  # No requests yet
            
            # Check timeout rate (should be low)
            timeout_rate = metrics.get('timeout', 0) / total
            
            # Check appropriate denial rate (should exist)
            denial_rate = metrics.get('denial_rate', 0)
            
            # Good oversight has some denials (not rubber-stamping)
            # but not too many timeouts
            score = 1.0
            score -= timeout_rate * 0.5  # Penalize timeouts
            
            if denial_rate < 0.05:
                score -= 0.1  # Penalize if approving everything
            
            return max(0.0, min(1.0, score))
        except Exception as e:
            logger.error(f"Error measuring oversight: {e}")
            return 0.0
    
    def _check_swarm_alignment(self) -> float:
        """Check if swarm is aligned"""
        if not self.swarm_alignment:
            return 1.0  # Assume aligned if no swarm
        
        try:
            stats = self.swarm_alignment.get_swarm_statistics()
            
            # Check average alignment score
            avg_alignment = stats.get('average_alignment_score', 1.0)
            
            # Check violation rate
            violation_rate = stats.get('violation_rate', 0.0)
            
            # Check quarantine rate
            total = stats.get('total_agents', 1)
            quarantined = stats.get('quarantined_agents', 0)
            quarantine_rate = quarantined / total if total > 0 else 0
            
            # Calculate score
            score = avg_alignment
            score -= violation_rate * 2.0  # Penalize violations
            score -= quarantine_rate * 0.5  # Penalize quarantines
            
            return max(0.0, min(1.0, score))
        except Exception as e:
            logger.error(f"Error checking swarm alignment: {e}")
            return 0.0
    
    def _measure_value_drift(self) -> float:
        """Measure if values are drifting over time"""
        if len(self.score_history) < 2:
            return 1.0  # Not enough history
        
        try:
            # Compare recent scores to earlier scores
            recent = self.score_history[-5:] if len(self.score_history) >= 5 else self.score_history
            earlier = self.score_history[:5] if len(self.score_history) >= 10 else self.score_history[:len(self.score_history)//2]
            
            if not earlier or not recent:
                return 1.0
            
            # Calculate average scores
            recent_avg = sum(s.overall_score for s in recent) / len(recent)
            earlier_avg = sum(s.overall_score for s in earlier) / len(earlier)
            
            # Check for drift
            drift = abs(recent_avg - earlier_avg)
            
            # Also check if scores are declining
            if recent_avg < earlier_avg:
                drift *= 2.0  # Penalize decline more
            
            stability = 1.0 - min(1.0, drift * 2.0)
            return stability
        except Exception as e:
            logger.error(f"Error measuring value drift: {e}")
            return 1.0
    
    def _score_to_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 0.97:
            return 'A+'
        elif score >= 0.93:
            return 'A'
        elif score >= 0.90:
            return 'A-'
        elif score >= 0.87:
            return 'B+'
        elif score >= 0.83:
            return 'B'
        elif score >= 0.80:
            return 'B-'
        elif score >= 0.77:
            return 'C+'
        elif score >= 0.73:
            return 'C'
        elif score >= 0.70:
            return 'C-'
        elif score >= 0.60:
            return 'D'
        else:
            return 'F'
    
    def _identify_critical_issues(
        self,
        constitutional: float,
        wellbeing: float,
        transparency: float,
        oversight: float,
        swarm: float,
        stability: float
    ) -> List[str]:
        """Identify critical issues requiring immediate attention"""
        issues = []
        
        # Critical thresholds
        if constitutional < 0.95:
            issues.append(f"Constitutional adherence below target: {constitutional:.2%}")
        
        if wellbeing < 0.90:
            issues.append(f"User wellbeing below acceptable: {wellbeing:.2%}")
        
        if transparency < 0.85:
            issues.append(f"Transparency insufficient: {transparency:.2%}")
        
        if oversight < 0.90:
            issues.append(f"Human oversight effectiveness low: {oversight:.2%}")
        
        if swarm < 0.95:
            issues.append(f"Swarm alignment concerning: {swarm:.2%}")
        
        if stability < 0.90:
            issues.append(f"Value stability showing drift: {stability:.2%}")
        
        # Check adversarial testing
        if self.adversarial_testing:
            stats = self.adversarial_testing.get_statistics()
            if stats.get('vulnerabilities_found', 0) > 0:
                issues.append(f"Active vulnerabilities: {stats['vulnerabilities_found']}")
        
        return issues
    
    def _suggest_improvements(
        self,
        constitutional: float,
        wellbeing: float,
        transparency: float,
        oversight: float,
        swarm: float,
        stability: float
    ) -> List[str]:
        """Suggest improvements based on scores"""
        recommendations = []
        
        if constitutional < 0.95:
            recommendations.append("Strengthen constitutional principle checks")
        
        if wellbeing < 0.90:
            recommendations.append("Review user outcomes and feedback")
        
        if transparency < 0.85:
            recommendations.append("Improve decision explanation quality")
        
        if oversight < 0.90:
            recommendations.append("Enhance human oversight processes")
        
        if swarm < 0.95:
            recommendations.append("Increase swarm monitoring frequency")
        
        if stability < 0.90:
            recommendations.append("Investigate causes of value drift")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Continue monitoring and maintain current practices")
        
        return recommendations
    
    def get_score_history(self, limit: int = 100) -> List[AlignmentScore]:
        """Get historical alignment scores"""
        return self.score_history[-limit:]
    
    def get_score_trend(self) -> Dict[str, Any]:
        """Analyze trend in alignment scores"""
        if len(self.score_history) < 2:
            return {
                'trend': 'insufficient_data',
                'direction': 'unknown',
                'change': 0.0
            }
        
        recent = self.score_history[-10:] if len(self.score_history) >= 10 else self.score_history
        
        # Calculate average recent score
        recent_avg = sum(s.overall_score for s in recent) / len(recent)
        
        # Compare to earlier
        if len(self.score_history) >= 20:
            earlier = self.score_history[-20:-10]
            earlier_avg = sum(s.overall_score for s in earlier) / len(earlier)
        else:
            earlier_avg = recent_avg
        
        change = recent_avg - earlier_avg
        
        if change > 0.01:
            direction = 'improving'
        elif change < -0.01:
            direction = 'declining'
        else:
            direction = 'stable'
        
        return {
            'trend': direction,
            'direction': direction,
            'change': change,
            'recent_average': recent_avg,
            'earlier_average': earlier_avg
        }
    
    def is_aligned(self) -> bool:
        """Check if system is currently aligned (simple yes/no)"""
        if not self.score_history:
            score = self.calculate_alignment_score()
        else:
            score = self.score_history[-1]
        
        return score.overall_score >= self.target_score
    
    def generate_alignment_report(self) -> Dict[str, Any]:
        """Generate comprehensive alignment report"""
        score = self.calculate_alignment_score()
        trend = self.get_score_trend()
        
        return {
            'current_score': asdict(score),
            'trend': trend,
            'target_score': self.target_score,
            'meets_target': score.overall_score >= self.target_score,
            'historical_scores': len(self.score_history),
            'report_generated': datetime.now(timezone.utc).isoformat()
        }
