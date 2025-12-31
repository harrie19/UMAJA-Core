"""
Simple Flask Server for UMAJA Text Sales
Minimal API for payment processing and dashboard
"""

import os
import sys
from flask import Flask, request, jsonify, render_template, redirect
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.simple_text_seller import SimpleTextSeller

app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

seller = SimpleTextSeller()


@app.route('/')
def home():
    """Simple dashboard showing sales and balance"""
    try:
        stats = seller.get_seller_dashboard()
        return render_template('dashboard.html', stats=stats)
    except Exception as e:
        return f"Error loading dashboard: {str(e)}", 500


@app.route('/api/create-sale', methods=['POST'])
def create_sale():
    """
    Create new text sale
    POST JSON: {
        "email": "customer@example.com",
        "topic": "AI ethics",
        "length": "short",  // optional, default: "short"
        "noise_level": 0.4   // optional, default: 0.4
    }
    Returns: {
        "success": true,
        "payment_url": "https://paypal.com/...",
        "amount": 1.27,
        "text_preview": "...",
        "payment_id": "..."
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        email = data.get('email')
        topic = data.get('topic')
        length = data.get('length', 'short')
        noise_level = data.get('noise_level', 0.4)
        
        if not email or not topic:
            return jsonify({
                'success': False,
                'error': 'Email and topic are required'
            }), 400
        
        result = seller.create_purchase_link(
            customer_email=email,
            topic=topic,
            length=length,
            noise_level=noise_level
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/check-payment/<payment_id>', methods=['GET'])
def check_payment(payment_id):
    """
    Check if payment completed and get text
    GET /api/check-payment/<payment_id>
    Returns: {
        "success": true,
        "status": "delivered",
        "text": "...",
        "message": "..."
    }
    """
    try:
        result = seller.check_and_deliver(payment_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'failed',
            'error': str(e)
        }), 500


@app.route('/api/payment-success', methods=['GET'])
def payment_success():
    """
    PayPal redirect after successful payment
    Query params: paymentId, PayerID
    """
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')
    
    if not payment_id or not payer_id:
        return "Missing payment information", 400
    
    # Execute and deliver
    result = seller.check_and_deliver(payment_id, payer_id)
    
    if result['success']:
        # In a real app, send email with text here
        return f"""
        <html>
            <head><title>Payment Success</title></head>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px;">
                <h1 style="color: #28a745;">✅ Payment Successful!</h1>
                <p>Your text has been generated and is ready.</p>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3>Your Text ({result['word_count']} words):</h3>
                    <p style="white-space: pre-wrap; line-height: 1.6;">{result['text']}</p>
                </div>
                <p><small>Text ID: {result['text_id']}</small></p>
                <p><small>Thank you for your purchase! 40% of this sale supports charity.</small></p>
            </body>
        </html>
        """
    else:
        return f"Payment processing error: {result.get('message')}", 500


@app.route('/api/payment-cancel', methods=['GET'])
def payment_cancel():
    """PayPal redirect after cancelled payment"""
    return """
    <html>
        <head><title>Payment Cancelled</title></head>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px;">
            <h1 style="color: #dc3545;">❌ Payment Cancelled</h1>
            <p>Your payment was cancelled. No charges were made.</p>
            <p><a href="/">Return to dashboard</a></p>
        </body>
    </html>
    """


@app.route('/webhook/paypal', methods=['POST'])
def paypal_webhook():
    """
    PayPal IPN webhook (optional - for automation)
    Auto-delivers text when payment completes
    """
    # Note: In production, verify webhook signature
    try:
        data = request.get_json()
        
        if data.get('event_type') == 'PAYMENT.SALE.COMPLETED':
            payment_id = data.get('resource', {}).get('parent_payment')
            
            if payment_id:
                result = seller.check_and_deliver(payment_id)
                
                if result['success']:
                    return jsonify({'status': 'delivered'}), 200
        
        return jsonify({'status': 'ignored'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/charity', methods=['GET'])
def charity_report():
    """
    Show how much charity transfer is recommended
    GET /api/reports/charity
    Returns: {
        "current_balance": 156.40,
        "total_reserved": 1234.56,
        "total_transferred": 1078.16,
        "last_transfer": "2025-11-01"
    }
    """
    try:
        balance = seller.logger.get_charity_balance()
        return jsonify(balance), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/monthly/<int:year>/<int:month>', methods=['GET'])
def monthly_report(year, month):
    """
    Get monthly sales report
    GET /api/reports/monthly/2025/12
    """
    try:
        report = seller.logger.get_monthly_report(month, year)
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/tax/<int:year>', methods=['GET'])
def tax_report(year):
    """
    Export tax report for a year
    GET /api/reports/tax/2025
    """
    try:
        transactions = seller.logger.export_for_taxes(year)
        return jsonify({
            'year': year,
            'transactions': transactions,
            'total_income': sum(t['your_income'] for t in transactions),
            'total_charity': sum(t['charity_reserved'] for t in transactions)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard', methods=['GET'])
def api_dashboard():
    """Get dashboard data as JSON"""
    try:
        stats = seller.get_seller_dashboard()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print("="*60)
    print("🚀 UMAJA Simple Payment Server Starting...")
    print("="*60)
    print(f"Server URL: http://localhost:{port}")
    print(f"Dashboard: http://localhost:{port}/")
    print(f"API Docs: http://localhost:{port}/api/dashboard")
    print("="*60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
