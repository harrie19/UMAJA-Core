"""
UMAJA-Core Minimal Server - Bringing smiles to 8 billion people
Bahá'í principle: Service, not profit
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys
import random
import logging
from datetime import datetime
import signal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Application version
VERSION = "1.0.0"
DEPLOYMENT_DATE = "2026-01-01"

app = Flask(__name__)
CORS(app)

# Validate critical environment variables on startup
REQUIRED_ENV_VARS = []  # No required vars for basic operation
OPTIONAL_ENV_VARS = ['PORT', 'ENVIRONMENT', 'DEBUG']

def validate_environment():
    """Validate environment variables are properly set"""
    missing_vars = [var for var in REQUIRED_ENV_VARS if not os.environ.get(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    logger.info("Environment validation passed")
    for var in OPTIONAL_ENV_VARS:
        value = os.environ.get(var, 'not set')
        logger.info(f"  {var}: {value}")
    return True

# Simple in-memory smile generation
SMILES = {
    "professor": [
        "Did you know that honey never spoils? Archaeologists have found 3000-year-old honey in Egyptian tombs that's still perfectly edible. Nature's time capsule! 🍯",
        "Every 60 seconds in Africa, a minute passes. But also - someone learns something new that changes their life forever. 📚",
        "Statistically speaking, you're more likely to be struck by lightning than win the lottery. But 100% of people who smile feel better for at least a moment. ⚡"
    ],
    "worrier": [
        "Is it just me, or does anyone else check if they locked the door three times? We're all in this together. 🚪",
        "That moment when you realize you've been worrying about something for hours... and then it works out fine. Classic us! 😅",
        "Do you ever worry that you worry too much? Yeah, me too. Let's worry about it together. 💭"
    ],
    "enthusiast": [
        "RIGHT NOW, somewhere in the world, someone just learned to ride a bike for the first time! EVERY. SINGLE. DAY. How amazing is that?! 🚴",
        "Can we just appreciate that dogs exist?! Literal happiness in fur form! 🐕",
        "You know what's incredible? You're alive during the time when we can see photos from Mars. MARS! 🌟"
    ]
}

@app.route('/health')
def health():
    """
    Comprehensive health check endpoint
    Returns 200 if service is operational
    """
    try:
        # Basic service check
        health_data = {
            "status": "healthy",
            "service": "UMAJA-Core",
            "version": VERSION,
            "mission": "8 billion smiles",
            "timestamp": datetime.utcnow().isoformat(),
            "environment": os.environ.get('ENVIRONMENT', 'production'),
            "checks": {
                "api": "ok",
                "smiles_loaded": len(SMILES) > 0,
                "archetypes_available": list(SMILES.keys())
            }
        }
        
        # Verify we can generate a smile
        test_archetype = random.choice(list(SMILES.keys()))
        test_smile = random.choice(SMILES[test_archetype])
        health_data["checks"]["content_generation"] = "ok" if test_smile else "failed"
        
        return jsonify(health_data), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 503

@app.route('/version')
def version():
    """Return version and deployment information"""
    return jsonify({
        "version": VERSION,
        "deployment_date": DEPLOYMENT_DATE,
        "service": "UMAJA-Core Minimal Server",
        "mission": "Bringing smiles to 8 billion people",
        "principle": "Service, not profit",
        "python_version": sys.version.split()[0]
    }), 200

@app.route('/deployment-info')
def deployment_info():
    """Return deployment environment information"""
    return jsonify({
        "environment": os.environ.get('ENVIRONMENT', 'production'),
        "debug_mode": os.environ.get('DEBUG', 'false'),
        "port": os.environ.get('PORT', '5000'),
        "version": VERSION,
        "uptime": "Service operational",
        "platform": "Railway",
        "timestamp": datetime.utcnow().isoformat()
    }), 200

@app.route('/api/daily-smile')
def daily_smile():
    """Generate today's smile"""
    try:
        archetype = random.choice(["professor", "worrier", "enthusiast"])
        smile = random.choice(SMILES[archetype])
        
        return jsonify({
            "content": smile,
            "archetype": archetype,
            "mission": "Serving 8 billion people",
            "principle": "Truth, Unity, Service"
        }), 200
        
    except Exception as e:
        logger.error(f"Error generating daily smile: {str(e)}")
        return jsonify({
            "error": "Failed to generate smile",
            "message": "Please try again"
        }), 500

@app.route('/api/smile/<archetype>')
def smile_by_archetype(archetype):
    """Get smile from specific archetype"""
    try:
        if archetype not in SMILES:
            return jsonify({
                "error": "Unknown archetype",
                "available_archetypes": list(SMILES.keys())
            }), 404
        
        smile = random.choice(SMILES[archetype])
        return jsonify({
            "content": smile,
            "archetype": archetype
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting smile for archetype {archetype}: {str(e)}")
        return jsonify({
            "error": "Failed to get smile",
            "message": "Please try again"
        }), 500

@app.route('/')
def root():
    """Root endpoint with API information"""
    return jsonify({
        "service": "UMAJA-Core API",
        "version": VERSION,
        "mission": "8 billion smiles 🌍",
        "endpoints": {
            "health": "/health",
            "version": "/version",
            "deployment_info": "/deployment-info",
            "daily_smile": "/api/daily-smile",
            "smile_by_archetype": "/api/smile/<archetype>"
        },
        "available_archetypes": list(SMILES.keys()),
        "principle": "Truth, Unity, Service"
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Not found",
        "message": "The requested endpoint does not exist",
        "available_endpoints": ["/health", "/version", "/deployment-info", "/api/daily-smile", "/api/smile/<archetype>"]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "error": "Internal server error",
        "message": "Something went wrong. Please try again later."
    }), 500

def shutdown_handler(signum, frame):
    """Graceful shutdown handler"""
    logger.info(f"Received shutdown signal {signum}")
    logger.info("UMAJA-Core server shutting down gracefully...")
    sys.exit(0)

if __name__ == '__main__':
    # Register shutdown handlers
    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)
    
    # Validate environment
    logger.info("Starting UMAJA-Core Minimal Server...")
    logger.info(f"Version: {VERSION}")
    logger.info(f"Mission: Bringing smiles to 8 billion people 🌍")
    
    if not validate_environment():
        logger.error("Environment validation failed. Server may not function correctly.")
    
    # Start server
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Starting server on 0.0.0.0:{port}")
    logger.info(f"Debug mode: {debug_mode}")
    logger.info("Service, not profit ✨")
    
    try:
        app.run(host='0.0.0.0', port=port, debug=debug_mode)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        sys.exit(1)
