# 🤖 UMAJA Worldtour Automation Guide

This guide explains how to automate daily worldtour content generation and posting.

## 📋 Overview

The UMAJA Worldtour visits a new city daily, generating comedy content from 3 AI personalities:
- 🎩 **John Cleese**: British wit and observational humor
- 🤖 **C-3PO**: Protocol-obsessed analytical comedy  
- 🎪 **Robin Williams**: High-energy improvisational style

## 🔄 Manual Daily Posts

### Quick Launch
Run the worldtour launcher to visit the next city:

```bash
# Visit next city and generate content templates
python scripts/launch_world_tour.py

# Generate full multimedia content (text, audio, images, video)
python scripts/daily_worldtour_post.py
```

### Expected Output
- ✅ City marked as visited in `data/worldtour_cities.json`
- 📁 Content saved to `output/worldtour/{city}_{timestamp}/`
- 🎭 Content from all 3 personalities generated

## 🤖 GitHub Actions Automation

### Option 1: Daily Scheduled Posts

Create `.github/workflows/daily_worldtour.yml`:

```yaml
name: Daily Worldtour Post

on:
  schedule:
    # Run daily at 10:00 AM UTC
    - cron: '0 10 * * *'
  workflow_dispatch: # Allow manual trigger

jobs:
  generate-content:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Launch Worldtour
        run: |
          python scripts/launch_world_tour.py
      
      - name: Generate Daily Content
        run: |
          python scripts/daily_worldtour_post.py
        continue-on-error: true
      
      - name: Commit and push changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data/worldtour_cities.json output/
          git commit -m "🌍 Daily Worldtour: $(date +'%Y-%m-%d')" || exit 0
          git push
```

### Option 2: Weekly Batch Generation

For more control, generate a week's worth of content at once:

```yaml
name: Weekly Worldtour Batch

on:
  schedule:
    # Run every Monday at 9:00 AM UTC
    - cron: '0 9 * * 1'
  workflow_dispatch:

jobs:
  batch-generate:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Generate Week of Content
        run: |
          for i in {1..7}; do
            echo "Generating day $i..."
            python scripts/launch_world_tour.py
            python scripts/daily_worldtour_post.py
            sleep 5
          done
      
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add data/worldtour_cities.json output/
          git commit -m "🌍 Weekly Worldtour Batch: $(date +'%Y-%m-%d')" || exit 0
          git push
```

## 📱 Social Media Distribution

### Manual Posting Workflow

After generating content:

1. **Review Content**: Check `output/worldtour/{city}_{date}/`
2. **Upload Video**: 
   - TikTok: Use `final_video.mp4`
   - YouTube Shorts: Upload same video
   - Instagram Reels: Upload same video
3. **Post Text**:
   - Twitter/X: Share teaser with video link
   - Use hashtags: `#UMAJAWorldtour #AIComedy #{city_name}`
4. **Engage**: Reply to comments, create polls

### Automation with APIs (Advanced)

For full automation, you'll need API keys from each platform:

```python
# Example pseudo-code for social media posting
from worldtour_poster import WorldtourPoster

poster = WorldtourPoster()
poster.post_to_tiktok(video_path, caption, hashtags)
poster.post_to_youtube_shorts(video_path, title, description)
poster.post_to_twitter(text, video_url)
```

**Note**: Most social platforms require OAuth and have rate limits. Manual posting is often more reliable.

## 🔍 Monitoring and Analytics

### Check Worldtour Progress

```bash
# View statistics
python -c "
import sys
sys.path.insert(0, 'src')
from worldtour_generator import WorldtourGenerator

gen = WorldtourGenerator()
stats = gen.get_stats()
print(f'Progress: {stats[\"visited_cities\"]}/{stats[\"total_cities\"]} cities')
print(f'Completion: {stats[\"completion_percentage\"]}%')
"
```

### Track Engagement

Monitor:
- 📊 Video views per city
- 💬 Comments and replies
- ❤️ Likes and shares
- 🌍 Geographic distribution

Update `data/worldtour_cities.json` with engagement metrics:

```json
{
  "jakarta": {
    "visited": true,
    "visit_date": "2026-01-02",
    "video_views": 12500,
    "video_url": "https://tiktok.com/@umaja/video/123"
  }
}
```

## 🛠️ Troubleshooting

### Content Generation Fails

```bash
# Check if city database is accessible
ls -la data/worldtour_cities.json

# Verify Python dependencies
pip list | grep -E "(pillow|requests)"

# Run in verbose mode
python scripts/launch_world_tour.py --dry-run
```

### No Unvisited Cities

Reset the database or expand with more cities:

```python
# Reset visited status (use with caution!)
import json
with open('data/worldtour_cities.json', 'r+') as f:
    cities = json.load(f)
    for city in cities.values():
        city['visited'] = False
    f.seek(0)
    json.dump(cities, f, indent=2)
    f.truncate()
```

## 📝 Best Practices

1. **Consistency**: Post at the same time daily for audience expectations
2. **Quality**: Review generated content before posting
3. **Engagement**: Respond to comments and build community
4. **Analytics**: Track what content performs best
5. **Backup**: Keep copies of all generated content
6. **Documentation**: Update this guide with learnings

## 🎯 Next Steps

- [ ] Set up GitHub Actions for automation
- [ ] Create social media accounts for UMAJA
- [ ] Build audience through consistent posting
- [ ] Monitor engagement and iterate
- [ ] Expand city database beyond 59 cities
- [ ] Add more content types and personalities

## 🌍 Vision

*"The earth is but one country, and mankind its citizens"* — Bahá'u'lláh

The Worldtour brings joy and laughter to all cultures, connecting humanity through comedy that transcends borders.

---

**Need Help?** Check [docs/WORLDTOUR.md](WORLDTOUR.md) for more details or file an issue on GitHub.
