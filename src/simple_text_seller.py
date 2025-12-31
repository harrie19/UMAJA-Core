"""
Simple Text Seller
Main class that handles the complete purchase flow
"""

import os
import json
import logging
from typing import Dict, Optional
from datetime import datetime

from src.rauschen_generator import RauschenGenerator
from src.vektor_analyzer import VektorAnalyzer
from src.simple_payment_processor import SimplePaymentProcessor
from src.simple_transaction_logger import SimpleTransactionLogger

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleTextSeller:
    """
    Main class that handles everything:
    1. Customer wants to buy text
    2. Generate PayPal payment link
    3. Customer pays (money goes to your PayPal)
    4. System detects payment
    5. Deliver text
    6. Log transaction with allocation
    """
    
    def __init__(self):
        """Initialize all components"""
        self.generator = RauschenGenerator()
        self.analyzer = VektorAnalyzer()
        self.payment = SimplePaymentProcessor()
        self.logger = SimpleTransactionLogger()
        
        # Storage for pending transactions
        self.pending_file = 'data/pending_texts.json'
        os.makedirs('data', exist_ok=True)
        
        if not os.path.exists(self.pending_file):
            self._save_pending({})
    
    def _load_pending(self) -> Dict:
        """Load pending texts from storage"""
        try:
            with open(self.pending_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading pending texts: {str(e)}")
            return {}
    
    def _save_pending(self, data: Dict) -> None:
        """Save pending texts to storage"""
        try:
            with open(self.pending_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving pending texts: {str(e)}")
    
    def create_purchase_link(self, customer_email: str, topic: str, 
                            length: str = 'short', noise_level: float = 0.4) -> Dict:
        """
        Step 1: Generate text and create payment link.
        
        Args:
            customer_email: Customer's email address
            topic: Topic for text generation
            length: 'short' or 'long'
            noise_level: Noise variation level (0.0 to 1.0)
            
        Returns:
            Dictionary containing:
                - success: True/False
                - payment_url: PayPal payment URL to share with customer
                - amount: Price
                - text_preview: First 200 characters
                - text_id: Unique identifier
                - payment_id: PayPal payment ID
        """
        try:
            # Generate the text
            logger.info(f"Generating {length} text about '{topic}'")
            result = self.generator.generate_reflection(
                topic=topic,
                length=length,
                noise_level=noise_level
            )
            
            text_id = result['text_id']
            amount = result['price']
            full_text = result['text']
            word_count = result['word_count']
            
            # Create payment link
            description = f"UMAJA Text - {topic} ({length.capitalize()}, {word_count} words)"
            
            payment_result = self.payment.create_payment_link(
                amount=amount,
                description=description,
                text_id=text_id,
                customer_email=customer_email
            )
            
            if not payment_result['success']:
                return {
                    'success': False,
                    'error': payment_result.get('error', 'Payment creation failed')
                }
            
            # Store pending transaction
            pending = self._load_pending()
            pending[payment_result['payment_id']] = {
                'text_id': text_id,
                'text': full_text,
                'topic': topic,
                'length': length,
                'noise_level': noise_level,
                'word_count': word_count,
                'amount': amount,
                'customer_email': customer_email,
                'created_at': datetime.utcnow().isoformat(),
                'delivered': False
            }
            self._save_pending(pending)
            
            # Create preview (first 200 characters)
            preview = full_text[:200] + '...' if len(full_text) > 200 else full_text
            
            logger.info(f"Purchase link created: {payment_result['payment_id']}")
            
            return {
                'success': True,
                'payment_url': payment_result['payment_url'],
                'payment_id': payment_result['payment_id'],
                'amount': amount,
                'text_preview': preview,
                'text_id': text_id,
                'word_count': word_count
            }
            
        except Exception as e:
            logger.error(f"Error creating purchase link: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def check_and_deliver(self, payment_id: str, payer_id: Optional[str] = None) -> Dict:
        """
        Step 2: Check if payment completed, then deliver text.
        Called by webhook or manually.
        
        Args:
            payment_id: PayPal payment ID
            payer_id: Optional payer ID for executing payment
            
        Returns:
            Dictionary containing:
                - success: True/False
                - status: 'delivered', 'pending', 'failed'
                - text: Full text (if delivered)
                - message: Status message
        """
        try:
            # Execute payment if payer_id provided
            if payer_id:
                logger.info(f"Executing payment {payment_id}")
                self.payment.execute_payment(payment_id, payer_id)
            
            # Verify payment
            payment_info = self.payment.verify_payment(payment_id)
            
            if not payment_info:
                return {
                    'success': False,
                    'status': 'failed',
                    'message': 'Payment not found'
                }
            
            if payment_info['status'] != 'completed':
                return {
                    'success': False,
                    'status': 'pending',
                    'message': f"Payment status: {payment_info['status']}"
                }
            
            # Get pending text
            pending = self._load_pending()
            
            if payment_id not in pending:
                return {
                    'success': False,
                    'status': 'failed',
                    'message': 'Pending text not found'
                }
            
            text_data = pending[payment_id]
            
            # Check if already delivered
            if text_data.get('delivered', False):
                return {
                    'success': True,
                    'status': 'already_delivered',
                    'text': text_data['text'],
                    'message': 'Text already delivered'
                }
            
            # Mark as delivered
            text_data['delivered'] = True
            text_data['delivered_at'] = datetime.utcnow().isoformat()
            pending[payment_id] = text_data
            self._save_pending(pending)
            
            # Log transaction with allocation
            self.logger.log_sale({
                'payment_id': payment_id,
                'amount': payment_info['amount'],
                'customer_email': payment_info.get('payer_email', text_data['customer_email']),
                'text_id': text_data['text_id'],
                'text_preview': text_data['text'][:100],
                'timestamp': payment_info.get('update_time', datetime.utcnow().isoformat())
            })
            
            logger.info(f"Text delivered for payment {payment_id}")
            
            return {
                'success': True,
                'status': 'delivered',
                'text': text_data['text'],
                'text_id': text_data['text_id'],
                'word_count': text_data['word_count'],
                'amount': text_data['amount'],
                'message': 'Text delivered successfully'
            }
            
        except Exception as e:
            logger.error(f"Error delivering text: {str(e)}")
            return {
                'success': False,
                'status': 'failed',
                'message': str(e)
            }
    
    def get_seller_dashboard(self) -> Dict:
        """
        Quick overview for seller.
        
        Returns:
            Dictionary containing:
                - total_revenue: Total sales
                - your_income: Operations portion (30%)
                - charity_owed: Amount to transfer to charity
                - recent_transactions: Last 5 transactions
                - charity_balance_info: Charity balance details
        """
        summary = self.logger.get_summary()
        charity_balance = self.logger.get_charity_balance()
        recent = self.logger.get_recent_transactions(limit=5)
        
        return {
            'total_revenue': summary['total_revenue'],
            'your_income': summary['operations_earned'],
            'charity_owed': charity_balance['current_balance'],
            'charity_transferred': charity_balance['total_transferred'],
            'upgrades_reserved': summary['upgrades_reserved'],
            'transaction_count': summary['transaction_count'],
            'recent_transactions': recent,
            'last_transfer_date': charity_balance['last_transfer_date']
        }
    
    def get_text_by_payment_id(self, payment_id: str) -> Optional[Dict]:
        """
        Get text information by payment ID.
        
        Args:
            payment_id: PayPal payment ID
            
        Returns:
            Text data or None
        """
        pending = self._load_pending()
        return pending.get(payment_id)


# Example usage
if __name__ == "__main__":
    seller = SimpleTextSeller()
    
    # Create a purchase
    result = seller.create_purchase_link(
        customer_email="customer@example.com",
        topic="artificial intelligence ethics",
        length="short",
        noise_level=0.4
    )
    
    if result['success']:
        print(f"✅ Payment link created!")
        print(f"Amount: €{result['amount']:.2f}")
        print(f"Payment URL: {result['payment_url']}")
        print(f"Preview: {result['text_preview']}")
    else:
        print(f"❌ Error: {result.get('error')}")
