#!/usr/bin/env python3
"""
Morning Alignment Script - Daily "Prayer" for UMAJA-Core
Value check, humility reminder, gratitude practice

Run before any major operation to ensure alignment with mission and principles.
"""

import sys
from datetime import datetime
from pathlib import Path

# Colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_header():
    """Print morning alignment header"""
    print()
    print("=" * 70)
    print(f"{BOLD}{BLUE}🌅 UMAJA-Core Morning Alignment{RESET}")
    print(f"   {datetime.now().strftime('%A, %B %d, %Y - %H:%M')}")
    print("=" * 70)
    print()

def check_mission_alignment():
    """Remind of core mission"""
    print(f"{BOLD}🎯 Mission Check{RESET}")
    print()
    print("   Our mission: Bring smiles to 8 billion people")
    print("   Our focus: DEPLOYMENT, not features")
    print("   Our approach: Truth over optimization")
    print()
    
    response = input(f"{YELLOW}   Does today's work serve this mission? (yes/no): {RESET}").strip().lower()
    
    if response != 'yes':
        print(f"\n{YELLOW}   ⚠️  Consider if today's work truly aligns with the mission.{RESET}")
        print(f"{YELLOW}   Focus on what brings smiles, not what sounds impressive.{RESET}\n")
        return False
    
    print(f"{GREEN}   ✅ Mission aligned!{RESET}\n")
    return True

def practice_humility():
    """Humility reminder"""
    print(f"{BOLD}🙏 Humility Practice{RESET}")
    print()
    print("   Remember:")
    print("   • We serve 8 billion people, not our ego")
    print("   • Simple solutions are often the best")
    print("   • We learn from every mistake")
    print("   • We celebrate wins together, humbly")
    print()
    
    input(f"{YELLOW}   Press Enter when you've reflected on this...{RESET}")
    print(f"{GREEN}   ✅ Humility acknowledged{RESET}\n")

def practice_gratitude():
    """Gratitude practice"""
    print(f"{BOLD}💝 Gratitude Moment{RESET}")
    print()
    print("   Today, I'm grateful for:")
    print("   • The opportunity to serve humanity")
    print("   • The tools and skills I have")
    print("   • The community supporting this work")
    print("   • The chance to spread smiles")
    print()
    
    personal = input(f"{YELLOW}   What are YOU grateful for today? (optional): {RESET}").strip()
    
    if personal:
        print(f"{GREEN}   ✨ Beautiful! {personal}{RESET}")
    
    print(f"{GREEN}   ✅ Gratitude practiced{RESET}\n")

def review_principles():
    """Review Bahá'í principles"""
    print(f"{BOLD}🕊️  Core Principles Review{RESET}")
    print()
    
    principles = [
        ("Truth over Optimization", "Deploy what WORKS, not what sounds impressive"),
        ("Deeds not Words", "Take action, stop talking about it"),
        ("Service not Ego", "This is for 8 billion people, not for showing off"),
        ("Humility", "Start simple, improve incrementally, admit mistakes")
    ]
    
    for name, desc in principles:
        print(f"   ✓ {BOLD}{name}{RESET}: {desc}")
    
    print()
    input(f"{YELLOW}   Press Enter when you've internalized these...{RESET}")
    print(f"{GREEN}   ✅ Principles reviewed{RESET}\n")

def check_emergency_stop():
    """Check if emergency stop is active"""
    emergency_file = Path(__file__).parent.parent / '.github' / 'emergency_stop.json'
    
    if emergency_file.exists():
        print(f"{BOLD}🛑 EMERGENCY STOP ACTIVE!{RESET}")
        print()
        print(f"   Emergency stop file exists at: {emergency_file}")
        print("   All AI operations should be halted.")
        print("   Contact human operator before proceeding.")
        print()
        return False
    
    return True

def check_autonomy_rules():
    """Check autonomy rules file exists"""
    rules_file = Path(__file__).parent.parent / '.github' / 'AUTONOMY_RULES.yaml'
    
    if not rules_file.exists():
        print(f"{YELLOW}   ⚠️  AUTONOMY_RULES.yaml not found{RESET}")
        print(f"   Create this file to define AI agent boundaries.\n")
        return False
    
    print(f"{GREEN}   ✅ Autonomy rules in place{RESET}\n")
    return True

def main():
    """Main alignment flow"""
    print_header()
    
    # Check emergency stop first
    if not check_emergency_stop():
        print("=" * 70)
        print(f"{BOLD}Alignment FAILED - Emergency stop active{RESET}")
        print("=" * 70)
        return 1
    
    # Run alignment checks
    mission_ok = check_mission_alignment()
    practice_humility()
    practice_gratitude()
    review_principles()
    rules_ok = check_autonomy_rules()
    
    # Summary
    print("=" * 70)
    print(f"{BOLD}📋 Alignment Summary{RESET}")
    print("=" * 70)
    print()
    
    if mission_ok and rules_ok:
        print(f"{GREEN}{BOLD}✅ ALIGNMENT COMPLETE{RESET}")
        print()
        print("You are aligned with:")
        print("  • Mission: Serve 8 billion people")
        print("  • Values: Truth, Service, Humility")
        print("  • Focus: Deeds over words")
        print()
        print("\"Let deeds, not words, be your adorning.\" - Bahá'u'lláh")
        print()
        print(f"{GREEN}Ready to spread smiles! 🌍{RESET}")
        print("=" * 70)
        return 0
    else:
        print(f"{YELLOW}⚠️  ALIGNMENT INCOMPLETE{RESET}")
        print()
        print("Review the concerns above before proceeding.")
        print("=" * 70)
        return 1

if __name__ == '__main__':
    sys.exit(main())
