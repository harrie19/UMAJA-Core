"""
VectorComm Serialization

Binary serialization and compression for efficient transmission of
vector messages.
"""

import struct
import json
import gzip
import numpy as np
from typing import Tuple
from .protocol import VectorCommMessage, VectorCommHeader, VectorCommPayload, VectorCommMetadata


def serialize_message(message: VectorCommMessage, compress: bool = True) -> bytes:
    """
    Serialize VectorComm message to binary format
    
    Format:
    - Magic bytes (4): 'VCMP' (VectorComm Protocol)
    - Version (2): uint16
    - Header length (4): uint32
    - Header (variable): JSON
    - Payload vectors (variable): binary numpy arrays
    - Metadata length (4): uint32
    - Metadata (variable): JSON
    - Checksum (32): SHA256
    
    Args:
        message: Message to serialize
        compress: Whether to compress with gzip
    
    Returns:
        Binary serialized message
    """
    # Magic bytes
    data = b'VCMP'
    
    # Version
    data += struct.pack('<H', 1)  # Version 1
    
    # Serialize header to JSON
    header_json = json.dumps(message.header.to_dict()).encode('utf-8')
    data += struct.pack('<I', len(header_json))
    data += header_json
    
    # Serialize payload vectors as binary
    # Primary vector
    primary_bytes = message.payload.primary_vector.tobytes()
    data += struct.pack('<I', len(primary_bytes))
    data += primary_bytes
    
    # Number of context vectors
    data += struct.pack('<I', len(message.payload.context_vectors))
    
    # Context vectors
    for context_vec in message.payload.context_vectors:
        context_bytes = context_vec.tobytes()
        data += struct.pack('<I', len(context_bytes))
        data += context_bytes
    
    # Attention weights (optional)
    if message.payload.attention_weights is not None:
        attention_bytes = message.payload.attention_weights.tobytes()
        data += struct.pack('<I', len(attention_bytes))
        data += attention_bytes
    else:
        data += struct.pack('<I', 0)
    
    # Uncertainty vector (optional)
    if message.payload.uncertainty_vector is not None:
        uncertainty_bytes = message.payload.uncertainty_vector.tobytes()
        data += struct.pack('<I', len(uncertainty_bytes))
        data += uncertainty_bytes
    else:
        data += struct.pack('<I', 0)
    
    # Payload metadata
    payload_meta_json = json.dumps(message.payload.metadata).encode('utf-8')
    data += struct.pack('<I', len(payload_meta_json))
    data += payload_meta_json
    
    # Serialize metadata to JSON
    metadata_json = json.dumps(message.metadata.to_dict()).encode('utf-8')
    data += struct.pack('<I', len(metadata_json))
    data += metadata_json
    
    # Checksum (if present)
    if message.checksum:
        checksum_bytes = message.checksum.encode('utf-8')
        data += struct.pack('<I', len(checksum_bytes))
        data += checksum_bytes
    else:
        data += struct.pack('<I', 0)
    
    # Compress if requested
    if compress:
        data = gzip.compress(data)
    
    return data


def deserialize_message(data: bytes, compressed: bool = True) -> VectorCommMessage:
    """
    Deserialize binary data back to VectorComm message
    
    Args:
        data: Binary serialized message
        compressed: Whether data is gzip compressed
    
    Returns:
        VectorCommMessage
    """
    # Decompress if needed
    if compressed:
        try:
            data = gzip.decompress(data)
        except:
            # Maybe not compressed, try anyway
            pass
    
    offset = 0
    
    # Check magic bytes
    magic = data[offset:offset+4]
    if magic != b'VCMP':
        raise ValueError(f"Invalid magic bytes: {magic}")
    offset += 4
    
    # Version
    version = struct.unpack('<H', data[offset:offset+2])[0]
    offset += 2
    
    # Header
    header_len = struct.unpack('<I', data[offset:offset+4])[0]
    offset += 4
    header_json = data[offset:offset+header_len].decode('utf-8')
    header_dict = json.loads(header_json)
    header = VectorCommHeader.from_dict(header_dict)
    offset += header_len
    
    # Determine dtype from encoding
    dtype_map = {
        'float32': np.float32,
        'float16': np.float16,
        'bfloat16': np.float16  # Approximate with float16
    }
    dtype = dtype_map[header.encoding]
    
    # Primary vector
    primary_len = struct.unpack('<I', data[offset:offset+4])[0]
    offset += 4
    primary_bytes = data[offset:offset+primary_len]
    primary_vector = np.frombuffer(primary_bytes, dtype=dtype)
    offset += primary_len
    
    # Number of context vectors
    num_context = struct.unpack('<I', data[offset:offset+4])[0]
    offset += 4
    
    # Context vectors
    context_vectors = []
    for _ in range(num_context):
        context_len = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        context_bytes = data[offset:offset+context_len]
        context_vec = np.frombuffer(context_bytes, dtype=dtype)
        context_vectors.append(context_vec)
        offset += context_len
    
    # Attention weights
    attention_len = struct.unpack('<I', data[offset:offset+4])[0]
    offset += 4
    if attention_len > 0:
        attention_bytes = data[offset:offset+attention_len]
        attention_weights = np.frombuffer(attention_bytes, dtype=np.float32)
        offset += attention_len
    else:
        attention_weights = None
    
    # Uncertainty vector
    uncertainty_len = struct.unpack('<I', data[offset:offset+4])[0]
    offset += 4
    if uncertainty_len > 0:
        uncertainty_bytes = data[offset:offset+uncertainty_len]
        uncertainty_vector = np.frombuffer(uncertainty_bytes, dtype=dtype)
        offset += uncertainty_len
    else:
        uncertainty_vector = None
    
    # Payload metadata
    payload_meta_len = struct.unpack('<I', data[offset:offset+4])[0]
    offset += 4
    payload_meta_json = data[offset:offset+payload_meta_len].decode('utf-8')
    payload_metadata = json.loads(payload_meta_json)
    offset += payload_meta_len
    
    # Create payload
    payload = VectorCommPayload(
        primary_vector=primary_vector,
        context_vectors=context_vectors,
        attention_weights=attention_weights,
        uncertainty_vector=uncertainty_vector,
        metadata=payload_metadata
    )
    
    # Metadata
    metadata_len = struct.unpack('<I', data[offset:offset+4])[0]
    offset += 4
    metadata_json = data[offset:offset+metadata_len].decode('utf-8')
    metadata_dict = json.loads(metadata_json)
    metadata = VectorCommMetadata.from_dict(metadata_dict)
    offset += metadata_len
    
    # Checksum
    checksum_len = struct.unpack('<I', data[offset:offset+4])[0]
    offset += 4
    if checksum_len > 0:
        checksum = data[offset:offset+checksum_len].decode('utf-8')
    else:
        checksum = None
    
    # Create message
    message = VectorCommMessage(
        header=header,
        payload=payload,
        metadata=metadata,
        checksum=checksum
    )
    
    return message


def compress_vectors(vectors: np.ndarray, method: str = 'quantize') -> Tuple[bytes, dict]:
    """
    Compress vectors for transmission
    
    Methods:
    - 'quantize': Reduce precision (float32 -> int8)
    - 'gzip': Standard compression
    
    Args:
        vectors: Numpy array to compress
        method: Compression method
    
    Returns:
        Tuple of (compressed bytes, metadata for decompression)
    """
    if method == 'quantize':
        # Quantize to int8 (-127 to 127)
        # Store min/max for reconstruction
        vmin = float(vectors.min())
        vmax = float(vectors.max())
        
        # Normalize to 0-255
        normalized = (vectors - vmin) / (vmax - vmin)
        quantized = (normalized * 254).astype(np.uint8)
        
        metadata = {
            'method': 'quantize',
            'vmin': vmin,
            'vmax': vmax,
            'shape': vectors.shape,
            'original_dtype': str(vectors.dtype)
        }
        
        return quantized.tobytes(), metadata
    
    elif method == 'gzip':
        compressed = gzip.compress(vectors.tobytes())
        metadata = {
            'method': 'gzip',
            'shape': vectors.shape,
            'dtype': str(vectors.dtype)
        }
        return compressed, metadata
    
    else:
        raise ValueError(f"Unknown compression method: {method}")


def decompress_vectors(data: bytes, metadata: dict) -> np.ndarray:
    """
    Decompress vectors
    
    Args:
        data: Compressed bytes
        metadata: Metadata from compression
    
    Returns:
        Decompressed numpy array
    """
    method = metadata['method']
    
    if method == 'quantize':
        # Reconstruct from quantized
        quantized = np.frombuffer(data, dtype=np.uint8)
        quantized = quantized.reshape(metadata['shape'])
        
        # Denormalize
        vmin = metadata['vmin']
        vmax = metadata['vmax']
        
        normalized = quantized.astype(np.float32) / 254.0
        reconstructed = normalized * (vmax - vmin) + vmin
        
        # Convert to original dtype if needed
        if metadata['original_dtype'] != 'float32':
            reconstructed = reconstructed.astype(metadata['original_dtype'])
        
        return reconstructed
    
    elif method == 'gzip':
        decompressed = gzip.decompress(data)
        vectors = np.frombuffer(decompressed, dtype=metadata['dtype'])
        return vectors.reshape(metadata['shape'])
    
    else:
        raise ValueError(f"Unknown compression method: {method}")


def estimate_compression_ratio(message: VectorCommMessage, method: str = 'gzip') -> float:
    """
    Estimate compression ratio for a message
    
    Args:
        message: Message to estimate
        method: Compression method
    
    Returns:
        Compression ratio (original_size / compressed_size)
    """
    # Serialize without compression
    uncompressed = serialize_message(message, compress=False)
    original_size = len(uncompressed)
    
    # Serialize with compression
    compressed = serialize_message(message, compress=True)
    compressed_size = len(compressed)
    
    if compressed_size == 0:
        return 1.0
    
    return original_size / compressed_size


def batch_serialize(messages: list) -> bytes:
    """
    Serialize multiple messages into a single batch
    
    Args:
        messages: List of VectorCommMessage
    
    Returns:
        Binary batch data
    """
    data = b'VCBT'  # Magic for batch
    data += struct.pack('<I', len(messages))  # Message count
    
    for message in messages:
        msg_data = serialize_message(message, compress=True)
        data += struct.pack('<I', len(msg_data))
        data += msg_data
    
    return gzip.compress(data)


def batch_deserialize(data: bytes) -> list:
    """
    Deserialize batch of messages
    
    Args:
        data: Binary batch data
    
    Returns:
        List of VectorCommMessage
    """
    data = gzip.decompress(data)
    offset = 0
    
    # Check magic
    magic = data[offset:offset+4]
    if magic != b'VCBT':
        raise ValueError("Invalid batch magic bytes")
    offset += 4
    
    # Message count
    count = struct.unpack('<I', data[offset:offset+4])[0]
    offset += 4
    
    messages = []
    for _ in range(count):
        msg_len = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        msg_data = data[offset:offset+msg_len]
        message = deserialize_message(msg_data, compressed=True)
        messages.append(message)
        offset += msg_len
    
    return messages
