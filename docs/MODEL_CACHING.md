# Model Caching and Offline Mode

This document explains how UMAJA-Core handles sentence-transformer models and supports offline testing.

## Overview

UMAJA-Core uses two sentence-transformer models from Huggingface:
- `sentence-transformers/all-MiniLM-L6-v2` (384D embeddings) - Used by VektorAnalyzer
- `sentence-transformers/all-mpnet-base-v2` (768D embeddings) - Used by EthicalValueEncoder

## Model Caching

Models are automatically cached in the following locations (in order of precedence):

1. `$SENTENCE_TRANSFORMERS_HOME` - If set, this directory is used
2. `$HF_HOME` - Fallback to Huggingface home directory
3. `~/.cache/huggingface` - Default cache location

### Local Development Setup

#### First-time Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

Download models (requires internet connection):
```bash
python -c "
from sentence_transformers import SentenceTransformer

print('Downloading models...')
model1 = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
model2 = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
print('Models downloaded and cached!')
"
```

#### Offline Development

Once models are cached, you can work offline. The code will automatically use cached models.

To verify models are cached:
```bash
ls -la ~/.cache/huggingface/hub/
```

You should see directories for both models.

## GitHub Actions Setup

### Pre-Firewall Model Download

The `.github/workflows/tests.yml` workflow includes a step that downloads models **before** the firewall is enabled:

```yaml
- name: 🤗 Cache Huggingface models
  uses: actions/cache@v4
  with:
    path: ~/.cache/huggingface
    key: huggingface-models-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      huggingface-models-

- name: ⬇️ Download sentence-transformer models (before firewall)
  run: |
    python -c "
    from sentence_transformers import SentenceTransformer
    model1 = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    model2 = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    print('Models cached!')
    "
```

This ensures:
1. Models are downloaded when the firewall is not yet active
2. Models are cached using GitHub Actions cache
3. Subsequent runs use the cached models (faster!)

### Alternative: GitHub Copilot Allowlist

Repository administrators can add `huggingface.co` to the custom allowlist:

1. Navigate to: `https://github.com/harrie19/UMAJA-Core/settings/copilot/coding_agent`
2. Add `huggingface.co` to the custom allowlist
3. This allows the agent to download models even after the firewall is enabled

**Note**: Using setup steps (as above) is preferred as it's more efficient with caching.

## Testing

### Fast Tests with Mocks

By default, tests use mocked models for speed:

```bash
pytest tests/
```

This uses the fixtures in `tests/conftest.py` which mock the SentenceTransformer class.

### Integration Tests with Real Models

To run tests with real models:

```bash
UMAJA_USE_REAL_MODELS=1 pytest tests/
```

You can also mark specific tests to require real models:

```python
@pytest.mark.real_models
def test_with_real_embeddings(analyzer):
    # This test will be skipped unless UMAJA_USE_REAL_MODELS=1
    pass
```

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `SENTENCE_TRANSFORMERS_HOME` | Cache directory for models | `~/.cache/huggingface` |
| `HF_HOME` | Huggingface home directory | `~/.cache/huggingface` |
| `UMAJA_USE_REAL_MODELS` | Use real models in tests | `0` (use mocks) |

## Troubleshooting

### Model Download Fails

If model download fails:

1. **Check internet connection**: Models require internet for first download
2. **Check firewall**: Ensure `huggingface.co` is accessible
3. **Clear cache**: Remove `~/.cache/huggingface` and try again
4. **Use setup steps**: In CI, ensure models are downloaded before firewall

### Tests Fail with "Model not found"

If tests fail with model errors:

1. **Run with mocks**: Default tests use mocks, don't require real models
2. **Check cache**: Verify models are in cache directory
3. **Re-download**: Run the download script from "First-time Setup" section

### Cache Directory Issues

If you want to use a custom cache directory:

```bash
export SENTENCE_TRANSFORMERS_HOME=/path/to/cache
python script.py
```

Or set it in code:
```python
import os
os.environ['SENTENCE_TRANSFORMERS_HOME'] = '/path/to/cache'
from vektor_analyzer import VektorAnalyzer
analyzer = VektorAnalyzer()
```

## Model Specifications

### all-MiniLM-L6-v2
- **Embedding Dimension**: 384
- **Model Size**: ~80 MB
- **Performance**: Fast inference
- **Use Case**: General semantic similarity, lightweight tasks

### all-mpnet-base-v2
- **Embedding Dimension**: 768
- **Model Size**: ~420 MB
- **Performance**: Higher quality embeddings
- **Use Case**: Ethical value alignment, nuanced comparisons

## Best Practices

1. **Cache models locally**: Download once, use many times
2. **Use mocks for unit tests**: Faster feedback loop
3. **Use real models for integration tests**: Validate actual behavior
4. **Cache in CI**: Use GitHub Actions cache to speed up workflows
5. **Pre-download in CI**: Download models before firewall activation
