#!/usr/bin/env python3
"""
Download and cache sentence-transformer models for UMAJA-Core.

This script downloads the required models to the cache directory.
Run this before working offline or before running tests with real models.
"""

import os
import sys
from pathlib import Path

def download_models():
    """Download both required models."""
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("❌ Error: sentence-transformers not installed")
        print("   Run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Set cache directory
    cache_dir = os.environ.get('SENTENCE_TRANSFORMERS_HOME', 
                               os.environ.get('HF_HOME',
                               os.path.expanduser('~/.cache/huggingface')))
    
    print(f"📦 Cache directory: {cache_dir}\n")
    
    models = [
        ('sentence-transformers/all-MiniLM-L6-v2', '384D embeddings for VektorAnalyzer'),
        ('sentence-transformers/all-mpnet-base-v2', '768D embeddings for EthicalValueEncoder')
    ]
    
    for model_name, description in models:
        print(f"📥 Downloading {model_name}")
        print(f"   Purpose: {description}")
        try:
            model = SentenceTransformer(model_name, cache_folder=cache_dir)
            print(f"   ✅ Successfully cached\n")
        except Exception as e:
            print(f"   ❌ Failed: {e}\n")
            sys.exit(1)
    
    print("🎉 All models downloaded and cached successfully!")
    print("\nYou can now:")
    print("  • Work offline (models are cached)")
    print("  • Run tests with real models: UMAJA_USE_REAL_MODELS=1 pytest tests/")
    print("  • Use the analyzers without internet connection")

if __name__ == "__main__":
    print("=" * 60)
    print("UMAJA-Core Model Downloader")
    print("=" * 60)
    print()
    
    download_models()
