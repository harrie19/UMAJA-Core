# UMAJA-AI Live Dashboard

## 🌐 View Live

The UMAJA-AI dashboard is deployed via GitHub Pages and shows real-time progress of the World Tour.

**Live URL:** `https://harrie19.github.io/UMAJA-Core/`

(Once GitHub Pages is enabled in repository settings)

## Features

- **Real-time Statistics**: Cities visited, content generated, days active
- **World Tour Map**: Visual progress through 50+ global cities
- **Content Feed**: Latest comedy pieces from The Distinguished Wit, The Anxious Analyzer, and The Energetic Improviser
- **Mission Statement**: Core values and Bahá'í-inspired vision
- **Responsive Design**: Works on desktop, tablet, and mobile

## How It Works

The dashboard pulls data directly from the repository:
- City data from `data/worldtour_cities.json`
- Updates automatically when new content is generated
- Pure HTML/CSS/JavaScript (no build process needed)

## Local Development

Open `index.html` directly in your browser:

```bash
cd docs
open index.html  # macOS
# or
start index.html  # Windows
# or
xdg-open index.html  # Linux
```

## Deployment

Automatically deployed via GitHub Actions workflow (`.github/workflows/deploy-pages.yml`) whenever code is pushed to main or the current branch.

## Setup GitHub Pages

To enable the live site:

1. Go to repository **Settings**
2. Click **Pages** in the left sidebar
3. Under "Build and deployment":
   - Source: **GitHub Actions**
4. The site will be live at `https://harrie19.github.io/UMAJA-Core/`

## Updates

The dashboard updates automatically:
- When new cities are visited (updates `worldtour_cities.json`)
- When content is generated
- Dashboard fetches latest data on each page load

---

**Happy Landing!** 🌟

*"Die Erde ist nur ein Land, und alle Menschen sind seine Bürger" — Bahá'u'lláh*
