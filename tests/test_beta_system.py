"""
Tests for UMAJA Beta System
"""
import sys
import json
from pathlib import Path
import tempfile
import shutil

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Add api and src to path
sys.path.insert(0, str(PROJECT_ROOT / "api"))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import pytest
from beta_tracker import BetaTracker
from freemium_model import FreemiumModel, UserType


# Import beta_server at module level for clarity
try:
    from api.beta_server import app as beta_app
    BETA_SERVER_AVAILABLE = True
except ImportError:
    BETA_SERVER_AVAILABLE = False
    beta_app = None


class TestBetaTracker:
    """Test BetaTracker functionality"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test data"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def tracker(self, temp_dir):
        """Create BetaTracker instance with temp directory"""
        return BetaTracker(data_dir=temp_dir)
    
    def test_create_session(self, tracker):
        """Test session creation"""
        session_id = tracker.create_session(user_agent="TestAgent/1.0")
        assert session_id is not None
        assert len(session_id) == 36  # UUID format
        
        # Verify session was written to file
        assert tracker.sessions_file.exists()
        
        with open(tracker.sessions_file, 'r') as f:
            session_data = json.loads(f.readline())
            assert session_data['session_id'] == session_id
            assert 'user_agent_hash' in session_data
            assert session_data['beta_version'] == '1.0.0'
    
    def test_record_consent(self, tracker):
        """Test consent recording"""
        session_id = tracker.create_session()
        consent_data = {
            'beta': True,
            'analytics': True,
            'future_paid': True,
            'free_forever': True
        }
        
        tracker.record_consent(session_id, consent_data)
        
        # Verify consent was written
        assert tracker.consent_file.exists()
        
        with open(tracker.consent_file, 'r') as f:
            consent_record = json.loads(f.readline())
            assert consent_record['session_id'] == session_id
            assert consent_record['agreed_to_beta'] is True
            assert consent_record['agreed_to_analytics'] is True
    
    def test_track_interaction(self, tracker):
        """Test interaction tracking"""
        session_id = tracker.create_session()
        
        tracker.track_interaction(session_id, 'content_generated', {
            'personality': 'professor',
            'topic': 'test',
            'length': 'short'
        })
        
        # Verify interaction was written
        assert tracker.interactions_file.exists()
        
        with open(tracker.interactions_file, 'r') as f:
            interaction = json.loads(f.readline())
            assert interaction['session_id'] == session_id
            assert interaction['event_type'] == 'content_generated'
            assert interaction['data']['personality'] == 'professor'
    
    def test_record_feedback(self, tracker):
        """Test feedback recording"""
        session_id = tracker.create_session()
        feedback_data = {
            'rating': 5,
            'comment': 'Great product!',
            'category': 'general'
        }
        
        tracker.record_feedback(session_id, feedback_data)
        
        # Verify feedback was written
        assert tracker.feedback_file.exists()
        
        with open(tracker.feedback_file, 'r') as f:
            feedback = json.loads(f.readline())
            assert feedback['session_id'] == session_id
            assert feedback['rating'] == 5
            assert feedback['comment'] == 'Great product!'
    
    def test_generate_insights(self, tracker):
        """Test insights generation"""
        # Create some test data
        session_id = tracker.create_session()
        
        tracker.track_interaction(session_id, 'personality_selected', {
            'personality': 'professor'
        })
        tracker.track_interaction(session_id, 'content_generated', {
            'personality': 'professor',
            'topic': 'test'
        })
        
        tracker.record_feedback(session_id, {
            'rating': 4,
            'comment': 'Good'
        })
        
        # Generate insights
        insights = tracker.generate_insights()
        
        assert insights['total_sessions'] == 1
        assert insights['total_interactions'] == 2
        assert 'professor' in insights['personality_popularity']
        assert insights['personality_popularity']['professor'] == 1
        assert insights['feedback_count'] == 1
        assert insights['average_rating'] == 4.0


class TestFreemiumModel:
    """Test FreemiumModel functionality"""
    
    @pytest.fixture
    def pricing_model(self):
        """Create FreemiumModel instance"""
        return FreemiumModel()
    
    def test_classify_beta_user(self, pricing_model):
        """Test classification of beta users"""
        user_type = pricing_model.classify_user(is_beta=True)
        assert user_type == UserType.FREE_FOREVER
    
    def test_classify_child_user(self, pricing_model):
        """Test classification of child users"""
        user_type = pricing_model.classify_user(age=15)
        assert user_type == UserType.FREE_FOREVER
    
    def test_classify_student_user(self, pricing_model):
        """Test classification of student users"""
        user_type = pricing_model.classify_user(email="student@university.edu")
        assert user_type == UserType.FREE_FOREVER
        
        user_type = pricing_model.classify_user(email="student@school.ac.uk")
        assert user_type == UserType.FREE_FOREVER
    
    def test_classify_regular_user(self, pricing_model):
        """Test classification of regular users"""
        user_type = pricing_model.classify_user(email="user@gmail.com")
        assert user_type == UserType.FREE_TIER
    
    def test_get_pricing_info(self, pricing_model):
        """Test getting pricing information"""
        info = pricing_model.get_pricing_info(UserType.FREE_FOREVER)
        assert info['price'] == 0
        assert 'Beta users' in info['who']
        assert info['features'] == 'All core features'
        
        info = pricing_model.get_pricing_info(UserType.PRO_INDIVIDUAL)
        assert info['price'] == 9.99
        assert 'Individuals' in info['who']
    
    def test_check_limit(self, pricing_model):
        """Test usage limit checking"""
        # Free forever user with 50 daily generations
        assert pricing_model.check_limit(UserType.FREE_FOREVER, 25, 'daily_generations') is True
        assert pricing_model.check_limit(UserType.FREE_FOREVER, 50, 'daily_generations') is False
        
        # Enterprise user with unlimited
        assert pricing_model.check_limit(UserType.ENTERPRISE, 10000, 'daily_generations') is True


class TestBetaAPI:
    """Test Beta API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        if not BETA_SERVER_AVAILABLE:
            pytest.skip("Beta server not available")
        
        beta_app.config['TESTING'] = True
        beta_app.config['SECRET_KEY'] = 'test-secret-key'
        with beta_app.test_client() as client:
            yield client
    
    def test_landing_page(self, client):
        """Test GET / returns landing page"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'UMAJA Beta' in response.data
        assert b'Versuchskaninchen' in response.data
    
    def test_health_endpoint(self, client):
        """Test GET /health"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'UMAJA Beta'
        assert data['version'] == '1.0.0'
    
    def test_consent_endpoint(self, client):
        """Test POST /api/beta/consent"""
        consent_data = {
            'beta': True,
            'analytics': True,
            'free_forever': True,
            'future_paid': True
        }
        
        response = client.post('/api/beta/consent',
                              data=json.dumps(consent_data),
                              content_type='application/json')
        
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'session_id' in data
    
    def test_analytics_insights(self, client):
        """Test GET /api/analytics/insights"""
        response = client.get('/api/analytics/insights')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'total_sessions' in data
        assert 'total_interactions' in data
        assert 'personality_popularity' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
