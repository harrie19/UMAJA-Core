#!/usr/bin/env python3
"""
AI Context Restoration Script
Generates compact AI context summary for new sessions to restore full context.

Usage:
    python scripts/restore_ai_context.py
    python scripts/restore_ai_context.py --format json
    python scripts/restore_ai_context.py --compact
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import argparse


def load_session_state():
    """Load the current session state from .ai_session_state.json"""
    state_file = Path(".ai_session_state.json")
    if not state_file.exists():
        return None
    
    try:
        with open(state_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Session state file not found at {state_file}")
        print("   Check if .ai_session_state.json exists in the repository root.")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in session state file: {e}")
        print("   Check if .ai_session_state.json contains valid JSON.")
        return None
    except Exception as e:
        print(f"❌ Error loading session state ({type(e).__name__}): {e}")
        return None


def load_latest_snapshot():
    """Load the latest snapshot from AI_CONTEXT_SNAPSHOTS.md"""
    snapshot_file = Path("docs/AI_CONTEXT_SNAPSHOTS.md")
    if not snapshot_file.exists():
        return None
    
    try:
        with open(snapshot_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract the latest snapshot (first one after "## Latest Snapshot:")
            if "## Latest Snapshot:" in content:
                lines = content.split("\n")
                snapshot_lines = []
                in_snapshot = False
                for line in lines:
                    if "## Latest Snapshot:" in line:
                        in_snapshot = True
                        snapshot_lines.append(line)
                    elif in_snapshot:
                        if line.startswith("## ") and "Snapshot:" in line:
                            break
                        snapshot_lines.append(line)
                return "\n".join(snapshot_lines)
            return content[:2000]  # Return first 2000 chars if no latest snapshot found
    except FileNotFoundError:
        print(f"❌ Error: Context snapshots file not found at {snapshot_file}")
        print("   Check if docs/AI_CONTEXT_SNAPSHOTS.md exists.")
        return None
    except Exception as e:
        print(f"❌ Error loading snapshot ({type(e).__name__}): {e}")
        print("   Check if docs/AI_CONTEXT_SNAPSHOTS.md is readable.")
        return None


def load_recent_log_entries(hours=24):
    """Load recent entries from MISSION_LOG.md"""
    log_file = Path("docs/MISSION_LOG.md")
    if not log_file.exists():
        return None
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Get today's section
            today = datetime.now().strftime("%Y-%m-%d")
            if f"## {today}" in content:
                sections = content.split("##")
                for section in sections:
                    if today in section:
                        return f"## {section}"
            # Return last 1500 chars if today's section not found
            return content[-1500:]
    except FileNotFoundError:
        print(f"❌ Error: Mission log file not found at {log_file}")
        print("   Check if docs/MISSION_LOG.md exists.")
        return None
    except Exception as e:
        print(f"❌ Error loading mission log ({type(e).__name__}): {e}")
        print("   Check if docs/MISSION_LOG.md is readable.")
        return None


def generate_context_summary(compact=False):
    """Generate formatted context summary for AI consumption"""
    state = load_session_state()
    snapshot = load_latest_snapshot()
    recent_log = load_recent_log_entries()
    
    if not state:
        return "❌ Error: Could not load session state. Ensure .ai_session_state.json exists."
    
    # Build the summary
    lines = []
    
    if not compact:
        lines.extend([
            "🧠 AI CONTEXT RESTORATION",
            "═" * 80,
            "",
            f"📅 Restoration Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}",
            "",
        ])
    
    # Current Mission
    lines.extend([
        "🎯 CURRENT MISSION",
        "─" * 80,
    ])
    
    if state.get("active_mission"):
        mission = state["active_mission"]
        lines.extend([
            f"Name: {mission.get('name', 'Unknown')}",
            f"Status: {mission.get('status', 'Unknown')}",
            f"Phase: {mission.get('phase', 'Unknown')}",
            f"Started: {mission.get('started', 'Unknown')}",
            f"Agent Mode: {mission.get('agent_mode', 'Unknown')}",
            "",
        ])
    
    # Active Tasks
    if state.get("current_tasks"):
        lines.extend([
            "📋 ACTIVE TASKS",
            "─" * 80,
        ])
        for i, task in enumerate(state["current_tasks"], 1):
            lines.append(f"{i}. {task.get('task', 'Unknown task')}")
            lines.append(f"   Status: {task.get('status', 'unknown')}")
            if task.get("priority"):
                lines.append(f"   Priority: {task.get('priority')}")
            if task.get("pr_url"):
                lines.append(f"   PR: {task.get('pr_url')}")
            lines.append("")
    
    # Key Decisions
    if state.get("key_decisions"):
        lines.extend([
            "🔑 KEY DECISIONS",
            "─" * 80,
        ])
        for decision in state["key_decisions"][-5:]:  # Last 5 decisions
            lines.append(f"[{decision.get('timestamp', 'Unknown')}]")
            lines.append(f"Decision: {decision.get('decision', 'Unknown')}")
            lines.append(f"Rationale: {decision.get('rationale', 'Unknown')}")
            lines.append("")
    
    # Repository State
    if state.get("repository_state"):
        lines.extend([
            "📊 REPOSITORY STATE",
            "─" * 80,
        ])
        repo = state["repository_state"]
        for key, value in repo.items():
            lines.append(f"{key.replace('_', ' ').title()}: {value}")
        lines.append("")
    
    # User Preferences
    if state.get("user_preferences"):
        lines.extend([
            "👤 USER PREFERENCES",
            "─" * 80,
        ])
        prefs = state["user_preferences"]
        for key, value in prefs.items():
            lines.append(f"{key.replace('_', ' ').title()}: {value}")
        lines.append("")
    
    # Latest Snapshot
    if snapshot and not compact:
        lines.extend([
            "📸 LATEST SNAPSHOT",
            "─" * 80,
            snapshot[:1000] if len(snapshot) > 1000 else snapshot,
            "",
        ])
    
    # Recent Log
    if recent_log and not compact:
        lines.extend([
            "📝 RECENT LOG (Last 24h)",
            "─" * 80,
            recent_log[:1000] if len(recent_log) > 1000 else recent_log,
            "",
        ])
    
    # Immediate Next Actions
    if state.get("next_actions"):
        lines.extend([
            "🎯 IMMEDIATE NEXT ACTIONS",
            "─" * 80,
        ])
        for i, action in enumerate(state["next_actions"][:5], 1):
            lines.append(f"{i}. {action.get('action', 'Unknown')}")
            lines.append(f"   Priority: {action.get('priority', 'unknown')}")
            lines.append(f"   Status: {action.get('status', 'unknown')}")
            if action.get("reason"):
                lines.append(f"   Reason: {action.get('reason')}")
            lines.append("")
    
    # Agent Mode
    if state.get("active_mission", {}).get("agent_mode"):
        lines.extend([
            "🤖 AGENT MODE",
            "─" * 80,
            f"Current Mode: {state['active_mission']['agent_mode']}",
            "",
        ])
    
    # Deployment Status
    if state.get("deployment_status"):
        lines.extend([
            "🚀 DEPLOYMENT STATUS",
            "─" * 80,
        ])
        deploy = state["deployment_status"]
        if deploy.get("backend"):
            backend = deploy["backend"]
            lines.append(f"Backend: {backend.get('status', 'unknown')} on {backend.get('platform', 'unknown')}")
            lines.append(f"  URL: {backend.get('url', 'unknown')}")
        if deploy.get("frontend"):
            frontend = deploy["frontend"]
            lines.append(f"Frontend: {frontend.get('status', 'unknown')} on {frontend.get('platform', 'unknown')}")
            lines.append(f"  URL: {frontend.get('url', 'unknown')}")
        lines.append("")
    
    # Quick Checks
    lines.extend([
        "✅ QUICK CHECKS",
        "─" * 80,
        "- [ ] Context loaded",
        "- [ ] Mission understood",
        "- [ ] Ready to continue",
        "",
    ])
    
    # Response Template
    if not compact:
        lines.extend([
            "💬 RESPONSE TEMPLATE",
            "─" * 80,
            "Welcome back! I've restored my context from the Memory Persistence System.",
            "",
            f"Current Mission: {state.get('active_mission', {}).get('name', 'Unknown')}",
            f"Status: {state.get('active_mission', {}).get('status', 'Unknown')}",
            "",
            "I'm ready to continue. What would you like me to work on?",
            "",
        ])
    
    if not compact:
        lines.extend([
            "═" * 80,
            "🧠 Context restoration complete. AI is now aware of full project history.",
            "═" * 80,
        ])
    
    return "\n".join(lines)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Restore AI context from memory persistence system")
    parser.add_argument("--format", choices=["text", "json"], default="text", 
                       help="Output format (default: text)")
    parser.add_argument("--compact", action="store_true",
                       help="Generate compact output")
    args = parser.parse_args()
    
    if args.format == "json":
        # JSON output - just dump the session state
        state = load_session_state()
        if state:
            print(json.dumps(state, indent=2))
        else:
            print(json.dumps({"error": "Could not load session state"}, indent=2))
            sys.exit(1)
    else:
        # Text output - formatted summary
        summary = generate_context_summary(compact=args.compact)
        print(summary)


if __name__ == "__main__":
    main()
