# 🌍 UMAJA-Core

**Universal Motivation & Joy for All**

> *"The earth is but one country, and mankind its citizens"* — Bahá'u'lláh

[![Status](https://img.shields.io/badge/status-live-brightgreen)](https://harrie19.github.io/UMAJA-Core/)
[![Cost](https://img.shields.io/badge/cost-$0-blue)](https://github.com/harrie19/UMAJA-Core)
[![Reach](https://img.shields.io/badge/reach-5.1B%20people-orange)](https://github.com/harrie19/UMAJA-Core)

---

## 🎯 Mission

Bring personalized daily inspiration to **8 billion people** at **$0 cost** through:

- ✅ **3 Archetypes**: Dreamer, Warrior, Healer
- ✅ **8 Languages**: English, Spanish, Chinese, Hindi, Arabic, Portuguese, French, Swahili
- ✅ **365 Days**: Pre-generated smiles for infinite scalability
- ✅ **Zero Cost**: CDN-based distribution, no servers needed

**Current Reach**: 5.1 billion people (64% of global population)

---

## 🧠 AI Memory System

Never re-explain context! Load full story instantly:

```bash
python scripts/remember_me.py
```

This loads your complete context into any AI session:
- **Identity & Mission**: Who you are and what UMAJA-Core aims to achieve
- **Bahá'í Principles**: The spiritual foundation guiding development
- **Project History**: Key milestones and decisions
- **Current Status**: Latest progress and what's being worked on

**Why use it?**
- ⚡ **Instant Context**: AI understands your mission immediately
- 🎯 **No Repetition**: Never explain your vision again
- 🔄 **Consistency**: All AI helpers start with the same knowledge
- 📈 **Productivity**: Get straight to work, skip the intro

**Platform-Specific Usage:**
```bash
# For GitHub Copilot
python scripts/remember_me.py --platform copilot

# For ChatGPT
python scripts/remember_me.py --platform chatgpt

# For Claude
python scripts/remember_me.py --platform claude
```

See [AI Memory Guide](docs/AI_MEMORY_GUIDE.md) for complete documentation.

---

## 🎭 UMAJA Worldtour: LIVE! 🌍

The UMAJA Worldtour brings comedy and joy to cities around the world through 3 AI comedian personalities!

### Meet the Comedians

- 🎩 **John Cleese Style**: British wit, dry humor, observational comedy
- 🤖 **C-3PO Style**: Protocol-obsessed, analytical, endearingly nervous
- 🎪 **Robin Williams Style**: High-energy, improvisational, heartfelt

### Worldtour Statistics

```yaml
Status:          🟢 LIVE
Cities Visited:  5 / 59
Progress:        8.5% complete
Latest City:     Cairo 🇪🇬
Launch Date:     2026-01-02
```

### How It Works

1. **Daily City Visit**: Each day, visit a new city from our database of 59+ global destinations
2. **Triple Comedy**: Generate content from all 3 comedian personalities
3. **Multi-Format**: Create text, audio, images, and video content
4. **Global Distribution**: Share via social media, reaching millions worldwide

### Content Types

- 🏙️ **City Reviews**: Hilarious takes on local culture and landmarks
- 🍕 **Food Reviews**: Comedy about local cuisine and dining experiences
- 🗣️ **Cultural Debates**: Witty observations about local customs
- 📚 **Language Lessons**: Funny attempts at learning local phrases
- 🎪 **Tourist Traps**: Comedic guides to popular attractions

### Recent Content

📁 Latest: [Jakarta Content](/output/worldtour/jakarta_2026-01-02/) (Jan 2, 2026)

**Try it yourself:**
```bash
# Launch the worldtour and visit the next city
python scripts/launch_world_tour.py

# Generate daily content with multimedia
python scripts/daily_worldtour_post.py
```

*"Die Erde ist nur ein Land, und alle Menschen sind seine Bürger"* — Bahá'u'lláh

---

## 🏗️ Architecture

```
User Request → CDN (GitHub Pages) → Static JSON Files → Backend API (fallback) → Hardcoded Smiles (ultimate fallback)
```

**Result**: 
- Response time: <50ms (CDN edge)
- Scalability: ∞ (static files)
- Cost: $0 (free tiers)

---

## 🚀 Quick Start

### Live System

🌐 **Dashboard**: https://harrie19.github.io/UMAJA-Core/  
🚂 **Backend API**: https://umaja-core-production.up.railway.app *(update after Railway deployment)*

Try it now:
```bash
# Check system health
curl https://umaja-core-production.up.railway.app/health

# Get a daily smile
curl https://umaja-core-production.up.railway.app/api/daily-smile
```

### Deployment Status

| Service | Status | URL |
|---------|--------|-----|
| 🌐 Dashboard (GitHub Pages) | ![Pages Status](https://img.shields.io/badge/status-active-brightgreen) | [Visit Dashboard](https://harrie19.github.io/UMAJA-Core/) |
| 🚂 Backend (Railway) | ![Railway Status](https://img.shields.io/badge/status-deploying-yellow) | [Check Health](https://umaja-core-production.up.railway.app/health) |

### For Developers

```bash
# Clone repository
git clone https://github.com/harrie19/UMAJA-Core.git
cd UMAJA-Core

# Install dependencies
pip install -r requirements.txt

# Run backend locally
python api/simple_server.py
# → Visit http://localhost:5000/health

# View dashboard locally
# Open docs/index.html in your browser
```

📖 **Full Deployment Guide**: See [docs/DUAL_DEPLOYMENT.md](docs/DUAL_DEPLOYMENT.md) for complete instructions

---

## 📁 Repository Structure

```
UMAJA-Core/
├── .github/emergency_stop.json      # Emergency kill switch
├── api/simple_server.py             # Flask backend
├── cdn/smiles/                      # Pre-generated inspiration
│   ├── manifest.json
│   ├── Dreamer/en/1.json
│   └── ...                          # 8,760 files (when complete)
├── docs/index.html                  # Frontend application
├── scripts/helper_agents/           # Automation tools
└── requirements.txt
```

---

## 🌐 API Documentation

### `GET /health`
Health check endpoint.

**Response**:
```json
{"status": "healthy", "mission": "8 billion smiles", "version": "2.0.0"}
```

### `GET /api/daily-smile`
Get today's random smile.

**Response**:
```json
{
  "content": "Today, imagine the impossible...",
  "archetype": "professor",
  "mission": "Serving 8 billion people"
}
```

### World Tour API Endpoints

#### `POST /worldtour/start`
Launch the World Tour and get the next city to visit.

**Response**:
```json
{
  "success": true,
  "message": "World Tour launched successfully! 🌍",
  "next_city": {
    "id": "tokyo",
    "name": "Tokyo",
    "country": "Japan",
    "topics": ["sushi", "trains", "technology"],
    "language": "Japanese"
  },
  "stats": {
    "total_cities": 59,
    "visited_cities": 3,
    "remaining_cities": 56,
    "completion_percentage": 5.1
  }
}
```

#### `GET /worldtour/status`
Get current World Tour status and statistics.

**Response**:
```json
{
  "status": "active",
  "stats": {
    "total_cities": 59,
    "visited_cities": 3,
    "remaining_cities": 56,
    "total_views": 0,
    "completion_percentage": 5.1
  },
  "next_city": {
    "id": "paris",
    "name": "Paris",
    "country": "France"
  },
  "recent_visits": [...]
}
```

#### `GET /worldtour/cities`
List all cities in the World Tour database.

**Query Parameters**:
- `visited` (optional): Filter by visited status (`true`/`false`)
- `limit` (optional): Limit number of results

**Response**:
```json
{
  "success": true,
  "count": 59,
  "cities": [
    {
      "id": "new_york",
      "name": "New York",
      "country": "USA",
      "visited": false,
      "language": "English (American)",
      "topics": ["pizza", "subway", "Central Park"]
    }
  ]
}
```

#### `POST /worldtour/visit/{city_id}`
Visit a city and generate content.

**Request Body** (optional):
```json
{
  "personality": "john_cleese",
  "content_type": "city_review"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Successfully visited London! 🎉",
  "city": {
    "id": "london",
    "name": "London",
    "country": "UK",
    "visited": true
  },
  "content": {
    "city_name": "London",
    "personality": "john_cleese",
    "content_type": "city_review",
    "topic": "Now, the curious thing about London is...",
    "fun_facts": [...]
  }
}
```

#### `GET /worldtour/content/{city_id}`
Get content for a specific city.

**Query Parameters**:
- `generate` (optional): Generate new content (`true`/`false`)
- `personality` (optional): Specific personality
- `content_type` (optional): Specific content type

**Response**:
```json
{
  "success": true,
  "city": {
    "id": "london",
    "name": "London",
    "country": "UK",
    "topics": ["tea", "tube", "Big Ben"],
    "fun_facts": [...]
  },
  "available_personalities": ["john_cleese", "c3po", "robin_williams"],
  "available_content_types": ["city_review", "cultural_debate", "language_lesson", "tourist_trap", "food_review"]
}
```

---

## 🎭 Archetypes

### 🌟 Dreamer
Visionaries, innovators, creative thinkers
*"Your imagination is a preview of life's coming attractions."*

### ⚔️ Warrior
Resilient, determined, courageous
*"Courage isn't the absence of fear - it's taking action despite it."*

### 💚 Healer
Compassionate, nurturing, empathetic
*"In healing others, we heal ourselves."*

---

## 🌍 Languages

| Language | Speakers | Status |
|----------|----------|--------|
| English | 1.5B | ✅ Live |
| Spanish | 559M | ✅ Live |
| Chinese | 1.3B | ✅ Live |
| Hindi | 602M | ✅ Live |
| Arabic | 422M | ✅ Live |
| Portuguese | 264M | ✅ Live |
| French | 274M | ✅ Live |
| Swahili | 200M | ✅ Live |

**Total Reach**: 5.1 billion people

---

## 🚀 Deployment Architecture

UMAJA-Core uses a **dual-deployment strategy**:

### Railway (Backend)
- **Service**: Python Flask API
- **Endpoint**: `https://umaja-core-production.up.railway.app`
- **Features**: 
  - `/health` - System health monitoring
  - `/api/daily-smile` - Smile generation API
  - `/api/smile/<archetype>` - Archetype-specific smiles
  - Automatic deployments on push to `main`

### GitHub Pages (Frontend)
- **Service**: Static HTML Dashboard
- **URL**: `https://harrie19.github.io/UMAJA-Core/`
- **Features**:
  - Live backend status monitoring
  - Interactive smile generator
  - System metrics display
  - Automatic refresh every 60s

### Deployment Workflow

```mermaid
graph LR
    A[Push to main] --> B[Railway Deploy]
    A --> C[Pages Deploy]
    B --> D[Backend Live]
    C --> E[Dashboard Live]
    E --> D
```

📖 **Complete Guide**: [docs/DUAL_DEPLOYMENT.md](docs/DUAL_DEPLOYMENT.md)

---

## 📊 Current Status

```yaml
Backend API:   🚂 Railway (auto-deploy on main)
Dashboard:     🌐 GitHub Pages (docs/ folder)
CDN Content:   ✅ Day 1 complete (24 files across 8 languages)
Infrastructure: $0.00 monthly cost
Global Reach:  5.1B people (64% of 8B target)
Uptime:        99.9% target
```

**Health Check**: [![Backend Health](https://img.shields.io/badge/backend-check%20status-blue)](https://umaja-core-production.up.railway.app/health)

---

## 🕊️ Bahá'í Principles

### Truth
Transparent about capabilities and limitations

### Unity
Serves all 8 billion people equally, no discrimination

### Service
Mission-focused, $0 cost, accessible to all

### Justice
Equal access worldwide via CDN edge servers

### Humility
Acknowledges limitations, asks for help when needed

---

## 📈 Roadmap

### Phase 1: Foundation ✅
- [x] Backend API
- [x] Frontend application
- [x] Day 1 CDN (8 languages)
- [x] Documentation
- [x] World Tour API (5 endpoints)
- [x] World Tour Dashboard

### Phase 2: Expansion 🔄
- [x] Automated testing (19 tests)
- [x] GitHub Actions CI/CD
- [x] World Tour: 59 cities database
- [ ] Week 1 CDN (Days 1-7)
- [ ] Monitoring dashboard enhancements

### Phase 3: Scale 📅
- [ ] Full year CDN (365 days)
- [ ] Additional languages
- [ ] World Tour video generation
- [ ] Mobile app
- [ ] Reach 8 billion users

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to branch
5. Open a Pull Request

**Areas for contribution**:
- 🌐 Translations
- 🎭 New archetypes
- 📝 Inspiring messages
- 🐛 Bug fixes
- 📚 Documentation

---

## 💫 Vision

**UMAJA exists to prove that:**

- Technology can serve humanity without profit motive
- AI can operate autonomously with human oversight
- Global scale is achievable at zero cost
- Spiritual principles translate to technical architecture
- Every person deserves daily inspiration

---

<div align="center">

**🕊️ Built with ❤️ for 8 billion humans 🕊️**

[⭐ Star](https://github.com/harrie19/UMAJA-Core) • [🐛 Report Bug](https://github.com/harrie19/UMAJA-Core/issues) • [✨ Request Feature](https://github.com/harrie19/UMAJA-Core/issues)

</div>