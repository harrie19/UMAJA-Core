"""
Auto Revenue System for UMAJA-Core
Main integration class that ties together text generation, payment processing,
revenue distribution, and email delivery
"""

import logging
from typing import Dict, Optional
from datetime import datetime
from src.rauschen_generator import RauschenGenerator
from src.vektor_analyzer import VektorAnalyzer
from src.payment_processor import PaymentProcessor
from src.revenue_distributor import RevenueDistributor
from src.transaction_logger import TransactionLogger
from src.email_sender import EmailSender

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutoRevenueSystem:
    """
    Orchestrates the complete revenue pipeline from text generation to delivery.
    """
    
    def __init__(self):
        """Initialize all system components."""
        logger.info("Initializing Auto Revenue System...")
        
        # Initialize components
        self.generator = RauschenGenerator()
        self.analyzer = VektorAnalyzer()
        self.payment_processor = PaymentProcessor()
        self.distributor = RevenueDistributor()
        self.logger = TransactionLogger()
        self.email_sender = EmailSender()
        
        # Check system readiness
        self.ready = self._check_system_readiness()
        
        if self.ready:
            logger.info("✅ Auto Revenue System ready")
        else:
            logger.warning("⚠️  Auto Revenue System partially configured")
    
    def _check_system_readiness(self) -> bool:
        """Check if all critical components are configured."""
        components = {
            'Payment Processor': self.payment_processor.configured,
            'Revenue Distributor': self.distributor.configured,
            'Email Sender': self.email_sender.configured
        }
        
        for component, status in components.items():
            if status:
                logger.info(f"  ✅ {component}: Ready")
            else:
                logger.warning(f"  ⚠️  {component}: Not configured")
        
        # System is ready if payment and distribution are configured
        return (self.payment_processor.configured and 
                self.distributor.configured)
    
    def process_text_purchase(self, customer_email: str, topic: str, 
                             length: str = 'short', 
                             noise_level: float = 0.3) -> Dict:
        """
        Process a text purchase request.
        
        This creates the text and payment request. The customer must then
        approve the payment via the returned URL.
        
        Args:
            customer_email: Customer's email address
            topic: Topic for text generation
            length: Text length ('short' or 'long')
            noise_level: Noise level for variation (0.0 to 1.0)
            
        Returns:
            Dictionary containing:
            - success: Boolean indicating success
            - text_id: Unique text identifier
            - payment_id: PayPal payment ID
            - approval_url: URL for customer to approve payment
            - amount: Payment amount
            - preview: Text preview (first 100 chars)
            - error: Error message (if failed)
        """
        try:
            logger.info(f"Processing text purchase for {customer_email}")
            
            # Step 1: Generate text
            logger.info(f"Generating text: topic='{topic}', length={length}, noise={noise_level}")
            text_result = self.generator.generate_reflection(
                topic=topic,
                length=length,
                noise_level=noise_level
            )
            
            text_id = text_result['text_id']
            amount = text_result['price']
            
            logger.info(f"Text generated: {text_id} ({text_result['word_count']} words, ${amount})")
            
            # Step 2: Analyze quality
            logger.info("Analyzing text quality...")
            analysis = self.analyzer.analyze_coherence(
                text_result['text'],
                topic
            )
            
            logger.info(f"Quality: {analysis['quality']} (score: {analysis['overall_score']:.3f})")
            
            # Step 3: Create payment request
            logger.info("Creating payment request...")
            payment_result = self.payment_processor.create_payment_request(
                amount=amount,
                description=f"UMAJA Generated Text - {topic} ({length})",
                text_id=text_id
            )
            
            if not payment_result['success']:
                logger.error(f"Payment creation failed: {payment_result.get('error')}")
                return {
                    'success': False,
                    'error': f"Payment creation failed: {payment_result.get('error')}"
                }
            
            # Store text data temporarily (would typically use Redis or database)
            # For now, we'll rely on transaction logger
            temp_transaction = {
                'text_id': text_id,
                'customer_email': customer_email,
                'payment_id': payment_result['payment_id'],
                'amount': amount,
                'text_data': text_result,
                'quality_analysis': analysis,
                'status': 'pending_payment'
            }
            
            self.logger.log_transaction(temp_transaction)
            
            logger.info(f"Payment request created: {payment_result['payment_id']}")
            
            return {
                'success': True,
                'text_id': text_id,
                'payment_id': payment_result['payment_id'],
                'approval_url': payment_result['approval_url'],
                'amount': amount,
                'word_count': text_result['word_count'],
                'quality': analysis['quality'],
                'preview': text_result['text'][:100] + '...',
                'message': 'Please complete payment via the approval URL'
            }
            
        except Exception as e:
            logger.error(f"Error processing text purchase: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def handle_completed_payment(self, payment_id: str, payer_id: str) -> Dict:
        """
        Handle a completed payment.
        
        This is called after the customer approves the payment via PayPal.
        
        Args:
            payment_id: PayPal payment ID
            payer_id: PayPal payer ID
            
        Returns:
            Dictionary containing:
            - success: Boolean indicating success
            - transaction_id: Final transaction ID
            - distribution_result: Revenue distribution details
            - error: Error message (if failed)
        """
        try:
            logger.info(f"Handling completed payment: {payment_id}")
            
            # Step 1: Execute payment
            logger.info("Executing payment...")
            execution_result = self.payment_processor.execute_payment(
                payment_id, payer_id
            )
            
            if not execution_result['success']:
                logger.error(f"Payment execution failed: {execution_result.get('error')}")
                return {
                    'success': False,
                    'error': f"Payment execution failed: {execution_result.get('error')}"
                }
            
            amount = execution_result['amount']
            payer_email = execution_result.get('payer_email')
            
            logger.info(f"Payment executed: ${amount} from {payer_email}")
            
            # Step 2: Find original transaction
            transactions = self.logger.get_all_transactions()
            original_tx = None
            for tx in transactions:
                if tx.get('payment_id') == payment_id:
                    original_tx = tx
                    break
            
            if not original_tx:
                logger.warning("Original transaction not found, continuing anyway...")
            
            text_id = original_tx.get('text_id') if original_tx else payment_id
            text_data = original_tx.get('text_data') if original_tx else None
            customer_email = original_tx.get('customer_email') or payer_email
            
            # Step 3: Distribute funds
            logger.info("Distributing revenue...")
            distribution_result = self.distributor.distribute_payment(
                total_amount=amount,
                transaction_id=payment_id,
                text_id=text_id,
                customer_email=customer_email,
                execute_payout=True
            )
            
            if not distribution_result['success']:
                logger.error(f"Distribution failed: {distribution_result.get('error')}")
                # Continue to deliver text even if distribution fails
            
            logger.info(f"Distribution completed: {distribution_result.get('payout_batch_id')}")
            
            # Step 4: Deliver text via email
            if text_data and customer_email:
                logger.info(f"Sending text to {customer_email}...")
                email_sent = self.email_sender.send_text_delivery(
                    recipient_email=customer_email,
                    text_data=text_data,
                    transaction_id=payment_id
                )
                
                if email_sent:
                    logger.info("Text delivered successfully")
                else:
                    logger.warning("Failed to send text email")
            else:
                logger.warning("Cannot send text - missing data or email")
            
            # Step 5: Update transaction status
            if original_tx:
                self.logger.update_transaction_status(
                    original_tx['transaction_id'],
                    'completed'
                )
            
            logger.info(f"✅ Payment {payment_id} processed successfully")
            
            return {
                'success': True,
                'transaction_id': payment_id,
                'amount': amount,
                'distribution_result': distribution_result,
                'email_delivered': text_data is not None and customer_email is not None,
                'message': 'Payment processed and text delivered'
            }
            
        except Exception as e:
            logger.error(f"Error handling completed payment: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_system_status(self) -> Dict:
        """
        Get current system status.
        
        Returns:
            Dictionary containing system status information
        """
        return {
            'ready': self.ready,
            'components': {
                'text_generator': True,  # Always available
                'quality_analyzer': True,  # Always available
                'payment_processor': self.payment_processor.configured,
                'revenue_distributor': self.distributor.configured,
                'email_sender': self.email_sender.configured
            },
            'distribution_summary': self.distributor.get_distribution_summary() if self.ready else {}
        }
    
    def generate_monthly_report(self, month: int, year: int) -> Dict:
        """
        Generate monthly financial report.
        
        Args:
            month: Month number (1-12)
            year: Year
            
        Returns:
            Monthly report data
        """
        return self.logger.get_monthly_report(month, year)


if __name__ == "__main__":
    # Example usage
    system = AutoRevenueSystem()
    
    print("="*60)
    print("UMAJA Auto Revenue System")
    print("="*60)
    
    status = system.get_system_status()
    
    print(f"\nSystem Status: {'✅ Ready' if status['ready'] else '⚠️ Not Ready'}")
    print("\nComponents:")
    for component, ready in status['components'].items():
        status_icon = '✅' if ready else '⚠️'
        print(f"  {status_icon} {component}")
    
    if status['ready']:
        print("\n✅ System is ready to process payments")
        print("\nTo test the system:")
        print("1. Configure all credentials in .env")
        print("2. Run the Flask API server")
        print("3. Create a test purchase via API")
    else:
        print("\n⚠️  System not fully configured")
        print("Please set the following in .env:")
        print("  - PAYPAL_CLIENT_ID and PAYPAL_SECRET")
        print("  - CHARITY_PAYPAL_EMAIL, OPERATIONS_PAYPAL_EMAIL, UPGRADES_PAYPAL_EMAIL")
        print("  - SMTP_USER and SMTP_PASSWORD")
