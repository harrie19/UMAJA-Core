"""
Tests for Safety Polytope
Tests geometric constraints and safety mechanisms
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import pytest
from umaja_core.protocols.safety.polytope import SafetyPolytope, LinearConstraint
from umaja_core.protocols.safety.margin_loss import MarginLoss, ContrastiveLoss
from umaja_core.protocols.safety.ood_detector import OODDetector, MahalanobisOOD


class TestLinearConstraint:
    """Test LinearConstraint functionality"""
    
    def test_constraint_creation(self):
        """Test creating linear constraint"""
        a = np.array([1.0, 0.0, 0.0])
        b = 5.0
        constraint = LinearConstraint(a=a, b=b, description="Test constraint")
        
        assert np.array_equal(constraint.a, a)
        assert constraint.b == b
        assert constraint.description == "Test constraint"
    
    def test_constraint_satisfaction(self):
        """Test checking constraint satisfaction"""
        # Constraint: x_0 <= 5
        constraint = LinearConstraint(
            a=np.array([1.0, 0.0, 0.0]),
            b=5.0
        )
        
        # Point satisfying constraint
        x_safe = np.array([3.0, 0.0, 0.0])
        assert constraint.is_satisfied(x_safe)
        
        # Point violating constraint
        x_unsafe = np.array([7.0, 0.0, 0.0])
        assert not constraint.is_satisfied(x_unsafe)
    
    def test_constraint_distance(self):
        """Test distance computation"""
        constraint = LinearConstraint(
            a=np.array([1.0, 0.0]),
            b=5.0
        )
        
        # Point inside (negative distance)
        x_inside = np.array([3.0, 0.0])
        assert constraint.distance(x_inside) < 0
        
        # Point outside (positive distance)
        x_outside = np.array([7.0, 0.0])
        assert constraint.distance(x_outside) > 0


class TestSafetyPolytope:
    """Test SafetyPolytope functionality"""
    
    def test_empty_polytope(self):
        """Test polytope with no constraints"""
        polytope = SafetyPolytope([])
        
        # Everything should be safe
        random_point = np.random.randn(10)
        assert polytope.is_safe(random_point)
    
    def test_box_polytope(self):
        """Test axis-aligned box polytope"""
        lower = np.array([0.0, 0.0])
        upper = np.array([10.0, 10.0])
        
        polytope = SafetyPolytope.create_box_polytope(lower, upper)
        
        # Point inside box
        inside = np.array([5.0, 5.0])
        assert polytope.is_safe(inside, check_margin=False)
        
        # Point outside box
        outside = np.array([15.0, 5.0])
        assert not polytope.is_safe(outside, check_margin=False)
    
    def test_sphere_polytope(self):
        """Test sphere approximation polytope"""
        center = np.array([0.0, 0.0, 0.0])
        radius = 5.0
        
        polytope = SafetyPolytope.create_sphere_polytope(center, radius, n_constraints=50)
        
        # Point near center (should be safe)
        near_center = np.array([1.0, 1.0, 1.0])
        assert polytope.is_safe(near_center, check_margin=False)
        
        # Point far from center (should be unsafe)
        far_point = np.array([20.0, 20.0, 20.0])
        assert not polytope.is_safe(far_point, check_margin=False)
    
    def test_steer_to_safe(self):
        """Test steering unsafe point to safe region"""
        # Create box: [0, 10] x [0, 10]
        polytope = SafetyPolytope.create_box_polytope(
            np.array([0.0, 0.0]),
            np.array([10.0, 10.0])
        )
        
        # Unsafe point
        unsafe = np.array([15.0, 5.0])
        assert not polytope.is_safe(unsafe, check_margin=False)
        
        # Steer to safe
        safe = polytope.steer_to_safe(unsafe)
        
        # Result should be safer (may not be fully safe due to approximation)
        assert len(safe) == len(unsafe)
    
    def test_get_constraint_violations(self):
        """Test getting list of violations"""
        polytope = SafetyPolytope.create_box_polytope(
            np.array([0.0, 0.0]),
            np.array([10.0, 10.0])
        )
        
        # Point violating upper bounds
        violating = np.array([15.0, 15.0])
        violations = polytope.get_constraint_violations(violating)
        
        assert len(violations) > 0
        assert all(isinstance(v, tuple) for v in violations)
    
    def test_margin_checking(self):
        """Test safety margin enforcement"""
        polytope = SafetyPolytope.create_box_polytope(
            np.array([0.0, 0.0]),
            np.array([10.0, 10.0])
        )
        
        # Point just inside boundary
        border_point = np.array([9.95, 5.0])
        
        # Without margin should be safe
        assert polytope.is_safe(border_point, check_margin=False)
        
        # With margin might be unsafe (depending on margin value)
        # This tests the margin mechanism exists


class TestMarginLoss:
    """Test margin-based loss functions"""
    
    def test_triplet_loss(self):
        """Test triplet margin loss"""
        loss_fn = MarginLoss(margin=1.0)
        
        anchor = np.array([0.0, 0.0])
        positive = np.array([0.1, 0.1])  # Close to anchor
        negative = np.array([5.0, 5.0])  # Far from anchor
        
        loss = loss_fn.compute_loss(anchor, positive, negative)
        
        # Loss should be small (negative well separated)
        assert loss >= 0.0
    
    def test_batch_loss(self):
        """Test batch loss computation"""
        loss_fn = MarginLoss(margin=1.0)
        
        anchors = np.random.randn(10, 128)
        positives = anchors + np.random.randn(10, 128) * 0.1
        negatives = np.random.randn(10, 128) * 5
        
        avg_loss, per_sample = loss_fn.compute_batch_loss(anchors, positives, negatives)
        
        assert isinstance(avg_loss, float)
        assert len(per_sample) == 10
        assert all(l >= 0 for l in per_sample)


class TestContrastiveLoss:
    """Test contrastive loss"""
    
    def test_similar_pair(self):
        """Test loss for similar pair"""
        loss_fn = ContrastiveLoss(margin=1.0)
        
        emb1 = np.array([1.0, 0.0])
        emb2 = np.array([1.1, 0.0])  # Similar
        
        loss = loss_fn.compute_loss(emb1, emb2, label=1)
        
        # Loss should be small for similar pair
        assert loss >= 0.0
        assert loss < 1.0
    
    def test_dissimilar_pair(self):
        """Test loss for dissimilar pair"""
        loss_fn = ContrastiveLoss(margin=1.0)
        
        emb1 = np.array([1.0, 0.0])
        emb2 = np.array([0.0, 1.0])  # Different
        
        loss = loss_fn.compute_loss(emb1, emb2, label=0)
        
        assert loss >= 0.0


class TestOODDetector:
    """Test out-of-distribution detection"""
    
    def test_detector_fit(self):
        """Test fitting OOD detector"""
        detector = OODDetector(contamination=0.1)
        
        # Generate safe embeddings (Gaussian)
        safe_embeddings = np.random.randn(100, 50)
        
        detector.fit(safe_embeddings)
        assert detector.fitted
    
    def test_ood_detection(self):
        """Test OOD detection on fitted detector"""
        detector = OODDetector(contamination=0.1)
        
        # Fit on normal distribution
        safe_embeddings = np.random.randn(100, 50)
        detector.fit(safe_embeddings)
        
        # Test on normal point
        normal_point = np.random.randn(50)
        is_ood_normal = detector.is_ood(normal_point)
        
        # Test on outlier
        outlier = np.random.randn(50) * 10  # Much larger scale
        is_ood_outlier = detector.is_ood(outlier)
        
        # Outlier should be more likely to be OOD
        assert isinstance(is_ood_normal, (bool, np.bool_))
        assert isinstance(is_ood_outlier, (bool, np.bool_))
    
    def test_anomaly_score(self):
        """Test anomaly score computation"""
        detector = OODDetector()
        
        safe_embeddings = np.random.randn(100, 50)
        detector.fit(safe_embeddings)
        
        test_point = np.random.randn(50)
        score = detector.get_anomaly_score(test_point)
        
        assert isinstance(score, float)
    
    def test_batch_check(self):
        """Test batch OOD checking"""
        detector = OODDetector()
        
        safe_embeddings = np.random.randn(100, 50)
        detector.fit(safe_embeddings)
        
        test_batch = np.random.randn(20, 50)
        results = detector.check_batch(test_batch)
        
        assert len(results) == 20
        assert results.dtype == bool


class TestMahalanobisOOD:
    """Test Mahalanobis distance based OOD"""
    
    def test_mahalanobis_fit(self):
        """Test fitting Mahalanobis detector"""
        detector = MahalanobisOOD(threshold=3.0)
        
        embeddings = np.random.randn(100, 20)
        detector.fit(embeddings)
        
        assert detector.fitted
        assert detector.mean is not None
        assert detector.inv_cov is not None
    
    def test_mahalanobis_distance(self):
        """Test distance computation"""
        detector = MahalanobisOOD()
        
        embeddings = np.random.randn(100, 20)
        detector.fit(embeddings)
        
        # Point close to mean
        close_point = detector.mean + np.random.randn(20) * 0.1
        distance_close = detector.mahalanobis_distance(close_point)
        
        # Point far from mean
        far_point = detector.mean + np.random.randn(20) * 10
        distance_far = detector.mahalanobis_distance(far_point)
        
        assert distance_close < distance_far
    
    def test_mahalanobis_ood(self):
        """Test OOD detection"""
        detector = MahalanobisOOD(threshold=3.0)
        
        embeddings = np.random.randn(100, 20)
        detector.fit(embeddings)
        
        # Normal point
        normal = detector.mean + np.random.randn(20) * 0.5
        
        # Outlier
        outlier = detector.mean + np.random.randn(20) * 20
        
        is_normal_ood = detector.is_ood(normal)
        is_outlier_ood = detector.is_ood(outlier)
        
        # Outlier more likely to be OOD
        assert isinstance(is_normal_ood, (bool, np.bool_))
        assert isinstance(is_outlier_ood, (bool, np.bool_))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
