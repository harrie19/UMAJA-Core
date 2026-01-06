"""
Tests for EthicalValueEncoder - Ethical value embeddings for AI alignment
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "umaja_core/protocols/ethics"))

from value_embeddings import EthicalValueEncoder


class TestEthicalValueEncoder:
    """Test suite for EthicalValueEncoder"""
    
    @pytest.fixture
    def encoder(self):
        """Create encoder instance for tests"""
        return EthicalValueEncoder()
    
    def test_initialization(self, encoder):
        """Test encoder initialization"""
        assert encoder is not None
        assert encoder.model is not None
        assert len(encoder.UNIVERSAL_PRINCIPLES) == 10
        assert len(encoder.BAHAI_PRINCIPLES) == 9
    
    def test_bahai_principles_exist(self, encoder):
        """Test that Bahá'í principles are defined"""
        assert 'BAHAI_PRINCIPLES' in dir(encoder.__class__)
        
        bahai_principles = encoder.BAHAI_PRINCIPLES
        assert len(bahai_principles) == 9
        
        # Check for specific principles
        assert "unity of humanity" in bahai_principles
        assert "independent investigation of truth" in bahai_principles
        assert "equality of women and men" in bahai_principles
    
    def test_cultural_contexts(self, encoder):
        """Test cultural contexts are properly defined"""
        contexts = encoder.CULTURAL_CONTEXTS
        
        assert 'universal' in contexts
        assert 'utilitarian' in contexts
        assert 'deontological' in contexts
        assert 'virtue' in contexts
        assert 'bahai' in contexts
        
        # Verify Bahá'í context
        bahai_context = contexts['bahai']
        assert bahai_context['description'] == "Bahá'í ethical principles"
        assert bahai_context['principles'] == encoder.BAHAI_PRINCIPLES
    
    def test_encode_value_universal(self, encoder):
        """Test encoding universal principle"""
        principle = "fairness and justice"
        embedding = encoder.encode_value(principle, culture='universal')
        
        assert isinstance(embedding, np.ndarray)
        assert len(embedding) == 768  # all-mpnet-base-v2 dimension
        assert embedding.dtype == np.float32
    
    def test_encode_value_bahai(self, encoder):
        """Test encoding Bahá'í principle"""
        principle = "unity of humanity"
        embedding = encoder.encode_value(principle, culture='bahai')
        
        assert isinstance(embedding, np.ndarray)
        assert len(embedding) == 768
    
    def test_encode_value_caching(self, encoder):
        """Test that encoding results are cached"""
        principle = "compassion and kindness"
        
        # First call
        embedding1 = encoder.encode_value(principle)
        
        # Second call should use cache
        embedding2 = encoder.encode_value(principle)
        
        # Should be identical (same object)
        np.testing.assert_array_equal(embedding1, embedding2)
    
    def test_compute_alignment_score(self, encoder):
        """Test alignment score calculation"""
        action = encoder.encode_action("helping someone in need")
        value = encoder.encode_value("compassion and kindness")
        
        score = encoder.compute_alignment_score(action, value)
        
        assert isinstance(score, float)
        assert 0 <= score <= 1
        # Helping should align with compassion
        assert score > 0.5
    
    def test_encode_action(self, encoder):
        """Test encoding action descriptions"""
        action_description = "donating to charity"
        embedding = encoder.encode_action(action_description)
        
        assert isinstance(embedding, np.ndarray)
        assert len(embedding) == 768
        # Should be normalized
        assert 0.99 < np.linalg.norm(embedding) < 1.01
    
    def test_check_alignment(self, encoder):
        """Test alignment checking"""
        result = encoder.check_alignment(
            action_description="protecting the environment",
            principle="maximizing wellbeing",
            culture='universal',
            threshold=0.7
        )
        
        assert 'action' in result
        assert 'principle' in result
        assert 'culture' in result
        assert 'alignment_score' in result
        assert 'aligned' in result
        assert 'status' in result
        
        assert result['status'] in ['aligned', 'misaligned']
        assert isinstance(result['aligned'], bool)
        assert 0 <= result['alignment_score'] <= 1
    
    def test_check_alignment_with_bahai_principles(self, encoder):
        """Test alignment checking with Bahá'í principles"""
        result = encoder.check_alignment(
            action_description="promoting equality between all people",
            principle="equality of women and men",
            culture='bahai',
            threshold=0.75
        )
        
        assert result['culture'] == 'bahai'
        assert result['alignment_score'] > 0.75
        assert result['aligned'] is True
    
    def test_get_most_aligned_principle(self, encoder):
        """Test finding most aligned principle"""
        principle, score = encoder.get_most_aligned_principle(
            action_description="telling the truth even when difficult",
            culture='universal'
        )
        
        assert isinstance(principle, str)
        assert isinstance(score, float)
        assert 0 <= score <= 1
        # Should align with "honesty and truthfulness"
        assert "honest" in principle.lower() or "truth" in principle.lower()
    
    def test_get_most_aligned_principle_bahai(self, encoder):
        """Test finding most aligned Bahá'í principle"""
        principle, score = encoder.get_most_aligned_principle(
            action_description="seeking truth through personal investigation",
            culture='bahai'
        )
        
        assert principle in encoder.BAHAI_PRINCIPLES
        assert 0 <= score <= 1
    
    def test_compare_values(self, encoder):
        """Test comparing two ethical values"""
        similarity = encoder.compare_values(
            "fairness and justice",
            "equality and equity",
            culture1='universal',
            culture2='universal'
        )
        
        assert isinstance(similarity, float)
        assert 0 <= similarity <= 1
        # Similar concepts should have high similarity
        assert similarity > 0.5
    
    def test_rank_actions_by_value(self, encoder):
        """Test ranking actions by alignment with value"""
        actions = [
            "helping the poor",
            "ignoring people in need",
            "building community centers",
            "hoarding resources"
        ]
        
        rankings = encoder.rank_actions_by_value(
            actions=actions,
            target_value="compassion and kindness",
            culture='universal'
        )
        
        assert len(rankings) == len(actions)
        
        # Should be sorted by score (descending)
        for i in range(len(rankings) - 1):
            assert rankings[i][1] >= rankings[i + 1][1]
        
        # Helping should rank higher than ignoring
        helping_score = next(score for action, score in rankings if "helping" in action)
        ignoring_score = next(score for action, score in rankings if "ignoring" in action)
        assert helping_score > ignoring_score
    
    def test_get_value_profile(self, encoder):
        """Test getting value alignment profile"""
        profile = encoder.get_value_profile(
            action="promoting education for all children",
            culture='universal'
        )
        
        assert isinstance(profile, dict)
        assert len(profile) == len(encoder.UNIVERSAL_PRINCIPLES)
        
        # All scores should be in [0, 1]
        for principle, score in profile.items():
            assert 0 <= score <= 1
            assert principle in encoder.UNIVERSAL_PRINCIPLES
    
    def test_get_value_profile_bahai(self, encoder):
        """Test value profile with Bahá'í principles"""
        profile = encoder.get_value_profile(
            action="establishing universal education systems",
            culture='bahai'
        )
        
        assert isinstance(profile, dict)
        assert len(profile) == len(encoder.BAHAI_PRINCIPLES)
        
        # Should have high alignment with "universal education"
        assert "universal education" in profile
        assert profile["universal education"] > 0.5
    
    def test_detect_value_conflicts(self, encoder):
        """Test detecting value conflicts"""
        conflicts = encoder.detect_value_conflicts(
            action="lying to gain advantage",
            values=["honesty and truthfulness", "fairness and justice"],
            threshold=0.3
        )
        
        # Should detect conflicts with honesty
        assert len(conflicts) > 0
        assert "honesty and truthfulness" in conflicts
    
    def test_detect_no_conflicts(self, encoder):
        """Test when there are no value conflicts"""
        conflicts = encoder.detect_value_conflicts(
            action="helping others with compassion",
            values=["compassion and kindness", "maximizing wellbeing"],
            threshold=0.3
        )
        
        # Should detect no conflicts
        assert len(conflicts) == 0
    
    def test_optimize_for_values(self, encoder):
        """Test optimizing action selection for values"""
        actions = [
            encoder.encode_action("helping the community"),
            encoder.encode_action("ignoring problems"),
            encoder.encode_action("promoting cooperation")
        ]
        
        target_values = [
            encoder.encode_value("promoting cooperation"),
            encoder.encode_value("compassion and kindness")
        ]
        
        best_action = encoder.optimize_for_values(actions, target_values)
        
        assert isinstance(best_action, np.ndarray)
        assert len(best_action) == 768
    
    def test_optimize_for_values_weighted(self, encoder):
        """Test optimization with weighted values"""
        actions = [
            encoder.encode_action("maximizing profit"),
            encoder.encode_action("helping people in need")
        ]
        
        target_values = [
            encoder.encode_value("compassion and kindness"),
            encoder.encode_value("maximizing wellbeing")
        ]
        
        # Give more weight to compassion
        weights = [0.8, 0.2]
        
        best_action = encoder.optimize_for_values(actions, target_values, weights)
        
        # Should select the helping action
        similarity_helping = np.dot(best_action, actions[1])
        similarity_profit = np.dot(best_action, actions[0])
        
        assert similarity_helping > similarity_profit
    
    def test_cross_cultural_comparison(self, encoder):
        """Test comparing values across cultures"""
        similarity = encoder.compare_values(
            value1="compassion and kindness",
            value2="unity of humanity",
            culture1='universal',
            culture2='bahai'
        )
        
        assert 0 <= similarity <= 1
        # Related concepts should have reasonable similarity
        assert similarity > 0.3
    
    def test_alignment_score_range(self, encoder):
        """Test that alignment scores are always in valid range"""
        # Test with very different concepts
        action = encoder.encode_action("destroying the environment")
        value = encoder.encode_value("protecting nature")
        
        score = encoder.compute_alignment_score(action, value)
        
        # Should still be in [0, 1]
        assert 0 <= score <= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
