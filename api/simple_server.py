"""
UMAJA-Core - Minimal Flask Server for DEPLOYMENT
Focus: WORKS, not impressive. Serves Daily Smiles to 8 billion people.
"""

import os
import sys
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from personality_engine import PersonalityEngine

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for GitHub Pages frontend

# Initialize personality engine
personality_engine = PersonalityEngine()

# ============================================
# MINIMAL ENDPOINTS - Truth over Optimization
# ============================================

@app.route('/health')
def health():
    """Health check endpoint - proves we're alive and serving smiles"""
    return jsonify({
        'status': 'alive',
        'mission': '8 billion smiles',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'UMAJA-Core'
    })


@app.route('/api/daily-smile')
def daily_smile():
    """
    Generate and return today's Daily Smile
    Simple. Works. Spreads joy.
    """
    try:
        # Get archetype from query params or use random
        archetype = request.args.get('archetype', None)
        
        # Generate the smile
        result = personality_engine.generate_daily_smile(archetype)
        
        return jsonify({
            'success': True,
            'date': datetime.utcnow().strftime('%Y-%m-%d'),
            'smile': result,
            'message': 'One smile, spreading joy!'
        })
    
    except Exception as e:
        logger.error(f"Daily smile generation failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Oops! We will fix this and smile again soon.'
        }), 500


@app.route('/api/generate', methods=['POST'])
def generate_smile():
    """
    Generate custom smile with topic and archetype
    POST body: {"topic": "something", "archetype": "professor|worrier|enthusiast"}
    Note: topic parameter accepted for future use but not yet implemented in v1
    """
    try:
        data = request.get_json() or {}
        topic = data.get('topic', None)  # Reserved for future enhancement
        archetype = data.get('archetype', None)
        
        # Generate with specific archetype (topic not yet supported in v1)
        result = personality_engine.generate_daily_smile(archetype)
        
        return jsonify({
            'success': True,
            'timestamp': datetime.utcnow().isoformat(),
            'topic': topic,  # Echo back for future compatibility
            'smile': result,
            'message': 'Custom smile generated!'
        })
    
    except Exception as e:
        logger.error(f"Custom smile generation failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Could not generate smile. We will improve!'
        }), 500


# ============================================
# MAIN - Keep it simple
# ============================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    logger.info("=" * 60)
    logger.info("🚀 UMAJA-Core Minimal Server Starting")
    logger.info(f"Mission: Bring smiles to 8 billion people")
    logger.info(f"Port: {port}")
    logger.info(f"Debug: {debug}")
    logger.info("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
