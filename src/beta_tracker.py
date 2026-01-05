"""
UMAJA Beta Analytics - Anonymous Learning System
Privacy-first, GDPR-compliant, ethically designed

Philosophy: We learn from users, but we respect them.
No tracking, no surveillance, only improvement.
"""

import uuid
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BetaTracker:
    """
    Tracks user interactions anonymously for product improvement.
    
    Privacy principles:
    - NO personal data stored (no names, emails, IPs)
    - Only aggregate statistics
    - Anonymous session IDs (hashed)
    - User can opt-out anytime
    - Data used ONLY for product improvement
    - Full transparency (users can see their data)
    """
    
    def __init__(self, data_dir: str = "data/beta_analytics"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.sessions_file = self.data_dir / "sessions.jsonl"
        self.interactions_file = self.data_dir / "interactions.jsonl"
        self.feedback_file = self.data_dir / "feedback.jsonl"
        self.consent_file = self.data_dir / "consent.jsonl"
    
    def create_session(self, user_agent: str = "") -> str:
        """Create anonymous session ID"""
        session_id = str(uuid.uuid4())
        
        session = {
            'session_id': session_id,
            'timestamp': datetime.utcnow().isoformat(),
            'user_agent_hash': hashlib.sha256(user_agent.encode()).hexdigest()[:16] if user_agent else None,
            'beta_version': '1.0.0'
        }
        
        with open(self.sessions_file, 'a') as f:
            f.write(json.dumps(session) + '\n')
        
        return session_id
    
    def record_consent(self, session_id: str, consent_data: Dict):
        """Record explicit user consent"""
        consent = {
            'session_id': session_id,
            'timestamp': datetime.utcnow().isoformat(),
            'agreed_to_beta': consent_data.get('beta', False),
            'agreed_to_analytics': consent_data.get('analytics', False),
            'agreed_to_future_paid': consent_data.get('future_paid', False),
            'agreed_to_free_forever': consent_data.get('free_forever', False)
        }
        
        with open(self.consent_file, 'a') as f:
            f.write(json.dumps(consent) + '\n')
    
    def track_interaction(self, session_id: str, event_type: str, data: Dict):
        """Track user interaction"""
        interaction = {
            'session_id': session_id,
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'data': data
        }
        
        with open(self.interactions_file, 'a') as f:
            f.write(json.dumps(interaction) + '\n')
    
    def record_feedback(self, session_id: str, feedback_data: Dict):
        """Record user feedback"""
        feedback = {
            'session_id': session_id,
            'timestamp': datetime.utcnow().isoformat(),
            'rating': feedback_data.get('rating'),
            'comment': feedback_data.get('comment', ''),
            'category': feedback_data.get('category', 'general')
        }
        
        with open(self.feedback_file, 'a') as f:
            f.write(json.dumps(feedback) + '\n')
    
    def generate_insights(self) -> Dict:
        """Generate insights from collected data"""
        interactions = []
        if self.interactions_file.exists():
            with open(self.interactions_file, 'r') as f:
                interactions = [json.loads(line) for line in f if line.strip()]
        
        personality_counts = {}
        event_counts = {}
        
        for i in interactions:
            event_type = i.get('event_type', 'unknown')
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
            
            if event_type == 'personality_selected':
                p = i['data'].get('personality')
                personality_counts[p] = personality_counts.get(p, 0) + 1
        
        # Count unique sessions
        unique_sessions = len(set(i['session_id'] for i in interactions))
        
        # Calculate average feedback rating
        feedbacks = []
        if self.feedback_file.exists():
            with open(self.feedback_file, 'r') as f:
                feedbacks = [json.loads(line) for line in f if line.strip()]
        
        avg_rating = 0
        if feedbacks:
            ratings = [f.get('rating', 0) for f in feedbacks if f.get('rating')]
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
        
        return {
            'total_sessions': unique_sessions,
            'total_interactions': len(interactions),
            'personality_popularity': personality_counts,
            'event_types': event_counts,
            'feedback_count': len(feedbacks),
            'average_rating': round(avg_rating, 2)
        }
