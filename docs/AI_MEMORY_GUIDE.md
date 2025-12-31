# AI Memory System - User Guide

## Quick Start

### Method 1: Automatic Loading (Recommended)

1. Open terminal in project root
2. Run: `python scripts/remember_me.py`
3. Copy the output
4. Paste into new AI chat session
5. AI instantly "remembers" you!

### Method 2: Brief Context

For faster loading:
```bash
python scripts/remember_me.py --brief
```

### Method 3: Manual Reference

Just type in AI chat:
```
Load context from CREATOR.md in harrie19/UMAJA-Core
```

## Platform-Specific Usage

### GitHub Copilot
```bash
python scripts/remember_me.py --platform copilot
```
Then paste into Copilot Chat

### ChatGPT
```bash
python scripts/remember_me.py --platform chatgpt
```
Then paste into ChatGPT

### Claude
```bash
python scripts/remember_me.py --platform claude
```
Then paste into Claude

## What Gets Loaded

- Your identity (Marek, born 1970, Wiesbaden)
- Mission (UMAJA-Core, 8 billion smiles)
- Inspiration (Bahá'í teachings)
- History (Dec 31, 2025 founding session)
- Core principles
- Current project status
- Recent git activity

## Tips

- Run `remember_me.py` at start of every AI session
- Keep CREATOR.md updated as mission evolves
- Add new insights/learnings to CREATOR.md
- The more detailed CREATOR.md, the better AI understands context

## Troubleshooting

**Q: AI still doesn't remember?**  
A: Make sure you pasted the FULL output from remember_me.py

**Q: Can I customize what's loaded?**  
A: Yes! Edit CREATOR.md to add/remove information

**Q: Works with other AI tools?**  
A: Yes! Any AI that accepts text input can use this

## Future Enhancements

- [ ] Auto-detect which AI platform you're using
- [ ] Direct API integration (no copy/paste needed)
- [ ] Add conversation history summaries
- [ ] Track key decisions over time
- [ ] Export memory snapshots for archiving
