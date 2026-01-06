"""
Tests for VektorAnalyzer - Semantic coherence checking
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from vektor_analyzer import VektorAnalyzer


class TestVektorAnalyzer:
    """Test suite for VektorAnalyzer"""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance for tests"""
        return VektorAnalyzer()
    
    def test_encode_texts_basic(self, analyzer):
        """Test basic text encoding"""
        texts = ["Hello world", "Machine learning is great"]
        embeddings = analyzer.encode_texts(texts)
        
        assert embeddings.shape[0] == 2
        assert embeddings.shape[1] == 384  # all-MiniLM-L6-v2 dimension
        assert embeddings.dtype == np.float32
    
    def test_encode_texts_empty(self, analyzer):
        """Test encoding empty list"""
        embeddings = analyzer.encode_texts([])
        assert len(embeddings) == 0
    
    def test_cosine_similarity(self, analyzer):
        """Test cosine similarity calculation"""
        texts = ["artificial intelligence", "machine learning"]
        embeddings = analyzer.encode_texts(texts)
        
        similarity = analyzer.cosine_similarity(embeddings[0], embeddings[1])
        
        # Similar concepts should have high similarity
        assert 0.5 < similarity < 1.0
        assert isinstance(similarity, float)
    
    def test_cosine_similarity_identical(self, analyzer):
        """Test similarity of identical vectors"""
        texts = ["test text", "test text"]
        embeddings = analyzer.encode_texts(texts)
        
        similarity = analyzer.cosine_similarity(embeddings[0], embeddings[1])
        
        # Identical texts should have similarity ~1.0
        assert similarity > 0.99
    
    def test_pairwise_similarity(self, analyzer):
        """Test pairwise similarity matrix"""
        texts = [
            "machine learning",
            "artificial intelligence",
            "cooking recipes"
        ]
        
        similarity_matrix = analyzer.pairwise_similarity(texts)
        
        assert similarity_matrix.shape == (3, 3)
        
        # Diagonal should be 1.0
        assert np.allclose(np.diag(similarity_matrix), 1.0)
        
        # Matrix should be symmetric
        assert np.allclose(similarity_matrix, similarity_matrix.T)
        
        # ML and AI should be more similar than ML and cooking
        assert similarity_matrix[0, 1] > similarity_matrix[0, 2]
    
    def test_semantic_coherence_score(self, analyzer):
        """Test semantic coherence metrics"""
        coherent_texts = [
            "Python is a programming language",
            "Machine learning uses Python",
            "Data science requires programming"
        ]
        
        coherence = analyzer.semantic_coherence_score(coherent_texts)
        
        assert 'mean_similarity' in coherence
        assert 'min_similarity' in coherence
        assert 'max_similarity' in coherence
        assert 'std_similarity' in coherence
        
        # Coherent texts should have reasonable similarity
        assert coherence['mean_similarity'] > 0.3
    
    def test_semantic_coherence_single_text(self, analyzer):
        """Test coherence with single text"""
        coherence = analyzer.semantic_coherence_score(["single text"])
        
        # Should return zero metrics
        assert coherence['mean_similarity'] == 0.0
    
    def test_find_outliers(self, analyzer):
        """Test outlier detection"""
        texts = [
            "machine learning is powerful",
            "artificial intelligence helps solve problems",
            "deep learning uses neural networks",
            "the weather is nice today"  # Outlier
        ]
        
        outliers = analyzer.find_outliers(texts, threshold=0.4)
        
        # Should detect at least one outlier
        assert len(outliers) > 0
        
        # At least one of the outliers should be the weather text at index 3
        outlier_indices = [idx for idx, _, _ in outliers]
        assert 3 in outlier_indices
        
        # All outliers should have low similarity
        for idx, text, similarity in outliers:
            assert similarity < 0.4
    
    def test_find_outliers_threshold(self, analyzer):
        """Test outlier detection with different thresholds"""
        texts = [
            "python programming",
            "java coding",
            "software development"
        ]
        
        # High threshold should find more outliers
        outliers_high = analyzer.find_outliers(texts, threshold=0.9)
        outliers_low = analyzer.find_outliers(texts, threshold=0.3)
        
        assert len(outliers_high) >= len(outliers_low)
    
    def test_analyze_coherence(self, analyzer):
        """Test comprehensive coherence analysis"""
        text = "Machine learning is a subset of AI. It uses algorithms to learn from data. Neural networks are powerful tools."
        theme = "artificial intelligence and machine learning"
        
        analysis = analyzer.analyze_coherence(text, theme)
        
        assert 'quality' in analysis
        assert 'theme_similarity' in analysis
        assert 'avg_inter_sentence_coherence' in analysis
        assert 'overall_score' in analysis
        
        assert analysis['quality'] in ['excellent', 'good', 'acceptable', 'poor']
        assert 0 <= analysis['theme_similarity'] <= 1.0
        assert 0 <= analysis['overall_score'] <= 1.0
    
    def test_analyze_coherence_empty(self, analyzer):
        """Test coherence analysis with empty text"""
        analysis = analyzer.analyze_coherence("", "theme")
        
        assert analysis['quality'] == 'poor'
        assert analysis['overall_score'] == 0.0
    
    def test_analyze_coherence_single_sentence(self, analyzer):
        """Test coherence analysis with single sentence"""
        text = "Machine learning is amazing."
        theme = "machine learning"
        
        analysis = analyzer.analyze_coherence(text, theme)
        
        # Single sentence should have perfect inter-sentence coherence
        assert analysis['avg_inter_sentence_coherence'] == 1.0
        assert analysis['quality'] in ['excellent', 'good', 'acceptable']
    
    def test_compare_texts(self, analyzer):
        """Test text comparison"""
        text1 = "I love programming in Python"
        text2 = "Python is my favorite programming language"
        
        similarity = analyzer.compare_texts(text1, text2)
        
        assert 0 <= similarity <= 1.0
        assert similarity > 0.5  # Similar texts
    
    def test_separate_signal_noise_implicit(self, analyzer):
        """Test signal/noise separation (implicitly via outliers)"""
        texts = [
            "machine learning signal",
            "artificial intelligence signal",
            "neural networks signal",
            "random noise text unrelated",
            "another noise piece"
        ]
        
        # Outliers with threshold 0.5 simulates signal/noise separation
        outliers = analyzer.find_outliers(texts, threshold=0.5)
        
        # Should find noise texts
        assert len(outliers) >= 1
    
    def test_most_similar_pairs(self, analyzer):
        """Test finding most similar pairs"""
        texts = [
            "machine learning",
            "artificial intelligence",
            "deep learning",
            "cooking recipes"
        ]
        
        pairs = analyzer.most_similar_pairs(texts, top_k=2)
        
        assert len(pairs) <= 2
        
        for idx1, idx2, similarity in pairs:
            assert 0 <= idx1 < len(texts)
            assert 0 <= idx2 < len(texts)
            assert idx1 < idx2
            assert 0 <= similarity <= 1.0
    
    def test_dimension_validation(self, analyzer):
        """Test that embeddings have correct dimensions"""
        texts = ["test text"]
        embeddings = analyzer.encode_texts(texts)
        
        # all-MiniLM-L6-v2 should produce 384-dimensional embeddings
        assert embeddings.shape[1] == 384


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
