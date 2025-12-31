"""
Flask API Server for UMAJA-Core
Provides REST API endpoints for text purchase and webhook handling
"""

import os
import sys
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.auto_revenue_system import AutoRevenueSystem
from src.webhook_handler import WebhookHandler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize system components
revenue_system = AutoRevenueSystem()
webhook_handler = WebhookHandler()

# Store payment sessions temporarily (in production, use Redis or database)
# TODO: For production deployment, replace with Redis or database storage
# Example: redis_client.setex(payment_id, 3600, json.dumps(session_data))
# This in-memory storage is only suitable for development/testing
payment_sessions = {}


@app.route('/')
def index():
    """API root endpoint."""
    return jsonify({
        'name': 'UMAJA-Core Payment API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'purchase': '/api/purchase',
            'status': '/api/status/<transaction_id>',
            'paypal_webhook': '/webhook/paypal',
            'gumroad_webhook': '/webhook/gumroad',
            'payment_success': '/payment/success',
            'payment_cancel': '/payment/cancel',
            'system_status': '/api/system/status'
        }
    })


@app.route('/api/purchase', methods=['POST'])
def create_purchase():
    """
    Create a text purchase and payment request.
    
    Request body:
    {
        "email": "customer@example.com",
        "topic": "artificial intelligence",
        "length": "short",  // optional, default: "short"
        "noise_level": 0.3  // optional, default: 0.3
    }
    
    Response:
    {
        "success": true,
        "text_id": "...",
        "payment_id": "...",
        "approval_url": "...",
        "amount": 10.00,
        "preview": "..."
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'email' not in data or 'topic' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: email, topic'
            }), 400
        
        email = data['email']
        topic = data['topic']
        length = data.get('length', 'short')
        noise_level = float(data.get('noise_level', 0.3))
        
        # Validate inputs
        if length not in ['short', 'long']:
            return jsonify({
                'success': False,
                'error': 'Length must be "short" or "long"'
            }), 400
        
        if not 0.0 <= noise_level <= 1.0:
            return jsonify({
                'success': False,
                'error': 'Noise level must be between 0.0 and 1.0'
            }), 400
        
        logger.info(f"Purchase request: email={email}, topic={topic}, length={length}")
        
        # Process purchase
        result = revenue_system.process_text_purchase(
            customer_email=email,
            topic=topic,
            length=length,
            noise_level=noise_level
        )
        
        if result['success']:
            # Store session data
            payment_sessions[result['payment_id']] = {
                'text_id': result['text_id'],
                'email': email,
                'created_at': request.headers.get('Date')
            }
            
            logger.info(f"Purchase created: {result['payment_id']}")
            return jsonify(result), 200
        else:
            logger.error(f"Purchase failed: {result.get('error')}")
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error creating purchase: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/payment/success', methods=['GET'])
def payment_success():
    """
    Handle successful payment return from PayPal.
    
    Query params: paymentId, PayerID
    """
    try:
        payment_id = request.args.get('paymentId')
        payer_id = request.args.get('PayerID')
        
        if not payment_id or not payer_id:
            return jsonify({
                'success': False,
                'error': 'Missing payment information'
            }), 400
        
        logger.info(f"Payment success callback: {payment_id}")
        
        # Handle completed payment
        result = revenue_system.handle_completed_payment(payment_id, payer_id)
        
        if result['success']:
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Payment Successful</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        max-width: 600px;
                        margin: 50px auto;
                        padding: 20px;
                        text-align: center;
                    }}
                    .success {{
                        color: #4CAF50;
                        font-size: 3em;
                    }}
                    .message {{
                        font-size: 1.2em;
                        margin: 20px 0;
                    }}
                    .details {{
                        background: #f0f0f0;
                        padding: 20px;
                        border-radius: 5px;
                        text-align: left;
                    }}
                </style>
            </head>
            <body>
                <div class="success">✅</div>
                <h1>Payment Successful!</h1>
                <p class="message">Your text has been generated and sent to your email.</p>
                <div class="details">
                    <p><strong>Transaction ID:</strong> {result['transaction_id']}</p>
                    <p><strong>Amount:</strong> ${result['amount']:.2f}</p>
                    <p><strong>Status:</strong> {result['message']}</p>
                </div>
                <p style="margin-top: 30px; color: #666;">
                    Thank you for supporting UMAJA!
                </p>
            </body>
            </html>
            """
        else:
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Processing Error</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        max-width: 600px;
                        margin: 50px auto;
                        padding: 20px;
                        text-align: center;
                    }}
                    .error {{
                        color: #f44336;
                        font-size: 3em;
                    }}
                </style>
            </head>
            <body>
                <div class="error">⚠️</div>
                <h1>Processing Error</h1>
                <p>There was an error processing your payment.</p>
                <p>{result.get('error', 'Unknown error')}</p>
                <p>Please contact support if this issue persists.</p>
            </body>
            </html>
            """
            
    except Exception as e:
        logger.error(f"Error in payment success handler: {e}")
        return f"<h1>Error</h1><p>{str(e)}</p>", 500


@app.route('/payment/cancel', methods=['GET'])
def payment_cancel():
    """Handle cancelled payment."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Payment Cancelled</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                text-align: center;
            }
            .cancel {
                color: #ff9800;
                font-size: 3em;
            }
        </style>
    </head>
    <body>
        <div class="cancel">🔙</div>
        <h1>Payment Cancelled</h1>
        <p>Your payment was cancelled.</p>
        <p>No charges were made to your account.</p>
        <p>Feel free to try again whenever you're ready.</p>
    </body>
    </html>
    """


@app.route('/webhook/paypal', methods=['POST'])
def paypal_webhook():
    """
    Handle PayPal webhook notifications.
    
    PayPal sends IPN (Instant Payment Notification) to this endpoint.
    """
    try:
        # Get raw payload and signature
        payload = request.get_data(as_text=True)
        signature = request.headers.get('PayPal-Transmission-Sig', '')
        
        logger.info("Received PayPal webhook")
        
        # Verify signature (required for security)
        if not webhook_handler.webhook_secret:
            logger.error("WEBHOOK_SECRET not configured - rejecting webhook")
            return jsonify({
                'success': False,
                'error': 'Webhook verification not configured'
            }), 500
        
        if not webhook_handler.verify_webhook_signature(payload, signature):
            logger.warning("Invalid webhook signature - possible attack attempt")
            return jsonify({
                'success': False,
                'error': 'Invalid signature'
            }), 401
        
        # Parse and handle webhook
        webhook_data = request.get_json()
        result = webhook_handler.handle_paypal_ipn(webhook_data)
        
        if result['success']:
            # For payment completion events, process the payment
            if result.get('event_type') == 'PAYMENT.SALE.COMPLETED':
                payment_id = result.get('payment_id')
                # Note: In production, you'd need to get payer_id from stored session
                logger.info(f"Payment completed via webhook: {payment_id}")
            
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error handling PayPal webhook: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/webhook/gumroad', methods=['POST'])
def gumroad_webhook():
    """
    Handle Gumroad webhook notifications.
    
    Gumroad is a simpler alternative to PayPal direct integration.
    """
    try:
        webhook_data = request.get_json()
        
        logger.info("Received Gumroad webhook")
        
        result = webhook_handler.handle_gumroad_ping(webhook_data)
        
        if result['success']:
            logger.info(f"Gumroad sale processed: {result.get('sale_id')}")
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        logger.error(f"Error handling Gumroad webhook: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/status/<transaction_id>', methods=['GET'])
def check_status(transaction_id):
    """
    Check transaction status.
    
    Response:
    {
        "success": true,
        "transaction": {...}
    }
    """
    try:
        transaction = revenue_system.logger.get_transaction(transaction_id)
        
        if transaction:
            return jsonify({
                'success': True,
                'transaction': transaction
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Transaction not found'
            }), 404
            
    except Exception as e:
        logger.error(f"Error checking status: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/system/status', methods=['GET'])
def system_status():
    """
    Get system status.
    
    Response:
    {
        "ready": true,
        "components": {...},
        "distribution_summary": {...}
    }
    """
    try:
        status = revenue_system.get_system_status()
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'system_ready': revenue_system.ready
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("="*60)
    print("UMAJA-Core Payment API Server")
    print("="*60)
    
    status = revenue_system.get_system_status()
    
    print(f"\nSystem Status: {'✅ Ready' if status['ready'] else '⚠️ Not Ready'}")
    print("\nComponents:")
    for component, ready in status['components'].items():
        status_icon = '✅' if ready else '⚠️'
        print(f"  {status_icon} {component}")
    
    if not status['ready']:
        print("\n⚠️  Warning: System not fully configured")
        print("Some features may not work. Check .env configuration.")
    
    print("\n" + "="*60)
    print("Starting server...")
    print("="*60 + "\n")
    
    # Run server
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
