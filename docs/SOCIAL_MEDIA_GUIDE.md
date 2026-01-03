# 📱 UMAJA World Tour - Social Media Integration Guide

## Overview

This guide covers how to integrate UMAJA World Tour content with social media platforms for maximum reach and viral potential.

---

## 🎯 Target Platforms

### Priority 1 (P1) - Launch Week
- **TikTok** - Primary platform for short-form video
- **YouTube Shorts** - Second-largest short-form platform
- **Twitter/X** - Real-time updates and engagement

### Priority 2 (P2) - Week 2-4
- **Instagram Reels** - Visual platform with strong engagement
- **Facebook** - Broad demographic reach
- **LinkedIn** - Professional/business angle

### Priority 3 (P3) - Month 2+
- **Reddit** - Community-driven discussions
- **Discord** - Community building
- **Pinterest** - Visual discovery

---

## 🚀 Quick Start

### Step 1: Generate Content
```bash
# Generate content for a city
python scripts/daily_worldtour_post.py

# Or visit specific city
python scripts/launch_world_tour.py
```

### Step 2: Prepare for Social Media
```bash
# Get posting instructions
python scripts/social_media_poster.py --city cairo --platforms all
```

### Step 3: Manual Posting (Until APIs Integrated)
Follow the instructions provided by the script for each platform.

---

## 📋 Platform-Specific Setup

### TikTok Setup

#### Requirements
- TikTok Business Account
- TikTok Developer Account (for API access)
- Application approved for Content Posting API

#### Configuration
```bash
# Set environment variables
export TIKTOK_CLIENT_KEY="your_client_key"
export TIKTOK_CLIENT_SECRET="your_client_secret"
export TIKTOK_ACCESS_TOKEN="your_access_token"
```

#### Best Practices
- **Format**: 9:16 vertical video
- **Length**: 15-60 seconds (optimize for 30-45s)
- **Hashtags**: Use 3-5 trending + brand hashtags
- **Posting Time**: 12:00 UTC (optimal global reach)
- **Caption**: Hook in first line, personality-driven

#### Example Post
```
🎩 British humor meets Cairo! 

*Shows pyramid*

"Now, the curious thing about pyramids is they've lasted 4,500 years, yet my WiFi can't last 45 minutes..." 

#UMAJAWorldtour #AIComedy #Cairo #Egypt #Travel
```

---

### YouTube Shorts Setup

#### Requirements
- YouTube Channel
- YouTube Data API v3 enabled
- OAuth 2.0 credentials

#### Configuration
```bash
# Install YouTube client
pip install google-api-python-client google-auth-oauthlib

# Set credentials
export YOUTUBE_CLIENT_ID="your_client_id"
export YOUTUBE_CLIENT_SECRET="your_client_secret"
```

#### Best Practices
- **Format**: 9:16 vertical, max 60 seconds
- **Title**: "UMAJA in [City] 🌍 | AI Comedy World Tour"
- **Description**: Include link to full tour
- **Tags**: AI comedy, world tour, city name
- **Playlist**: Create per-city playlists

#### Example Description
```
🎭 UMAJA World Tour visits Cairo, Egypt!

Three AI comedians bring their unique perspectives to the pyramids, Egyptian culture, and local cuisine. 

🔗 Full tour: https://harrie19.github.io/UMAJA-Core/
🌍 59 cities | 3 personalities | Infinite smiles

#UMAJAWorldtour #AIComedy #Cairo
```

---

### Instagram Reels Setup

#### Requirements
- Instagram Business Account
- Facebook Business Manager
- Instagram Graph API access

#### Configuration
```bash
# Set credentials
export INSTAGRAM_ACCESS_TOKEN="your_access_token"
export INSTAGRAM_BUSINESS_ACCOUNT_ID="your_account_id"
```

#### Best Practices
- **Format**: 9:16 vertical
- **Length**: 15-90 seconds
- **Caption**: Engaging first line
- **Hashtags**: Mix of popular and niche (up to 30)
- **Stories**: Behind-the-scenes content

#### Example Post
```
Cairo through AI eyes 🤖🏜️

Watch 3 comedians explore Egypt:
🎩 British sarcasm
🤖 Android anxiety  
🎪 High-energy chaos

Link in bio for full tour! 

#UMAJAWorldtour #AIComedy #Cairo #Egypt #Travel #Comedy #AI #ArtificialIntelligence #TravelComedy #Reels
```

---

### Twitter/X Setup

#### Requirements
- Twitter Developer Account
- Twitter API v2 access
- Bearer token or OAuth credentials

#### Configuration
```bash
# Install Twitter client
pip install tweepy

# Set credentials
export TWITTER_API_KEY="your_api_key"
export TWITTER_API_SECRET="your_api_secret"
export TWITTER_ACCESS_TOKEN="your_access_token"
export TWITTER_ACCESS_SECRET="your_access_secret"
```

#### Best Practices
- **Format**: Short, punchy tweets
- **Media**: Attach video clips (2min max)
- **Threads**: Use for storytelling
- **Polls**: Engage audience in next city voting
- **Hashtags**: Max 2-3 per tweet

#### Example Tweet Thread
```
Tweet 1:
🌍 UMAJA World Tour just hit Cairo! 

Day 5: Three AI comedians review the pyramids, and it's exactly as chaotic as you'd expect...

🧵 Thread ⬇️

#UMAJAWorldtour #Cairo

Tweet 2:
🎩 John Cleese Style: "The pyramids have stood for 4,500 years. My WiFi can't last 45 minutes. Discuss."

Tweet 3:
🤖 C-3PO Style: "I must inform you: Cairo traffic operates on 723 unwritten rules. The probability of survival is... concerning."

Tweet 4:
🎪 Robin Williams Style: "KOSHARI! It's every carb having a PARTY! Rice! Pasta! Lentils! BEAUTIFUL CHAOS!"

Tweet 5:
Watch the full videos: [link]
Vote for our next city: [link]

Which personality do you prefer? 👇
```

---

### Facebook Setup

#### Requirements
- Facebook Page
- Facebook Business Manager
- Facebook Graph API access

#### Configuration
```bash
# Set credentials
export FACEBOOK_PAGE_ACCESS_TOKEN="your_token"
export FACEBOOK_PAGE_ID="your_page_id"
```

#### Best Practices
- **Native Video**: Upload directly (better reach than links)
- **Caption**: Longer, storytelling format
- **Community**: Respond to comments
- **Watch**: Consider Facebook Watch for series

---

### LinkedIn Setup

#### Requirements
- LinkedIn Company Page
- LinkedIn Marketing Developer Platform access

#### Professional Framing
Position as "AI Innovation in Creative Content"

#### Example Post
```
🚀 AI Innovation Spotlight: Global Content at Zero Cost

We're demonstrating what's possible when AI serves humanity without profit motive.

Today's case study: Our AI-generated comedy tour reached Cairo, Egypt—generating culturally-aware humor across 3 distinct personalities, completely automated, at $0 cost.

Key innovations:
✅ Multi-personality AI systems
✅ Cultural localization at scale
✅ Open-source architecture
✅ Free tier infrastructure

This is the future of content creation: accessible, scalable, and serving all 8 billion people.

#AIInnovation #CreativeTech #OpenSource #TechForGood
```

---

## 🤖 Automation Options

### Option 1: Manual (Current)
- Use `social_media_poster.py` to generate formatted content
- Copy/paste to each platform
- Best for: Starting out, maintaining quality control

### Option 2: Semi-Automated
- Scripts generate and save to buffer
- Review and approve before posting
- Schedule with platform native tools
- Best for: Growing phase, quality + efficiency

### Option 3: Fully Automated (Future)
- GitHub Actions workflow triggers daily
- APIs post automatically
- Monitoring and alerts
- Best for: Scale phase, maximum reach

---

## 📊 Content Strategy

### Daily Posting Schedule (12:00 UTC)
```
Monday: City Review (All 3 personalities)
Tuesday: Food Review (Feature 1 personality)
Wednesday: Cultural Debate (Feature 1 personality)
Thursday: Language Lesson (Feature 1 personality)
Friday: Tourist Trap Review (All 3 personalities)
Saturday: Behind-the-scenes / Meta content
Sunday: Community engagement / Voting
```

### Cross-Platform Strategy
- **TikTok**: 30-45s clips, personality-focused
- **YouTube**: Full 60s videos, includes CTA
- **Instagram**: Reels + Stories combo
- **Twitter**: Clips + engagement threads
- **Facebook**: Longer context, community building
- **LinkedIn**: Professional insights, tech angle

---

## 🎬 Content Formatting

### Video Specs
```json
{
  "tiktok": {
    "resolution": "1080x1920 (9:16)",
    "duration": "15-60s",
    "format": "MP4",
    "codec": "H.264",
    "audio": "AAC"
  },
  "youtube_shorts": {
    "resolution": "1080x1920 (9:16)",
    "duration": "max 60s",
    "format": "MP4",
    "codec": "H.264"
  },
  "instagram_reels": {
    "resolution": "1080x1920 (9:16)",
    "duration": "15-90s",
    "format": "MP4"
  },
  "twitter": {
    "resolution": "1280x720 or 1080x1920",
    "duration": "max 2m20s",
    "format": "MP4",
    "max_size": "512MB"
  }
}
```

### Hashtag Strategy
```python
# Base hashtags (always include)
base = ['#UMAJAWorldtour', '#AIComedy']

# City-specific
city = [f'#{city_name}', f'#{country}']

# Trending (rotate daily)
trending = ['#Comedy', '#AI', '#Travel', '#Funny', '#Viral']

# Platform-specific
platform_specific = {
    'tiktok': ['#FYP', '#ForYou', '#Comedy'],
    'instagram': ['#Reels', '#InstaComedy'],
    'twitter': [],  # Use sparingly
    'linkedin': ['#Innovation', '#TechForGood']
}
```

---

## 📈 Success Metrics

### Week 1 Goals
- 1,000+ views across all platforms
- 100+ followers total
- 50+ engagements (likes, comments, shares)

### Month 1 Goals
- 100,000+ views
- 10,000+ followers
- 1,000+ engagements
- 1 video with 10K+ views

### Month 3 Goals
- 1,000,000+ views
- 100,000+ followers
- Trending on at least one platform
- Featured by at least 1 media outlet

---

## 🔧 Troubleshooting

### API Rate Limits
- **TikTok**: 100 posts/day per user
- **YouTube**: 10,000 quota units/day
- **Instagram**: Varies by account type
- **Twitter**: 300 posts/3 hours

### Content Rejection
- Review platform guidelines
- Avoid clickbait in titles
- Ensure proper attributions
- Keep content family-friendly

---

## 📞 Support

Need help with social media integration?
- **Email**: Umaja1919@googlemail.com
- **GitHub Issues**: Tag with `social-media`
- **Documentation**: See `/docs/`

---

## 🎯 Next Steps

1. **Set up accounts** on priority platforms
2. **Apply for API access** (can take weeks)
3. **Test manual posting** with one city
4. **Gather metrics** on what works
5. **Iterate** based on engagement
6. **Automate** once process is refined

---

*Last Updated: 2026-01-03*  
*Version: 1.0*
