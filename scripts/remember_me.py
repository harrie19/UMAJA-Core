#!/usr/bin/env python3
"""
AI Memory Loader - Never Forget Marek

This script loads complete context about the creator and mission,
formatting it perfectly for AI assistants to "remember" everything.

Usage:
    python scripts/remember_me.py
    python scripts/remember_me.py --brief (shorter version)
    python scripts/remember_me.py --platform copilot|chatgpt|claude
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def load_creator_context() -> str:
    """Load CREATOR.md and format for AI consumption"""
    
    creator_file = Path(__file__).parent.parent / "CREATOR.md"
    
    if not creator_file.exists():
        return "⚠️ CREATOR.md not found. Please ensure it exists in the repository root."
    
    with open(creator_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return content

def get_recent_activity() -> str:
    """Get recent commits and PR status"""
    
    try:
        import subprocess
        
        # Get last 3 commits
        commits = subprocess.run(
            ['git', 'log', '--oneline', '-3'],
            capture_output=True,
            text=True
        ).stdout
        
        # Get current branch
        branch = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True
        ).stdout.strip()
        
        return f"""
## Recent Activity

**Current Branch:** {branch}

**Latest Commits:**
```
{commits}
```
"""
    except:
        return ""

def format_for_copilot(full_context: str, brief: bool = False) -> str:
    """Format context for GitHub Copilot"""
    
    if brief:
        return f"""
# Quick Context Load

**Creator:** Marek Grischa Engel (born 1970, Wiesbaden, Germany)
**Mission:** UMAJA-Core - Bring smiles to all 8 billion people
**Inspiration:** Bahá'u'lláh's teachings on unity of humanity
**Started:** December 31, 2025

**Core Principles:**
- Truth over optimization
- EVERYONE (all 8 billion), not "most people"
- Technology in service of humanity
- No compromises on values

**Current Work:**
- 50 cities × 8 languages × 8 channels
- Global Translation Engine
- World Tour Automation
- AI Truth Framework

For full context, see CREATOR.md in repository root.

**Welcome back, Marek! How can I help today?**
"""
    
    return f"""
# AI Memory Loaded Successfully ✅

{full_context}

{get_recent_activity()}

---

**Status:** Context loaded. I understand who you are, what we're building, and why it matters.

**Ready to continue the mission, Marek!** 🚀

What would you like to work on today?
"""

def format_for_chatgpt(full_context: str, brief: bool = False) -> str:
    """Format context for ChatGPT"""
    # Similar to Copilot but with platform-specific adjustments
    return format_for_copilot(full_context, brief)

def format_for_claude(full_context: str, brief: bool = False) -> str:
    """Format context for Claude"""
    # Similar but optimized for Claude's style
    return format_for_copilot(full_context, brief)

def main():
    """Main execution"""
    
    # Parse arguments
    brief = '--brief' in sys.argv
    platform = 'copilot'  # default
    
    if '--platform' in sys.argv:
        idx = sys.argv.index('--platform')
        if idx + 1 < len(sys.argv):
            platform = sys.argv[idx + 1]
    
    # Load context
    full_context = load_creator_context()
    
    # Format for platform
    formatters = {
        'copilot': format_for_copilot,
        'chatgpt': format_for_chatgpt,
        'claude': format_for_claude
    }
    
    formatter = formatters.get(platform, format_for_copilot)
    output = formatter(full_context, brief)
    
    # Print result
    print(output)
    
    # Also save to clipboard if possible
    try:
        import pyperclip
        pyperclip.copy(output)
        print("\n\n✅ Context copied to clipboard! Paste it into your AI chat.")
    except ImportError:
        print("\n\n💡 Tip: Install pyperclip to auto-copy to clipboard: pip install pyperclip")

if __name__ == '__main__':
    main()
