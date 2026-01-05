#!/usr/bin/env python3
"""
AI Context Restoration Script for UMAJA
Restores full context for any AI session
"""
import sys
import json
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from memory.engine import MemoryEngine
from memory.session_manager import SessionManager


def restore_context(format_type: str = "markdown", compact: bool = False, query: str = "current context") -> str:
    """Restore AI context from memory and session state"""
    
    # Initialize managers
    memory_engine = MemoryEngine()
    session_manager = SessionManager()
    
    # Load session
    session = session_manager.load_session()
    
    # Build context from memories
    context = memory_engine.build_context(query, max_memories=20 if not compact else 5)
    
    if format_type == "json":
        return json.dumps({
            "session": session.to_dict(),
            "context": {
                "summary": context.summary,
                "entities": context.entities,
                "topics": context.topics,
                "confidence": context.confidence,
                "memory_count": len(context.memories)
            }
        }, indent=2)
    
    # Markdown format
    output = []
    
    if not compact:
        output.append("# UMAJA AI Context Restoration")
        output.append("")
        output.append(f"**Session ID**: {session.session_id}")
        output.append(f"**Started**: {session.started_at}")
        output.append(f"**Last Updated**: {session.last_updated}")
        output.append("")
    
    # Active Missions
    if session.active_missions:
        output.append("## Active Missions")
        for mission in session.active_missions:
            output.append(f"- {mission}")
        output.append("")
    
    # Pending Tasks
    if session.pending_tasks:
        output.append("## Pending Tasks")
        for task in session.pending_tasks:
            output.append(f"- [ ] {task}")
        output.append("")
    
    # Completed Tasks
    if session.completed_tasks and not compact:
        output.append("## Completed Tasks")
        for task in session.completed_tasks[:10]:  # Last 10
            output.append(f"- [x] {task}")
        output.append("")
    
    # Context Summary
    output.append("## Context Summary")
    output.append(f"**Confidence**: {context.confidence:.1%}")
    output.append("")
    output.append(context.summary)
    output.append("")
    
    # Entities
    if context.entities:
        output.append("## Key Entities")
        output.append(", ".join(context.entities[:20]))
        output.append("")
    
    # Topics
    if context.topics:
        output.append("## Topics")
        output.append(", ".join(context.topics))
        output.append("")
    
    # Recent Decisions
    if session.decisions and not compact:
        output.append("## Recent Decisions")
        for decision in session.decisions[-5:]:  # Last 5
            output.append(f"- **{decision['decision']}**: {decision['rationale']}")
        output.append("")
    
    # Repository Snapshot
    if session.repository_snapshot and not compact:
        output.append("## Repository State")
        snap = session.repository_snapshot
        output.append(f"- **Branch**: {snap.get('branch', 'unknown')}")
        output.append(f"- **Last Commit**: {snap.get('last_commit', 'unknown')[:8]}")
        if snap.get('modified_files'):
            output.append(f"- **Modified Files**: {len(snap['modified_files'])}")
        output.append("")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="Restore AI context for UMAJA project"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format"
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Compact output (less detail)"
    )
    parser.add_argument(
        "--query",
        default="current context",
        help="Query for context retrieval"
    )
    
    args = parser.parse_args()
    
    try:
        output = restore_context(
            format_type=args.format,
            compact=args.compact,
            query=args.query
        )
        print(output)
    except Exception as e:
        print(f"Error restoring context: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
