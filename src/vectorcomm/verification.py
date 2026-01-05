"""
VectorComm Verification

Checksum calculation and message validation for integrity.
"""

import hashlib
import hmac
import numpy as np
from typing import Optional
from .protocol import VectorCommMessage


def calculate_checksum(message: VectorCommMessage, secret_key: Optional[bytes] = None) -> str:
    """
    Calculate SHA256 checksum for message integrity
    
    Args:
        message: Message to checksum
        secret_key: Optional HMAC secret key for authentication
    
    Returns:
        Hexadecimal checksum string
    """
    # Gather all data to hash
    data_parts = []
    
    # Header
    header_str = f"{message.header.dimension}:{message.header.encoding}:{message.header.semantic_space}:{message.header.confidence}"
    data_parts.append(header_str.encode('utf-8'))
    
    # Primary vector
    data_parts.append(message.payload.primary_vector.tobytes())
    
    # Context vectors
    for context_vec in message.payload.context_vectors:
        data_parts.append(context_vec.tobytes())
    
    # Attention weights
    if message.payload.attention_weights is not None:
        data_parts.append(message.payload.attention_weights.tobytes())
    
    # Uncertainty vector
    if message.payload.uncertainty_vector is not None:
        data_parts.append(message.payload.uncertainty_vector.tobytes())
    
    # Metadata
    metadata_str = f"{message.metadata.source_agent}:{message.metadata.destination_agent}:{message.metadata.intent.value}"
    data_parts.append(metadata_str.encode('utf-8'))
    
    # Combine all parts
    data = b''.join(data_parts)
    
    # Calculate checksum
    if secret_key:
        # HMAC for authentication
        h = hmac.new(secret_key, data, hashlib.sha256)
        return h.hexdigest()
    else:
        # Simple SHA256
        h = hashlib.sha256(data)
        return h.hexdigest()


def verify_checksum(message: VectorCommMessage, secret_key: Optional[bytes] = None) -> bool:
    """
    Verify message checksum
    
    Args:
        message: Message with checksum to verify
        secret_key: Optional HMAC secret key
    
    Returns:
        True if checksum is valid, False otherwise
    """
    if message.checksum is None:
        return False
    
    # Calculate expected checksum
    expected = calculate_checksum(message, secret_key)
    
    # Compare (constant time to prevent timing attacks)
    return hmac.compare_digest(expected, message.checksum)


def add_checksum(message: VectorCommMessage, secret_key: Optional[bytes] = None) -> VectorCommMessage:
    """
    Add checksum to message
    
    Args:
        message: Message to add checksum to
        secret_key: Optional HMAC secret key
    
    Returns:
        Message with checksum added
    """
    message.checksum = calculate_checksum(message, secret_key)
    return message


def validate_message(message: VectorCommMessage, strict: bool = True) -> tuple[bool, list[str]]:
    """
    Comprehensive message validation
    
    Args:
        message: Message to validate
        strict: Whether to enforce strict validation
    
    Returns:
        Tuple of (is_valid, list of errors)
    """
    errors = []
    
    # Validate header
    if message.header.dimension not in [384, 768, 1536, 4096]:
        errors.append(f"Invalid dimension: {message.header.dimension}")
    
    if message.header.encoding not in ['float32', 'float16', 'bfloat16']:
        errors.append(f"Invalid encoding: {message.header.encoding}")
    
    if not 0.0 <= message.header.confidence <= 1.0:
        errors.append(f"Invalid confidence: {message.header.confidence}")
    
    # Validate payload dimensions
    if len(message.payload.primary_vector) != message.header.dimension:
        errors.append(
            f"Primary vector dimension mismatch: "
            f"{len(message.payload.primary_vector)} != {message.header.dimension}"
        )
    
    # Validate context vectors
    for i, context_vec in enumerate(message.payload.context_vectors):
        if len(context_vec) != message.header.dimension:
            errors.append(
                f"Context vector {i} dimension mismatch: "
                f"{len(context_vec)} != {message.header.dimension}"
            )
    
    # Validate attention weights
    if message.payload.attention_weights is not None:
        if len(message.payload.attention_weights) != len(message.payload.context_vectors):
            errors.append(
                f"Attention weights count mismatch: "
                f"{len(message.payload.attention_weights)} != {len(message.payload.context_vectors)}"
            )
        
        # Check attention weights sum to ~1.0 (if strict)
        if strict and len(message.payload.attention_weights) > 0:
            weights_sum = float(np.sum(message.payload.attention_weights))
            if not 0.99 <= weights_sum <= 1.01:
                errors.append(f"Attention weights don't sum to 1.0: {weights_sum}")
    
    # Validate uncertainty vector
    if message.payload.uncertainty_vector is not None:
        if len(message.payload.uncertainty_vector) != message.header.dimension:
            errors.append(
                f"Uncertainty vector dimension mismatch: "
                f"{len(message.payload.uncertainty_vector)} != {message.header.dimension}"
            )
        
        # Check uncertainty is in valid range [0, 1] (if strict)
        if strict:
            if float(np.min(message.payload.uncertainty_vector)) < 0.0:
                errors.append("Uncertainty vector contains negative values")
            if float(np.max(message.payload.uncertainty_vector)) > 1.0:
                errors.append("Uncertainty vector contains values > 1.0")
    
    # Validate metadata
    if not message.metadata.source_agent:
        errors.append("Missing source_agent in metadata")
    
    # Check if expired
    if message.metadata.is_expired():
        errors.append("Message has expired")
    
    # Validate vector values (no NaN or Inf)
    if strict:
        if np.any(np.isnan(message.payload.primary_vector)):
            errors.append("Primary vector contains NaN values")
        if np.any(np.isinf(message.payload.primary_vector)):
            errors.append("Primary vector contains Inf values")
        
        for i, context_vec in enumerate(message.payload.context_vectors):
            if np.any(np.isnan(context_vec)):
                errors.append(f"Context vector {i} contains NaN values")
            if np.any(np.isinf(context_vec)):
                errors.append(f"Context vector {i} contains Inf values")
    
    # Validate checksum if present
    if message.checksum:
        if not verify_checksum(message):
            errors.append("Checksum verification failed")
    
    is_valid = len(errors) == 0
    return is_valid, errors


def validate_semantic_similarity(
    vector1: np.ndarray,
    vector2: np.ndarray,
    min_similarity: float = 0.5,
    max_similarity: float = 1.0
) -> tuple[bool, float]:
    """
    Validate semantic similarity between two vectors
    
    Args:
        vector1: First vector
        vector2: Second vector
        min_similarity: Minimum acceptable similarity
        max_similarity: Maximum acceptable similarity
    
    Returns:
        Tuple of (is_valid, similarity_score)
    """
    # Cosine similarity
    dot_product = np.dot(vector1, vector2)
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
    
    if norm1 == 0 or norm2 == 0:
        return False, 0.0
    
    similarity = float(dot_product / (norm1 * norm2))
    
    # Check if in valid range
    is_valid = min_similarity <= similarity <= max_similarity
    
    return is_valid, similarity


def validate_vector_norm(
    vector: np.ndarray,
    min_norm: float = 0.1,
    max_norm: float = 100.0
) -> tuple[bool, float]:
    """
    Validate vector norm (magnitude)
    
    Args:
        vector: Vector to validate
        min_norm: Minimum acceptable norm
        max_norm: Maximum acceptable norm
    
    Returns:
        Tuple of (is_valid, norm)
    """
    norm = float(np.linalg.norm(vector))
    is_valid = min_norm <= norm <= max_norm
    return is_valid, norm


def validate_batch(messages: list) -> dict:
    """
    Validate a batch of messages
    
    Args:
        messages: List of VectorCommMessage
    
    Returns:
        Dictionary with validation results
    """
    results = {
        'total': len(messages),
        'valid': 0,
        'invalid': 0,
        'errors': []
    }
    
    for i, message in enumerate(messages):
        is_valid, errors = validate_message(message, strict=True)
        
        if is_valid:
            results['valid'] += 1
        else:
            results['invalid'] += 1
            results['errors'].append({
                'message_index': i,
                'message_id': message.metadata.message_id,
                'errors': errors
            })
    
    return results


def sanitize_vector(vector: np.ndarray) -> np.ndarray:
    """
    Sanitize vector by removing NaN/Inf and normalizing
    
    Args:
        vector: Vector to sanitize
    
    Returns:
        Sanitized vector
    """
    # Replace NaN with 0
    vector = np.nan_to_num(vector, nan=0.0, posinf=1.0, neginf=-1.0)
    
    # Clip to reasonable range
    vector = np.clip(vector, -100.0, 100.0)
    
    return vector


def detect_anomalies(message: VectorCommMessage) -> list[str]:
    """
    Detect anomalies in message that might indicate corruption or attack
    
    Args:
        message: Message to check
    
    Returns:
        List of detected anomalies
    """
    anomalies = []
    
    # Check for very low confidence
    if message.header.confidence < 0.5:
        anomalies.append(f"Low confidence: {message.header.confidence}")
    
    # Check vector norms
    primary_norm = float(np.linalg.norm(message.payload.primary_vector))
    if primary_norm < 0.01 or primary_norm > 100.0:
        anomalies.append(f"Unusual primary vector norm: {primary_norm}")
    
    # Check for zero vectors
    if primary_norm < 0.001:
        anomalies.append("Primary vector is near-zero")
    
    # Check for suspicious patterns
    # All values the same
    if np.all(message.payload.primary_vector == message.payload.primary_vector[0]):
        anomalies.append("Primary vector has constant values")
    
    # Check context vectors
    for i, context_vec in enumerate(message.payload.context_vectors):
        context_norm = float(np.linalg.norm(context_vec))
        if context_norm < 0.01 or context_norm > 100.0:
            anomalies.append(f"Unusual context vector {i} norm: {context_norm}")
    
    # Check message size
    size_bytes = message.get_size_bytes()
    if size_bytes > 10_000_000:  # 10MB
        anomalies.append(f"Unusually large message: {size_bytes} bytes")
    
    return anomalies
