# 📡 UMAJA World Tour - RSS/Atom Feeds

This directory contains RSS and Atom feeds for automated consumption of UMAJA World Tour content.

## Available Feeds

### World Tour Feed
- **File**: `worldtour.xml`
- **URL**: https://harrie19.github.io/UMAJA-Core/feeds/worldtour.xml
- **Description**: Updates about city visits, new content, and tour progress
- **Update Frequency**: Daily at 12:00 UTC

## How to Subscribe

### For AI Agents
Use standard RSS/Atom parsing libraries:

```python
import feedparser

feed = feedparser.parse('https://harrie19.github.io/UMAJA-Core/feeds/worldtour.xml')

for entry in feed.entries:
    print(f"Title: {entry.title}")
    print(f"Link: {entry.link}")
    print(f"Published: {entry.published}")
    print(f"Summary: {entry.summary}")
    print("---")
```

### For Humans
Subscribe using your favorite RSS reader:
- **Feedly**: Add feed URL
- **NewsBlur**: Import feed
- **RSS readers**: Copy and paste feed URL

## Feed Format

All feeds follow RSS 2.0 standard with additional namespaces:
- `atom:` - Atom namespace for self-referencing
- `content:` - Rich content encoding
- `dc:` - Dublin Core metadata

## License

All feed content is licensed under **CC-BY 4.0**. Attribution required when sharing.

## Contact

Questions about feeds? Contact Umaja1919@googlemail.com
