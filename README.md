# UMAJA-Core 😊

[![Tests](https://github.com/harrie19/UMAJA-Core/actions/workflows/tests.yml/badge.svg)](https://github.com/harrie19/UMAJA-Core/actions/workflows/tests.yml)
[![Text Generation](https://github.com/harrie19/UMAJA-Core/actions/workflows/text-generation.yml/badge.svg)](https://github.com/harrie19/UMAJA-Core/actions/workflows/text-generation.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Mission: Put smiles on faces through AI-powered text generation and semantic analysis**

UMAJA-Core is an advanced text generation and analysis platform that combines friendly personality engines with cutting-edge NLP technology. It creates warm, engaging content while maintaining high semantic coherence and quality standards. The platform features three core components: intelligent text generation with controlled variation, semantic coherence analysis using vector embeddings, and ethical fund distribution for charitable causes.

## 🧠 AI Memory System

Never re-explain context! Load Marek's full story instantly:

```bash
python scripts/remember_me.py
```

Paste the output into any AI chat (Copilot, ChatGPT, Claude) and the AI will instantly understand the full mission, history, and context.

See [AI Memory Guide](docs/AI_MEMORY_GUIDE.md) for details.

## 🌟 Our Friendly Archetypes

We've moved away from impersonating real people to create original, friendly personality archetypes:

### 🎓 The Professor
- **Traits:** Curious, thoughtful, educational, warm
- **Tone:** Friendly and informative
- **Focus:** Sharing fascinating facts that make people smile with knowledge
- **Example:** "Here's something fascinating that might brighten your day! Sea otters hold hands while they sleep so they don't drift apart. They're nature's reminder to stay connected!"

### 😰 The Worrier
- **Traits:** Relatable, caring, authentic, humorous
- **Tone:** Warm and understanding
- **Focus:** Finding humor in everyday concerns and making people feel less alone
- **Example:** "Is it just me, or does anyone else send a text and immediately reread it 47 times wondering if the punctuation made you sound angry? We're all in this together!"

### 🎉 The Enthusiast
- **Traits:** Energetic, joyful, optimistic, uplifting
- **Tone:** Warm and encouraging
- **Focus:** Celebrating life's small joys and spreading positive energy
- **Example:** "Friends! Right now, somewhere in the world, someone just laughed so hard they snorted. And that made someone else laugh even harder! We're living in a beautiful world!"

## 🚀 Features

### Core Components

#### 🎨 RauschenGenerator - Advanced Text Generation Engine
Generate high-quality reflective text with controlled noise variation and semantic coherence checking.

**Key Features:**
- Multiple reflection styles (philosophical, analytical, creative, practical)
- Controlled noise variation for text diversity
- Real-time semantic coherence validation
- Automatic word count targeting (50-150 words for short, 200-500 for long)
- Integrated pricing system with metadata

**Example Usage:**
```python
from src.rauschen_generator import RauschenGenerator

generator = RauschenGenerator()
result = generator.generate_reflection(
    topic="artificial intelligence",
    length="short",  # or "long"
    noise_level=0.4  # 0.0 to 1.0
)

print(f"Generated {result['word_count']} words")
print(f"Text: {result['text']}")
print(f"Price: ${result['price']}")
print(f"Coherence: {result['metadata']['coherence_score']}")
```

#### 🔍 VektorAnalyzer - Semantic Coherence Analysis
Analyze text quality using sentence transformer embeddings and vector similarity.

**Key Features:**
- Semantic coherence scoring using state-of-the-art transformers
- Theme similarity analysis
- Text comparison and similarity metrics
- Quality rating system (excellent, good, acceptable, poor)
- Inter-sentence coherence tracking

**Example Usage:**
```python
from src.vektor_analyzer import VektorAnalyzer

analyzer = VektorAnalyzer()

# Analyze text quality relative to a theme
analysis = analyzer.analyze_coherence(
    text="Your generated text here...",
    theme="artificial intelligence"
)

print(f"Quality: {analysis['quality']}")
print(f"Theme Similarity: {analysis['theme_similarity']:.3f}")
print(f"Overall Score: {analysis['overall_score']:.3f}")

# Compare two texts
similarity = analyzer.compare_texts(text1, text2)
print(f"Similarity: {similarity:.3f}")
```

#### 💰 DistributionEngine - Ethical Fund Allocation
Transparent fund distribution system prioritizing charitable causes.

**Distribution Model:**
- 40% to charitable causes
- 30% to operations
- 30% to upgrades and improvements

**Example Usage:**
```python
from src.distribution_engine import DistributionEngine

engine = DistributionEngine()
allocation = engine.allocate_payment(10.0)

print(f"Charity: €{allocation['charity']:.2f}")      # €4.00
print(f"Operations: €{allocation['operations']:.2f}")  # €3.00
print(f"Upgrades: €{allocation['upgrades']:.2f}")     # €3.00
```

### 🎭 Personality Archetypes

## ✨ Daily Smile Generator

Our flagship feature creates 30-60 second friendly content designed to:
- Put smiles on faces
- Build authentic community connections
- Encourage engagement through thoughtful questions
- Spread warmth without impersonation risks

### Quick Start

```bash
# Generate a random Daily Smile
python scripts/generate_daily_smile.py

# Use a specific archetype
python scripts/generate_daily_smile.py --archetype professor

# Generate multiple smiles
python scripts/generate_daily_smile.py --count 5

# Save to file
python scripts/generate_daily_smile.py --save

# Export as JSON
python scripts/generate_daily_smile.py --format json
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/harrie19/UMAJA-Core.git
cd UMAJA-Core

# Install dependencies
pip install -r requirements.txt

# Copy environment configuration
cp .env.example .env
```

### Quick Start

#### Generate Text via Python API
```python
from src.rauschen_generator import RauschenGenerator
from src.vektor_analyzer import VektorAnalyzer
from src.distribution_engine import DistributionEngine

# Initialize components
generator = RauschenGenerator()
analyzer = VektorAnalyzer()
engine = DistributionEngine()

# Generate text
result = generator.generate_reflection(
    topic="machine learning",
    length="short",
    noise_level=0.5
)

# Analyze quality
analysis = analyzer.analyze_coherence(result['text'], "machine learning")

# Calculate distribution
allocation = engine.allocate_payment(result['price'])

print(f"Generated {result['word_count']} words")
print(f"Quality: {analysis['quality']}")
print(f"Charity contribution: ${allocation['charity']:.2f}")
```

#### Generate Daily Smiles
```bash
# Generate a random Daily Smile
python scripts/generate_daily_smile.py

# Use a specific archetype
python scripts/generate_daily_smile.py --archetype professor

# Generate multiple smiles
python scripts/generate_daily_smile.py --count 5

# Save to file
python scripts/generate_daily_smile.py --save

# Export as JSON
python scripts/generate_daily_smile.py --format json
```

#### On-Demand Text Generation via GitHub Actions
1. Navigate to the **Actions** tab in your repository
2. Select **"🎨 On-Demand Text Generation"** workflow
3. Click **"Run workflow"**
4. Enter your parameters:
   - **Topic:** e.g., "artificial intelligence"
   - **Length:** short, medium, or long
   - **Noise Level:** 0.0 to 1.0 (default: 0.5)
5. Download the generated text from artifacts

### Configuration

Edit `.env` to customize your experience:

```env
# Mission and tone
MISSION=daily_smile
CONTENT_TONE=warm

# Default personality archetype
DEFAULT_ARCHETYPE=random

# Output settings
OUTPUT_DIR=output/daily_smiles
OUTPUT_FORMAT=text
```

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      UMAJA-Core Platform                     │
└─────────────────────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌───────────────┐    ┌─────────────────┐
│  Rauschen    │───▶│    Vektor     │───▶│  Distribution   │
│  Generator   │    │   Analyzer    │    │     Engine      │
└──────────────┘    └───────────────┘    └─────────────────┘
   Text Gen.         Quality Check         Fund Allocation
        │                    │                    │
        └────────────────────┴────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Generated Text │
                    │   + Analysis    │
                    │   + Pricing     │
                    └─────────────────┘
```

### Component Interaction Flow

1. **RauschenGenerator**: Creates reflective text with controlled variation
   - Applies multiple writing styles (philosophical, analytical, creative, practical)
   - Maintains semantic coherence through embeddings
   - Calculates pricing based on word count and complexity

2. **VektorAnalyzer**: Validates and scores text quality
   - Analyzes theme alignment using cosine similarity
   - Measures inter-sentence coherence
   - Provides quality ratings and detailed metrics

3. **DistributionEngine**: Handles ethical fund distribution
   - Transparently allocates funds (40% charity, 30% operations, 30% upgrades)
   - Tracks all transactions with timestamps
   - Ensures accountability

## 🎯 Use Cases

### 1. Content Creation
Generate high-quality reflective content on any topic with guaranteed semantic coherence.

```python
result = generator.generate_reflection("climate change", "long", 0.6)
# Perfect for blog posts, articles, and thought pieces
```

### 2. Quality Assurance
Validate text quality and theme alignment before publication.

```python
analysis = analyzer.analyze_coherence(your_text, "sustainability")
if analysis['quality'] in ['excellent', 'good']:
    publish(your_text)
```

### 3. Content Comparison
Compare different versions of text to find the most semantically similar.

```python
similarity = analyzer.compare_texts(version_a, version_b)
# Use the version with higher similarity to original theme
```

### 4. Social Impact
Every text generation contributes to charitable causes through transparent fund allocation.

```python
allocation = engine.allocate_payment(price)
# 40% automatically goes to charity
```

## 🧪 Testing

### Run All Tests
```bash
# Using pytest
pytest

# With coverage report
pytest --cov=src --cov-report=html

# Run specific component tests (as in CI/CD)
python -m pytest tests/ -v
```

### Manual Component Testing
```bash
# Test RauschenGenerator
python src/rauschen_generator.py

# Test VektorAnalyzer
python src/vektor_analyzer.py

# Test DistributionEngine
python src/distribution_engine.py
```

### CI/CD Testing
Tests run automatically on:
- Push to main branch
- Pull requests to main branch
- Manual workflow dispatch

View test results in the [Actions tab](https://github.com/harrie19/UMAJA-Core/actions/workflows/tests.yml).

## 📈 Benchmarks

### Text Generation Performance
- **Short text (50-150 words)**: ~2-5 seconds
- **Long text (200-500 words)**: ~5-10 seconds
- **Coherence score**: Average 0.7+ (excellent quality)

### Quality Metrics
- **Theme similarity**: Typically 0.6-0.9
- **Inter-sentence coherence**: Typically 0.5-0.8
- **Overall quality**: 85%+ rated "good" or "excellent"

### Pricing Model
- **Base rate**: $0.01 per word
- **Noise modifier**: +50% at maximum noise (1.0)
- **Length modifier**: +20% for long texts
- **Example**: 100-word text at 0.5 noise = $1.25

## 📚 Usage Examples

### Python API

```python
from personality_engine import PersonalityEngine

# Create engine
engine = PersonalityEngine()

# Generate a Daily Smile
smile = engine.generate_daily_smile()
print(smile['content'])

# Use specific archetype
smile = engine.generate_daily_smile('enthusiast')
print(f"{smile['personality']}: {smile['content']}")

# Get archetype directly
worrier = engine.get_archetype('worrier')
text = worrier.generate_smile_text()
print(text)
```

### Complete Integration Example

```python
from src.rauschen_generator import RauschenGenerator
from src.vektor_analyzer import VektorAnalyzer
from src.distribution_engine import DistributionEngine
import json

# Initialize all components
generator = RauschenGenerator()
analyzer = VektorAnalyzer()
engine = DistributionEngine()

# Generate text on a topic
topic = "sustainable technology"
result = generator.generate_reflection(topic, "medium", 0.5)

# Perform quality analysis
analysis = analyzer.analyze_coherence(result['text'], topic)

# Calculate fund distribution
allocation = engine.allocate_payment(result['price'])

# Compile complete output
output = {
    "text": result['text'],
    "word_count": result['word_count'],
    "quality": analysis['quality'],
    "scores": {
        "theme_similarity": analysis['theme_similarity'],
        "coherence": analysis['avg_inter_sentence_coherence'],
        "overall": analysis['overall_score']
    },
    "pricing": {
        "total": result['price'],
        "charity": allocation['charity'],
        "operations": allocation['operations'],
        "upgrades": allocation['upgrades']
    }
}

# Save or use the output
with open('output.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"Generated {result['word_count']}-word text")
print(f"Quality: {analysis['quality']}")
print(f"Charity contribution: ${allocation['charity']:.2f}")
```

### Command Line

```bash
# Basic generation
python scripts/generate_daily_smile.py

# Professor archetype with markdown output
python scripts/generate_daily_smile.py --archetype professor --format markdown

# Generate and save 3 smiles
python scripts/generate_daily_smile.py --count 3 --save

# Custom output file
python scripts/generate_daily_smile.py --output my_smile.txt
```

## 🤖 GitHub Actions Workflows

### 🧪 Automated Testing (`tests.yml`)
Runs comprehensive tests on every push and pull request to main branch.

**Test Coverage:**
- RauschenGenerator unit tests
- VektorAnalyzer unit tests
- DistributionEngine unit tests
- Full integration tests

**Triggers:**
- Push to main
- Pull requests to main
- Manual workflow dispatch

### 🎨 On-Demand Text Generation (`text-generation.yml`)
Generate text directly from GitHub's Actions interface.

**Features:**
- Custom topic input
- Configurable length (short/medium/long)
- Adjustable noise level (0.0-1.0)
- Automatic quality analysis
- Downloadable artifacts (JSON + TXT)

**How to Use:**
1. Go to Actions → "🎨 On-Demand Text Generation"
2. Click "Run workflow"
3. Fill in parameters and run
4. Download results from artifacts

### 🌍 Daily World Tour (`daily-worldtour.yml`)
Automated daily content generation for social media engagement.

## 🎯 Design Philosophy

### Why Archetypes Instead of Impersonations?

1. **Authenticity:** Our archetypes are original creations that feel genuine
2. **Safety:** No risk of misrepresenting real people or their estates
3. **Flexibility:** Archetypes can evolve based on community feedback
4. **Warmth:** Focus on connection rather than performance
5. **Scalability:** Easy to add new archetypes as needs grow

### Community Engagement Focus

Every piece of content includes:
- **Warmth:** Friendly, inclusive tone
- **Engagement:** Questions that invite community response
- **Relatability:** Scenarios everyone can connect with
- **Positivity:** Uplifting messages that spread smiles
- **Brevity:** 30-60 seconds of content, perfect for social media

### Technical Excellence

**Semantic Coherence:**
- Use sentence transformers for embeddings
- Maintain coherence scores above 0.7
- Real-time validation during generation

**Controlled Variation:**
- Noise levels from 0.0 (deterministic) to 1.0 (highly varied)
- Balance between creativity and coherence
- Predictable output quality

**Ethical Distribution:**
- Transparent fund allocation
- Prioritize charitable causes (40%)
- Sustainable operations model
- Regular upgrades and improvements

## 🌟 Key Advantages

### For Content Creators
- **High-quality text**: Guaranteed semantic coherence
- **Flexible styles**: Multiple reflection modes
- **Fast generation**: Results in seconds
- **Quality metrics**: Detailed analysis for every generation

### For Developers
- **Clean API**: Simple, intuitive interfaces
- **Well-documented**: Comprehensive docs and examples
- **Extensible**: Easy to add new features
- **Type-safe**: Full type hints throughout
- **Tested**: Comprehensive test suite

### For Organizations
- **Ethical**: 40% of revenue to charity
- **Transparent**: Full visibility into fund allocation
- **Scalable**: Handle high-volume content needs
- **Reliable**: Automated testing and CI/CD

### For Communities
- **Engaging**: Content designed for connection
- **Authentic**: Original archetypes, not impersonations
- **Inclusive**: Warm, welcoming tone
- **Impact**: Direct contribution to charitable causes

## 📋 API Reference

### RauschenGenerator

```python
class RauschenGenerator:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2')
    
    def generate_reflection(
        self,
        topic: str,
        length: Literal['short', 'long'] = 'short',
        noise_level: float = 0.3
    ) -> Dict:
        """
        Returns:
            {
                'text': str,              # Generated text
                'text_id': str,           # Unique identifier
                'word_count': int,        # Number of words
                'price': float,           # Price in credits
                'timestamp': str,         # ISO format timestamp
                'metadata': {
                    'topic': str,
                    'length': str,
                    'noise_level': float,
                    'coherence_score': float,
                    'model': int
                }
            }
        """
```

### VektorAnalyzer

```python
class VektorAnalyzer:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2')
    
    def analyze_coherence(
        self,
        text: str,
        theme: str
    ) -> Dict[str, any]:
        """
        Returns:
            {
                'quality': str,                          # Rating
                'theme_similarity': float,               # 0-1
                'avg_inter_sentence_coherence': float,   # 0-1
                'overall_score': float                   # 0-1
            }
        """
    
    def compare_texts(
        self,
        text1: str,
        text2: str
    ) -> float:
        """Returns similarity score between 0 and 1"""
```

### DistributionEngine

```python
class DistributionEngine:
    def __init__(self)
    
    def allocate_payment(self, amount: float) -> Dict:
        """
        Returns:
            {
                'total': float,
                'charity': float,        # 40%
                'operations': float,     # 30%
                'upgrades': float,       # 30%
                'timestamp': str
            }
        """
```

## 🔐 Security & Privacy

- **No personal data collection**: We don't store user information
- **Open source**: Full transparency in code
- **Secure dependencies**: Regular security audits
- **Environment variables**: Sensitive config in `.env` files
- **No external calls**: Runs entirely locally (after model download)

## 🚀 Deployment

### Railway (Recommended)
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Docker
```bash
# Build image
docker build -t umaja-core .

# Run container
docker run -p 5000:5000 umaja-core
```

### Manual Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MISSION=daily_smile
export CONTENT_TONE=warm

# Run server
python api/simple_server.py
```

## 📞 Support & Resources

- **Documentation**: You're reading it! 📚
- **Issues**: [GitHub Issues](https://github.com/harrie19/UMAJA-Core/issues)
- **Discussions**: [GitHub Discussions](https://github.com/harrie19/UMAJA-Core/discussions)
- **CI/CD**: [GitHub Actions](https://github.com/harrie19/UMAJA-Core/actions)

### Common Issues

**Model Download Fails:**
```bash
# Pre-download models
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

**Memory Issues:**
```bash
# Use CPU-only PyTorch for lower memory
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**Import Errors:**
```bash
# Ensure you're in the project root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## 🛠️ Development

### Project Structure

```
UMAJA-Core/
├── .github/
│   ├── workflows/
│   │   ├── tests.yml              # Automated testing workflow
│   │   ├── text-generation.yml    # On-demand text generation
│   │   ├── daily-worldtour.yml    # Daily content automation
│   │   └── deploy.yml             # Deployment workflow
│   └── DEPLOYMENT_SETUP.md
├── src/
│   ├── __init__.py
│   ├── rauschen_generator.py      # Text generation engine
│   ├── vektor_analyzer.py         # Semantic analysis
│   ├── distribution_engine.py     # Fund allocation
│   ├── personality_engine.py      # Personality archetypes
│   ├── worldtour_generator.py     # World tour content
│   ├── voice_synthesizer.py       # Voice synthesis
│   ├── image_generator.py         # Image generation
│   ├── video_generator.py         # Video generation
│   ├── bundle_builder.py          # Content bundling
│   └── multimedia_text_seller.py  # Sales integration
├── scripts/
│   ├── generate_daily_smile.py    # Daily Smile generator
│   ├── generate_demo_content.py   # Demo content creation
│   ├── daily_worldtour_post.py    # World tour automation
│   └── setup_multimedia.py        # Multimedia setup
├── api/
│   └── simple_server.py           # Flask API server
├── docs/
│   ├── PERSONALITY_GUIDE.md       # Personality documentation
│   ├── DEPLOYMENT.md              # Deployment guide
│   ├── WORLDTOUR.md               # World tour guide
│   └── MULTIMEDIA_SYSTEM.md       # Multimedia docs
├── templates/                      # HTML templates
├── data/                          # Data storage
├── output/                        # Generated content
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── .gitignore
├── Procfile                       # Process file
├── railway.json                   # Railway config
└── README.md                      # This file
```

### Technology Stack

**Core Technologies:**
- **Python 3.11+**: Primary programming language
- **PyTorch**: Deep learning framework
- **Sentence Transformers**: Semantic embeddings (all-MiniLM-L6-v2)
- **Transformers (Hugging Face)**: NLP models
- **scikit-learn**: Machine learning utilities
- **NumPy**: Numerical computing

**Testing & Quality:**
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **black**: Code formatting
- **flake8**: Linting

**Additional Features:**
- **Flask**: Web API framework
- **MoviePy**: Video generation
- **Pillow**: Image processing
- **gTTS/ElevenLabs**: Voice synthesis

### Adding New Archetypes

```python
from src.personality_engine import PersonalityArchetype

class TheNewArchetype(PersonalityArchetype):
    """Description of the new archetype"""
    
    def __init__(self):
        super().__init__(
            name="The New Archetype",
            traits=["trait1", "trait2", "trait3"],
            tone="warm and [characteristic]"
        )
    
    def generate_smile_text(self, topic: str = None) -> str:
        """Generate smile text for this archetype"""
        # Implement your smile generation logic
        templates = [
            "Template 1 with {}",
            "Template 2 about {}",
        ]
        # Add archetype-specific personality
        return self._format_with_personality(templates, topic)
```

### Extending the RauschenGenerator

```python
from src.rauschen_generator import RauschenGenerator

class CustomGenerator(RauschenGenerator):
    """Custom text generator with additional features"""
    
    def __init__(self):
        super().__init__()
        # Add custom templates or configurations
        self.custom_templates = {
            'technical': [
                "In technical terms, {} involves",
                "The architecture of {} consists of",
            ]
        }
    
    def generate_technical_doc(self, topic: str) -> dict:
        """Generate technical documentation"""
        # Use parent class methods with custom logic
        return self.generate_reflection(
            topic=topic,
            length='long',
            noise_level=0.2  # Lower noise for technical content
        )
```

## 🤝 Contributing

We welcome contributions that help us put more smiles on faces and improve the platform! Here's how you can contribute:

### Getting Started

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Follow our coding standards
4. **Test your changes**: Run the test suite
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to your branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Contribution Guidelines

**Code Quality:**
- Keep content warm and friendly
- Follow PEP 8 style guidelines
- Write clear, descriptive commit messages
- Add docstrings to all functions and classes
- Include type hints where appropriate

**Testing:**
- Add tests for new features
- Ensure all tests pass before submitting PR
- Maintain or improve code coverage
- Test edge cases and error handling

**Documentation:**
- Update README.md if adding new features
- Document API changes
- Include usage examples for new components
- Keep docstrings up to date

**Content Guidelines:**
- Focus on authentic connection
- Avoid impersonating real people
- Include community engagement elements
- Maintain the warm, friendly tone
- Test content thoroughly

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/UMAJA-Core.git
cd UMAJA-Core

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Run tests
pytest

# Format code
black src/ scripts/

# Lint code
flake8 src/ scripts/
```

### Areas for Contribution

We're especially interested in contributions in these areas:

- **🎨 New personality archetypes**: Add diverse, authentic personalities
- **🔍 Analysis improvements**: Enhance quality metrics and coherence checking
- **🌐 Internationalization**: Add support for multiple languages
- **📊 Visualization**: Create dashboards and analytics
- **🎯 Optimization**: Improve performance and efficiency
- **📚 Documentation**: Improve guides and examples
- **🧪 Testing**: Expand test coverage
- **♿ Accessibility**: Make the platform more accessible

### Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers feel welcome
- Celebrate diversity and different perspectives
- Report unacceptable behavior to maintainers

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Thank you to everyone who believes in spreading joy through authentic connection. Every smile matters!

---

**Remember: Our mission is to put smiles on faces. Let's do it with warmth, authenticity, and care.** 😊
