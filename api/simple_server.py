"""
UMAJA-Core Minimal Server - Bringing smiles to 8 billion people
Bahá'í principle: Service, not profit
"""
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import os
import sys
import random
import logging
from datetime import datetime, timezone
import signal
from pathlib import Path

# Add src to path for worldtour_generator
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

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
VERSION = "2.1.0"
DEPLOYMENT_DATE = "2026-01-02"

app = Flask(__name__)
CORS(app)

# Configure rate limiting to prevent API quota exhaustion
# Default: 100 requests per hour per IP
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"],
    storage_uri="memory://",
    strategy="fixed-window"
)

# Request timeout configuration (handled by gunicorn in production)
REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 30))  # 30 seconds default

# Ensure src is on path for worldtour imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from worldtour_generator import WorldtourGenerator  # noqa: E402

WORLDTOUR_DB_PATH = Path(
    os.environ.get(
        "WORLDTOUR_DB_PATH",
        PROJECT_ROOT / "data" / "worldtour_cities.json",
    )
)
WORLDTOUR_VOTES_PATH = Path(
    os.environ.get(
        "WORLDTOUR_VOTES_PATH",
        PROJECT_ROOT / "data" / "worldtour_votes.json",
    )
)

worldtour_gen = WorldtourGenerator(str(WORLDTOUR_DB_PATH))

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
        "What if we all just... took a deep breath together? In... and out... There. Better. 🌬️"
    ],
    "optimist": [
        "Today's gonna be a great day! You know why? Because YOU'RE in it! 🌟",
        "Remember: every expert was once a beginner who refused to give up. You're on your way! 🚀",
        "Fun fact: Smiling actually makes you feel happier, not just look it. So let's do this! 😊"
    ]
}

def _load_votes() -> dict:
    """Load stored worldtour votes."""
    if WORLDTOUR_VOTES_PATH.exists():
        try:
            return json.loads(WORLDTOUR_VOTES_PATH.read_text())
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning(f"Could not load votes file: {exc}")
    return {}


def _save_votes(votes: dict) -> None:
    """Persist worldtour votes to disk."""
    try:
        WORLDTOUR_VOTES_PATH.parent.mkdir(parents=True, exist_ok=True)
        WORLDTOUR_VOTES_PATH.write_text(json.dumps(votes, indent=2))
    except Exception as exc:  # pragma: no cover - defensive
        logger.error(f"Could not save votes file: {exc}")


@app.route('/health')
def health():
    """
    Health check endpoint for load balancers and monitoring
    Returns: 200 if service is healthy
    """
    try:
        # Basic health check - service is running
        return jsonify({
            "status": "healthy",
            "service": "UMAJA-Core-Minimal",
            "version": VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

@app.route('/version')
def version():
    """Return API version information"""
    return jsonify({
        "version": VERSION,
        "deployment_date": DEPLOYMENT_DATE,
        "principle": "Truth, Unity, Service"
    }), 200

@app.route('/deployment-info')
def deployment_info():
    """Return deployment information"""
    return jsonify({
        "version": VERSION,
        "deployment_date": DEPLOYMENT_DATE,
        "environment": os.environ.get('ENVIRONMENT', 'development'),
        "principle": "Service to humanity, not profit",
        "commitment": "Bringing smiles to 8 billion people"
    }), 200

@app.route('/api/daily-smile')
def daily_smile():
    """
    Generate a random daily smile from any archetype
    Returns: JSON with smile content
    """
    try:
        # Pick random archetype and random smile
        archetype = random.choice(list(SMILES.keys()))
        smile = random.choice(SMILES[archetype])
        
        return jsonify({
            "smile": smile,
            "archetype": archetype,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "principle": "Truth, Unity, Service"
        }), 200
    except Exception as e:
        logger.error(f"Error generating daily smile: {e}")
        return jsonify({
            "error": "Failed to generate smile",
            "message": "Please try again"
        }), 500

@app.route('/api/smile/<archetype>')
def smile_by_archetype(archetype):
    """
    Generate a smile for a specific archetype
    Args:
        archetype: professor, worrier, or optimist
    Returns: JSON with smile content
    """
    try:
        if archetype not in SMILES:
            return jsonify({
                "error": "Invalid archetype",
                "available_archetypes": list(SMILES.keys())
            }), 400
        
        smile = random.choice(SMILES[archetype])
        
        return jsonify({
            "smile": smile,
            "archetype": archetype,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "principle": "Truth, Unity, Service"
        }), 200
    except Exception as e:
        logger.error(f"Error generating smile for {archetype}: {e}")
        return jsonify({
            "error": "Failed to generate smile",
            "message": "Please try again"
        }), 500


@app.route('/api/worldtour/cities')
def worldtour_cities():
    """List cities with optional visited filter and stats."""
    visited_param = request.args.get('visited')
    visited_only = str(visited_param).lower() == 'true' if visited_param is not None else False

    cities = worldtour_gen.list_cities(visited_only=visited_only)
    stats = worldtour_gen.get_stats()

    return jsonify({
        "cities": cities,
        "stats": stats
    }), 200


@app.route('/api/worldtour/next')
def worldtour_next():
    """Return next unvisited city."""
    next_city = worldtour_gen.get_next_city()
    if not next_city:
        return jsonify({
            "error": "No cities remaining",
            "message": "All cities have been visited"
        }), 404

    return jsonify(next_city), 200


@app.route('/api/worldtour/queue')
def worldtour_queue():
    """Return planned content queue for upcoming days."""
    try:
        days = int(request.args.get('days', 7))
    except (TypeError, ValueError):
        days = 7

    queue = worldtour_gen.create_content_queue(days=days)
    return jsonify({
        "queue": queue,
        "days": days
    }), 200


@app.route('/api/worldtour/start', methods=['POST'])
def worldtour_start():
    """Start or continue the worldtour from this server."""
    data = request.get_json(force=True, silent=True) or {}

    city_id = data.get('city_id')
    if not city_id:
        next_city = worldtour_gen.get_next_city()
        if not next_city:
            return jsonify({
                "success": False,
                "error": "No cities available to start",
            }), 404
        city_id = next_city['id']

    personality = data.get('personality', worldtour_gen.PERSONALITIES[0])
    content_type = data.get('content_type', worldtour_gen.CONTENT_TYPES[0])

    try:
        content = worldtour_gen.generate_city_content(
            city_id=city_id,
            personality=personality,
            content_type=content_type
        )
    except ValueError as exc:
        return jsonify({
            "success": False,
            "error": str(exc)
        }), 400

    marked = worldtour_gen.mark_city_visited(city_id)
    if not marked:
        return jsonify({
            "success": False,
            "error": "Could not mark city as visited"
        }), 500

    return jsonify({
        "success": True,
        "city_id": city_id,
        "content": content,
        "stats": worldtour_gen.get_stats()
    }), 200


@app.route('/api/worldtour/vote', methods=['POST'])
def worldtour_vote():
    """Record a vote for the next city."""
    data = request.get_json(force=True, silent=True) or {}
    city_id = data.get('city_id')

    if not city_id:
        return jsonify({
            "success": False,
            "error": "city_id is required"
        }), 400

    city = worldtour_gen.get_city(city_id)
    if not city:
        return jsonify({
            "success": False,
            "error": "Unknown city"
        }), 404

    votes = _load_votes()
    votes[city_id] = votes.get(city_id, 0) + 1
    _save_votes(votes)

    return jsonify({
        "success": True,
        "city_id": city_id,
        "message": f"Vote recorded for {city.get('name', city_id)}"
    }), 200


@app.route('/api/analytics/worldtour')
def worldtour_analytics():
    """Return basic analytics for the worldtour."""
    stats = worldtour_gen.get_stats()
    votes = _load_votes()

    response = {
        "total_cities": stats["total_cities"],
        "visited_cities": stats["visited_cities"],
        "remaining_cities": stats["remaining_cities"],
        "total_views": stats["total_views"],
        "completion_percentage": stats["completion_percentage"],
    }

    if votes:
        top_votes = sorted(votes.items(), key=lambda item: item[1], reverse=True)
        response["top_voted_cities"] = [
            {"city_id": city_id, "votes": count}
            for city_id, count in top_votes[:5]
        ]

    return jsonify(response), 200

@app.route('/')
def root():
    """Root endpoint with API information"""
    return jsonify({
        "message": "UMAJA-Core Minimal Server",
        "version": VERSION,
        "endpoints": {
            "health": "/health",
            "version": "/version",
            "deployment_info": "/deployment-info",
            "daily_smile": "/api/daily-smile",
            "smile_by_archetype": "/api/smile/<archetype>",
            "worldtour_cities": "/api/worldtour/cities",
            "worldtour_next": "/api/worldtour/next",
            "worldtour_queue": "/api/worldtour/queue",
            "worldtour_start": "/api/worldtour/start",
            "worldtour_vote": "/api/worldtour/vote",
            "worldtour_analytics": "/api/analytics/worldtour",
        },
        "available_archetypes": list(SMILES.keys()),
        "principle": "Truth, Unity, Service"
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not found",
        "message": "The requested endpoint does not exist",
        "available_endpoints": [
            "/health",
            "/version",
            "/deployment-info",
            "/api/daily-smile",
            "/api/smile/<archetype>",
            "/api/worldtour/cities",
            "/api/worldtour/next",
            "/api/worldtour/queue",
            "/api/worldtour/start",
            "/api/worldtour/vote",
            "/api/analytics/worldtour",
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Received signal {sig}, shutting down gracefully...")
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    # Validate environment before starting
    if not validate_environment():
        logger.error("Environment validation failed, exiting")
        sys.exit(1)
    
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Starting UMAJA-Core Minimal Server v{VERSION}")
    logger.info(f"Port: {port}, Debug: {debug}")
    logger.info("Bahá'í principle: Service to humanity, not profit")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
