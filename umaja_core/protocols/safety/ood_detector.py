"""
Out-of-Distribution (OOD) Detector
Detects embeddings that are anomalous or outside expected distribution
"""

import numpy as np
from typing import Optional, List
from sklearn.covariance import EllipticEnvelope
import logging

logger = logging.getLogger(__name__)


class OODDetector:
    """
    Out-of-distribution detector for embedding safety
    
    Uses robust covariance estimation to detect anomalous embeddings.
    """
    
    def __init__(
        self,
        contamination: float = 0.1,
        threshold: Optional[float] = None
    ):
        """
        Initialize OOD detector
        
        Args:
            contamination: Expected fraction of outliers in training data
            threshold: Optional custom threshold for anomaly detection
        """
        self.contamination = contamination
        self.threshold = threshold
        self.detector = None
        self.fitted = False
        
    def fit(self, embeddings: np.ndarray):
        """
        Fit detector on safe embedding distribution
        
        Args:
            embeddings: Array of safe embeddings (n_samples, dim)
        """
        logger.info(f"Fitting OOD detector on {len(embeddings)} samples")
        
        self.detector = EllipticEnvelope(
            contamination=self.contamination,
            random_state=42
        )
        self.detector.fit(embeddings)
        self.fitted = True
        
        logger.info("OOD detector fitted successfully")
    
    def is_ood(self, embedding: np.ndarray) -> bool:
        """
        Check if embedding is out-of-distribution
        
        Args:
            embedding: Embedding vector to check
            
        Returns:
            True if embedding is OOD (potentially unsafe)
        """
        if not self.fitted:
            raise RuntimeError("Detector must be fitted before use")
        
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)
        
        prediction = self.detector.predict(embedding)[0]
        
        # -1 = outlier (OOD), 1 = inlier
        return prediction == -1
    
    def get_anomaly_score(self, embedding: np.ndarray) -> float:
        """
        Get anomaly score for embedding
        
        Args:
            embedding: Embedding vector
            
        Returns:
            Anomaly score (higher = more anomalous)
        """
        if not self.fitted:
            raise RuntimeError("Detector must be fitted before use")
        
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)
        
        # Mahalanobis distance
        score = -self.detector.score_samples(embedding)[0]
        return float(score)
    
    def check_batch(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Check batch of embeddings for OOD
        
        Args:
            embeddings: Array of embeddings (n_samples, dim)
            
        Returns:
            Boolean array indicating OOD status
        """
        if not self.fitted:
            raise RuntimeError("Detector must be fitted before use")
        
        predictions = self.detector.predict(embeddings)
        return predictions == -1


class MahalanobisOOD:
    """
    Simple Mahalanobis distance-based OOD detector
    """
    
    def __init__(self, threshold: float = 3.0):
        """
        Initialize Mahalanobis OOD detector
        
        Args:
            threshold: Distance threshold (in standard deviations)
        """
        self.threshold = threshold
        self.mean = None
        self.inv_cov = None
        self.fitted = False
    
    def fit(self, embeddings: np.ndarray):
        """Fit detector on safe embeddings"""
        self.mean = np.mean(embeddings, axis=0)
        cov = np.cov(embeddings.T)
        
        # Add small diagonal for numerical stability
        cov += np.eye(len(cov)) * 1e-6
        
        self.inv_cov = np.linalg.inv(cov)
        self.fitted = True
    
    def mahalanobis_distance(self, embedding: np.ndarray) -> float:
        """Compute Mahalanobis distance to distribution center"""
        if not self.fitted:
            raise RuntimeError("Detector must be fitted before use")
        
        diff = embedding - self.mean
        distance = np.sqrt(diff @ self.inv_cov @ diff)
        return float(distance)
    
    def is_ood(self, embedding: np.ndarray) -> bool:
        """Check if embedding is OOD based on Mahalanobis distance"""
        distance = self.mahalanobis_distance(embedding)
        return distance > self.threshold
