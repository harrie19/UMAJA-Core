"""
Test AI Memory Persistence System
Tests the restore_ai_context.py script and related components
"""

import sys
import json
import subprocess
from pathlib import Path

# Add root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_session_state_file_exists():
    """Test that .ai_session_state.json exists and is valid JSON"""
    state_file = Path(".ai_session_state.json")
    assert state_file.exists(), "Session state file not found"
    
    with open(state_file, 'r', encoding='utf-8') as f:
        state = json.load(f)
    
    # Check required fields
    assert "last_updated" in state, "Missing last_updated field"
    assert "session_id" in state, "Missing session_id field"
    assert "active_mission" in state, "Missing active_mission field"
    assert "current_tasks" in state, "Missing current_tasks field"
    assert "repository_state" in state, "Missing repository_state field"
    
    print("✅ Session state file is valid")


def test_mission_log_exists():
    """Test that MISSION_LOG.md exists"""
    log_file = Path("docs/MISSION_LOG.md")
    assert log_file.exists(), "Mission log file not found"
    
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert "# UMAJA Mission Log" in content, "Mission log header not found"
    assert "2026-01-03" in content, "Current date not found in log"
    
    print("✅ Mission log file exists and has content")


def test_context_snapshots_exists():
    """Test that AI_CONTEXT_SNAPSHOTS.md exists"""
    snapshot_file = Path("docs/AI_CONTEXT_SNAPSHOTS.md")
    assert snapshot_file.exists(), "Context snapshots file not found"
    
    with open(snapshot_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert "# AI Context Snapshots" in content, "Snapshots header not found"
    assert "## Latest Snapshot:" in content, "Latest snapshot section not found"
    
    print("✅ Context snapshots file exists and has content")


def test_restore_script_exists():
    """Test that restore_ai_context.py exists and is executable"""
    script_file = Path("scripts/restore_ai_context.py")
    assert script_file.exists(), "Restore script not found"
    
    # Check it's a Python file
    with open(script_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert "#!/usr/bin/env python3" in content or "import" in content, "Not a valid Python script"
    assert "def main(" in content, "Missing main function"
    
    print("✅ Restore script exists and looks valid")


def test_restore_script_runs():
    """Test that restore_ai_context.py runs without errors"""
    result = subprocess.run(
        ["python", "scripts/restore_ai_context.py", "--compact"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Restore script failed: {result.stderr}"
    assert len(result.stdout) > 0, "Restore script produced no output"
    assert "CURRENT MISSION" in result.stdout, "Output missing mission section"
    
    print("✅ Restore script runs successfully")
    print(f"   Output length: {len(result.stdout)} characters")


def test_restore_script_json_format():
    """Test that restore_ai_context.py can output JSON"""
    result = subprocess.run(
        ["python", "scripts/restore_ai_context.py", "--format", "json"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Restore script failed: {result.stderr}"
    
    # Parse JSON output
    output = json.loads(result.stdout)
    assert "last_updated" in output, "JSON output missing last_updated"
    assert "active_mission" in output, "JSON output missing active_mission"
    
    print("✅ Restore script JSON output is valid")


def test_memory_system_integration():
    """Test full integration of memory persistence system"""
    # Load session state
    with open(".ai_session_state.json", 'r', encoding='utf-8') as f:
        state = json.load(f)
    
    # Check mission is tracked
    assert state["active_mission"]["name"] == "AI Memory Persistence System", "Mission name mismatch"
    assert state["active_mission"]["status"] in ["in_progress", "complete"], "Mission status should be tracked"
    
    # Check memory system components are tracked
    metrics = state.get("metrics", {})
    assert metrics.get("memory_system_components") == 4, "Should have 4 memory components"
    assert metrics.get("context_preservation_active") == True, "Context preservation should be active"
    
    # Run restore script
    result = subprocess.run(
        ["python", "scripts/restore_ai_context.py"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, "Integration test failed"
    assert "AI CONTEXT RESTORATION" in result.stdout, "Missing restoration header"
    assert "AI Memory Persistence System" in result.stdout, "Mission not in output"
    
    print("✅ Memory system integration test passed")


if __name__ == "__main__":
    print("=" * 80)
    print("Testing AI Memory Persistence System")
    print("=" * 80)
    print()
    
    test_session_state_file_exists()
    test_mission_log_exists()
    test_context_snapshots_exists()
    test_restore_script_exists()
    test_restore_script_runs()
    test_restore_script_json_format()
    test_memory_system_integration()
    
    print()
    print("=" * 80)
    print("✅ ALL MEMORY PERSISTENCE TESTS PASSED")
    print("=" * 80)
