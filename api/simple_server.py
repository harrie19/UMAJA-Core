"""
UMAJA WORLDTOUR - Flask API Server
Complete web server with 15+ endpoints for multimedia content generation and worldtour
"""

import os
import sys
from pathlib import Path
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from personality_engine import PersonalityEngine
from voice_synthesizer import VoiceSynthesizer
from image_generator import ImageGenerator
from video_generator import VideoGenerator
from worldtour_generator import WorldtourGenerator
from bundle_builder import BundleBuilder
from multimedia_text_seller import MultimediaTextSeller

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')
CORS(app)

# Initialize all engines
personality_engine = PersonalityEngine()
voice_synthesizer = VoiceSynthesizer()
image_generator = ImageGenerator()
video_generator = VideoGenerator()
worldtour_generator = WorldtourGenerator()
bundle_builder = BundleBuilder()
multimedia_seller = MultimediaTextSeller()


# ============================================
# HELPER FUNCTIONS
# ============================================

def check_sales_enabled():
    """
    Check if sales/payment functionality is enabled.
    Returns 403 error response if disabled.
    """
    if os.getenv('SALES_ENABLED', 'false').lower() != 'true':
        return jsonify({
            'error': 'Shop coming soon! Follow our Worldtour 🌍',
            'message': 'Payment system is currently disabled. We are building our audience through the Worldtour campaign.',
            'worldtour_active': True,
            'status': 'disabled'
        }), 403
    return None


# ============================================
# HEALTH & INFO ENDPOINTS
# ============================================

@app.route('/')
def index():
    """Landing page."""
    return render_template('worldtour_landing.html')


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'UMAJA Worldtour API',
        'version': '1.0.0'
    })


@app.route('/api/info')
def api_info():
    """API information and capabilities."""
    backends = voice_synthesizer.list_available_backends()
    
    return jsonify({
        'personalities': personality_engine.PERSONALITIES,
        'content_types': ['text', 'audio', 'image', 'video'],
        'product_tiers': list(bundle_builder.PRODUCT_TIERS.keys()),
        'tts_backends': backends,
        'worldtour_enabled': True,
        'sales_enabled': os.getenv('SALES_ENABLED', 'false').lower() == 'true'
    })


# ============================================
# WORLDTOUR ENDPOINTS
# ============================================

@app.route('/worldtour')
def worldtour_map():
    """Interactive world map landing page."""
    return render_template('worldtour_map.html')


@app.route('/worldtour/city/<city_id>')
def worldtour_city(city_id):
    """City-specific content page."""
    city = worldtour_generator.get_city(city_id)
    if not city:
        return jsonify({'error': 'City not found'}), 404
    
    return render_template('worldtour_city.html', city=city, city_id=city_id)


@app.route('/api/worldtour/cities')
def list_cities():
    """List all cities with stats."""
    visited_only = request.args.get('visited', 'false').lower() == 'true'
    cities = worldtour_generator.list_cities(visited_only=visited_only)
    stats = worldtour_generator.get_stats()
    
    return jsonify({
        'cities': cities,
        'stats': stats
    })


@app.route('/api/worldtour/next')
def get_next_city():
    """Get next scheduled city."""
    next_city = worldtour_generator.get_next_city()
    
    if not next_city:
        return jsonify({'error': 'No unvisited cities'}), 404
    
    return jsonify(next_city)


@app.route('/api/worldtour/queue')
def get_content_queue():
    """Get upcoming content queue."""
    days = int(request.args.get('days', 7))
    queue = worldtour_generator.create_content_queue(days)
    
    return jsonify({
        'queue': queue,
        'days': days
    })


@app.route('/api/worldtour/vote', methods=['POST'])
def vote_next_city():
    """Vote for next city (placeholder for real voting system)."""
    data = request.json
    city_id = data.get('city_id')
    
    if not city_id:
        return jsonify({'error': 'Missing city_id'}), 400
    
    city = worldtour_generator.get_city(city_id)
    if not city:
        return jsonify({'error': 'City not found'}), 404
    
    # In real implementation, this would update a voting database
    return jsonify({
        'success': True,
        'city_id': city_id,
        'message': f'Vote recorded for {city["name"]}'
    })


# ============================================
# CONTENT GENERATION ENDPOINTS
# ============================================

@app.route('/api/generate/text', methods=['POST'])
def generate_text():
    """Generate text content."""
    data = request.json
    
    try:
        result = personality_engine.generate_text(
            topic=data.get('topic'),
            personality=data.get('personality'),
            length=data.get('length', 'medium'),
            style_intensity=float(data.get('style_intensity', 0.7))
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Text generation failed: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate/audio', methods=['POST'])
def generate_audio():
    """Generate audio content."""
    data = request.json
    
    try:
        result = voice_synthesizer.synthesize(
            text=data.get('text'),
            personality=data.get('personality'),
            format=data.get('format', 'mp3')
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Audio generation failed: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate/image', methods=['POST'])
def generate_image():
    """Generate image content."""
    data = request.json
    image_type = data.get('type', 'quote_card')
    
    try:
        if image_type == 'quote_card':
            result = image_generator.generate_quote_card(
                quote=data.get('text'),
                personality=data.get('personality'),
                author_name=data.get('author_name')
            )
        else:  # ai_image
            result = image_generator.generate_ai_image(
                topic=data.get('topic'),
                personality=data.get('personality')
            )
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate/video', methods=['POST'])
def generate_video():
    """Generate video content."""
    data = request.json
    
    try:
        result = video_generator.create_lyric_video(
            text=data.get('text'),
            audio_path=data.get('audio_path'),
            personality=data.get('personality'),
            background_image=data.get('background_image')
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Video generation failed: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate/city-content', methods=['POST'])
def generate_city_content():
    """Generate city-specific content."""
    data = request.json
    
    try:
        result = worldtour_generator.generate_city_content(
            city_id=data.get('city_id'),
            personality=data.get('personality'),
            content_type=data.get('content_type')
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"City content generation failed: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================
# MULTIMEDIA PURCHASE ENDPOINTS
# ============================================

@app.route('/api/create-multimedia-sale', methods=['POST'])
def create_multimedia_sale():
    """Create multimedia purchase with all requested content types."""
    # Check if sales are enabled
    error_response = check_sales_enabled()
    if error_response:
        return error_response
    
    data = request.json
    
    try:
        result = multimedia_seller.create_multimedia_purchase(
            email=data.get('email'),
            topic=data.get('topic'),
            personality=data.get('personality'),
            content_types=data.get('content_types', ['text']),
            extras=data.get('extras', []),
            length=data.get('length', 'medium'),
            style_intensity=float(data.get('style_intensity', 0.7))
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Purchase creation failed: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/bundle/calculate', methods=['POST'])
def calculate_bundle():
    """Calculate bundle pricing."""
    # Check if sales are enabled
    error_response = check_sales_enabled()
    if error_response:
        return error_response
    
    data = request.json
    
    try:
        result = bundle_builder.calculate_bundle_price(
            items=data.get('items', []),
            personality_count=int(data.get('personality_count', 1)),
            extras=data.get('extras', []),
            apply_discount=data.get('apply_discount', True)
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"Bundle calculation failed: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/bundle/recommend', methods=['POST'])
def recommend_bundle():
    """Get bundle recommendations and upsells."""
    # Check if sales are enabled
    error_response = check_sales_enabled()
    if error_response:
        return error_response
    
    data = request.json
    
    try:
        current_items = data.get('items', [])
        recommendations = bundle_builder.get_upsell_recommendations(current_items)
        popular = bundle_builder.get_popular_bundles()
        
        return jsonify({
            'recommendations': recommendations,
            'popular_bundles': popular
        })
    except Exception as e:
        logger.error(f"Recommendation failed: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================
# DOWNLOAD & PREVIEW ENDPOINTS
# ============================================

@app.route('/download/<purchase_id>')
def download_purchase(purchase_id):
    """Download purchase package."""
    # Remove .zip extension if present
    if purchase_id.endswith('.zip'):
        purchase_id = purchase_id[:-4]
    
    zip_path = Path(multimedia_seller.output_dir) / f"{purchase_id}.zip"
    
    if not zip_path.exists():
        return jsonify({'error': 'Purchase not found'}), 404
    
    return send_file(
        str(zip_path),
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'umaja_{purchase_id}.zip'
    )


@app.route('/api/preview/<content_type>/<path:file_path>')
def preview_content(content_type, file_path):
    """Preview generated content."""
    # Security: ensure file is within allowed directories
    allowed_dirs = ['static/audio', 'static/images', 'static/videos']
    
    full_path = Path(file_path)
    if not any(str(full_path).startswith(d) for d in allowed_dirs):
        return jsonify({'error': 'Access denied'}), 403
    
    if not full_path.exists():
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(str(full_path))


# ============================================
# GALLERY & UI ENDPOINTS
# ============================================

@app.route('/gallery')
def gallery():
    """Content gallery page."""
    return render_template('gallery.html')


@app.route('/bundle-builder')
def bundle_builder_page():
    """Bundle builder interactive page."""
    return render_template('bundle_builder.html')


@app.route('/api/gallery/samples')
def get_gallery_samples():
    """Get sample content for gallery."""
    # In production, this would query a database or filesystem
    samples = {
        'john_cleese': [
            {
                'type': 'text',
                'topic': 'New York Pizza',
                'preview': 'Now, the curious thing about New York pizza...'
            }
        ],
        'c3po': [
            {
                'type': 'audio',
                'topic': 'London Tea',
                'preview': 'Oh my! London tea presents precisely 2,479...'
            }
        ],
        'robin_williams': [
            {
                'type': 'video',
                'topic': 'Tokyo Sushi',
                'preview': 'So Tokyo sushi walks into a bar... *laughs*'
            }
        ]
    }
    
    return jsonify(samples)


# ============================================
# ANALYTICS ENDPOINTS
# ============================================

@app.route('/api/analytics/sales')
def get_sales_analytics():
    """Get sales analytics."""
    try:
        stats = multimedia_seller.get_sales_stats()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Analytics failed: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analytics/worldtour')
def get_worldtour_analytics():
    """Get worldtour analytics."""
    try:
        stats = worldtour_generator.get_stats()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Analytics failed: {e}")
        return jsonify({'error': str(e)}), 500


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Endpoint not found'}), 404
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    logger.error(f"Server error: {error}")
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('500.html'), 500


# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'true').lower() == 'true'
    
    logger.info(f"Starting UMAJA Worldtour API on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
