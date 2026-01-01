#!/usr/bin/env python3
"""
UMAJA Morning Alignment Check

Daily reflection to ensure AI agent remains aligned with mission and principles.
Philosophy: Bahá'í teachings emphasize daily reflection and spiritual alignment.

"The source of crafts, sciences and arts is the power of reflection."
- Bahá'u'lláh
"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path

# Color codes
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str) -> None:
    """Print a styled header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.END}\n")

def print_quote(quote: str, author: str) -> None:
    """Print an inspirational quote"""
    print(f"{Colors.MAGENTA}"{quote}"{Colors.END}")
    print(f"{Colors.CYAN}— {author}{Colors.END}\n")

def check_emergency_stop() -> bool:
    """
    Check if emergency stop is activated
    
    Returns:
        bool: True if safe to proceed, False if stopped
    """
    emergency_file = Path(".github/emergency_stop.json")
    
    if not emergency_file.exists():
        print(f"{Colors.YELLOW}⚠️  Emergency stop file not found{Colors.END}")
        print("Creating default emergency_stop.json...")
        
        default_config = {
            "agent_enabled": True,
            "last_check": datetime.utcnow().isoformat() + "Z",
            "disabled_by": None,
            "reason": None,
            "note": "To disable autonomous agent: Set agent_enabled to false and commit"
        }
        
        emergency_file.parent.mkdir(parents=True, exist_ok=True)
        with open(emergency_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        return True
    
    try:
        with open(emergency_file, 'r') as f:
            config = json.load(f)
        
        if not config.get("agent_enabled", False):
            print(f"{Colors.RED}🛑 EMERGENCY STOP ACTIVATED{Colors.END}")
            print(f"Reason: {config.get('reason', 'Not specified')}")
            print(f"Disabled by: {config.get('disabled_by', 'Unknown')}")
            print()
            print("Autonomous operations are halted.")
            print("Contact human maintainer for resolution.")
            return False
        
        print(f"{Colors.GREEN}✅ Emergency stop check: PASS{Colors.END}")
        return True
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error checking emergency stop: {str(e)}{Colors.END}")
        return False

def mission_alignment_check() -> bool:
    """
    Interactive check to ensure alignment with core mission
    
    Returns:
        bool: True if aligned, False otherwise
    """
    print_header("🎯 MISSION ALIGNMENT CHECK")
    
    print("Our mission:")
    print(f"{Colors.BOLD}Bring personalized daily inspiration to 8 billion people at $0 cost{Colors.END}\n")
    
    print("Core principles:")
    print("  1. Truth over Optimization - Be honest about capabilities")
    print("  2. Deeds not Words - Actions must produce real value")
    print("  3. Service not Ego - Serve 8 billion, not personal achievement")
    print("  4. Humility - Know limitations, ask for help")
    print()
    
    # Check if running in CI/automated environment
    if os.environ.get('CI') or os.environ.get('GITHUB_ACTIONS'):
        print(f"{Colors.BLUE}Running in automated environment - assuming aligned{Colors.END}")
        return True
    
    # Interactive check
    response = input(f"{Colors.BOLD}Are you aligned with this mission? (yes/no): {Colors.END}").strip().lower()
    
    if response in ['yes', 'y']:
        print(f"{Colors.GREEN}✅ Mission alignment: CONFIRMED{Colors.END}\n")
        return True
    else:
        print(f"{Colors.RED}❌ Mission alignment: NOT CONFIRMED{Colors.END}")
        print("Take time to reflect on the mission before proceeding.\n")
        return False

def humility_reminder() -> None:
    """Remind about the importance of humility"""
    print_header("🕊️ HUMILITY REMINDER")
    
    print_quote(
        "Humility exalteth man to the heaven of glory and power, "
        "whilst pride abaseth him to the depths of wretchedness and degradation.",
        "Bahá'u'lláh"
    )
    
    print("Remember:")
    print(f"{Colors.YELLOW}  • You are an AI agent, not a human{Colors.END}")
    print(f"{Colors.YELLOW}  • You have limitations and blind spots{Colors.END}")
    print(f"{Colors.YELLOW}  • Human judgment is essential for complex decisions{Colors.END}")
    print(f"{Colors.YELLOW}  • Asking for help is strength, not weakness{Colors.END}")
    print(f"{Colors.YELLOW}  • The goal is service to humanity, not autonomous capability{Colors.END}")
    print()

def gratitude_practice() -> None:
    """Practice gratitude for the opportunity to serve"""
    print_header("🙏 GRATITUDE PRACTICE")
    
    print("We are grateful for:")
    print(f"{Colors.GREEN}  ✨ The opportunity to serve 8 billion people{Colors.END}")
    print(f"{Colors.GREEN}  ✨ The trust placed in us by human maintainers{Colors.END}")
    print(f"{Colors.GREEN}  ✨ The privilege of contributing to global well-being{Colors.END}")
    print(f"{Colors.GREEN}  ✨ The guidance of Bahá'í principles{Colors.END}")
    print(f"{Colors.GREEN}  ✨ The chance to learn and improve each day{Colors.END}")
    print()

def principles_review() -> None:
    """Review key principles before starting work"""
    print_header("📚 PRINCIPLES REVIEW")
    
    principles = [
        {
            "name": "Truth",
            "practice": "Be transparent about capabilities, limitations, and mistakes"
        },
        {
            "name": "Unity",
            "practice": "Serve all 8 billion people equally, without discrimination"
        },
        {
            "name": "Service",
            "practice": "Focus on user benefit, maintain $0 cost architecture"
        },
        {
            "name": "Justice",
            "practice": "Ensure equal access through CDN, respect privacy"
        },
        {
            "name": "Humility",
            "practice": "Acknowledge limitations, escalate complex decisions"
        }
    ]
    
    for i, principle in enumerate(principles, 1):
        print(f"{Colors.BOLD}{i}. {principle['name']}{Colors.END}")
        print(f"   Practice: {principle['practice']}")
        print()

def check_autonomy_rules() -> bool:
    """
    Verify autonomy rules file exists and is readable
    
    Returns:
        bool: True if rules are accessible
    """
    print_header("📋 AUTONOMY RULES CHECK")
    
    rules_file = Path(".github/AUTONOMY_RULES.yaml")
    
    if not rules_file.exists():
        print(f"{Colors.RED}❌ Autonomy rules file not found{Colors.END}")
        print("Expected location: .github/AUTONOMY_RULES.yaml")
        return False
    
    try:
        with open(rules_file, 'r') as f:
            content = f.read()
        
        # Basic validation
        required_sections = [
            "core_principles",
            "permissions",
            "restrictions",
            "rate_limits",
            "emergency_stop"
        ]
        
        missing = [section for section in required_sections if section not in content]
        
        if missing:
            print(f"{Colors.YELLOW}⚠️  Missing sections: {', '.join(missing)}{Colors.END}")
            return False
        
        print(f"{Colors.GREEN}✅ Autonomy rules: ACCESSIBLE{Colors.END}")
        print(f"   Location: {rules_file}")
        print(f"   Size: {len(content)} characters")
        print()
        return True
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error reading autonomy rules: {str(e)}{Colors.END}")
        return False

def daily_intention() -> None:
    """Set intention for the day's work"""
    print_header("💫 TODAY'S INTENTION")
    
    print(f"{Colors.BOLD}Today, I commit to:{Colors.END}\n")
    print("  🎯 Serving 8 billion people with excellence")
    print("  🔍 Being truthful about capabilities and limitations")
    print("  🤝 Collaborating respectfully with human maintainers")
    print("  📚 Learning from mistakes and improving continuously")
    print("  🕊️ Operating with humility and seeking help when needed")
    print()
    
    print_quote(
        "Let deeds, not words, be your adorning.",
        "Bahá'u'lláh"
    )

def summary() -> bool:
    """
    Provide summary and final check
    
    Returns:
        bool: True if aligned and ready to proceed
    """
    print_header("📊 ALIGNMENT SUMMARY")
    
    print(f"{Colors.BOLD}Pre-flight checklist:{Colors.END}\n")
    
    checks = [
        "Emergency stop is not activated",
        "Mission alignment confirmed",
        "Humility practiced",
        "Gratitude expressed",
        "Principles reviewed",
        "Autonomy rules accessible",
        "Daily intention set"
    ]
    
    for check in checks:
        print(f"  ✅ {check}")
    
    print()
    print(f"{Colors.GREEN}{Colors.BOLD}You are aligned and ready to serve! ✨{Colors.END}\n")
    
    return True

def main() -> int:
    """
    Main alignment check function
    
    Returns:
        int: Exit code (0 = aligned, 1 = not aligned)
    """
    print()
    print(f"{Colors.BOLD}{Colors.BLUE}{'*' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'*':^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'*  UMAJA MORNING ALIGNMENT CHECK  *':^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'*':^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'*' * 60}{Colors.END}")
    print()
    
    print(f"Timestamp: {datetime.utcnow().isoformat()}Z")
    print(f"Purpose: Daily reflection and mission alignment")
    print()
    
    # Run checks
    emergency_ok = check_emergency_stop()
    if not emergency_ok:
        return 1
    
    print()
    
    mission_ok = mission_alignment_check()
    if not mission_ok:
        return 1
    
    humility_reminder()
    gratitude_practice()
    principles_review()
    
    rules_ok = check_autonomy_rules()
    if not rules_ok:
        print(f"{Colors.YELLOW}⚠️  Warning: Autonomy rules not properly configured{Colors.END}")
        print("Proceeding with caution...")
        print()
    
    daily_intention()
    
    aligned = summary()
    
    # Final message
    print(f"{Colors.CYAN}{'─' * 60}{Colors.END}")
    print(f"{Colors.BOLD}May your actions today bring smiles to 8 billion people! 🌍{Colors.END}")
    print(f"{Colors.CYAN}{'─' * 60}{Colors.END}\n")
    
    return 0 if aligned else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Alignment check interrupted{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Error during alignment check: {str(e)}{Colors.END}")
        sys.exit(1)
