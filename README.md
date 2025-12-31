# 🌍 Daily Smile World Tour

**Mission**: Put a smile on faces worldwide through friendly AI personalities exploring cities.

## What We Do

3 friendly AI personalities travel the world (virtually), sharing:
- 😊 Warm observations about cities
- 🌆 Relatable travel experiences  
- 💭 Innocent curiosity about local culture
- 🤝 Community stories and connections

**Not stand-up comedy. Not performance. Just... smiles.**

## The Travelers

| 🎓 The Professor | 😰 The Worrier | 🎉 The Enthusiast |
|---|---|---|
| Curious academic | Lovably anxious | Eternally optimistic |
| Asks innocent questions | Finds "dangers" everywhere | Sees joy in everything |
| Warm, inquisitive | Cautious, considerate | Excited, positive |

**No impersonations. Just friendly archetypes.**

---

## ✨ Key Features

### Content Generation
- **Text Generation**: 3 distinct friendly personalities with unique styles
- **Voice Synthesis**: Multi-backend TTS (ElevenLabs, Google TTS, offline)
- **Image Generation**: AI images + personality-themed quote cards
- **Video Creation**: Lyric-style videos with synced text and audio
- **City Content**: 50+ cities with topics, local culture, fun facts

### Daily Smile Mission
- **Micro Content**: 30-60 second friendly observations
- **Community Engagement**: Every post includes a question for followers
- **Personality Rotation**: Different archetype each day
- **Warm Tone**: Friendly, inclusive, relatable content
- **World Tour**: Visit every major city, one smile at a time

### Monetization
- **8 Product Tiers**: From text-only (€1.50) to viral kit (€20)
- **Smart Bundling**: Automatic discounts (10-20% off)
- **Upsell Engine**: Intelligent recommendations
- **One-Click Purchase**: Automated ZIP package delivery

### Worldtour
- **Interactive Map**: Leaflet.js-powered city tracking
- **Voting System**: Community-driven city selection
- **Content Queue**: Automated 7-day scheduling
- **Analytics Dashboard**: Real-time stats and insights

### Deployment Ready
- **One-Command Setup**: `python scripts/setup_multimedia.py --quick`
- **Railway/Heroku**: Pre-configured deployment files
- **Environment Templates**: Complete `.env.example`
- **20+ API Endpoints**: RESTful API with full documentation

---

## 🚀 Quick Start

### 5-Minute Setup

```bash
# 1. Clone repository
git clone https://github.com/harrie19/UMAJA-Core.git
cd UMAJA-Core

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate a daily smile
python scripts/generate_daily_smile.py

# 4. Generate demo content
python scripts/generate_demo_smiles.py
```

Visit **output/demos/** to see your generated smiles! 🎉

### Test Personality Engine

```bash
# Test all three personalities
python src/personality_engine.py

# Test worldtour manager
python src/worldtour_manager.py
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Web Interface Layer                    │
│          (Landing, Map, Bundle Builder, Gallery)         │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                    Flask API Server                      │
│             (20+ Endpoints, RESTful API)                 │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                   Core Engine Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Personality  │  │    Voice     │  │    Image     │ │
│  │   Engine     │  │ Synthesizer  │  │  Generator   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │    Video     │  │  Worldtour   │  │    Bundle    │ │
│  │  Generator   │  │  Generator   │  │   Builder    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                  External Services Layer                 │
│  (ElevenLabs, Stable Diffusion, Social Media APIs)      │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Core Modules

### 1. Personality Engine (`src/personality_engine.py`)
Generates text in friendly personality archetypes with warm, relatable styles.

```python
from src.personality_engine import PersonalityEngine

engine = PersonalityEngine()
result = engine.generate_text(
    topic="New York pizza",
    personality="the_professor",
    length="medium",
    style_intensity=0.7
)

print(result['text'])
# "I've been studying New York pizza and what fascinates me..."

# Generate micro-content for daily smiles
smile = engine.generate_smile_text(
    city="Tokyo",
    topic="sushi",
    personality="the_enthusiast",
    length="micro"
)
```

### 2. Worldtour Manager (`src/worldtour_manager.py`)
Manages cities, generates community questions, tracks progress.

```python
from src.worldtour_manager import WorldtourManager

manager = WorldtourManager()

# Get next city
city = manager.get_next_city()

# Generate community question
question = manager.get_community_question(city)
# "What's your favorite Tokyo memory?"

# Override for testing
manager.override_next('paris')
```

### 3. Daily Smile Generator (`scripts/generate_daily_smile.py`)
Creates complete daily smile content with community engagement.

```python
from scripts.generate_daily_smile import DailySmileGenerator

generator = DailySmileGenerator()
smile = generator.generate_daily_smile()

print(smile['text'])
# Includes: city intro, personality observation, community question
print(smile['hashtags'])
# ['#DailySmileFromTokyo', '#DailySmileWorldTour', '#TravelSmiles']
```

---

## 🌐 API Endpoints

### Content Generation
- `POST /api/generate/text` - Generate comedy text
- `POST /api/generate/audio` - Synthesize voice
- `POST /api/generate/image` - Create images
- `POST /api/generate/video` - Generate videos
- `POST /api/generate/city-content` - City-specific content

### Worldtour
- `GET /api/worldtour/cities` - List all cities
- `GET /api/worldtour/next` - Get next city
- `GET /api/worldtour/queue?days=7` - Content queue
- `POST /api/worldtour/vote` - Vote for city

### Purchases
- `POST /api/create-multimedia-sale` - Create purchase
- `POST /api/bundle/calculate` - Calculate pricing
- `POST /api/bundle/recommend` - Get recommendations
- `GET /download/:purchase_id` - Download package

### Analytics
- `GET /api/analytics/sales` - Sales statistics
- `GET /api/analytics/worldtour` - Tour statistics

**[Full API Documentation →](docs/MULTIMEDIA_SYSTEM.md)**

---

## 💰 Product Tiers & Pricing

| Tier | Price | Includes | Discount |
|------|-------|----------|----------|
| Text Only | €1.50 | Comedy text | - |
| Audio Only | €2.50 | Voice synthesis | - |
| Text + Audio | €3.50 | Both formats | Save €0.50 |
| Image | €3.00 | Quote card/AI image | - |
| **Standard Bundle** | €5.00 | Text + Audio + Image | Save €2.00 |
| Worldtour Bundle | €8.00 | Standard + City theme | Save €3.00 |
| Deluxe Video | €12.00 | All + Video | Save €7.00 |
| Viral Kit | €20.00 | Everything + Optimization | Save €15.00 |

**Volume Discounts:**
- 2 items: 10% off
- 3 items: 15% off
- 4+ items: 20% off

**40% of all profits go to charity** 💚

---

## 📊 Project Structure

```
UMAJA-Core/
├── api/
│   └── simple_server.py        # Flask API server (20+ endpoints)
├── src/
│   ├── personality_engine.py   # Text generation
│   ├── voice_synthesizer.py    # TTS with multiple backends
│   ├── image_generator.py      # Images and quote cards
│   ├── video_generator.py      # Video creation
│   ├── worldtour_generator.py  # City content (50+ cities)
│   ├── bundle_builder.py       # Pricing engine
│   └── multimedia_text_seller.py  # Purchase system
├── templates/
│   ├── worldtour_landing.html  # Hero landing page
│   ├── worldtour_map.html      # Interactive map (Leaflet.js)
│   ├── bundle_builder.html     # Bundle configurator
│   └── gallery.html            # Content gallery
├── scripts/
│   ├── setup_multimedia.py     # One-command setup
│   ├── daily_worldtour_post.py # Auto-posting (planned)
│   └── generate_marketing_content.py  # Marketing (planned)
├── docs/
│   ├── MULTIMEDIA_SYSTEM.md    # Complete API reference
│   ├── WORLDTOUR.md            # Strategy guide
│   ├── PERSONALITY_GUIDE.md    # Comedian styles
│   └── DEPLOYMENT.md           # Deploy to Railway/Heroku
├── data/
│   └── worldtour_cities.json   # 50+ cities database
├── static/
│   ├── audio/                  # Generated audio files
│   ├── images/                 # Generated images
│   ├── videos/                 # Generated videos
│   └── purchases/              # Customer packages
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── Procfile                    # Heroku config
└── railway.json                # Railway config
```

---

## 🎬 Examples

### Generate The Professor Text
```python
from src.personality_engine import PersonalityEngine

engine = PersonalityEngine()
result = engine.generate_text(
    topic="British tea",
    personality="the_professor",
    length="short"
)

print(result['text'])
```

**Output:**
> "I've been studying British tea and what fascinates me is how it brings people together. The wonderful thing about British tea is how welcoming it feels. It reminds me that everyday life is full of wonder."

### Generate The Worrier Audio
```python
from src.voice_synthesizer import VoiceSynthesizer

synth = VoiceSynthesizer()
result = synth.synthesize(
    text="Does anyone else get nervous about visiting new cities?",
    personality="the_worrier"
)
```

### Generate The Enthusiast Daily Smile
```python
from scripts.generate_daily_smile import DailySmileGenerator

generator = DailySmileGenerator()

# Override to specific city
generator.worldtour.override_next('tokyo')
smile = generator.generate_daily_smile()

print(smile['text'])
# Includes warm observation + community question
```

---

## 🚢 Deployment

### Railway (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

### Heroku
```bash
# Create app
heroku create umaja-worldtour

# Deploy
git push heroku main

# Set environment
heroku config:set ENVIRONMENT=production
```

### Docker (Coming Soon)
```bash
docker build -t umaja-worldtour .
docker run -p 5000:5000 umaja-worldtour
```

**[Full Deployment Guide →](docs/DEPLOYMENT.md)**

---

## 📚 Documentation

- **[Complete API Reference](docs/MULTIMEDIA_SYSTEM.md)** - All 20+ endpoints documented
- **[Worldtour Strategy Guide](docs/WORLDTOUR.md)** - Viral marketing playbook
- **[Personality Guide](docs/PERSONALITY_GUIDE.md)** - Master the 3 comedians
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Railway, Heroku, Docker

---

## 🎯 Roadmap

### Phase 1: Daily Smile Mission (Current) ✅
- [x] 3 friendly personality archetypes
- [x] 50+ cities database
- [x] Text generation with warm tone
- [x] Daily smile generator
- [x] Community engagement questions
- [x] Demo content generation
- [ ] Voice synthesis integration
- [ ] Social media auto-posting
- [ ] 10k+ followers goal

### Phase 2: Community Growth (Month 2-3)
- [ ] Daily auto-posting
- [ ] Community response tracking
- [ ] User-generated content features
- [ ] City voting system
- [ ] Smile analytics dashboard
- [ ] 100k+ followers goal

### Phase 3: Multimedia Expansion (Month 4+)
- [ ] Image generation with quotes
- [ ] Short-form video content
- [ ] Community story highlights
- [ ] Collaboration features
- [ ] Mobile app
- [ ] 500k+ followers goal

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

**Development Setup:**
```bash
# Install dev dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest tests/

# Format code
black src/ api/

# Lint
flake8 src/ api/
```

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

**Commercial use allowed** - Build your own comedy empire! 🎭

---

## 💬 Support

- 📖 **Documentation**: `/docs` folder
- 💡 **GitHub Discussions**: Ask questions, share ideas
- 🐛 **Issues**: Report bugs via GitHub Issues
- 📧 **Email**: (if applicable)

---

## 🌟 Success Stories

*Coming soon - Be the first to create amazing comedy content!*

---

## 🙏 Acknowledgments

- Open-source community for amazing tools
- Everyone who brings smiles to the world 😊
- All the wonderful cities that inspire us 🌍

---

## 📊 Success Metrics

**Mission Success = Community Engagement**

We measure success by:
- ✅ Comments and shares
- ✅ Friend tags and mentions  
- ✅ Smile emoji reactions 😊
- ✅ User stories shared
- ✅ Community connections made

**Not** by:
- ❌ "Funniness" scores
- ❌ Viral metrics alone
- ❌ Comedian approval

---

<div align="center">

**Made with ❤️ and 😊 by the UMAJA Team**

[Docs](docs/) • [Daily Smile Generator](scripts/generate_daily_smile.py) • [Worldtour](docs/WORLDTOUR.md)

*Let's put smiles on faces, one city at a time!* 😊🌍

</div>
