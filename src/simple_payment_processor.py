"""
Simple PayPal Payment Processor
All payments go to ONE PayPal account - no complex payouts
"""

import os
import logging
from typing import Dict, Optional
import paypalrestsdk
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimplePaymentProcessor:
    """
    Simplified payment processor - all money goes to ONE PayPal account.
    No complex payouts, just payment links and tracking.
    """
    
    def __init__(self):
        """
        Initialize PayPal SDK with configuration from .env
        """
        self.paypal_email = os.getenv('PAYPAL_EMAIL', 'your-paypal@example.com')
        
        # Configure PayPal SDK
        paypalrestsdk.configure({
            "mode": os.getenv('PAYPAL_MODE', 'sandbox'),
            "client_id": os.getenv('PAYPAL_CLIENT_ID', ''),
            "client_secret": os.getenv('PAYPAL_SECRET', '')
        })
        
        self.server_url = os.getenv('SERVER_URL', 'http://localhost:5000')
        logger.info(f"PayPal configured in {os.getenv('PAYPAL_MODE', 'sandbox')} mode")
    
    def create_payment_link(self, amount: float, description: str, 
                           text_id: str, customer_email: str) -> Dict:
        """
        Create PayPal payment button/link.
        All money goes to PAYPAL_EMAIL from .env
        
        Args:
            amount: Payment amount in EUR
            description: Description of the purchase
            text_id: Unique text identifier
            customer_email: Customer's email address
            
        Returns:
            Dictionary containing:
                - payment_id: PayPal payment ID
                - payment_url: URL customer clicks to pay
                - amount: Payment amount
                - status: Payment status
        """
        try:
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": f"{self.server_url}/api/payment-success",
                    "cancel_url": f"{self.server_url}/api/payment-cancel"
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": description,
                            "sku": text_id,
                            "price": f"{amount:.2f}",
                            "currency": "EUR",
                            "quantity": 1
                        }]
                    },
                    "amount": {
                        "total": f"{amount:.2f}",
                        "currency": "EUR"
                    },
                    "description": description,
                    "custom": text_id,  # Store text_id for webhook lookup
                    "invoice_number": text_id[:10]  # Truncate for invoice
                }]
            })
            
            if payment.create():
                logger.info(f"Payment created: {payment.id}")
                
                # Get approval URL
                approval_url = None
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = link.href
                        break
                
                return {
                    'success': True,
                    'payment_id': payment.id,
                    'payment_url': approval_url,
                    'amount': amount,
                    'status': payment.state,
                    'text_id': text_id
                }
            else:
                logger.error(f"Payment creation failed: {payment.error}")
                return {
                    'success': False,
                    'error': payment.error,
                    'payment_id': None,
                    'payment_url': None
                }
                
        except Exception as e:
            logger.error(f"Exception creating payment: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'payment_id': None,
                'payment_url': None
            }
    
    def verify_payment(self, payment_id: str) -> Optional[Dict]:
        """
        Check if payment was completed and return details.
        
        Args:
            payment_id: PayPal payment ID
            
        Returns:
            Payment details or None if not found/failed
        """
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            
            if payment.state == "approved":
                # Extract transaction details
                transaction = payment.transactions[0]
                
                return {
                    'payment_id': payment.id,
                    'status': 'completed',
                    'amount': float(transaction.amount.total),
                    'currency': transaction.amount.currency,
                    'payer_email': payment.payer.payer_info.email,
                    'text_id': transaction.custom if hasattr(transaction, 'custom') else None,
                    'create_time': payment.create_time,
                    'update_time': payment.update_time
                }
            else:
                return {
                    'payment_id': payment.id,
                    'status': payment.state,
                    'amount': None,
                    'currency': None
                }
                
        except Exception as e:
            logger.error(f"Error verifying payment {payment_id}: {str(e)}")
            return None
    
    def get_payment_status(self, payment_id: str) -> str:
        """
        Get current payment status: pending/completed/failed
        
        Args:
            payment_id: PayPal payment ID
            
        Returns:
            Status string
        """
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            
            status_map = {
                'created': 'pending',
                'approved': 'completed',
                'failed': 'failed',
                'canceled': 'failed'
            }
            
            return status_map.get(payment.state, 'unknown')
            
        except Exception as e:
            logger.error(f"Error getting payment status: {str(e)}")
            return 'unknown'
    
    def execute_payment(self, payment_id: str, payer_id: str) -> bool:
        """
        Execute an approved PayPal payment.
        Called after user approves payment on PayPal site.
        
        Args:
            payment_id: PayPal payment ID
            payer_id: PayPal payer ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            
            if payment.execute({"payer_id": payer_id}):
                logger.info(f"Payment {payment_id} executed successfully")
                return True
            else:
                logger.error(f"Payment execution failed: {payment.error}")
                return False
                
        except Exception as e:
            logger.error(f"Exception executing payment: {str(e)}")
            return False


# Example usage
if __name__ == "__main__":
    processor = SimplePaymentProcessor()
    
    # Create a test payment
    result = processor.create_payment_link(
        amount=1.50,
        description="UMAJA Text - AI Ethics (Short)",
        text_id="test-12345",
        customer_email="customer@example.com"
    )
    
    if result['success']:
        print(f"✅ Payment created!")
        print(f"Payment URL: {result['payment_url']}")
        print(f"Payment ID: {result['payment_id']}")
    else:
        print(f"❌ Payment failed: {result.get('error')}")
