"""
UMAJA Beta API - All endpoints unified
"""

from flask import Flask, request, jsonify, render_template, session, redirect
from flask_cors import CORS
import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from beta_tracker import BetaTracker
from personality_engine import PersonalityEngine
from freemium_model import FreemiumModel
from beta_config import CONTACT_EMAIL, GITHUB_REPO, PRIVACY_POLICY_URL

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
CORS(app)
app.secret_key = os.urandom(24)

tracker = BetaTracker()
personality_engine = PersonalityEngine()
pricing = FreemiumModel()

# Template context processor to inject config into all templates
@app.context_processor
def inject_config():
    return {
        'contact_email': CONTACT_EMAIL,
        'github_repo': GITHUB_REPO,
        'privacy_url': PRIVACY_POLICY_URL
    }


@app.route('/')
def landing():
    """Beta landing page"""
    return render_template('beta_landing.html')


@app.route('/app')
def dashboard():
    """Main app dashboard"""
    if 'session_id' not in session:
        return redirect('/')
    return render_template('dashboard.html')


@app.route('/api/beta/consent', methods=['POST'])
def record_consent():
    """Record user consent"""
    data = request.json
    session_id = tracker.create_session(request.headers.get('User-Agent', ''))
    tracker.record_consent(session_id, data)
    
    session['session_id'] = session_id
    session['beta_user'] = True
    
    return jsonify({'success': True, 'session_id': session_id})


@app.route('/api/generate', methods=['POST'])
def generate_content():
    """Generate content"""
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'No session found'}), 401
    
    data = request.json
    
    # Get personality from engine
    personality_id = data.get('personality', 'professor')
    topic = data.get('topic', 'life')
    length = data.get('length', 'short')
    
    # Map friendly names to actual personality IDs
    personality_map = {
        'professor': 'john_cleese',
        'worrier': 'c3po',
        'enthusiast': 'robin_williams'
    }
    
    actual_personality = personality_map.get(personality_id, personality_id)
    
    try:
        comedian = personality_engine.get_comedian(actual_personality)
        if comedian:
            result = comedian.generate_text(topic, length)
        else:
            # Log missing personality for debugging
            logger.warning(f"Personality '{actual_personality}' not found, using fallback")
            result = {
                'text': f"I'm still learning about {topic}! This personality is being developed. "
                       f"Try another personality or check back soon.",
                'personality': personality_id,
                'tone': 'apologetic'
            }
        
        # Track the interaction
        tracker.track_interaction(session_id, 'content_generated', {
            'personality': personality_id,
            'topic': topic,
            'length': length,
            'fallback_used': comedian is None
        })
        
        return jsonify({
            'success': True,
            'content': result.get('text'),
            'personality': personality_id,
            'tone': result.get('tone')
        })
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback"""
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'No session found'}), 401
    
    data = request.json
    tracker.record_feedback(session_id, data)
    
    return jsonify({'success': True, 'message': 'Thank you for your feedback!'})


@app.route('/api/analytics/insights', methods=['GET'])
def get_insights():
    """Get analytics insights"""
    insights = tracker.generate_insights()
    return jsonify(insights)


@app.route('/api/personality/switch', methods=['POST'])
def switch_personality():
    """Switch personality"""
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'No session found'}), 401
    
    data = request.json
    personality = data.get('personality')
    
    tracker.track_interaction(session_id, 'personality_selected', {
        'personality': personality
    })
    
    return jsonify({'success': True, 'personality': personality})


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'UMAJA Beta',
        'version': '1.0.0'
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
