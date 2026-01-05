"""
Session State Manager for UMAJA
Tracks active missions, tasks, and context across restarts
"""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field


@dataclass
class SessionState:
    """Represents the current AI session state"""
    session_id: str
    started_at: str
    last_updated: str
    active_missions: List[str] = field(default_factory=list)
    completed_tasks: List[str] = field(default_factory=list)
    pending_tasks: List[str] = field(default_factory=list)
    decisions: List[Dict[str, Any]] = field(default_factory=list)
    repository_snapshot: Dict[str, Any] = field(default_factory=dict)
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return asdict(self)


class SessionManager:
    """
    Manages AI session state persistence
    Enables context restoration across restarts
    """
    
    def __init__(self, state_file: str = ".ai_session_state.json", repo_path: Optional[Path] = None):
        self.state_file = Path(state_file)
        self.repo_path = repo_path or Path.cwd()
        self.current_state: Optional[SessionState] = None
    
    def load_session(self) -> SessionState:
        """Load existing session or create new one"""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    data = json.load(f)
                self.current_state = SessionState(**data)
                
                # Update last_updated
                self.current_state.last_updated = datetime.now(timezone.utc).isoformat()
                
                return self.current_state
            except Exception as e:
                print(f"Warning: Could not load session state: {e}")
        
        # Create new session
        self.current_state = SessionState(
            session_id=f"session_{datetime.now(timezone.utc).timestamp()}",
            started_at=datetime.now(timezone.utc).isoformat(),
            last_updated=datetime.now(timezone.utc).isoformat()
        )
        
        return self.current_state
    
    def save_session(self, state: Optional[SessionState] = None) -> None:
        """Save session state to disk"""
        if state is None:
            state = self.current_state
        
        if state is None:
            return
        
        # Update timestamp
        state.last_updated = datetime.now(timezone.utc).isoformat()
        
        # Save to file
        with open(self.state_file, 'w') as f:
            json.dump(state.to_dict(), f, indent=2)
    
    def add_mission(self, mission: str) -> None:
        """Add an active mission"""
        if self.current_state is None:
            self.load_session()
        
        if mission not in self.current_state.active_missions:
            self.current_state.active_missions.append(mission)
            self.save_session()
    
    def complete_task(self, task: str) -> None:
        """Mark a task as completed"""
        if self.current_state is None:
            self.load_session()
        
        # Move from pending to completed
        if task in self.current_state.pending_tasks:
            self.current_state.pending_tasks.remove(task)
        
        if task not in self.current_state.completed_tasks:
            self.current_state.completed_tasks.append(task)
        
        self.save_session()
    
    def add_pending_task(self, task: str) -> None:
        """Add a pending task"""
        if self.current_state is None:
            self.load_session()
        
        if task not in self.current_state.pending_tasks:
            self.current_state.pending_tasks.append(task)
            self.save_session()
    
    def record_decision(self, decision: str, rationale: str, context: Optional[Dict] = None) -> None:
        """Record an AI decision for audit trail"""
        if self.current_state is None:
            self.load_session()
        
        decision_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "decision": decision,
            "rationale": rationale,
            "context": context or {}
        }
        
        self.current_state.decisions.append(decision_record)
        self.save_session()
    
    def update_repository_snapshot(self) -> None:
        """Update snapshot of repository state"""
        if self.current_state is None:
            self.load_session()
        
        snapshot = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "branch": self._get_current_branch(),
            "last_commit": self._get_last_commit(),
            "modified_files": self._get_modified_files()
        }
        
        self.current_state.repository_snapshot = snapshot
        self.save_session()
    
    def set_preference(self, key: str, value: Any) -> None:
        """Set a user preference"""
        if self.current_state is None:
            self.load_session()
        
        self.current_state.user_preferences[key] = value
        self.save_session()
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a user preference"""
        if self.current_state is None:
            self.load_session()
        
        return self.current_state.user_preferences.get(key, default)
    
    def _get_current_branch(self) -> str:
        """Get current git branch"""
        try:
            import subprocess
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                cwd=str(self.repo_path)
            )
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except Exception:
            return "unknown"
    
    def _get_last_commit(self) -> str:
        """Get last commit hash"""
        try:
            import subprocess
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                cwd=str(self.repo_path)
            )
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except Exception:
            return "unknown"
    
    def _get_modified_files(self) -> List[str]:
        """Get list of modified files"""
        try:
            import subprocess
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=str(self.repo_path)
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                return [line[3:] for line in lines if line]
            return []
        except Exception:
            return []
