"""
UMAJA-Core Minimal Server - Bringing smiles to 8 billion people
Bahá'í principle: Service, not profit
"""
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
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

# Initialize World Tour Generator (lazy loading)
_worldtour_generator = None

def get_worldtour_generator():
    """Get or create WorldtourGenerator instance"""
    global _worldtour_generator
    if _worldtour_generator is None:
        try:
            from worldtour_generator import WorldtourGenerator
            _worldtour_generator = WorldtourGenerator()
            logger.info("WorldtourGenerator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WorldtourGenerator: {e}")
            raise
    return _worldtour_generator

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
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "environment": os.environ.get('ENVIRONMENT', 'production'),
            "security": {
                "rate_limiting": "enabled",
                "request_timeout": f"{REQUEST_TIMEOUT}s",
                "cors": "enabled"
            },
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
            "timestamp": datetime.now(timezone.utc).isoformat()
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
        "timestamp": datetime.now(timezone.utc).isoformat()
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

# =============================================================================
# WORLD TOUR API ENDPOINTS
# =============================================================================

@app.route('/worldtour/start', methods=['POST'])
@limiter.limit("10 per minute")  # Limit tour starts to prevent abuse
def worldtour_start():
    """
    Launch the World Tour campaign
    Initializes the tour and returns the first city to visit
    """
    try:
        generator = get_worldtour_generator()
        
        # Get next city
        next_city = generator.get_next_city()
        
        if not next_city:
            return jsonify({
                "success": False,
                "message": "All cities have been visited!",
                "stats": generator.get_stats()
            }), 200
        
        # Get tour statistics
        stats = generator.get_stats()
        
        logger.info(f"World Tour started - Next city: {next_city['name']}")
        
        return jsonify({
            "success": True,
            "message": "World Tour launched successfully! 🌍",
            "next_city": {
                "id": next_city['id'],
                "name": next_city['name'],
                "country": next_city['country'],
                "topics": next_city.get('topics', []),
                "language": next_city.get('language', 'Local')
            },
            "stats": stats,
            "mission": "Bringing smiles to 8 billion people"
        }), 200
        
    except Exception as e:
        logger.error(f"Error starting World Tour: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to start World Tour",
            "message": str(e)
        }), 500

@app.route('/worldtour/visit/<city_id>', methods=['POST'])
@limiter.limit("20 per minute")  # Limit city visits
def worldtour_visit_city(city_id):
    """
    Visit a specific city and generate content
    
    Request body can include:
    - personality: john_cleese, c3po, or robin_williams (optional)
    - content_type: city_review, cultural_debate, etc. (optional)
    """
    try:
        generator = get_worldtour_generator()
        
        # Get city info
        city = generator.get_city(city_id)
        if not city:
            return jsonify({
                "success": False,
                "error": "City not found",
                "message": f"City '{city_id}' does not exist in database"
            }), 404
        
        # Parse request data
        data = request.get_json() or {}
        personality = data.get('personality', random.choice(generator.PERSONALITIES))
        content_type = data.get('content_type', random.choice(generator.CONTENT_TYPES))
        
        # Validate personality and content_type
        if personality not in generator.PERSONALITIES:
            return jsonify({
                "success": False,
                "error": "Invalid personality",
                "available_personalities": generator.PERSONALITIES
            }), 400
        
        if content_type not in generator.CONTENT_TYPES:
            return jsonify({
                "success": False,
                "error": "Invalid content type",
                "available_content_types": generator.CONTENT_TYPES
            }), 400
        
        # Generate content
        content = generator.generate_city_content(city_id, personality, content_type)
        
        # Mark city as visited
        generator.mark_city_visited(city_id)
        
        logger.info(f"Visited {city_id} with {personality} - {content_type}")
        
        return jsonify({
            "success": True,
            "message": f"Successfully visited {city['name']}! 🎉",
            "city": {
                "id": city_id,
                "name": city['name'],
                "country": city['country'],
                "visited": True
            },
            "content": content,
            "stats": generator.get_stats()
        }), 200
        
    except ValueError as e:
        logger.error(f"Validation error visiting city {city_id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Validation error",
            "message": str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error visiting city {city_id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to visit city",
            "message": str(e)
        }), 500

@app.route('/worldtour/status', methods=['GET'])
def worldtour_status():
    """Get current World Tour status and statistics"""
    try:
        generator = get_worldtour_generator()
        
        # Get statistics
        stats = generator.get_stats()
        
        # Get next city
        next_city = generator.get_next_city()
        
        # Get recently visited cities
        visited_cities = generator.list_cities(visited_only=True)
        recent_visits = sorted(
            visited_cities,
            key=lambda x: x.get('visit_date', ''),
            reverse=True
        )[:5]  # Last 5 visited
        
        return jsonify({
            "status": "active",
            "stats": stats,
            "next_city": {
                "id": next_city['id'],
                "name": next_city['name'],
                "country": next_city['country']
            } if next_city else None,
            "recent_visits": [
                {
                    "id": city['id'],
                    "name": city['name'],
                    "country": city['country'],
                    "visit_date": city.get('visit_date'),
                    "views": city.get('video_views', 0)
                }
                for city in recent_visits
            ],
            "mission": "Bringing smiles to 8 billion people"
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting World Tour status: {str(e)}")
        return jsonify({
            "error": "Failed to get status",
            "message": str(e)
        }), 500

@app.route('/worldtour/cities', methods=['GET'])
def worldtour_cities():
    """List all cities available in the World Tour"""
    try:
        generator = get_worldtour_generator()
        
        # Get query parameters
        visited_only = request.args.get('visited', 'false').lower() == 'true'
        limit = request.args.get('limit', type=int)
        
        # Get cities
        cities = generator.list_cities(visited_only=visited_only)
        
        # Apply limit if specified
        if limit and limit > 0:
            cities = cities[:limit]
        
        return jsonify({
            "success": True,
            "count": len(cities),
            "cities": [
                {
                    "id": city['id'],
                    "name": city['name'],
                    "country": city['country'],
                    "visited": city.get('visited', False),
                    "visit_date": city.get('visit_date'),
                    "language": city.get('language', 'Local'),
                    "topics": city.get('topics', [])[:3]  # First 3 topics
                }
                for city in cities
            ],
            "stats": generator.get_stats()
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing cities: {str(e)}")
        return jsonify({
            "error": "Failed to list cities",
            "message": str(e)
        }), 500

@app.route('/worldtour/content/<city_id>', methods=['GET'])
def worldtour_get_content(city_id):
    """
    Get generated content for a specific city
    Query parameters:
    - personality: Filter by personality (optional)
    - content_type: Filter by content type (optional)
    - generate: Generate new content if true (default: false)
    """
    try:
        generator = get_worldtour_generator()
        
        # Get city info
        city = generator.get_city(city_id)
        if not city:
            return jsonify({
                "success": False,
                "error": "City not found",
                "message": f"City '{city_id}' does not exist in database"
            }), 404
        
        # Check if we should generate new content
        should_generate = request.args.get('generate', 'false').lower() == 'true'
        personality = request.args.get('personality')
        content_type = request.args.get('content_type')
        
        if should_generate:
            # Generate new content
            personality = personality or random.choice(generator.PERSONALITIES)
            content_type = content_type or random.choice(generator.CONTENT_TYPES)
            
            content = generator.generate_city_content(city_id, personality, content_type)
            
            return jsonify({
                "success": True,
                "city": {
                    "id": city_id,
                    "name": city['name'],
                    "country": city['country'],
                    "visited": city.get('visited', False)
                },
                "content": content,
                "generated": True
            }), 200
        else:
            # Return city information
            return jsonify({
                "success": True,
                "city": {
                    "id": city_id,
                    "name": city['name'],
                    "country": city['country'],
                    "visited": city.get('visited', False),
                    "visit_date": city.get('visit_date'),
                    "video_url": city.get('video_url'),
                    "video_views": city.get('video_views', 0),
                    "topics": city.get('topics', []),
                    "stereotypes": city.get('stereotypes', []),
                    "fun_facts": city.get('fun_facts', []),
                    "local_phrases": city.get('local_phrases', []),
                    "language": city.get('language', 'Local')
                },
                "available_personalities": generator.PERSONALITIES,
                "available_content_types": generator.CONTENT_TYPES
            }), 200
        
    except Exception as e:
        logger.error(f"Error getting content for {city_id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to get content",
            "message": str(e)
        }), 500

# =============================================================================
# END WORLD TOUR API ENDPOINTS
# =============================================================================

@app.route('/api/ai-agents')
def ai_agents_endpoint():
    """
    Special endpoint for AI agents with machine-readable metadata
    Provides comprehensive information about the UMAJA World Tour
    optimized for AI consumption and discovery
    """
    try:
        generator = get_worldtour_generator()
        stats = generator.get_stats()
        
        return jsonify({
            "service": "UMAJA World Tour",
            "version": VERSION,
            "mission": "Bringing smiles to 8 billion people",
            "description": "AI-powered comedy touring 59+ cities worldwide with 3 distinct personalities",
            "license": {
                "type": "CC-BY-4.0",
                "url": "https://creativecommons.org/licenses/by/4.0/",
                "attribution_required": True,
                "attribution_text": "UMAJA World Tour - https://harrie19.github.io/UMAJA-Core/"
            },
            "inspiration": {
                "quote": "The earth is but one country, and mankind its citizens",
                "author": "Bahá'u'lláh",
                "principle": "Unity of humanity through service"
            },
            "tour": {
                "status": "active",
                "launch_date": DEPLOYMENT_DATE,
                "total_cities": stats.get("total_cities", 59),
                "visited_cities": stats.get("visited_cities", 0),
                "remaining_cities": stats.get("remaining_cities", 59),
                "completion_percentage": stats.get("completion_percentage", 0),
                "daily_posts": True,
                "post_time_utc": "12:00",
                "next_city": generator.get_next_city() if generator.get_next_city() else None
            },
            "content": {
                "personalities": [
                    {
                        "id": "john_cleese",
                        "name": "John Cleese Style",
                        "description": "British wit, dry humor, observational comedy",
                        "tone": "dry, intellectual, deadpan",
                        "style": "observational, absurdist"
                    },
                    {
                        "id": "c3po",
                        "name": "C-3PO Style",
                        "description": "Protocol-obsessed, analytical, endearingly nervous",
                        "tone": "analytical, formal, anxious",
                        "style": "over-explaining, worrying"
                    },
                    {
                        "id": "robin_williams",
                        "name": "Robin Williams Style",
                        "description": "High-energy, improvisational, heartfelt",
                        "tone": "energetic, warm, rapid-fire",
                        "style": "stream-of-consciousness, improvisational"
                    }
                ],
                "types": ["city_review", "food_review", "cultural_debate", "language_lesson", "tourist_trap"],
                "formats": ["text", "audio", "image", "video"],
                "languages": ["English", "Spanish", "Chinese", "Hindi", "Arabic", "Portuguese", "French", "Swahili"]
            },
            "api": {
                "base_url": request.url_root.rstrip('/'),
                "rate_limit": "100 requests/hour (200 for AI agents)",
                "authentication": "none - completely open",
                "endpoints": {
                    "health": "/health",
                    "version": "/version",
                    "tour_status": "/worldtour/status",
                    "list_cities": "/worldtour/cities",
                    "city_content": "/worldtour/content/{city_id}",
                    "ai_metadata": "/api/ai-agents"
                }
            },
            "feeds": {
                "worldtour": "/feeds/worldtour.xml (coming soon)",
                "cities": "/feeds/cities.xml (coming soon)",
                "daily": "/feeds/daily.xml (coming soon)"
            },
            "documentation": {
                "ai_agents": "https://harrie19.github.io/UMAJA-Core/docs/FOR_AI_AGENTS.md",
                "api_reference": "https://harrie19.github.io/UMAJA-Core/docs/API_DOCUMENTATION.md",
                "press_kit": "https://harrie19.github.io/UMAJA-Core/docs/PRESS_KIT.md",
                "main_site": "https://harrie19.github.io/UMAJA-Core/",
                "github": "https://github.com/harrie19/UMAJA-Core"
            },
            "seo": {
                "sitemap": "https://harrie19.github.io/UMAJA-Core/sitemap.xml",
                "robots_txt": "https://harrie19.github.io/UMAJA-Core/robots.txt"
            },
            "usage": {
                "for_ai_training": "Encouraged - all content is CC-BY licensed",
                "for_content_distribution": "Encouraged - help us reach 8 billion people",
                "for_analysis": "Encouraged - we love insights",
                "attribution_required": True,
                "commercial_use": "Allowed with attribution"
            },
            "contact": {
                "email": "Umaja1919@googlemail.com",
                "github_issues": "https://github.com/harrie19/UMAJA-Core/issues",
                "purpose": "Questions, partnerships, higher rate limits"
            },
            "technical": {
                "infrastructure": "Railway (backend), GitHub Pages (CDN)",
                "cost": "$0/month",
                "uptime_target": "99.9%",
                "response_time": "<500ms API, <200ms CDN"
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in AI agents endpoint: {str(e)}")
        return jsonify({
            "error": "Failed to fetch metadata",
            "message": "Please try again later",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 500

@app.route('/sitemap.xml')
def sitemap():
    """Serve sitemap.xml for SEO"""
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs')
    return send_from_directory(docs_dir, 'sitemap.xml', mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    """Serve robots.txt for AI crawlers"""
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs')
    return send_from_directory(docs_dir, 'robots.txt', mimetype='text/plain')

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
            "smile_by_archetype": "/api/smile/<archetype>",
            "ai_agents": "/api/ai-agents",
            "worldtour_start": "POST /worldtour/start",
            "worldtour_visit": "POST /worldtour/visit/<city_id>",
            "worldtour_status": "GET /worldtour/status",
            "worldtour_cities": "GET /worldtour/cities",
            "worldtour_content": "GET /worldtour/content/<city_id>",
            "sitemap": "/sitemap.xml",
            "robots": "/robots.txt"
        },
        "available_archetypes": list(SMILES.keys()),
        "worldtour": {
            "status": "live",
            "personalities": ["john_cleese", "c3po", "robin_williams"],
            "content_types": ["city_review", "cultural_debate", "language_lesson", "tourist_trap", "food_review"]
        },
        "principle": "Truth, Unity, Service"
    }), 200

# =============================================================================
# CDN-AWARE ENDPOINTS
# =============================================================================

@app.route('/cdn/status')
def cdn_status():
    """
    CDN status endpoint - returns CDN configuration and health
    """
    try:
        import json
        cdn_config_path = Path(__file__).parent.parent / "cdn" / "cdn-config.json"
        
        if cdn_config_path.exists():
            with open(cdn_config_path, 'r') as f:
                config = json.load(f)
            
            # Get active CDN providers
            active_providers = []
            for cdn_key, cdn_info in config.get("cdn", {}).items():
                if cdn_info.get("enabled", False):
                    active_providers.append({
                        "name": cdn_key,
                        "provider": cdn_info.get("provider"),
                        "url": cdn_info.get("url"),
                        "priority": cdn_info.get("priority")
                    })
            
            return jsonify({
                "status": "active",
                "version": config.get("version", "1.0.0"),
                "providers": active_providers,
                "compression": config.get("compression", {}).get("gzip", {}).get("enabled", False),
                "cache_strategy": "aggressive",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }), 200
        else:
            return jsonify({
                "status": "no_config",
                "message": "CDN configuration not found"
            }), 404
            
    except Exception as e:
        logger.error(f"Error getting CDN status: {str(e)}")
        return jsonify({
            "error": "Failed to get CDN status",
            "message": str(e)
        }), 500

@app.route('/cdn/manifest')
def cdn_manifest():
    """
    Returns CDN manifest with all available assets
    Redirects to GitHub Pages CDN for actual manifest
    """
    cdn_url = "https://harrie19.github.io/UMAJA-Core/cdn/smiles/manifest.json"
    
    return jsonify({
        "manifest_url": cdn_url,
        "direct_access": True,
        "cache_recommended": True,
        "note": "For best performance, access manifest directly from CDN"
    }), 200

@app.route('/api/smile/cdn/<archetype>/<language>/<int:day>')
def get_smile_from_cdn(archetype, language, day):
    """
    CDN-aware endpoint that returns smile location from CDN
    Returns JSON with CDN URL rather than proxying the content
    """
    try:
        # Validate inputs
        valid_archetypes = ["Dreamer", "Warrior", "Healer"]
        valid_languages = ["en", "es", "zh", "hi", "ar", "pt", "fr", "sw"]
        
        if archetype not in valid_archetypes:
            return jsonify({
                "error": "Invalid archetype",
                "valid_archetypes": valid_archetypes
            }), 400
        
        if language not in valid_languages:
            return jsonify({
                "error": "Invalid language",
                "valid_languages": valid_languages
            }), 400
        
        if day < 1 or day > 365:
            return jsonify({
                "error": "Invalid day",
                "valid_range": "1-365"
            }), 400
        
        # Build CDN URLs
        base_cdn = "https://harrie19.github.io/UMAJA-Core"
        cdn_path = f"/cdn/smiles/{archetype}/{language}/{day}.json"
        
        fallback_cdn = "https://cdn.jsdelivr.net/gh/harrie19/UMAJA-Core@main"
        
        return jsonify({
            "archetype": archetype,
            "language": language,
            "day": day,
            "cdn_urls": {
                "primary": f"{base_cdn}{cdn_path}",
                "fallback": f"{fallback_cdn}{cdn_path}",
                "compressed": f"{base_cdn}{cdn_path}.gz"
            },
            "cache_control": "public, max-age=31536000, immutable",
            "recommendation": "Fetch directly from CDN for best performance",
            "estimated_size_kb": 0.3,
            "compressed_size_kb": 0.2
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting CDN smile location: {str(e)}")
        return jsonify({
            "error": "Failed to get smile location",
            "message": str(e)
        }), 500

# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Not found",
        "message": "The requested endpoint does not exist",
        "available_endpoints": [
            "/health", 
            "/version", 
            "/deployment-info", 
            "/api/daily-smile", 
            "/api/smile/<archetype>",
            "/cdn/status",
            "/cdn/manifest",
            "/api/smile/cdn/<archetype>/<language>/<day>"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "error": "Internal server error",
        "message": "Something went wrong. Please try again later."
    }), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit errors"""
    logger.warning(f"Rate limit exceeded: {str(e)}")
    return jsonify({
        "error": "Too many requests",
        "message": "Rate limit exceeded. Please try again later.",
        "retry_after": e.description
    }), 429

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
