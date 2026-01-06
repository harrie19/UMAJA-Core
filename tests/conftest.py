"""
Pytest configuration and fixtures for UMAJA-Core tests.

Provides fixtures for mocking sentence-transformer models to speed up tests
and allow offline testing.
"""

import pytest
import numpy as np
from unittest.mock import Mock, MagicMock
import os


@pytest.fixture
def mock_sentence_transformer(monkeypatch):
    """
    Mock SentenceTransformer to avoid downloading models during tests.
    
    Returns a mock model that generates random embeddings of the correct dimensions.
    """
    class MockSentenceTransformer:
        def __init__(self, model_name, cache_folder=None):
            self.model_name = model_name
            # Determine embedding dimension based on model name
            if 'all-MiniLM-L6-v2' in model_name:
                self.embedding_dim = 384
            elif 'all-mpnet-base-v2' in model_name:
                self.embedding_dim = 768
            else:
                self.embedding_dim = 384  # Default
        
        def encode(self, texts, convert_to_numpy=True, normalize_embeddings=False):
            """Mock encode method that returns random embeddings."""
            if isinstance(texts, str):
                texts = [texts]
            
            # Generate random embeddings
            embeddings = np.random.randn(len(texts), self.embedding_dim).astype(np.float32)
            
            # Normalize if requested
            if normalize_embeddings:
                norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
                embeddings = embeddings / (norms + 1e-10)
            
            return embeddings
    
    # Monkeypatch the SentenceTransformer class
    monkeypatch.setattr('sentence_transformers.SentenceTransformer', MockSentenceTransformer)
    
    return MockSentenceTransformer


@pytest.fixture
def mock_vektor_analyzer(mock_sentence_transformer):
    """
    Create a VektorAnalyzer instance with mocked model.
    """
    import sys
    from pathlib import Path
    
    # Add src to path if not already there
    src_path = str(Path(__file__).parent.parent / "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    from vektor_analyzer import VektorAnalyzer
    return VektorAnalyzer()


@pytest.fixture
def mock_ethical_encoder(mock_sentence_transformer):
    """
    Create an EthicalValueEncoder instance with mocked model.
    """
    import sys
    from pathlib import Path
    
    # Add ethics module to path if not already there
    ethics_path = str(Path(__file__).parent.parent / "umaja_core" / "protocols" / "ethics")
    if ethics_path not in sys.path:
        sys.path.insert(0, ethics_path)
    
    from value_embeddings import EthicalValueEncoder
    return EthicalValueEncoder()


@pytest.fixture
def sample_texts():
    """Sample texts for testing semantic analysis."""
    return [
        "Machine learning is a subset of artificial intelligence.",
        "Deep learning uses neural networks with multiple layers.",
        "Python is a popular programming language for data science.",
        "Natural language processing helps computers understand human language.",
        "The weather is nice today."
    ]


@pytest.fixture
def sample_coherent_texts():
    """Sample texts that are semantically coherent."""
    return [
        "Artificial intelligence is transforming the world.",
        "Machine learning enables computers to learn from data.",
        "Neural networks are inspired by the human brain.",
        "Deep learning has revolutionized image recognition."
    ]


@pytest.fixture
def cache_dir(tmp_path, monkeypatch):
    """
    Create a temporary cache directory for models.
    
    Sets environment variables to use this cache directory.
    """
    cache = tmp_path / "huggingface_cache"
    cache.mkdir(exist_ok=True)
    
    # Set environment variables
    monkeypatch.setenv('SENTENCE_TRANSFORMERS_HOME', str(cache))
    monkeypatch.setenv('HF_HOME', str(cache))
    
    return cache


@pytest.fixture
def use_real_models():
    """
    Fixture that determines if tests should use real models or mocks.
    
    Set UMAJA_USE_REAL_MODELS=1 to use real models (for integration tests).
    Default is to use mocks for faster tests.
    """
    return os.environ.get('UMAJA_USE_REAL_MODELS', '0') == '1'


# Skip marker for tests that require real models
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "real_models: mark test as requiring real sentence-transformer models"
    )


def pytest_collection_modifyitems(config, items):
    """
    Automatically skip tests marked with 'real_models' if UMAJA_USE_REAL_MODELS is not set.
    """
    if os.environ.get('UMAJA_USE_REAL_MODELS', '0') != '1':
        skip_real_models = pytest.mark.skip(reason="Skipping real model tests (set UMAJA_USE_REAL_MODELS=1 to run)")
        for item in items:
            if "real_models" in item.keywords:
                item.add_marker(skip_real_models)
