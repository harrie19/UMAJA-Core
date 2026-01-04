"""
Tests for Unity Manifold Physics implementation.

Validates geometric projection and principle alignment.
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import numpy as np
from src.ethics.unity_manifold_physics import UnityManifoldPhysics
from src.rule_bank import RuleBank


class TestUnityManifoldPhysics:
    """Test suite for Unity Manifold Physics."""
    
    def test_principle_vectors_initialized(self):
        """Test that all 5 Bahá'í principles have vector representations."""
        manifold = UnityManifoldPhysics()
        
        assert 'truth' in manifold.principles
        assert 'unity' in manifold.principles
        assert 'service' in manifold.principles
        assert 'justice' in manifold.principles
        assert 'moderation' in manifold.principles
        
        # Each principle should have a non-zero vector
        for principle_name, principle_vector in manifold.principles.items():
            assert principle_vector is not None
            assert len(principle_vector) > 0
            assert np.linalg.norm(principle_vector) > 0
        
        print("✅ All principles initialized with vectors")
    
    def test_centroid_calculation(self):
        """Test that Unity Manifold centroid is geometric center."""
        manifold = UnityManifoldPhysics()
        
        # Centroid should be average of all principle vectors
        manual_centroid = np.mean(
            list(manifold.principles.values()),
            axis=0
        )
        
        # Normalize (as done in calculate_centroid)
        norm = np.linalg.norm(manual_centroid)
        if norm > 0:
            manual_centroid = manual_centroid / norm
        
        np.testing.assert_array_almost_equal(
            manifold.unity_centroid,
            manual_centroid,
            decimal=5
        )
        
        print("✅ Centroid calculation correct")
    
    def test_aligned_vector_passes(self):
        """Test that vector close to centroid passes validation."""
        manifold = UnityManifoldPhysics()
        
        # Create vector very close to centroid (small random noise)
        aligned_vector = manifold.unity_centroid + np.random.normal(0, 0.01, manifold.unity_centroid.shape)
        
        result = manifold.project_onto_unity_manifold(aligned_vector)
        
        assert result['allowed'] == True
        assert result['distance_from_unity'] < manifold.energy_threshold
        assert result['alignment_score'] > 0.85
        
        print(f"✅ Aligned vector passes (distance={result['distance_from_unity']:.4f})")
    
    def test_violated_vector_gets_projected(self):
        """Test that vector far from centroid gets corrected."""
        manifold = UnityManifoldPhysics()
        
        # Create vector far from centroid (opposite direction)
        violated_vector = -2 * manifold.unity_centroid
        
        result = manifold.project_onto_unity_manifold(violated_vector)
        
        assert result['allowed'] == False
        assert result['distance_from_unity'] > manifold.energy_threshold
        assert 'corrected_output' in result
        assert len(result['violated_principles']) > 0
        
        # Corrected output should be closer to centroid
        corrected_distance = manifold.cosine_distance(
            result['corrected_output'],
            manifold.unity_centroid
        )
        assert corrected_distance < result['distance_from_unity']
        
        print(f"✅ Violated vector projected (distance={result['distance_from_unity']:.4f})")
    
    def test_principle_scoring(self):
        """Test individual principle alignment scoring."""
        manifold = UnityManifoldPhysics()
        
        # Use truth principle vector directly
        truth_vector = manifold.principles['truth']
        
        scores = manifold.score_per_principle(truth_vector)
        
        # Should score high on truth
        assert scores['truth'] > 0.9
        
        # Should score reasonably on others (all principles related)
        assert all(score >= 0 for score in scores.values())
        
        print(f"✅ Principle scoring works: {scores}")
    
    def test_violation_identification(self):
        """Test that specific principle violations are correctly identified."""
        manifold = UnityManifoldPhysics()
        
        # Create vector opposite to 'truth' principle
        anti_truth_vector = -manifold.principles['truth']
        
        distance = manifold.cosine_distance(anti_truth_vector, manifold.unity_centroid)
        violations = manifold.identify_violations(anti_truth_vector, distance)
        
        # Should identify truth violation
        violation_principles = [v['principle'] for v in violations]
        assert 'truth' in violation_principles
        
        # Check severity classification
        for violation in violations:
            assert violation['severity'] in ['HIGH', 'MEDIUM']
            # Similarity can be negative (opposite direction)
            assert -1 <= violation['similarity'] <= 1
        
        print(f"✅ Violation identification works: {violations}")
    
    def test_cosine_similarity(self):
        """Test cosine similarity calculation."""
        manifold = UnityManifoldPhysics()
        
        # Test with identical vectors
        v1 = np.array([1, 2, 3])
        similarity_same = manifold.cosine_similarity(v1, v1)
        assert abs(similarity_same - 1.0) < 0.001
        
        # Test with opposite vectors
        v2 = -v1
        similarity_opposite = manifold.cosine_similarity(v1, v2)
        assert abs(similarity_opposite - (-1.0)) < 0.001
        
        # Test with orthogonal vectors
        v3 = np.array([1, 0, 0])
        v4 = np.array([0, 1, 0])
        similarity_orthogonal = manifold.cosine_similarity(v3, v4)
        assert abs(similarity_orthogonal - 0.0) < 0.001
        
        print("✅ Cosine similarity calculation correct")
    
    def test_projection_mechanism(self):
        """Test vector projection mechanism."""
        manifold = UnityManifoldPhysics()
        
        v = np.array([1, 0, 0, 0])
        target = np.array([0, 1, 0, 0])
        
        # Full projection (strength=1.0)
        projected_full = manifold.project_vector(v, target, strength=1.0)
        np.testing.assert_array_almost_equal(projected_full, target)
        
        # No projection (strength=0.0)
        projected_none = manifold.project_vector(v, target, strength=0.0)
        np.testing.assert_array_almost_equal(projected_none, v)
        
        # Partial projection (strength=0.5)
        projected_half = manifold.project_vector(v, target, strength=0.5)
        expected_half = 0.5 * v + 0.5 * target
        np.testing.assert_array_almost_equal(projected_half, expected_half)
        
        print("✅ Projection mechanism works correctly")
    
    def test_integration_with_rule_bank(self):
        """Test that Unity Manifold integrates with Rule Bank."""
        # Create temporary test directory
        import tempfile
        import shutil
        
        test_dir = tempfile.mkdtemp()
        
        try:
            rule_bank = RuleBank(memory_path=test_dir)
            
            # Rule Bank should have unity_manifold attribute
            assert hasattr(rule_bank, 'unity_manifold')
            assert isinstance(rule_bank.unity_manifold, UnityManifoldPhysics)
            
            # Test validation with aligned content
            action_good = {
                'type': 'response',
                'content': 'I want to help everyone learn and grow together in unity'
            }
            result_good = rule_bank.validate_action(action_good)
            assert result_good['allowed'] == True
            
            # Test get_principle_scores
            scores = rule_bank.get_principle_scores('helping humanity with honesty and fairness')
            assert 'truth' in scores
            assert 'unity' in scores
            assert 'service' in scores
            assert 'justice' in scores
            assert 'moderation' in scores
            
            print("✅ Integration with Rule Bank successful")
        
        finally:
            # Clean up
            shutil.rmtree(test_dir)


def test_information_transduction():
    """Test information transduction module."""
    from src.information_theory.transduction import InformationTransduction
    
    transduction = InformationTransduction()
    
    # Test embedding
    text = "truth unity service"
    vector = transduction.embed(text)
    assert vector is not None
    assert len(vector) == transduction.embedding_dim
    
    # Test information content
    bits = transduction.calculate_information_content(vector)
    assert bits > 0
    
    # Test Landauer energy
    energy = transduction.landauer_energy(bits)
    assert energy > 0
    assert energy < 1e-18  # Should be very small
    
    # Test efficiency ratio
    actual_energy = 1e-6  # 1 microjoule
    ratio = transduction.efficiency_ratio(actual_energy, bits)
    assert ratio > 0
    
    print("✅ Information transduction works correctly")


if __name__ == "__main__":
    print("=" * 70)
    print("🌌 Unity Manifold Physics - Unit Tests")
    print("=" * 70)
    print()
    
    # Run tests
    test_suite = TestUnityManifoldPhysics()
    
    tests = [
        ("Principle Vectors Initialized", test_suite.test_principle_vectors_initialized),
        ("Centroid Calculation", test_suite.test_centroid_calculation),
        ("Aligned Vector Passes", test_suite.test_aligned_vector_passes),
        ("Violated Vector Gets Projected", test_suite.test_violated_vector_gets_projected),
        ("Principle Scoring", test_suite.test_principle_scoring),
        ("Violation Identification", test_suite.test_violation_identification),
        ("Cosine Similarity", test_suite.test_cosine_similarity),
        ("Projection Mechanism", test_suite.test_projection_mechanism),
        ("Integration with Rule Bank", test_suite.test_integration_with_rule_bank),
        ("Information Transduction", test_information_transduction),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            print(f"Running: {name}...")
            test_func()
            passed += 1
            print()
        except Exception as e:
            print(f"❌ FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
            print()
    
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    if failed == 0:
        print("✨ All tests passed!")
        exit(0)
    else:
        print(f"⚠️  {failed} test(s) failed")
        exit(1)
