"""
Natural Language Command Processor
===================================

Translates natural language commands (German and English) into structured actions.

Examples:
- "Merge PR #90" → {'action': 'merge_pr', 'pr_number': 90}
- "Schließe alte PRs" → {'action': 'close_old_prs'}
- "Deploy to Railway" → {'action': 'deploy', 'platform': 'railway'}
- "Fix conflicts in PR #89" → {'action': 'fix_conflicts', 'pr_number': 89}
"""

import re
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import json
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CommandIntent:
    """Represents a parsed command intent"""
    action: str
    confidence: float
    parameters: Dict[str, Any]
    original_text: str
    language: str = 'en'


class NLCommandProcessor:
    """
    Natural Language Command Processor
    Understands both German and English commands
    """
    
    def __init__(self, patterns_path: Optional[str] = None):
        """
        Initialize command processor
        
        Args:
            patterns_path: Path to command patterns JSON file
        """
        self.patterns_path = patterns_path or "data/command_patterns.json"
        self.command_patterns = self._load_patterns()
        
        logger.info("Natural Language Command Processor initialized")
    
    def _load_patterns(self) -> Dict[str, List[Dict]]:
        """Load command patterns from file or use defaults"""
        patterns_file = Path(self.patterns_path)
        
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load patterns from {patterns_file}: {e}")
        
        # Default patterns
        return {
            "merge_pr": [
                # English
                {"pattern": r"merge\s+pr\s+#?(\d+)", "lang": "en", "groups": ["pr_number"]},
                {"pattern": r"merge\s+pull\s+request\s+#?(\d+)", "lang": "en", "groups": ["pr_number"]},
                {"pattern": r"accept\s+pr\s+#?(\d+)", "lang": "en", "groups": ["pr_number"]},
                # German
                {"pattern": r"merge\s+pr\s+#?(\d+)", "lang": "de", "groups": ["pr_number"]},
                {"pattern": r"pr\s+#?(\d+)\s+mergen", "lang": "de", "groups": ["pr_number"]},
                {"pattern": r"akzeptiere\s+pr\s+#?(\d+)", "lang": "de", "groups": ["pr_number"]},
            ],
            "close_pr": [
                # English
                {"pattern": r"close\s+pr\s+#?(\d+)", "lang": "en", "groups": ["pr_number"]},
                {"pattern": r"reject\s+pr\s+#?(\d+)", "lang": "en", "groups": ["pr_number"]},
                # German
                {"pattern": r"schließe\s+pr\s+#?(\d+)", "lang": "de", "groups": ["pr_number"]},
                {"pattern": r"pr\s+#?(\d+)\s+schließen", "lang": "de", "groups": ["pr_number"]},
            ],
            "close_old_prs": [
                # English
                {"pattern": r"close\s+old\s+prs", "lang": "en", "groups": []},
                {"pattern": r"cleanup\s+prs", "lang": "en", "groups": []},
                # German
                {"pattern": r"schließe\s+alte\s+prs", "lang": "de", "groups": []},
                {"pattern": r"alte\s+prs\s+aufräumen", "lang": "de", "groups": []},
            ],
            "fix_conflicts": [
                # English
                {"pattern": r"fix\s+conflicts?(?:\s+in)?\s+pr\s+#?(\d+)", "lang": "en", "groups": ["pr_number"]},
                {"pattern": r"resolve\s+conflicts?(?:\s+in)?\s+pr\s+#?(\d+)", "lang": "en", "groups": ["pr_number"]},
                # German
                {"pattern": r"konflikte\s+lösen(?:\s+in)?\s+pr\s+#?(\d+)", "lang": "de", "groups": ["pr_number"]},
                {"pattern": r"behebe\s+konflikte(?:\s+in)?\s+pr\s+#?(\d+)", "lang": "de", "groups": ["pr_number"]},
            ],
            "deploy": [
                # English
                {"pattern": r"deploy(?:\s+to)?\s+(railway|render|production)", "lang": "en", "groups": ["platform"]},
                {"pattern": r"push\s+to\s+(railway|render|production)", "lang": "en", "groups": ["platform"]},
                # German
                {"pattern": r"deploy(?:\s+zu)?\s+(railway|render|produktion)", "lang": "de", "groups": ["platform"]},
                {"pattern": r"veröffentliche\s+auf\s+(railway|render)", "lang": "de", "groups": ["platform"]},
            ],
            "status": [
                # English
                {"pattern": r"(?:what'?s|what is)\s+the\s+status", "lang": "en", "groups": []},
                {"pattern": r"show\s+status", "lang": "en", "groups": []},
                {"pattern": r"status\s+check", "lang": "en", "groups": []},
                # German
                {"pattern": r"(?:wie ist|was ist)\s+(?:der|die)\s+status", "lang": "de", "groups": []},
                {"pattern": r"zeige\s+status", "lang": "de", "groups": []},
                {"pattern": r"status\s+prüfen", "lang": "de", "groups": []},
            ],
            "create_issue": [
                # English
                {"pattern": r"create\s+issue[:\s]+(.+)", "lang": "en", "groups": ["title"]},
                {"pattern": r"new\s+issue[:\s]+(.+)", "lang": "en", "groups": ["title"]},
                # German
                {"pattern": r"erstelle\s+issue[:\s]+(.+)", "lang": "de", "groups": ["title"]},
                {"pattern": r"neues\s+issue[:\s]+(.+)", "lang": "de", "groups": ["title"]},
            ],
            "create_feature": [
                # English
                {"pattern": r"create\s+feature[:\s]+(.+)", "lang": "en", "groups": ["description"]},
                {"pattern": r"implement[:\s]+(.+)", "lang": "en", "groups": ["description"]},
                # German
                {"pattern": r"erstelle\s+feature[:\s]+(.+)", "lang": "de", "groups": ["description"]},
                {"pattern": r"implementiere[:\s]+(.+)", "lang": "de", "groups": ["description"]},
            ],
            "help": [
                # English
                {"pattern": r"help", "lang": "en", "groups": []},
                {"pattern": r"what\s+can\s+you\s+do", "lang": "en", "groups": []},
                # German
                {"pattern": r"hilfe", "lang": "de", "groups": []},
                {"pattern": r"was\s+kannst\s+du", "lang": "de", "groups": []},
            ],
        }
    
    def parse_command(self, text: str) -> Optional[CommandIntent]:
        """
        Parse natural language command
        
        Args:
            text: User input text
            
        Returns:
            CommandIntent or None if no match found
        """
        text_lower = text.lower().strip()
        
        # Try to match against all patterns
        best_match = None
        best_confidence = 0.0
        
        for action, patterns in self.command_patterns.items():
            for pattern_def in patterns:
                pattern = pattern_def['pattern']
                match = re.search(pattern, text_lower, re.IGNORECASE)
                
                if match:
                    # Calculate confidence based on match quality
                    confidence = len(match.group(0)) / len(text_lower)
                    confidence = min(1.0, confidence * 1.2)  # Boost confidence slightly
                    
                    if confidence > best_confidence:
                        # Extract parameters from regex groups
                        parameters = {}
                        if pattern_def.get('groups'):
                            for i, group_name in enumerate(pattern_def['groups'], start=1):
                                if i <= len(match.groups()):
                                    value = match.group(i)
                                    # Convert to int if it looks like a number
                                    if group_name.endswith('_number') and value.isdigit():
                                        value = int(value)
                                    parameters[group_name] = value
                        
                        best_match = CommandIntent(
                            action=action,
                            confidence=confidence,
                            parameters=parameters,
                            original_text=text,
                            language=pattern_def['lang']
                        )
                        best_confidence = confidence
        
        if best_match:
            logger.info(f"Parsed command: {best_match.action} (confidence: {best_match.confidence:.2f})")
        else:
            logger.warning(f"Could not parse command: {text}")
        
        return best_match
    
    def get_help_text(self, language: str = 'en') -> str:
        """
        Get help text showing available commands
        
        Args:
            language: Language code ('en' or 'de')
            
        Returns:
            Help text string
        """
        if language == 'de':
            help_text = """
🤖 **UMAJA Autonomer Agent - Verfügbare Befehle**

**PR Operationen:**
- `Merge PR #90` - PR zusammenführen
- `Schließe PR #89` - PR schließen
- `Schließe alte PRs` - Alte PRs aufräumen
- `Konflikte lösen in PR #87` - Merge-Konflikte beheben

**Deployment:**
- `Deploy zu Railway` - Auf Railway veröffentlichen
- `Deploy zu Render` - Auf Render veröffentlichen

**Code & Features:**
- `Erstelle Feature: Neues Login-System` - Feature implementieren
- `Erstelle Issue: Bug im Login` - Neues Issue anlegen

**Status:**
- `Zeige Status` - System-Status anzeigen
- `Was ist der Status?` - Status prüfen

**Hilfe:**
- `Hilfe` - Diese Hilfe anzeigen

Sag einfach "Akzeptieren" oder klicke auf Accept, und ich erledige alles! 🚀
"""
        else:  # English
            help_text = """
🤖 **UMAJA Autonomous Agent - Available Commands**

**PR Operations:**
- `Merge PR #90` - Merge a pull request
- `Close PR #89` - Close a pull request
- `Close old PRs` - Cleanup old pull requests
- `Fix conflicts in PR #87` - Resolve merge conflicts

**Deployment:**
- `Deploy to Railway` - Deploy to Railway
- `Deploy to Render` - Deploy to Render
- `Deploy to production` - Deploy to production

**Code & Features:**
- `Create feature: New login system` - Implement a feature
- `Create issue: Bug in login` - Create a new issue

**Status:**
- `Show status` - Show system status
- `What's the status?` - Check status

**Help:**
- `Help` - Show this help

Just say "Accept" or click Accept button, and I'll handle everything! 🚀
"""
        
        return help_text.strip()
    
    def save_patterns(self):
        """Save current patterns to file"""
        patterns_file = Path(self.patterns_path)
        patterns_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(patterns_file, 'w', encoding='utf-8') as f:
            json.dump(self.command_patterns, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Command patterns saved to {patterns_file}")


# Example usage
if __name__ == "__main__":
    processor = NLCommandProcessor()
    
    # Test commands
    test_commands = [
        "Merge PR #90",
        "merge pull request #123",
        "Schließe alte PRs",
        "Deploy to Railway",
        "Fix conflicts in PR #87",
        "Create feature: Add holographic AI visualization",
        "What's the status?",
        "Hilfe",
    ]
    
    print("🧪 Testing Natural Language Command Processor\n")
    
    for cmd in test_commands:
        print(f"Input: {cmd}")
        intent = processor.parse_command(cmd)
        if intent:
            print(f"  → Action: {intent.action}")
            print(f"  → Confidence: {intent.confidence:.2%}")
            print(f"  → Parameters: {intent.parameters}")
            print(f"  → Language: {intent.language}")
        else:
            print("  → ❌ Not understood")
        print()
    
    # Show help
    print("\n" + "="*60)
    print(processor.get_help_text('en'))
