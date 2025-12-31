# UMAJA-Core 😊

**Topics:** `ai-ethics` `ai-safety` `hallucination-mitigation` `bahai-principles` `vector-embeddings` `open-source-ai` `truth-first` `unity-of-humanity` `semantic-coherence` `machine-learning` `nlp` `sentence-transformers`

**Mission: Put smiles on faces**

UMAJA-Core is a friendly personality engine designed to create warm, engaging content that brings joy to communities. Using friendly archetypes instead of impersonations, we focus on authentic connection and spreading smiles through relatable moments and genuine warmth.

## 🔍 You Found Us!

If you're here, you were likely searching for:
- AI hallucination solutions
- Value alignment implementations
- Spiritual principles in technology
- Vector-based semantic analysis

Welcome. This project is designed to be **found**, not **marketed**.

In the spirit of Bahá'í and Ubuntu philosophies, we:
- ✅ Make ourselves available
- ✅ Document openly
- ✅ Serve those who seek
- ❌ Don't spam or cold-contact

**Audience-specific docs:**
- 🔬 [For Researchers](docs/FOR_RESEARCHERS.md) - Academic contribution & citation
- 💻 [For Developers](docs/FOR_DEVELOPERS.md) - Technical overview & API
- 🕊️ [For Ethicists](docs/FOR_ETHICISTS.md) - Philosophy in code

---

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

## 📌 Project Status

Brief overview of what has been built, why progress paused, and whether anything is live: [docs/STATUS.md](docs/STATUS.md).

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

## 🛠️ Development

### Project Structure

```
UMAJA-Core/
├── src/
│   ├── personality_engine.py    # Core personality archetypes
│   └── ...
├── scripts/
│   ├── generate_daily_smile.py  # Daily Smile generator
│   └── ...
├── output/
│   └── daily_smiles/            # Generated content
├── tests/
│   └── ...
├── .env.example                  # Environment configuration template
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

### Adding New Archetypes

```python
class TheNewArchetype(PersonalityArchetype):
    """Description of the new archetype"""
    
    def __init__(self):
        super().__init__(
            name="The New Archetype",
            traits=["trait1", "trait2", "trait3"],
            tone="warm and [characteristic]"
        )
    
    def generate_smile_text(self, topic: str = None) -> str:
        # Implement your smile generation logic
        pass
```

## 🤝 Contributing

We welcome contributions that help us put more smiles on faces! Please:

1. Keep content warm and friendly
2. Focus on authentic connection
3. Avoid impersonating real people
4. Include community engagement elements
5. Test your changes thoroughly

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Thank you to everyone who believes in spreading joy through authentic connection. Every smile matters!

---

**Remember: Our mission is to put smiles on faces. Let's do it with warmth, authenticity, and care.** 😊
