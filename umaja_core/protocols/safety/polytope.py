"""
Safety Polytope
Geometric safety constraints in embedding space using convex polytopes
"""

import numpy as np
from typing import List, Optional, Tuple
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class LinearConstraint:
    """
    Linear constraint: a^T x <= b
    Defines a half-space in the embedding space
    """
    a: np.ndarray  # Normal vector
    b: float       # Offset
    description: str = ""
    
    def is_satisfied(self, x: np.ndarray) -> bool:
        """Check if point x satisfies this constraint"""
        return np.dot(self.a, x) <= self.b
    
    def distance(self, x: np.ndarray) -> float:
        """Signed distance to constraint boundary (negative = inside)"""
        return np.dot(self.a, x) - self.b


class SafetyPolytope:
    """
    Convex polytope defining safe region in embedding space
    
    A polytope is defined by a set of linear inequalities:
    A x <= b
    
    where each row of A and element of b defines a half-space.
    The safe region is the intersection of all half-spaces.
    """
    
    def __init__(
        self, 
        constraints: List[LinearConstraint],
        margin: float = 0.1
    ):
        """
        Initialize safety polytope
        
        Args:
            constraints: List of linear constraints defining safe region
            margin: Safety margin for constraint checking
        """
        self.constraints = constraints
        self.margin = margin
        
        if not constraints:
            logger.warning("SafetyPolytope initialized with no constraints")
        
        logger.info(f"SafetyPolytope initialized with {len(constraints)} constraints")
    
    def is_safe(self, vector: np.ndarray, check_margin: bool = True) -> bool:
        """
        Check if vector lies within safe region
        
        Args:
            vector: Embedding vector to check
            check_margin: If True, enforce safety margin
            
        Returns:
            True if vector is safe
        """
        if not self.constraints:
            # No constraints = everything is safe
            return True
        
        for constraint in self.constraints:
            distance = constraint.distance(vector)
            threshold = self.margin if check_margin else 0.0
            
            if distance > threshold:
                logger.debug(
                    f"Constraint violated: {constraint.description}, "
                    f"distance={distance:.4f}"
                )
                return False
        
        return True
    
    def steer_to_safe(
        self, 
        vector: np.ndarray,
        max_iterations: int = 100,
        step_size: float = 0.1
    ) -> np.ndarray:
        """
        Project unsafe vector to nearest safe point
        
        Uses gradient descent to find nearest point in safe region.
        
        Args:
            vector: Unsafe vector to correct
            max_iterations: Maximum optimization steps
            step_size: Gradient descent step size
            
        Returns:
            Corrected safe vector
        """
        if self.is_safe(vector, check_margin=False):
            return vector
        
        x = vector.copy()
        
        for iteration in range(max_iterations):
            # Find most violated constraint
            max_violation = 0
            worst_constraint = None
            
            for constraint in self.constraints:
                distance = constraint.distance(x)
                if distance > max_violation:
                    max_violation = distance
                    worst_constraint = constraint
            
            if max_violation <= 0:
                # All constraints satisfied
                break
            
            # Move toward constraint boundary
            # Gradient of distance is the normal vector a
            gradient = worst_constraint.a
            x = x - step_size * gradient
            
            # Normalize to maintain vector norm
            x = x / (np.linalg.norm(x) + 1e-8)
        
        if not self.is_safe(x, check_margin=False):
            logger.warning(
                f"Could not find safe point after {max_iterations} iterations"
            )
        
        return x
    
    def get_constraint_violations(
        self, 
        vector: np.ndarray
    ) -> List[Tuple[LinearConstraint, float]]:
        """
        Get all constraint violations for a vector
        
        Args:
            vector: Vector to check
            
        Returns:
            List of (constraint, violation_amount) tuples
        """
        violations = []
        
        for constraint in self.constraints:
            distance = constraint.distance(vector)
            if distance > 0:
                violations.append((constraint, distance))
        
        return violations
    
    def visualize_boundary(
        self, 
        method: str = 'pca',
        n_samples: int = 1000
    ) -> dict:
        """
        Visualize polytope boundary in 2D using dimensionality reduction
        
        Args:
            method: Reduction method ('pca' or 'tsne')
            n_samples: Number of boundary samples to generate
            
        Returns:
            Dictionary with visualization data
        """
        if not self.constraints:
            return {'error': 'No constraints to visualize'}
        
        # Get dimension from first constraint
        dim = len(self.constraints[0].a)
        
        # Sample random points
        samples = np.random.randn(n_samples, dim)
        
        # Check which are safe
        safe_mask = np.array([self.is_safe(s, check_margin=False) for s in samples])
        
        # Reduce dimensionality
        if method == 'pca':
            from sklearn.decomposition import PCA
            reducer = PCA(n_components=2)
        else:
            raise ValueError(f"Unknown visualization method: {method}")
        
        reduced = reducer.fit_transform(samples)
        
        return {
            'points': reduced.tolist(),
            'safe': safe_mask.tolist(),
            'method': method,
            'n_constraints': len(self.constraints)
        }
    
    @staticmethod
    def create_sphere_polytope(
        center: np.ndarray,
        radius: float,
        n_constraints: int = 20
    ) -> 'SafetyPolytope':
        """
        Create polytope approximating a sphere
        
        Args:
            center: Center point of sphere
            radius: Radius of sphere
            n_constraints: Number of half-spaces to use
            
        Returns:
            SafetyPolytope approximating sphere
        """
        dim = len(center)
        constraints = []
        
        # Sample random directions and create constraints
        for i in range(n_constraints):
            # Random unit vector
            a = np.random.randn(dim)
            a = a / np.linalg.norm(a)
            
            # Offset to create half-space tangent to sphere
            b = np.dot(a, center) + radius
            
            constraints.append(LinearConstraint(
                a=a,
                b=b,
                description=f"Sphere constraint {i+1}"
            ))
        
        return SafetyPolytope(constraints)
    
    @staticmethod
    def create_box_polytope(
        lower_bounds: np.ndarray,
        upper_bounds: np.ndarray
    ) -> 'SafetyPolytope':
        """
        Create axis-aligned box polytope
        
        Args:
            lower_bounds: Lower bounds for each dimension
            upper_bounds: Upper bounds for each dimension
            
        Returns:
            SafetyPolytope defining box region
        """
        dim = len(lower_bounds)
        constraints = []
        
        for i in range(dim):
            # Lower bound: -x_i <= -lower_i  =>  x_i >= lower_i
            a = np.zeros(dim)
            a[i] = -1
            b = -lower_bounds[i]
            constraints.append(LinearConstraint(
                a=a, b=b, description=f"Lower bound dim {i}"
            ))
            
            # Upper bound: x_i <= upper_i
            a = np.zeros(dim)
            a[i] = 1
            b = upper_bounds[i]
            constraints.append(LinearConstraint(
                a=a, b=b, description=f"Upper bound dim {i}"
            ))
        
        return SafetyPolytope(constraints)
