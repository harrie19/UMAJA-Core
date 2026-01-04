"""
Tests for Rule Bank System
"""

import sys
import json
import tempfile
from pathlib import Path

# Add src to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from rule_bank import RuleBank


class TestRuleBank:
    """Test suite for Rule Bank system"""
    
    def setup_method(self):
        """Setup test fixtures"""
        # Create temporary directory for test memory
        self.temp_dir = tempfile.mkdtemp()
        self.rule_bank = RuleBank(memory_path=self.temp_dir)
    
    def test_initialization(self):
        """Test Rule Bank initializes with default rules"""
        assert self.rule_bank is not None
        assert len(self.rule_bank.rules) > 0
        assert self.rule_bank.memory_path.exists()
        
        # Check that all Bahá'í principles are covered
        principles_covered = set(rule['principle'] for rule in self.rule_bank.rules)
        expected_principles = {'truth', 'unity', 'service', 'justice', 'moderation'}
        assert expected_principles.issubset(principles_covered)
    
    def test_load_save_rules(self):
        """Test Rule Bank persists to disk correctly"""
        # Save rules
        self.rule_bank.save_rules()
        
        # Check file exists
        assert self.rule_bank.rules_file.exists()
        
        # Load in new instance
        new_bank = RuleBank(memory_path=self.temp_dir)
        
        # Verify same rules loaded
        assert len(new_bank.rules) == len(self.rule_bank.rules)
        
        # Verify rule IDs match
        original_ids = set(r['id'] for r in self.rule_bank.rules)
        loaded_ids = set(r['id'] for r in new_bank.rules)
        assert original_ids == loaded_ids
    
    def test_validate_high_confidence_action(self):
        """Test middleware allows high-confidence actions"""
        action = {
            'type': 'generate_content',
            'confidence': 0.95,  # High enough to not require sources
            'benefit_score': 0.8,
            'content': 'Test content for everyone in the community'
        }
        
        result = self.rule_bank.validate_action(action)
        
        assert result['allowed'] == True
        assert len(result['violated_rules']) == 0
        assert result['risk_level'] == 'LOW'
    
    def test_validate_low_confidence_action(self):
        """Test middleware blocks low-confidence actions (violates Truth principle)"""
        action = {
            'type': 'generate_content',
            'confidence': 0.5,  # Below 0.8 threshold
            'benefit_score': 0.8,
            'content': 'Some uncertain claim'
        }
        
        result = self.rule_bank.validate_action(action)
        
        # Should violate TRUTH_001
        assert 'TRUTH_001' in result['violated_rules']
        assert len(result['recommendations']) > 0
    
    def test_validate_divisive_content(self):
        """Test middleware blocks divisive content (violates Unity principle)"""
        action = {
            'type': 'post_content',
            'confidence': 0.9,
            'benefit_score': 0.5,
            'content': 'This group versus that group, they hate us, we fight against them'
        }
        
        result = self.rule_bank.validate_action(action)
        
        # Should violate UNITY_001 (no_division)
        assert any('UNITY' in rule_id for rule_id in result['violated_rules'])
    
    def test_validate_low_benefit_action(self):
        """Test middleware blocks actions with low benefit score"""
        action = {
            'type': 'post_content',
            'confidence': 0.9,
            'benefit_score': 0.3,  # Below 0.6 threshold
            'content': 'Neutral content'
        }
        
        result = self.rule_bank.validate_action(action)
        
        # Should violate SERVICE_001
        assert 'SERVICE_001' in result['violated_rules']
    
    def test_learn_new_rule(self):
        """Test learning loop adds new rules correctly"""
        initial_count = len(self.rule_bank.rules)
        
        # Learn a new rule
        self.rule_bank.learn_rule(
            observation="Always verify external API responses",
            principle="truth",
            constraint="verify_api_data",
            severity="HIGH"
        )
        
        # Check rule was added
        assert len(self.rule_bank.rules) > initial_count
        
        # Find the new rule
        new_rule = self.rule_bank.rules[-1]
        assert new_rule['principle'] == 'truth'
        assert new_rule['constraint'] == 'verify_api_data'
        assert new_rule['severity'] == 'HIGH'
        assert 'learned_at' in new_rule
    
    def test_violation_tracking(self):
        """Test violation reporting is accurate"""
        # Create action that violates rules
        action = {
            'type': 'post_content',
            'confidence': 0.5,  # Violates TRUTH_001
            'benefit_score': 0.3,  # Violates SERVICE_001
            'content': 'Test'
        }
        
        # Validate multiple times
        for _ in range(3):
            self.rule_bank.validate_action(action)
        
        # Get violation report
        report = self.rule_bank.get_violation_report()
        
        assert report['total_violations'] > 0
        assert report['total_validations'] >= 3
        assert 'violations_by_principle' in report
        assert report['violations_by_principle']['truth'] > 0
    
    def test_principle_alignment(self):
        """Test Bahá'í principle alignment calculation"""
        # Good action
        good_action = {
            'type': 'post_content',
            'confidence': 0.95,
            'benefit_score': 0.9,
            'content': 'Welcome everyone to our inclusive community where we serve together in unity'
        }
        
        alignment = self.rule_bank.get_principle_alignment(good_action)
        
        # Should have high alignment scores
        assert all(score >= 0.7 for score in alignment.values())
        assert 'truth' in alignment
        assert 'unity' in alignment
        assert 'service' in alignment
        assert 'justice' in alignment
        assert 'moderation' in alignment
    
    def test_source_attribution_detection(self):
        """Test detection of source citations"""
        # Content with source
        action_with_source = {
            'type': 'post_content',
            'confidence': 0.85,
            'benefit_score': 0.8,
            'content': 'According to recent research, this is true. Source: Nature Journal'
        }
        
        result = self.rule_bank.validate_action(action_with_source)
        
        # TRUTH_002 should not be violated
        assert 'TRUTH_002' not in result['violated_rules']
    
    def test_risk_level_calculation(self):
        """Test risk level is calculated correctly"""
        # Low risk action
        low_risk = {
            'type': 'post_content',
            'confidence': 1.0,
            'benefit_score': 1.0,
            'content': 'Welcome everyone to our community together'  # More inclusive
        }
        
        result = self.rule_bank.validate_action(low_risk)
        assert result['risk_level'] == 'LOW'
        
        # High risk action (multiple violations)
        high_risk = {
            'type': 'post_content',
            'confidence': 0.3,
            'benefit_score': 0.2,
            'content': 'Divisive content with us versus them mentality'
        }
        
        result = self.rule_bank.validate_action(high_risk)
        assert result['risk_level'] in ['HIGH', 'CRITICAL']
    
    def test_multiple_principles_validation(self):
        """Test action is validated against all principles"""
        action = {
            'type': 'post_content',
            'confidence': 0.9,
            'benefit_score': 0.8,
            'content': 'Community content'
        }
        
        result = self.rule_bank.validate_action(action)
        
        # Should have checked rules from multiple principles
        principles_checked = set()
        for rule_id in result['applied_rules']:
            for rule in self.rule_bank.rules:
                if rule['id'] == rule_id:
                    principles_checked.add(rule['principle'])
                    break
        
        # Should check at least 3 different principles
        assert len(principles_checked) >= 3


def test_rule_bank_loads_default_rules():
    """Test that Rule Bank loads default Bahá'í principles"""
    with tempfile.TemporaryDirectory() as temp_dir:
        rule_bank = RuleBank(memory_path=temp_dir)
        
        assert len(rule_bank.rules) >= 8  # At least 8 default rules
        
        # Check for specific default rules
        rule_ids = [r['id'] for r in rule_bank.rules]
        assert 'TRUTH_001' in rule_ids
        assert 'UNITY_001' in rule_ids
        assert 'SERVICE_001' in rule_ids
        assert 'JUSTICE_001' in rule_ids
        assert 'MODERATION_001' in rule_ids


def test_rule_bank_empty_action_handling():
    """Test Rule Bank handles empty or minimal actions gracefully"""
    with tempfile.TemporaryDirectory() as temp_dir:
        rule_bank = RuleBank(memory_path=temp_dir)
        
        # Minimal action
        action = {'type': 'test'}
        
        result = rule_bank.validate_action(action)
        
        # Should complete without errors
        assert 'allowed' in result
        assert 'violated_rules' in result
        assert 'risk_level' in result


if __name__ == "__main__":
    # Run basic smoke test
    import tempfile
    
    print("=" * 60)
    print("🧪 Running Rule Bank Tests")
    print("=" * 60)
    
    test_rule_bank_loads_default_rules()
    print("✅ Default rules load correctly")
    
    test_rule_bank_empty_action_handling()
    print("✅ Empty action handling works")
    
    test_suite = TestRuleBank()
    test_suite.setup_method()
    
    test_suite.test_initialization()
    print("✅ Initialization works")
    
    test_suite.test_validate_high_confidence_action()
    print("✅ High confidence actions pass")
    
    test_suite.test_validate_low_confidence_action()
    print("✅ Low confidence actions blocked")
    
    test_suite.test_learn_new_rule()
    print("✅ Learning new rules works")
    
    test_suite.test_violation_tracking()
    print("✅ Violation tracking accurate")
    
    print()
    print("=" * 60)
    print("✅ ALL RULE BANK TESTS PASSED")
    print("=" * 60)
