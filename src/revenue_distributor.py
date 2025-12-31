"""
Revenue Distributor for UMAJA-Core
Handles automated distribution of funds to charity, operations, and upgrades accounts
"""

import os
import logging
from typing import Dict, List
from dotenv import load_dotenv
from src.distribution_engine import DistributionEngine
from src.payment_processor import PaymentProcessor
from src.transaction_logger import TransactionLogger

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RevenueDistributor:
    """
    Handles the distribution of revenue to charity, operations, and upgrades accounts.
    """
    
    def __init__(self):
        """
        Initialize revenue distributor.
        
        Environment variables required:
        - CHARITY_PAYPAL_EMAIL: PayPal email for charity account
        - OPERATIONS_PAYPAL_EMAIL: PayPal email for operations account
        - UPGRADES_PAYPAL_EMAIL: PayPal email for upgrades account
        """
        self.charity_email = os.getenv('CHARITY_PAYPAL_EMAIL', '')
        self.operations_email = os.getenv('OPERATIONS_PAYPAL_EMAIL', '')
        self.upgrades_email = os.getenv('UPGRADES_PAYPAL_EMAIL', '')
        
        # Initialize components
        self.distribution_engine = DistributionEngine()
        self.payment_processor = PaymentProcessor()
        self.transaction_logger = TransactionLogger()
        
        # Check configuration
        self.configured = self._check_configuration()
    
    def _check_configuration(self) -> bool:
        """Check if all required accounts are configured."""
        missing = []
        
        if not self.charity_email:
            missing.append('CHARITY_PAYPAL_EMAIL')
        if not self.operations_email:
            missing.append('OPERATIONS_PAYPAL_EMAIL')
        if not self.upgrades_email:
            missing.append('UPGRADES_PAYPAL_EMAIL')
        
        if missing:
            logger.warning(f"Missing configuration: {', '.join(missing)}")
            return False
        
        logger.info("Revenue distributor configured successfully")
        return True
    
    def distribute_payment(self, total_amount: float, transaction_id: str,
                          text_id: str = None, customer_email: str = None,
                          execute_payout: bool = True) -> Dict:
        """
        Distribute a payment to all three accounts.
        
        Args:
            total_amount: Total payment amount to distribute
            transaction_id: Unique transaction identifier
            text_id: Optional text ID associated with payment
            customer_email: Optional customer email
            execute_payout: Whether to execute PayPal payout (False for dry-run)
            
        Returns:
            Dictionary containing:
            - success: Boolean indicating success
            - allocation: Distribution breakdown
            - payout_batch_id: PayPal payout batch ID (if executed)
            - transaction_id: Logged transaction ID
            - error: Error message (if failed)
        """
        if not self.configured:
            return {
                'success': False,
                'error': 'Revenue distributor not configured. Check account emails in .env'
            }
        
        try:
            # Calculate distribution using engine
            allocation = self.distribution_engine.allocate_payment(total_amount)
            
            logger.info(f"Distributing ${total_amount:.2f}:")
            logger.info(f"  Charity: ${allocation['charity']:.2f}")
            logger.info(f"  Operations: ${allocation['operations']:.2f}")
            logger.info(f"  Upgrades: ${allocation['upgrades']:.2f}")
            
            # Prepare recipients for payout
            recipients = [
                {
                    'email': self.charity_email,
                    'amount': allocation['charity'],
                    'recipient_type': 'charity',
                    'note': f'UMAJA Charity Distribution - {transaction_id}',
                    'transaction_id': transaction_id
                },
                {
                    'email': self.operations_email,
                    'amount': allocation['operations'],
                    'recipient_type': 'operations',
                    'note': f'UMAJA Operations Distribution - {transaction_id}',
                    'transaction_id': transaction_id
                },
                {
                    'email': self.upgrades_email,
                    'amount': allocation['upgrades'],
                    'recipient_type': 'upgrades',
                    'note': f'UMAJA Upgrades Distribution - {transaction_id}',
                    'transaction_id': transaction_id
                }
            ]
            
            payout_batch_id = None
            payout_status = 'pending'
            
            # Execute payout if requested
            if execute_payout:
                payout_result = self.payment_processor.create_payout(recipients)
                
                if payout_result['success']:
                    payout_batch_id = payout_result['batch_id']
                    payout_status = payout_result['status']
                    logger.info(f"Payout created: {payout_batch_id}")
                else:
                    logger.error(f"Payout failed: {payout_result.get('error')}")
                    # Continue to log transaction even if payout fails
                    payout_status = 'failed'
            else:
                payout_status = 'dry_run'
                logger.info("Dry run - payout not executed")
            
            # Log transaction
            transaction_data = {
                'transaction_id': transaction_id,
                'text_id': text_id,
                'amount': total_amount,
                'customer_email': customer_email,
                'charity_amount': allocation['charity'],
                'operations_amount': allocation['operations'],
                'upgrades_amount': allocation['upgrades'],
                'charity_email': self.charity_email,
                'operations_email': self.operations_email,
                'upgrades_email': self.upgrades_email,
                'payout_batch_id': payout_batch_id,
                'payout_status': payout_status,
                'status': 'completed' if payout_batch_id else 'logged'
            }
            
            logged_tx_id = self.transaction_logger.log_transaction(transaction_data)
            
            return {
                'success': True,
                'allocation': allocation,
                'payout_batch_id': payout_batch_id,
                'payout_status': payout_status,
                'transaction_id': logged_tx_id,
                'recipients': recipients
            }
            
        except Exception as e:
            logger.error(f"Error distributing payment: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_distribution(self, batch_id: str) -> Dict:
        """
        Verify the status of a distribution payout.
        
        Args:
            batch_id: PayPal payout batch ID
            
        Returns:
            Dictionary containing verification results
        """
        if not self.configured or not self.payment_processor.configured:
            return {
                'success': False,
                'error': 'Not configured'
            }
        
        try:
            result = self.payment_processor.verify_payout_status(batch_id)
            
            if result['success']:
                logger.info(f"Payout {batch_id} status: {result['status']}")
                
                # Log status by recipient
                for item in result.get('items', []):
                    logger.info(f"  {item['recipient']}: {item['status']} (${item['amount']})")
            
            return result
            
        except Exception as e:
            logger.error(f"Error verifying distribution: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_distribution_summary(self) -> Dict:
        """
        Get a summary of all distributions.
        
        Returns:
            Dictionary containing distribution statistics
        """
        try:
            all_transactions = self.transaction_logger.get_all_transactions()
            
            total_distributed = 0.0
            total_charity = 0.0
            total_operations = 0.0
            total_upgrades = 0.0
            completed_count = 0
            
            for tx in all_transactions:
                if tx.get('status') == 'completed':
                    completed_count += 1
                    total_distributed += tx.get('amount', 0.0)
                    total_charity += tx.get('charity_amount', 0.0)
                    total_operations += tx.get('operations_amount', 0.0)
                    total_upgrades += tx.get('upgrades_amount', 0.0)
            
            return {
                'total_transactions': len(all_transactions),
                'completed_transactions': completed_count,
                'total_distributed': round(total_distributed, 2),
                'total_charity': round(total_charity, 2),
                'total_operations': round(total_operations, 2),
                'total_upgrades': round(total_upgrades, 2),
                'charity_email': self.charity_email,
                'operations_email': self.operations_email,
                'upgrades_email': self.upgrades_email
            }
            
        except Exception as e:
            logger.error(f"Error getting distribution summary: {e}")
            return {
                'error': str(e)
            }


if __name__ == "__main__":
    # Example usage
    distributor = RevenueDistributor()
    
    if distributor.configured:
        print("✅ Revenue distributor configured")
        print(f"Charity: {distributor.charity_email}")
        print(f"Operations: {distributor.operations_email}")
        print(f"Upgrades: {distributor.upgrades_email}")
        
        # Dry run test
        result = distributor.distribute_payment(
            total_amount=10.0,
            transaction_id='TEST_TX_001',
            text_id='text_12345',
            customer_email='customer@example.com',
            execute_payout=False  # Dry run
        )
        
        if result['success']:
            print("\n✅ Distribution test successful (dry run)")
            print(f"Charity: ${result['allocation']['charity']:.2f}")
            print(f"Operations: ${result['allocation']['operations']:.2f}")
            print(f"Upgrades: ${result['allocation']['upgrades']:.2f}")
        else:
            print(f"\n❌ Distribution test failed: {result.get('error')}")
    else:
        print("⚠️  Revenue distributor not configured")
        print("Set CHARITY_PAYPAL_EMAIL, OPERATIONS_PAYPAL_EMAIL, and UPGRADES_PAYPAL_EMAIL in .env")
