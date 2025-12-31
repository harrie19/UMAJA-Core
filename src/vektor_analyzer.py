"""
Vector Analyzer for Semantic Coherence Checking
Using Sentence Transformers for semantic similarity analysis
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VektorAnalyzer:
    """
    Analyzes semantic coherence using sentence transformers and vector embeddings.
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the VektorAnalyzer with a sentence transformer model.
        
        Args:
            model_name: Name of the sentence transformer model to use
                       Default: 'all-MiniLM-L6-v2' (lightweight and efficient)
        """
        logger.info(f"Loading sentence transformer model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        
    def encode_texts(self, texts: List[str]) -> np.ndarray:
        """
        Encode a list of texts into vector embeddings.
        
        Args:
            texts: List of text strings to encode
            
        Returns:
            numpy array of embeddings with shape (len(texts), embedding_dim)
        """
        if not texts:
            return np.array([])
        
        logger.debug(f"Encoding {len(texts)} texts")
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score between -1 and 1
        """
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def pairwise_similarity(self, texts: List[str]) -> np.ndarray:
        """
        Calculate pairwise cosine similarity between all texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            Similarity matrix of shape (len(texts), len(texts))
        """
        embeddings = self.encode_texts(texts)
        
        if len(embeddings) == 0:
            return np.array([])
        
        # Normalize embeddings for efficient cosine similarity
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        normalized_embeddings = embeddings / (norms + 1e-10)
        
        # Calculate similarity matrix
        similarity_matrix = np.dot(normalized_embeddings, normalized_embeddings.T)
        
        return similarity_matrix
    
    def semantic_coherence_score(self, texts: List[str]) -> Dict[str, float]:
        """
        Calculate semantic coherence metrics for a list of texts.
        
        Args:
            texts: List of text strings to analyze
            
        Returns:
            Dictionary containing coherence metrics:
            - mean_similarity: Average pairwise similarity
            - min_similarity: Minimum pairwise similarity
            - max_similarity: Maximum pairwise similarity (excluding diagonal)
            - std_similarity: Standard deviation of similarities
        """
        if len(texts) < 2:
            logger.warning("Need at least 2 texts for coherence analysis")
            return {
                'mean_similarity': 0.0,
                'min_similarity': 0.0,
                'max_similarity': 0.0,
                'std_similarity': 0.0
            }
        
        similarity_matrix = self.pairwise_similarity(texts)
        
        # Extract upper triangle (excluding diagonal)
        n = len(texts)
        upper_indices = np.triu_indices(n, k=1)
        similarities = similarity_matrix[upper_indices]
        
        return {
            'mean_similarity': float(np.mean(similarities)),
            'min_similarity': float(np.min(similarities)),
            'max_similarity': float(np.max(similarities)),
            'std_similarity': float(np.std(similarities))
        }
    
    def find_outliers(self, texts: List[str], threshold: float = 0.5) -> List[Tuple[int, str, float]]:
        """
        Find texts that are semantic outliers (low similarity to others).
        
        Args:
            texts: List of text strings
            threshold: Similarity threshold below which texts are considered outliers
            
        Returns:
            List of tuples: (index, text, avg_similarity)
        """
        if len(texts) < 2:
            return []
        
        similarity_matrix = self.pairwise_similarity(texts)
        
        outliers = []
        for i in range(len(texts)):
            # Calculate average similarity to all other texts
            mask = np.ones(len(texts), dtype=bool)
            mask[i] = False
            avg_similarity = np.mean(similarity_matrix[i][mask])
            
            if avg_similarity < threshold:
                outliers.append((i, texts[i], float(avg_similarity)))
        
        # Sort by similarity (lowest first)
        outliers.sort(key=lambda x: x[2])
        
        return outliers
    
    def compare_document_sections(self, sections: Dict[str, str]) -> Dict[str, Dict[str, float]]:
        """
        Compare semantic similarity between different document sections.
        
        Args:
            sections: Dictionary mapping section names to text content
            
        Returns:
            Dictionary of pairwise similarities between sections
        """
        section_names = list(sections.keys())
        section_texts = list(sections.values())
        
        if len(section_texts) < 2:
            return {}
        
        similarity_matrix = self.pairwise_similarity(section_texts)
        
        results = {}
        for i, name1 in enumerate(section_names):
            results[name1] = {}
            for j, name2 in enumerate(section_names):
                if i != j:
                    results[name1][name2] = float(similarity_matrix[i][j])
        
        return results
    
    def semantic_drift_analysis(self, text_sequence: List[str], window_size: int = 3) -> List[float]:
        """
        Analyze semantic drift across a sequence of texts using a sliding window.
        
        Args:
            text_sequence: Ordered list of texts
            window_size: Size of sliding window for comparison
            
        Returns:
            List of drift scores (lower = more coherent)
        """
        if len(text_sequence) < window_size:
            logger.warning(f"Text sequence too short for window size {window_size}")
            return []
        
        embeddings = self.encode_texts(text_sequence)
        drift_scores = []
        
        for i in range(len(text_sequence) - window_size + 1):
            window_embeddings = embeddings[i:i+window_size]
            
            # Calculate average pairwise similarity within window
            similarities = []
            for j in range(len(window_embeddings)):
                for k in range(j + 1, len(window_embeddings)):
                    sim = self.cosine_similarity(window_embeddings[j], window_embeddings[k])
                    similarities.append(sim)
            
            # Drift score is inverse of average similarity
            drift_score = 1.0 - np.mean(similarities)
            drift_scores.append(float(drift_score))
        
        return drift_scores
    
    def most_similar_pairs(self, texts: List[str], top_k: int = 5) -> List[Tuple[int, int, float]]:
        """
        Find the most semantically similar pairs of texts.
        
        Args:
            texts: List of text strings
            top_k: Number of top pairs to return
            
        Returns:
            List of tuples: (index1, index2, similarity_score)
        """
        if len(texts) < 2:
            return []
        
        similarity_matrix = self.pairwise_similarity(texts)
        
        # Get upper triangle indices
        n = len(texts)
        upper_indices = np.triu_indices(n, k=1)
        
        pairs = []
        for i, j in zip(upper_indices[0], upper_indices[1]):
            pairs.append((i, j, float(similarity_matrix[i][j])))
        
        # Sort by similarity (highest first)
        pairs.sort(key=lambda x: x[2], reverse=True)
        
        return pairs[:top_k]
    
    def analyze_coherence(self, text: str, theme: str) -> Dict:
        """
        Analyze the coherence of a text relative to a theme.
        
        Args:
            text: The text to analyze
            theme: The theme/topic to compare against
            
        Returns:
            Dictionary containing:
                - quality: 'excellent', 'good', or 'acceptable'
                - theme_similarity: Similarity to theme (0-1)
                - avg_inter_sentence_coherence: Average coherence between sentences (0-1)
                - overall_score: Combined score (0-1)
        """
        # Split text into sentences
        sentences = [s.strip() + '.' for s in text.split('.') if s.strip()]
        
        if len(sentences) == 0:
            return {
                'quality': 'acceptable',
                'theme_similarity': 0.0,
                'avg_inter_sentence_coherence': 0.0,
                'overall_score': 0.0
            }
        
        # Calculate theme similarity
        text_embedding = self.encode_texts([text])[0]
        theme_embedding = self.encode_texts([theme])[0]
        theme_similarity = float(self.cosine_similarity(text_embedding, theme_embedding))
        
        # Calculate inter-sentence coherence
        if len(sentences) > 1:
            coherence_metrics = self.semantic_coherence_score(sentences)
            avg_coherence = coherence_metrics['mean_similarity']
        else:
            avg_coherence = 1.0
        
        # Calculate overall score (weighted average)
        overall_score = (theme_similarity * 0.6) + (avg_coherence * 0.4)
        
        # Determine quality level
        if overall_score >= 0.7:
            quality = 'excellent'
        elif overall_score >= 0.5:
            quality = 'good'
        else:
            quality = 'acceptable'
        
        return {
            'quality': quality,
            'theme_similarity': round(theme_similarity, 3),
            'avg_inter_sentence_coherence': round(avg_coherence, 3),
            'overall_score': round(overall_score, 3)
        }
    
    def compare_texts(self, text1: str, text2: str) -> float:
        """
        Compare semantic similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        embeddings = self.encode_texts([text1, text2])
        
        if len(embeddings) < 2:
            return 0.0
        
        similarity = self.cosine_similarity(embeddings[0], embeddings[1])
        return float(max(0.0, min(1.0, similarity)))


def main():
    """
    Example usage of VektorAnalyzer
    """
    # Initialize analyzer
    analyzer = VektorAnalyzer()
    
    # Example texts
    texts = [
        "Machine learning is a subset of artificial intelligence.",
        "Deep learning uses neural networks with multiple layers.",
        "Python is a popular programming language for data science.",
        "Natural language processing helps computers understand human language.",
        "The weather is nice today."
    ]
    
    print("=== Semantic Coherence Analysis ===\n")
    
    # Calculate coherence scores
    coherence = analyzer.semantic_coherence_score(texts)
    print("Coherence Metrics:")
    for key, value in coherence.items():
        print(f"  {key}: {value:.4f}")
    
    print("\n=== Finding Outliers ===\n")
    
    # Find outliers
    outliers = analyzer.find_outliers(texts, threshold=0.3)
    if outliers:
        print("Semantic Outliers:")
        for idx, text, similarity in outliers:
            print(f"  [{idx}] {text[:50]}... (avg similarity: {similarity:.4f})")
    else:
        print("No outliers found.")
    
    print("\n=== Most Similar Pairs ===\n")
    
    # Find most similar pairs
    similar_pairs = analyzer.most_similar_pairs(texts, top_k=3)
    print("Top Similar Pairs:")
    for idx1, idx2, similarity in similar_pairs:
        print(f"  [{idx1}] <-> [{idx2}]: {similarity:.4f}")
        print(f"    Text 1: {texts[idx1][:50]}...")
        print(f"    Text 2: {texts[idx2][:50]}...")


if __name__ == "__main__":
    main()
