"""
Simple Transaction Logger
Tracks all transactions with internal allocation tracking.
User decides when to actually transfer charity portion.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleTransactionLogger:
    """
    Logs all transactions with internal allocation tracking.
    User decides when to actually transfer charity portion.
    """
    
    def __init__(self, log_file: str = 'data/transactions.json'):
        """
        Initialize transaction logger.
        
        Args:
            log_file: Path to JSON file for storing transactions
        """
        self.log_file = log_file
        self.charity_percentage = 0.40
        self.operations_percentage = 0.30
        self.upgrades_percentage = 0.30
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Initialize log file if it doesn't exist
        if not os.path.exists(log_file):
            self._save_data({
                'transactions': [],
                'charity_transfers': [],
                'summary': {
                    'total_revenue': 0.0,
                    'charity_reserved': 0.0,
                    'charity_transferred': 0.0,
                    'operations_earned': 0.0,
                    'upgrades_reserved': 0.0
                }
            })
    
    def _load_data(self) -> Dict:
        """Load transaction data from file"""
        try:
            with open(self.log_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return {
                'transactions': [],
                'charity_transfers': [],
                'summary': {
                    'total_revenue': 0.0,
                    'charity_reserved': 0.0,
                    'charity_transferred': 0.0,
                    'operations_earned': 0.0,
                    'upgrades_reserved': 0.0
                }
            }
    
    def _save_data(self, data: Dict) -> None:
        """Save transaction data to file"""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
    
    def log_sale(self, transaction_data: Dict) -> Dict:
        """
        Log a completed sale transaction.
        
        Args:
            transaction_data: Dictionary containing:
                - payment_id: PayPal payment ID
                - amount: Total amount received
                - customer_email: Customer email
                - text_id: Text identifier
                - text_preview: Preview of delivered text
                - timestamp: Transaction timestamp
                
        Returns:
            Dictionary with allocation details
        """
        data = self._load_data()
        
        amount = transaction_data.get('amount', 0.0)
        
        # Calculate allocation
        allocation = {
            'charity': round(amount * self.charity_percentage, 2),
            'operations': round(amount * self.operations_percentage, 2),
            'upgrades': round(amount * self.upgrades_percentage, 2)
        }
        
        # Create transaction record
        transaction = {
            'payment_id': transaction_data.get('payment_id'),
            'text_id': transaction_data.get('text_id'),
            'amount': amount,
            'allocation': allocation,
            'customer_email': transaction_data.get('customer_email'),
            'text_preview': transaction_data.get('text_preview', '')[:100],
            'timestamp': transaction_data.get('timestamp', datetime.utcnow().isoformat())
        }
        
        # Add to transactions
        data['transactions'].append(transaction)
        
        # Update summary
        data['summary']['total_revenue'] += amount
        data['summary']['charity_reserved'] += allocation['charity']
        data['summary']['operations_earned'] += allocation['operations']
        data['summary']['upgrades_reserved'] += allocation['upgrades']
        
        self._save_data(data)
        
        logger.info(f"Transaction logged: {transaction['payment_id']} - €{amount:.2f}")
        
        return allocation
    
    def get_charity_balance(self) -> Dict:
        """
        Calculate total "owed" to charity (not yet transferred).
        
        Returns:
            Dictionary containing:
                - total_reserved: Total charity amount from all sales
                - total_transferred: Total already transferred
                - current_balance: Amount still to transfer
                - last_transfer_date: Date of last transfer
        """
        data = self._load_data()
        
        total_reserved = data['summary']['charity_reserved']
        total_transferred = data['summary']['charity_transferred']
        current_balance = total_reserved - total_transferred
        
        # Get last transfer date
        last_transfer_date = None
        if data['charity_transfers']:
            last_transfer_date = data['charity_transfers'][-1]['date']
        
        return {
            'total_reserved': round(total_reserved, 2),
            'total_transferred': round(total_transferred, 2),
            'current_balance': round(current_balance, 2),
            'last_transfer_date': last_transfer_date
        }
    
    def mark_charity_transferred(self, amount: float, date: str, 
                                charity: str, proof: str) -> None:
        """
        Record when you actually transfer money to charity.
        Updates balance tracking.
        
        Args:
            amount: Amount transferred
            date: Date of transfer (ISO format)
            charity: Charity name/organization
            proof: PayPal transaction ID or other proof
        """
        data = self._load_data()
        
        transfer = {
            'amount': amount,
            'date': date,
            'charity': charity,
            'proof': proof,
            'recorded_at': datetime.utcnow().isoformat()
        }
        
        data['charity_transfers'].append(transfer)
        data['summary']['charity_transferred'] += amount
        
        self._save_data(data)
        
        logger.info(f"Charity transfer recorded: €{amount:.2f} to {charity}")
    
    def get_monthly_report(self, month: int, year: int) -> Dict:
        """
        Generate monthly report.
        
        Args:
            month: Month number (1-12)
            year: Year (e.g., 2025)
            
        Returns:
            Dictionary containing:
                - total_revenue: Total received in your PayPal
                - charity_reserved: Amount reserved for charity
                - your_income: Your actual income (operations %)
                - upgrades_reserved: Amount for reinvestment
                - transaction_count: Number of transactions
        """
        data = self._load_data()
        
        # Filter transactions for the month
        month_transactions = []
        for t in data['transactions']:
            timestamp = datetime.fromisoformat(t['timestamp'].replace('Z', '+00:00'))
            if timestamp.month == month and timestamp.year == year:
                month_transactions.append(t)
        
        # Calculate totals
        total_revenue = sum(t['amount'] for t in month_transactions)
        charity_reserved = sum(t['allocation']['charity'] for t in month_transactions)
        your_income = sum(t['allocation']['operations'] for t in month_transactions)
        upgrades_reserved = sum(t['allocation']['upgrades'] for t in month_transactions)
        
        return {
            'month': month,
            'year': year,
            'total_revenue': round(total_revenue, 2),
            'charity_reserved': round(charity_reserved, 2),
            'your_income': round(your_income, 2),
            'upgrades_reserved': round(upgrades_reserved, 2),
            'transaction_count': len(month_transactions),
            'transactions': month_transactions
        }
    
    def export_for_taxes(self, year: int) -> List[Dict]:
        """
        Generate CSV-ready data for tax purposes.
        Shows all income and charity donations.
        
        Args:
            year: Year to export
            
        Returns:
            List of transaction dictionaries
        """
        data = self._load_data()
        
        # Filter for the year
        year_transactions = []
        for t in data['transactions']:
            timestamp = datetime.fromisoformat(t['timestamp'].replace('Z', '+00:00'))
            if timestamp.year == year:
                year_transactions.append({
                    'date': timestamp.strftime('%Y-%m-%d'),
                    'payment_id': t['payment_id'],
                    'total_amount': t['amount'],
                    'your_income': t['allocation']['operations'],
                    'charity_reserved': t['allocation']['charity'],
                    'upgrades_reserved': t['allocation']['upgrades']
                })
        
        return year_transactions
    
    def get_recent_transactions(self, limit: int = 10) -> List[Dict]:
        """
        Get most recent transactions.
        
        Args:
            limit: Maximum number of transactions to return
            
        Returns:
            List of recent transactions
        """
        data = self._load_data()
        return data['transactions'][-limit:][::-1]  # Most recent first
    
    def get_summary(self) -> Dict:
        """
        Get overall summary statistics.
        
        Returns:
            Summary dictionary
        """
        data = self._load_data()
        charity_balance = self.get_charity_balance()
        
        return {
            **data['summary'],
            'charity_balance': charity_balance['current_balance'],
            'transaction_count': len(data['transactions']),
            'transfer_count': len(data['charity_transfers'])
        }


# Example usage
if __name__ == "__main__":
    logger = SimpleTransactionLogger()
    
    # Log a test sale
    allocation = logger.log_sale({
        'payment_id': 'PAY-123456',
        'amount': 10.0,
        'customer_email': 'test@example.com',
        'text_id': 'text-abc-123',
        'text_preview': 'This is a test reflection...',
        'timestamp': datetime.utcnow().isoformat()
    })
    
    print("Allocation:")
    print(f"  Charity (40%): €{allocation['charity']:.2f}")
    print(f"  Operations (30%): €{allocation['operations']:.2f}")
    print(f"  Upgrades (30%): €{allocation['upgrades']:.2f}")
    
    # Check charity balance
    balance = logger.get_charity_balance()
    print(f"\nCharity Balance: €{balance['current_balance']:.2f}")
    
    # Get summary
    summary = logger.get_summary()
    print(f"\nTotal Revenue: €{summary['total_revenue']:.2f}")
    print(f"Transactions: {summary['transaction_count']}")
