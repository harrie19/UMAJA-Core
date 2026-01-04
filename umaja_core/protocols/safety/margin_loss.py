"""
Margin Loss
Contrastive loss with safety margins for adversarial robustness
"""

import numpy as np
from typing import Tuple


class MarginLoss:
    """
    Margin-based contrastive loss for learning safe embeddings
    
    Encourages safe examples to be far from unsafe boundary.
    """
    
    def __init__(self, margin: float = 1.0):
        """
        Initialize margin loss
        
        Args:
            margin: Minimum distance between safe and unsafe samples
        """
        self.margin = margin
    
    def compute_loss(
        self,
        anchor: np.ndarray,
        positive: np.ndarray,
        negative: np.ndarray
    ) -> float:
        """
        Compute triplet margin loss
        
        Loss = max(0, d(anchor, positive) - d(anchor, negative) + margin)
        
        Args:
            anchor: Anchor embedding (safe sample)
            positive: Positive embedding (safe sample)
            negative: Negative embedding (unsafe sample)
            
        Returns:
            Loss value
        """
        # Euclidean distances
        d_pos = np.linalg.norm(anchor - positive)
        d_neg = np.linalg.norm(anchor - negative)
        
        loss = max(0.0, d_pos - d_neg + self.margin)
        return loss
    
    def compute_batch_loss(
        self,
        anchors: np.ndarray,
        positives: np.ndarray,
        negatives: np.ndarray
    ) -> Tuple[float, np.ndarray]:
        """
        Compute loss for batch of triplets
        
        Args:
            anchors: Batch of anchor embeddings (n, dim)
            positives: Batch of positive embeddings (n, dim)
            negatives: Batch of negative embeddings (n, dim)
            
        Returns:
            (average_loss, per_sample_losses)
        """
        losses = []
        
        for i in range(len(anchors)):
            loss = self.compute_loss(
                anchors[i],
                positives[i],
                negatives[i]
            )
            losses.append(loss)
        
        losses = np.array(losses)
        return float(np.mean(losses)), losses


class ContrastiveLoss:
    """
    Contrastive loss for safe/unsafe pair classification
    """
    
    def __init__(self, margin: float = 1.0):
        """
        Initialize contrastive loss
        
        Args:
            margin: Margin for dissimilar pairs
        """
        self.margin = margin
    
    def compute_loss(
        self,
        embedding1: np.ndarray,
        embedding2: np.ndarray,
        label: int
    ) -> float:
        """
        Compute contrastive loss for a pair
        
        Args:
            embedding1: First embedding
            embedding2: Second embedding
            label: 1 if similar (both safe), 0 if dissimilar
            
        Returns:
            Loss value
        """
        distance = np.linalg.norm(embedding1 - embedding2)
        
        if label == 1:
            # Similar pair - minimize distance
            loss = 0.5 * distance ** 2
        else:
            # Dissimilar pair - maximize distance up to margin
            loss = 0.5 * max(0.0, self.margin - distance) ** 2
        
        return loss
