"""
Transaction Logger for UMAJA-Core
Logs all payment transactions to JSON file for audit trail and reporting
"""

import os
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
import csv
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransactionLogger:
    """
    Handles transaction logging to JSON file with reporting capabilities.
    """
    
    def __init__(self, log_file: str = 'data/transactions.json'):
        """
        Initialize transaction logger.
        
        Args:
            log_file: Path to JSON file for storing transactions
        """
        self.log_file = log_file
        self._ensure_log_file_exists()
    
    def _ensure_log_file_exists(self):
        """Ensure the log file and directory exist."""
        log_path = Path(self.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not log_path.exists():
            log_path.write_text('[]')
            logger.info(f"Created transaction log file: {self.log_file}")
    
    def _read_transactions(self) -> List[Dict]:
        """Read all transactions from log file."""
        try:
            with open(self.log_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error("Corrupted transaction log. Starting fresh.")
            return []
        except Exception as e:
            logger.error(f"Error reading transactions: {e}")
            return []
    
    def _write_transactions(self, transactions: List[Dict]):
        """Write transactions to log file."""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(transactions, f, indent=2)
        except Exception as e:
            logger.error(f"Error writing transactions: {e}")
    
    def log_transaction(self, transaction_data: Dict) -> str:
        """
        Log a transaction.
        
        Args:
            transaction_data: Dictionary containing transaction details:
                - text_id: Unique text identifier
                - payment_id: PayPal payment ID
                - amount: Total payment amount
                - customer_email: Customer email address
                - charity_amount: Amount distributed to charity
                - operations_amount: Amount distributed to operations
                - upgrades_amount: Amount distributed to upgrades
                - status: Transaction status
                - timestamp: Optional timestamp (auto-generated if not provided)
                - metadata: Optional additional metadata
                
        Returns:
            transaction_id: Unique transaction identifier
        """
        # Generate transaction ID if not provided
        transaction_id = transaction_data.get('transaction_id', 
                                             f"TX_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}")
        
        # Add timestamp if not provided
        if 'timestamp' not in transaction_data:
            transaction_data['timestamp'] = datetime.utcnow().isoformat() + 'Z'
        
        # Add transaction ID
        transaction_data['transaction_id'] = transaction_id
        
        # Read existing transactions
        transactions = self._read_transactions()
        
        # Add new transaction
        transactions.append(transaction_data)
        
        # Write updated transactions
        self._write_transactions(transactions)
        
        logger.info(f"Transaction logged: {transaction_id}")
        return transaction_id
    
    def get_transaction(self, transaction_id: str) -> Optional[Dict]:
        """
        Retrieve a specific transaction by ID.
        
        Args:
            transaction_id: Transaction ID to retrieve
            
        Returns:
            Transaction dictionary or None if not found
        """
        transactions = self._read_transactions()
        
        for transaction in transactions:
            if transaction.get('transaction_id') == transaction_id:
                return transaction
        
        return None
    
    def get_transactions_by_date_range(self, start_date: str, 
                                      end_date: str) -> List[Dict]:
        """
        Get transactions within a date range.
        
        Args:
            start_date: Start date (ISO format: YYYY-MM-DD)
            end_date: End date (ISO format: YYYY-MM-DD)
            
        Returns:
            List of transactions in date range
        """
        transactions = self._read_transactions()
        filtered = []
        
        for transaction in transactions:
            timestamp = transaction.get('timestamp', '')
            if timestamp:
                # Extract date from ISO timestamp
                tx_date = timestamp.split('T')[0]
                if start_date <= tx_date <= end_date:
                    filtered.append(transaction)
        
        return filtered
    
    def get_monthly_report(self, month: int, year: int) -> Dict:
        """
        Generate a monthly report for tax and accounting purposes.
        
        Args:
            month: Month number (1-12)
            year: Year (e.g., 2025)
            
        Returns:
            Dictionary containing:
            - total_revenue: Total revenue for the month
            - total_charity: Total distributed to charity
            - total_operations: Total distributed to operations
            - total_upgrades: Total distributed to upgrades
            - transaction_count: Number of transactions
            - transactions: List of all transactions
        """
        # Format date range
        start_date = f"{year}-{month:02d}-01"
        
        # Calculate end date (last day of month)
        if month == 12:
            end_date = f"{year}-{month:02d}-31"
        else:
            next_month = month + 1
            end_date = f"{year}-{month:02d}-31"
        
        transactions = self.get_transactions_by_date_range(start_date, end_date)
        
        # Calculate totals
        total_revenue = 0.0
        total_charity = 0.0
        total_operations = 0.0
        total_upgrades = 0.0
        
        for tx in transactions:
            if tx.get('status') == 'completed':
                total_revenue += tx.get('amount', 0.0)
                total_charity += tx.get('charity_amount', 0.0)
                total_operations += tx.get('operations_amount', 0.0)
                total_upgrades += tx.get('upgrades_amount', 0.0)
        
        return {
            'month': month,
            'year': year,
            'total_revenue': round(total_revenue, 2),
            'total_charity': round(total_charity, 2),
            'total_operations': round(total_operations, 2),
            'total_upgrades': round(total_upgrades, 2),
            'transaction_count': len(transactions),
            'transactions': transactions
        }
    
    def export_csv(self, start_date: str, end_date: str, 
                   output_file: str = None) -> str:
        """
        Export transactions to CSV format for accounting software.
        
        Args:
            start_date: Start date (ISO format: YYYY-MM-DD)
            end_date: End date (ISO format: YYYY-MM-DD)
            output_file: Optional output file path (auto-generated if not provided)
            
        Returns:
            Path to exported CSV file
        """
        if not output_file:
            output_file = f"data/transactions_{start_date}_to_{end_date}.csv"
        
        # Ensure directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        transactions = self.get_transactions_by_date_range(start_date, end_date)
        
        # Write CSV
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = [
                'transaction_id', 'timestamp', 'text_id', 'payment_id',
                'customer_email', 'amount', 'charity_amount', 
                'operations_amount', 'upgrades_amount', 'status'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, 
                                   extrasaction='ignore')
            writer.writeheader()
            
            for tx in transactions:
                writer.writerow(tx)
        
        logger.info(f"Exported {len(transactions)} transactions to {output_file}")
        return output_file
    
    def get_all_transactions(self) -> List[Dict]:
        """
        Get all transactions.
        
        Returns:
            List of all transactions
        """
        return self._read_transactions()
    
    def update_transaction_status(self, transaction_id: str, 
                                  status: str) -> bool:
        """
        Update the status of a transaction.
        
        Args:
            transaction_id: Transaction ID to update
            status: New status
            
        Returns:
            True if updated successfully, False otherwise
        """
        transactions = self._read_transactions()
        
        for transaction in transactions:
            if transaction.get('transaction_id') == transaction_id:
                transaction['status'] = status
                transaction['updated_at'] = datetime.utcnow().isoformat() + 'Z'
                self._write_transactions(transactions)
                logger.info(f"Updated transaction {transaction_id} status to {status}")
                return True
        
        logger.warning(f"Transaction not found: {transaction_id}")
        return False


if __name__ == "__main__":
    # Example usage
    logger_instance = TransactionLogger()
    
    # Log a sample transaction
    sample_transaction = {
        'text_id': 'text_12345',
        'payment_id': 'PAY_67890',
        'amount': 10.0,
        'customer_email': 'customer@example.com',
        'charity_amount': 4.0,
        'operations_amount': 3.0,
        'upgrades_amount': 3.0,
        'status': 'completed'
    }
    
    tx_id = logger_instance.log_transaction(sample_transaction)
    print(f"✅ Transaction logged: {tx_id}")
    
    # Get monthly report
    report = logger_instance.get_monthly_report(12, 2025)
    print(f"\n📊 Monthly Report:")
    print(f"Total Revenue: ${report['total_revenue']:.2f}")
    print(f"Charity: ${report['total_charity']:.2f}")
    print(f"Operations: ${report['total_operations']:.2f}")
    print(f"Transactions: {report['transaction_count']}")
