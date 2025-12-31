"""
Webhook Handler for UMAJA-Core
Handles incoming webhooks from PayPal and other payment providers
"""

import os
import hmac
import hashlib
import json
import logging
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebhookHandler:
    """
    Handles webhook notifications from payment providers.
    """
    
    def __init__(self):
        """
        Initialize webhook handler.
        
        Environment variables:
        - WEBHOOK_SECRET: Secret for verifying webhook signatures
        """
        self.webhook_secret = os.getenv('WEBHOOK_SECRET', '')
        
        if not self.webhook_secret:
            logger.warning("WEBHOOK_SECRET not set. Webhook signature verification disabled.")
    
    def verify_webhook_signature(self, payload: str, signature: str, 
                                 algorithm: str = 'sha256') -> bool:
        """
        Verify webhook signature to ensure authenticity.
        
        Args:
            payload: Raw webhook payload (string)
            signature: Signature from webhook header
            algorithm: Hash algorithm (default: sha256)
            
        Returns:
            True if signature is valid, False otherwise
        """
        if not self.webhook_secret:
            logger.warning("Cannot verify signature - WEBHOOK_SECRET not configured")
            return False
        
        try:
            # Compute expected signature
            expected_signature = hmac.new(
                self.webhook_secret.encode(),
                payload.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Compare signatures (constant-time comparison)
            return hmac.compare_digest(signature, expected_signature)
            
        except Exception as e:
            logger.error(f"Error verifying signature: {e}")
            return False
    
    def handle_paypal_ipn(self, webhook_data: Dict) -> Dict:
        """
        Handle PayPal Instant Payment Notification (IPN).
        
        Args:
            webhook_data: Parsed webhook data from PayPal
            
        Returns:
            Dictionary containing:
            - success: Boolean indicating processing success
            - event_type: Type of PayPal event
            - action_taken: Description of action taken
            - error: Error message (if failed)
        """
        try:
            event_type = webhook_data.get('event_type', '')
            logger.info(f"Processing PayPal webhook: {event_type}")
            
            # Handle different event types
            if event_type == 'PAYMENT.SALE.COMPLETED':
                return self._handle_payment_completed(webhook_data)
            
            elif event_type == 'PAYMENT.SALE.REFUNDED':
                return self._handle_payment_refunded(webhook_data)
            
            elif event_type == 'PAYMENT.SALE.REVERSED':
                return self._handle_payment_reversed(webhook_data)
            
            else:
                logger.info(f"Unhandled event type: {event_type}")
                return {
                    'success': True,
                    'event_type': event_type,
                    'action_taken': 'Event logged but not processed'
                }
                
        except Exception as e:
            logger.error(f"Error handling PayPal webhook: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _handle_payment_completed(self, webhook_data: Dict) -> Dict:
        """Handle completed payment event."""
        try:
            # Extract payment details
            resource = webhook_data.get('resource', {})
            payment_id = resource.get('id', '')
            amount = float(resource.get('amount', {}).get('total', 0))
            payer_email = resource.get('payer', {}).get('email_address', '')
            
            logger.info(f"Payment completed: {payment_id} (${amount})")
            
            # This would trigger:
            # 1. Text generation (if not already done)
            # 2. Revenue distribution
            # 3. Email delivery
            # These should be handled by the AutoRevenueSystem
            
            return {
                'success': True,
                'event_type': 'PAYMENT.SALE.COMPLETED',
                'action_taken': 'Payment recorded, ready for processing',
                'payment_id': payment_id,
                'amount': amount,
                'payer_email': payer_email
            }
            
        except Exception as e:
            logger.error(f"Error handling payment completion: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _handle_payment_refunded(self, webhook_data: Dict) -> Dict:
        """Handle payment refund event."""
        try:
            resource = webhook_data.get('resource', {})
            payment_id = resource.get('sale_id', '')
            refund_amount = float(resource.get('amount', {}).get('total', 0))
            
            logger.info(f"Payment refunded: {payment_id} (${refund_amount})")
            
            return {
                'success': True,
                'event_type': 'PAYMENT.SALE.REFUNDED',
                'action_taken': 'Refund recorded',
                'payment_id': payment_id,
                'refund_amount': refund_amount
            }
            
        except Exception as e:
            logger.error(f"Error handling refund: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _handle_payment_reversed(self, webhook_data: Dict) -> Dict:
        """Handle payment reversal event."""
        try:
            resource = webhook_data.get('resource', {})
            payment_id = resource.get('id', '')
            
            logger.warning(f"Payment reversed: {payment_id}")
            
            return {
                'success': True,
                'event_type': 'PAYMENT.SALE.REVERSED',
                'action_taken': 'Reversal recorded',
                'payment_id': payment_id
            }
            
        except Exception as e:
            logger.error(f"Error handling reversal: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def handle_gumroad_ping(self, webhook_data: Dict) -> Dict:
        """
        Handle Gumroad webhook notification.
        
        Gumroad is simpler than PayPal and may be preferred for some users.
        
        Args:
            webhook_data: Parsed webhook data from Gumroad
            
        Returns:
            Dictionary containing processing results
        """
        try:
            sale_id = webhook_data.get('sale_id', '')
            product_id = webhook_data.get('product_id', '')
            email = webhook_data.get('email', '')
            price = float(webhook_data.get('price', 0)) / 100  # Gumroad sends cents
            
            logger.info(f"Gumroad sale: {sale_id} (${price})")
            
            # Extract custom fields if any
            custom_fields = webhook_data.get('custom_fields', {})
            text_id = custom_fields.get('text_id', '')
            
            return {
                'success': True,
                'platform': 'gumroad',
                'action_taken': 'Sale recorded, ready for processing',
                'sale_id': sale_id,
                'product_id': product_id,
                'email': email,
                'price': price,
                'text_id': text_id
            }
            
        except Exception as e:
            logger.error(f"Error handling Gumroad webhook: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def parse_webhook_payload(self, raw_payload: str, 
                             content_type: str = 'application/json') -> Dict:
        """
        Parse raw webhook payload.
        
        Args:
            raw_payload: Raw webhook payload string
            content_type: Content type of payload
            
        Returns:
            Parsed webhook data as dictionary
        """
        try:
            if content_type == 'application/json':
                return json.loads(raw_payload)
            else:
                logger.warning(f"Unsupported content type: {content_type}")
                return {}
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON payload: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error parsing payload: {e}")
            return {}


if __name__ == "__main__":
    # Example usage
    handler = WebhookHandler()
    
    # Test PayPal webhook
    sample_paypal_webhook = {
        'event_type': 'PAYMENT.SALE.COMPLETED',
        'resource': {
            'id': 'PAY_12345',
            'amount': {
                'total': '10.00',
                'currency': 'USD'
            },
            'payer': {
                'email_address': 'customer@example.com'
            }
        }
    }
    
    result = handler.handle_paypal_ipn(sample_paypal_webhook)
    print(f"✅ PayPal webhook handling test:")
    print(f"   Event: {result.get('event_type')}")
    print(f"   Action: {result.get('action_taken')}")
    
    # Test Gumroad webhook
    sample_gumroad_webhook = {
        'sale_id': 'GUMROAD_12345',
        'product_id': 'PROD_001',
        'email': 'customer@example.com',
        'price': 1000,  # $10.00 in cents
        'custom_fields': {
            'text_id': 'text_67890'
        }
    }
    
    result = handler.handle_gumroad_ping(sample_gumroad_webhook)
    print(f"\n✅ Gumroad webhook handling test:")
    print(f"   Platform: {result.get('platform')}")
    print(f"   Price: ${result.get('price')}")
