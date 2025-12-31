# 🎭 UMAJA WORLDTOUR - 3 AI Comedians on World Tour

[![Build Status](https://github.com/harrie19/UMAJA-Core/workflows/CI/badge.svg)](https://github.com/harrie19/UMAJA-Core/actions)
[![Shop Coming Soon](https://img.shields.io/badge/shop-coming%20soon-orange.svg)](README.md#shop-coming-soon)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-green.svg)](https://github.com/harrie19/UMAJA-Core/releases)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**Follow 3 AI Comedians as They Tour 50+ Cities Worldwide** 🌍

John Cleese, C-3PO, and Robin Williams are embarking on an epic comedy world tour, creating hilarious content about cities worldwide. Join the journey!

🌍 **[Follow the Tour](https://your-deployment.railway.app)** | 📖 **[Documentation](docs/)** | 🎬 **[See Examples](#examples)** | 🛍️ **[Shop Coming Soon](#shop-coming-soon)**

---

## 🎯 What is UMAJA WORLDTOUR?

**Join the world's first AI comedy world tour!** Three legendary AI comedians are visiting 50+ cities worldwide, creating unique comedy content about each destination.

### 🌍 The Worldtour

- **Daily Content**: New city, new jokes, every single day
- **50+ Cities**: From New York to Tokyo, London to Rio
- **Community Driven**: Vote for the next destination
- **100% Free**: Follow the journey, enjoy the comedy

### The Comedians

| 🎩 **John Cleese** | 🤖 **C-3PO** | 🎪 **Robin Williams** |
|---|---|---|
| Dry British wit | Anxious protocol droid | Energetic improv |
| Monty Python style | Statistical obsession | Rapid-fire delivery |
| Deep, sarcastic voice | Higher pitch, robotic | Dynamic, warm |

---

## 🚀 Follow the Journey

### Social Media

Join us on social media for daily comedy content:

- 🎵 **TikTok**: [@umajaWorldtour](https://tiktok.com/@umajaworldtour) - Daily 60-second videos
- 📺 **YouTube**: [UMAJA Worldtour](https://youtube.com/@umajaworldtour) - Shorts & full episodes
- 📸 **Instagram**: [@umaja.worldtour](https://instagram.com/umaja.worldtour) - Reels & behind-the-scenes
- 🐦 **Twitter/X**: [@UMAJAtour](https://twitter.com/umajatour) - Daily updates & polls

**Vote for the next city!** 🗳️ Participate in our daily Twitter polls to decide where the comedians go next.

---

## 🛍️ Shop Coming Soon

Love the content? Want custom comedy about your favorite topics?

**Our shop is launching soon!** After we build an amazing community through the Worldtour, we'll offer:

- 🎭 Custom comedy text in any personality
- 🎙️ Personalized voice messages
- 🖼️ Custom quote cards and images
- 🎬 Full video packages
- 💼 Commercial licenses

**Sign up for early access**: [Get notified when we launch →](https://your-deployment.railway.app)

Until then, enjoy the free Worldtour content! 🌍

---

## ✨ Key Features

### 🌍 Worldtour Campaign (Active Now!)
- **Daily Posts**: New comedy content every day at 12:00 UTC
- **50+ Cities**: Major destinations worldwide with unique cultural humor
- **Interactive Map**: Track where the comedians have been
- **Community Voting**: Help choose the next destination
- **Progress Tracking**: Follow the journey in real-time

### Content Generation (Free During Worldtour)
- **Text Generation**: 3 distinct comedian personalities with unique styles
- **Voice Synthesis**: Multi-backend TTS (works offline, no API keys required!)
- **Image Generation**: AI images + personality-themed quote cards
- **Video Creation**: Lyric-style videos with synced text and audio
- **City Content**: 50+ cities with topics, stereotypes, fun facts

### Future Features (Coming with Shop Launch)
- **8 Product Tiers**: From text-only to full viral kits
- **Smart Bundling**: Automatic discounts (10-20% off)
- **Upsell Engine**: Intelligent recommendations
- **One-Click Purchase**: Automated ZIP package delivery
- **40% to Charity**: Supporting good causes with every purchase 💚

### Technical Features
- **One-Command Setup**: `python scripts/setup_multimedia.py --quick`
- **Railway/Heroku**: Pre-configured deployment files
- **Worldtour Mode**: Works without payment system or API keys
- **Environment Templates**: Complete `.env.example`
- **20+ API Endpoints**: RESTful API with full documentation

---

## 🚀 Quick Start (For Developers)

Want to run the Worldtour system locally or contribute?

### 5-Minute Setup

```bash
# 1. Clone repository
git clone https://github.com/harrie19/UMAJA-Core.git
cd UMAJA-Core

# 2. Run setup
python scripts/setup_multimedia.py --quick

# 3. Start server
python api/simple_server.py
```

Visit **http://localhost:5000** - You're live! 🎉

### Generate Demo Content

Create sample videos to see the system in action:

```bash
# Generate 5 demo videos (one per personality)
python scripts/generate_demo_content.py --count 5

# Check output in output/demos/
```

### Generate Daily Worldtour Content

```bash
# Generate today's worldtour content
python scripts/daily_worldtour_post.py

# Content will be in output/worldtour/
```

### Test API Endpoints

```bash
# Generate comedy text (free, always available)
curl -X POST http://localhost:5000/api/generate/text \
  -H "Content-Type: application/json" \
  -d '{"topic":"pizza","personality":"john_cleese","length":"short"}'

# Try to purchase (will return 403 during Worldtour mode)
curl -X POST http://localhost:5000/api/create-multimedia-sale \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "topic":"New York pizza", 
    "personality":"john_cleese",
    "content_types":["text","audio","image"]
  }'
# Response: {"error": "Shop coming soon! Follow our Worldtour 🌍"}
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
Generates text in comedian styles with personality markers and humor patterns.

```python
from personality_engine import PersonalityEngine

engine = PersonalityEngine()
result = engine.generate_text(
    topic="New York pizza",
    personality="john_cleese",
    length="medium",
    style_intensity=0.7
)

print(result['text'])
# "Now, the curious thing about New York pizza..."
```

### 2. Voice Synthesizer (`src/voice_synthesizer.py`)
Multi-backend TTS with personality voices.

```python
from voice_synthesizer import VoiceSynthesizer

synthesizer = VoiceSynthesizer()
result = synthesizer.synthesize(
    text="Hello world",
    personality="c3po",
    format="mp3"
)
# Generates: static/audio/c3po_abc123.mp3
```

### 3. Image Generator (`src/image_generator.py`)
Quote cards and AI images with personality themes.

```python
from image_generator import ImageGenerator

generator = ImageGenerator()
result = generator.generate_quote_card(
    quote="The curious thing about pizza...",
    personality="john_cleese"
)
# Generates: static/images/quote_john_cleese_abc123.png
```

### 4. Video Generator (`src/video_generator.py`)
Creates lyric-style videos and slideshows.

```python
from video_generator import VideoGenerator

generator = VideoGenerator()
result = generator.create_lyric_video(
    text="Comedy text here...",
    audio_path="audio.mp3",
    personality="robin_williams"
)
# Generates: static/videos/lyric_robin_williams_abc123.mp4
```

### 5. Worldtour Generator (`src/worldtour_generator.py`)
City-specific content for 50+ cities.

```python
from worldtour_generator import WorldtourGenerator

generator = WorldtourGenerator()
content = generator.generate_city_content(
    city_id="new_york",
    personality="john_cleese",
    content_type="city_review"
)
```

### 6. Bundle Builder (`src/bundle_builder.py`)
Smart pricing with automatic discounts.

```python
from bundle_builder import BundleBuilder

builder = BundleBuilder()
pricing = builder.calculate_bundle_price(
    items=['standard_bundle'],
    extras=['commercial_license']
)
# Automatically applies volume discounts
```

### 7. Multimedia Seller (`src/multimedia_text_seller.py`)
Complete purchase workflow with ZIP packaging.

```python
from multimedia_text_seller import MultimediaTextSeller

seller = MultimediaTextSeller()
result = seller.create_multimedia_purchase(
    email="customer@example.com",
    topic="pizza",
    personality="john_cleese",
    content_types=['text', 'audio', 'image']
)
# Creates downloadable ZIP package
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
- `GET /api/analytics/sales` - Sales statistics (disabled during Worldtour)
- `GET /api/analytics/worldtour` - Tour statistics

**Note:** Purchase endpoints return HTTP 403 during Worldtour mode with message: "Shop coming soon! Follow our Worldtour 🌍"

**[Full API Documentation →](docs/MULTIMEDIA_SYSTEM.md)**

---

## 💰 Future Product Tiers (Coming Soon)

When the shop launches, we'll offer:

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
│   ├── daily_worldtour_post.py # Daily content automation
│   └── generate_demo_content.py  # Quick demo generation
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

### Generate John Cleese Text
```python
from src.personality_engine import PersonalityEngine

engine = PersonalityEngine()
result = engine.generate_text(
    topic="British tea",
    personality="john_cleese",
    length="short"
)

print(result['text'])
```

**Output:**
> "Now, the curious thing about British tea is that it's rather like a religion practiced exclusively by confused penguins. One observes that the average person's understanding of proper brewing technique rivals that of a medieval alchemist attempting to transmute biscuits into gold. Quite."

### Create C-3PO Audio
```python
from src.voice_synthesizer import VoiceSynthesizer

synth = VoiceSynthesizer()
result = synth.synthesize(
    text="Oh my! This presents 2,479 interpretations!",
    personality="c3po"
)
```

### Generate Robin Williams Video
```python
from src.multimedia_text_seller import MultimediaTextSeller

seller = MultimediaTextSeller()
result = seller.create_multimedia_purchase(
    email="fan@example.com",
    topic="Stand-up comedy",
    personality="robin_williams",
    content_types=['text', 'audio', 'video']
)

print(f"Download: {result['download_url']}")
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

### Phase 1: Worldtour (Active Now! Months 1-3) ✅
- [x] 50+ cities database
- [x] 3 AI comedian personalities
- [x] Text, audio, image, video generation
- [x] Interactive world map
- [x] Voting system
- [x] Daily auto-generation scripts
- [ ] Social media automation
- [ ] 500k+ followers goal

### Phase 2: Shop Launch (Month 4+)
- [x] 8 product tiers designed
- [x] Bundle builder UI
- [x] Smart pricing engine
- [x] Purchase workflow
- [ ] Enable payment system (PayPal integration)
- [ ] Email notifications
- [ ] Launch marketing campaign
- [ ] €10k/month revenue goal

### Phase 3: Scale (Month 6+)
- [ ] Mobile app
- [ ] More personalities
- [ ] Live comedy shows
- [ ] API marketplace
- [ ] Affiliate program
- [ ] White-label solution

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

- Inspired by the legendary comedians: John Cleese, Robin Williams
- Star Wars franchise for C-3PO
- Open-source community for amazing tools
- Everyone who makes the world laugh 🎭

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/harrie19/UMAJA-Core?style=social)
![GitHub forks](https://img.shields.io/github/forks/harrie19/UMAJA-Core?style=social)
![GitHub issues](https://img.shields.io/github/issues/harrie19/UMAJA-Core)
![Last commit](https://img.shields.io/github/last-commit/harrie19/UMAJA-Core)

---

<div align="center">

**Made with ❤️ and 😂 by the UMAJA Team**

**Follow the Worldtour** 🌍

[TikTok](https://tiktok.com/@umajaworldtour) • [YouTube](https://youtube.com/@umajaworldtour) • [Instagram](https://instagram.com/umaja.worldtour) • [Twitter](https://twitter.com/umajatour)

**40% of future profits go to charity** 💚

[Website](https://umaja-worldtour.com) • [Docs](docs/) • [API](docs/MULTIMEDIA_SYSTEM.md) • [Worldtour](docs/WORLDTOUR.md)

*Let's make humanity laugh, one city at a time!* 🎭🌍

</div>
