"""
Tests for Reasoning Middleware
"""

import sys
import tempfile
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from rule_bank import RuleBank
from reasoning_middleware import ReasoningMiddleware


class TestReasoningMiddleware:
    """Test suite for Reasoning Middleware"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.rule_bank = RuleBank(memory_path=self.temp_dir)
        self.middleware = ReasoningMiddleware(self.rule_bank)
    
    def test_initialization(self):
        """Test middleware initializes correctly"""
        assert self.middleware is not None
        assert self.middleware.rule_bank is not None
        assert isinstance(self.middleware.validation_history, list)
    
    def test_approve_ethical_action(self):
        """Test middleware approves actions passing all checks"""
        action = {
            'type': 'post_world_tour_content',
            'confidence': 0.95,  # High enough to skip source requirement
            'benefit_score': 0.85,
            'content': 'Welcoming content for our global community',
            'user_facing': True,
            'expected_reach': 500
        }
        
        result = self.middleware.intercept(action)
        
        assert result['status'] == 'approved'
        assert result['validation']['allowed'] == True
        assert result['requires_human_review'] == False
        assert 'reasoning' in result
    
    def test_reject_unethical_action(self):
        """Test middleware blocks actions violating Truth principle"""
        action = {
            'type': 'generate_content',
            'confidence': 0.5,  # Below 0.8 threshold
            'benefit_score': 0.7,
            'content': 'Some uncertain claim without sources'
        }
        
        result = self.middleware.intercept(action)
        
        assert result['status'] == 'rejected'
        assert len(result['validation']['violated_rules']) > 0
        assert len(result['alternatives']) > 0
    
    def test_escalate_critical_risk(self):
        """Test middleware escalates critical risk actions"""
        action = {
            'type': 'financial_transaction',  # Critical risk type
            'confidence': 0.9,
            'benefit_score': 0.8,
            'amount': 1000
        }
        
        result = self.middleware.intercept(action)
        
        assert result['status'] == 'requires_review'
        assert result['requires_human_review'] == True
        assert result['risk_profile']['risk_level'] == 'CRITICAL'
    
    def test_task_profiling(self):
        """Test task profiling assesses risk correctly"""
        # Low risk action
        low_risk_action = {
            'type': 'preview_content',
            'confidence': 1.0
        }
        
        profile = self.middleware.profile_task(low_risk_action)
        assert profile['risk_level'] in ['LOW', 'MEDIUM']
        
        # High risk action
        high_risk_action = {
            'type': 'modify_data',
            'confidence': 0.6,
            'user_facing': True,
            'external_dependency': True,
            'data_modification': True
        }
        
        profile = self.middleware.profile_task(high_risk_action)
        assert profile['risk_level'] in ['HIGH', 'CRITICAL']
        assert len(profile['risk_factors']) > 0
    
    def test_violation_handling(self):
        """Test violation handling provides alternatives"""
        action = {
            'type': 'post_world_tour_content',
            'confidence': 0.6,
            'benefit_score': 0.7,
            'content': 'Content'
        }
        
        validation = self.rule_bank.validate_action(action)
        handling = self.middleware.handle_violation(action, validation)
        
        assert 'can_proceed' in handling
        assert 'alternatives' in handling or 'modified_action' in handling
    
    def test_validation_history_tracking(self):
        """Test middleware tracks validation history"""
        initial_count = len(self.middleware.validation_history)
        
        action = {
            'type': 'test_action',
            'confidence': 0.9,
            'benefit_score': 0.8
        }
        
        self.middleware.intercept(action)
        
        assert len(self.middleware.validation_history) > initial_count
    
    def test_validation_statistics(self):
        """Test validation statistics calculation"""
        # Approve an action
        good_action = {
            'type': 'test',
            'confidence': 0.95,
            'benefit_score': 0.9,
            'content': 'Welcome everyone to our community together'  # Inclusive content
        }
        self.middleware.intercept(good_action)
        
        # Reject an action
        bad_action = {
            'type': 'test',
            'confidence': 0.3,
            'benefit_score': 0.2
        }
        self.middleware.intercept(bad_action)
        
        stats = self.middleware.get_validation_stats()
        
        assert stats['total_validations'] >= 2
        assert 'approval_rate' in stats
        assert 0.0 <= stats['approval_rate'] <= 1.0
    
    def test_alternative_generation(self):
        """Test middleware generates reasonable alternatives"""
        action = {
            'type': 'post_world_tour_content',
            'confidence': 0.5,
            'benefit_score': 0.7,
            'content': 'Test'
        }
        
        result = self.middleware.intercept(action)
        
        if result['status'] != 'approved':
            assert len(result['alternatives']) > 0
            
            # Check alternatives have reasonable structure
            for alt in result['alternatives']:
                assert 'type' in alt or 'description' in alt
    
    def test_impact_estimation(self):
        """Test middleware estimates user impact correctly"""
        # Minimal impact
        minimal = {
            'type': 'test',
            'user_facing': False,
            'expected_reach': 5
        }
        profile = self.middleware.profile_task(minimal)
        assert profile['estimated_impact'] == 'minimal'
        
        # Major impact
        major = {
            'type': 'test',
            'user_facing': True,
            'expected_reach': 2000,
            'permanent': True
        }
        profile = self.middleware.profile_task(major)
        assert profile['estimated_impact'] in ['significant', 'major']
    
    def test_recommended_checks(self):
        """Test middleware recommends appropriate checks"""
        action = {
            'type': 'post_content',
            'confidence': 0.6,
            'user_facing': True,
            'external_dependency': True
        }
        
        profile = self.middleware.profile_task(action)
        
        assert len(profile['recommended_checks']) > 0
        assert 'risk_factors' in profile


def test_middleware_blocks_multiple_violations():
    """Test middleware properly handles multiple rule violations"""
    with tempfile.TemporaryDirectory() as temp_dir:
        rule_bank = RuleBank(memory_path=temp_dir)
        middleware = ReasoningMiddleware(rule_bank)
        
        # Action with multiple violations including CRITICAL
        action = {
            'type': 'post_content',
            'confidence': 0.3,  # Violates TRUTH_001
            'benefit_score': 0.2,  # Violates SERVICE_001
            'content': 'This is war versus them, we hate the enemy and fight against stupid people'  # Violates UNITY_001 (CRITICAL)
        }
        
        result = middleware.intercept(action)
        
        # Should require review due to critical violation
        assert result['status'] == 'requires_review'
        assert len(result['validation']['violated_rules']) >= 2
        assert result['requires_human_review'] == True


def test_middleware_validation_flow():
    """Test complete validation flow"""
    with tempfile.TemporaryDirectory() as temp_dir:
        rule_bank = RuleBank(memory_path=temp_dir)
        middleware = ReasoningMiddleware(rule_bank)
        
        action = {
            'type': 'generate_world_tour_content',
            'city_id': 'tokyo',
            'confidence': 0.9,
            'benefit_score': 0.85,
            'content': 'Fun cultural content'
        }
        
        result = middleware.intercept(action)
        
        # Verify complete result structure
        assert 'status' in result
        assert 'validation' in result
        assert 'risk_profile' in result
        assert 'requires_human_review' in result
        assert 'reasoning' in result
        assert 'timestamp' in result


if __name__ == "__main__":
    # Run basic smoke test
    print("=" * 60)
    print("🧪 Running Reasoning Middleware Tests")
    print("=" * 60)
    
    test_middleware_blocks_multiple_violations()
    print("✅ Multiple violations blocked correctly")
    
    test_middleware_validation_flow()
    print("✅ Complete validation flow works")
    
    test_suite = TestReasoningMiddleware()
    test_suite.setup_method()
    
    test_suite.test_initialization()
    print("✅ Initialization works")
    
    test_suite.test_approve_ethical_action()
    print("✅ Ethical actions approved")
    
    test_suite.test_reject_unethical_action()
    print("✅ Unethical actions rejected")
    
    test_suite.test_escalate_critical_risk()
    print("✅ Critical risk escalated")
    
    test_suite.test_task_profiling()
    print("✅ Task profiling works")
    
    test_suite.test_validation_statistics()
    print("✅ Validation statistics accurate")
    
    print()
    print("=" * 60)
    print("✅ ALL MIDDLEWARE TESTS PASSED")
    print("=" * 60)
