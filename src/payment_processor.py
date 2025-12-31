"""
Payment Processor for UMAJA-Core
Handles PayPal SDK integration for payment creation and execution
"""

import os
import logging
from typing import Dict, Optional, List
from datetime import datetime
import paypalrestsdk
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PaymentProcessor:
    """
    Handles PayPal payment processing including creation, execution,
    and payout distribution.
    """
    
    def __init__(self):
        """
        Initialize PayPal SDK with credentials from environment variables.
        
        Environment variables required:
        - PAYPAL_MODE: 'sandbox' or 'live'
        - PAYPAL_CLIENT_ID: PayPal API client ID
        - PAYPAL_SECRET: PayPal API secret
        """
        self.mode = os.getenv('PAYPAL_MODE', 'sandbox')
        self.client_id = os.getenv('PAYPAL_CLIENT_ID', '')
        self.secret = os.getenv('PAYPAL_SECRET', '')
        
        if not self.client_id or not self.secret:
            logger.warning("PayPal credentials not configured. Set PAYPAL_CLIENT_ID and PAYPAL_SECRET in .env")
            self.configured = False
            return
        
        # Configure PayPal SDK
        try:
            paypalrestsdk.configure({
                'mode': self.mode,
                'client_id': self.client_id,
                'client_secret': self.secret
            })
            self.configured = True
            logger.info(f"PayPal SDK configured in {self.mode} mode")
        except Exception as e:
            logger.error(f"Failed to configure PayPal SDK: {e}")
            self.configured = False
    
    def create_payment_request(self, amount: float, description: str, 
                              text_id: str, return_url: str = None,
                              cancel_url: str = None) -> Dict:
        """
        Create a PayPal payment request.
        
        Args:
            amount: Payment amount in USD
            description: Payment description
            text_id: Unique text identifier
            return_url: URL to redirect after payment approval
            cancel_url: URL to redirect if payment is cancelled
            
        Returns:
            Dictionary containing:
            - success: Boolean indicating success
            - payment_id: PayPal payment ID (if successful)
            - approval_url: URL for customer to approve payment (if successful)
            - error: Error message (if failed)
        """
        if not self.configured:
            return {
                'success': False,
                'error': 'PayPal not configured. Check credentials.'
            }
        
        # Default URLs
        base_url = os.getenv('SERVER_URL', 'http://localhost:5000')
        if not return_url:
            return_url = f"{base_url}/payment/success"
        if not cancel_url:
            cancel_url = f"{base_url}/payment/cancel"
        
        try:
            # Create payment object
            payment = paypalrestsdk.Payment({
                'intent': 'sale',
                'payer': {
                    'payment_method': 'paypal'
                },
                'redirect_urls': {
                    'return_url': return_url,
                    'cancel_url': cancel_url
                },
                'transactions': [{
                    'item_list': {
                        'items': [{
                            'name': 'UMAJA Generated Text',
                            'sku': text_id,
                            'price': f'{amount:.2f}',
                            'currency': 'USD',
                            'quantity': 1
                        }]
                    },
                    'amount': {
                        'total': f'{amount:.2f}',
                        'currency': 'USD'
                    },
                    'description': description
                }]
            })
            
            # Create payment
            if payment.create():
                logger.info(f"Payment created successfully: {payment.id}")
                
                # Extract approval URL
                approval_url = None
                for link in payment.links:
                    if link.rel == 'approval_url':
                        approval_url = link.href
                        break
                
                return {
                    'success': True,
                    'payment_id': payment.id,
                    'approval_url': approval_url,
                    'status': payment.state
                }
            else:
                logger.error(f"Payment creation failed: {payment.error}")
                return {
                    'success': False,
                    'error': str(payment.error)
                }
                
        except Exception as e:
            logger.error(f"Exception during payment creation: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def execute_payment(self, payment_id: str, payer_id: str) -> Dict:
        """
        Execute an approved payment.
        
        Args:
            payment_id: PayPal payment ID
            payer_id: PayPal payer ID
            
        Returns:
            Dictionary containing:
            - success: Boolean indicating success
            - transaction_id: Transaction ID (if successful)
            - amount: Payment amount (if successful)
            - status: Payment status
            - error: Error message (if failed)
        """
        if not self.configured:
            return {
                'success': False,
                'error': 'PayPal not configured. Check credentials.'
            }
        
        try:
            # Find payment
            payment = paypalrestsdk.Payment.find(payment_id)
            
            # Execute payment
            if payment.execute({'payer_id': payer_id}):
                logger.info(f"Payment executed successfully: {payment_id}")
                
                # Extract transaction details
                transaction = payment.transactions[0]
                amount = float(transaction.amount.total)
                
                return {
                    'success': True,
                    'transaction_id': payment.id,
                    'amount': amount,
                    'status': payment.state,
                    'payer_email': payment.payer.payer_info.email if hasattr(payment.payer, 'payer_info') else None,
                    'timestamp': datetime.utcnow().isoformat() + 'Z'
                }
            else:
                logger.error(f"Payment execution failed: {payment.error}")
                return {
                    'success': False,
                    'error': str(payment.error)
                }
                
        except Exception as e:
            logger.error(f"Exception during payment execution: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_payout(self, recipients: List[Dict]) -> Dict:
        """
        Create a mass payout to multiple recipients.
        
        Args:
            recipients: List of recipient dictionaries, each containing:
                - email: Recipient PayPal email
                - amount: Amount to send
                - note: Optional note
                - recipient_type: Type of recipient (charity, operations, upgrades)
                
        Returns:
            Dictionary containing:
            - success: Boolean indicating success
            - batch_id: Payout batch ID (if successful)
            - status: Payout status
            - error: Error message (if failed)
        """
        if not self.configured:
            return {
                'success': False,
                'error': 'PayPal not configured. Check credentials.'
            }
        
        try:
            # Create payout batch
            payout_items = []
            for idx, recipient in enumerate(recipients):
                payout_items.append({
                    'recipient_type': 'EMAIL',
                    'amount': {
                        'value': f"{recipient['amount']:.2f}",
                        'currency': 'USD'
                    },
                    'receiver': recipient['email'],
                    'note': recipient.get('note', f"UMAJA distribution - {recipient.get('recipient_type', 'payment')}"),
                    'sender_item_id': f"{recipient.get('transaction_id', 'tx')}_{idx}"
                })
            
            payout = paypalrestsdk.Payout({
                'sender_batch_header': {
                    'sender_batch_id': f"batch_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                    'email_subject': 'You have received a payment from UMAJA',
                },
                'items': payout_items
            })
            
            # Create payout
            if payout.create():
                logger.info(f"Payout created successfully: {payout.batch_header.payout_batch_id}")
                return {
                    'success': True,
                    'batch_id': payout.batch_header.payout_batch_id,
                    'status': payout.batch_header.batch_status
                }
            else:
                logger.error(f"Payout creation failed: {payout.error}")
                return {
                    'success': False,
                    'error': str(payout.error)
                }
                
        except Exception as e:
            logger.error(f"Exception during payout creation: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_payout_status(self, batch_id: str) -> Dict:
        """
        Verify the status of a payout batch.
        
        Args:
            batch_id: Payout batch ID
            
        Returns:
            Dictionary containing payout status information
        """
        if not self.configured:
            return {
                'success': False,
                'error': 'PayPal not configured. Check credentials.'
            }
        
        try:
            payout = paypalrestsdk.Payout.find(batch_id)
            
            return {
                'success': True,
                'batch_id': batch_id,
                'status': payout.batch_header.batch_status,
                'time_created': payout.batch_header.time_created,
                'items': [
                    {
                        'recipient': item.payout_item.receiver,
                        'amount': item.payout_item.amount.value,
                        'status': item.transaction_status
                    }
                    for item in payout.items
                ] if hasattr(payout, 'items') else []
            }
            
        except Exception as e:
            logger.error(f"Exception verifying payout status: {e}")
            return {
                'success': False,
                'error': str(e)
            }


if __name__ == "__main__":
    # Example usage
    processor = PaymentProcessor()
    
    if processor.configured:
        print("✅ PayPal SDK configured successfully")
        print(f"Mode: {processor.mode}")
    else:
        print("⚠️  PayPal not configured")
        print("Set PAYPAL_CLIENT_ID and PAYPAL_SECRET in .env file")
