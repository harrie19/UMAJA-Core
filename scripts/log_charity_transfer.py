#!/usr/bin/env python3
"""
Quick script to log when you transfer charity money
Usage: python scripts/log_charity_transfer.py --amount 156.40 --charity "Red Cross" --date "2025-12-31" --proof "PayPal TX: 12345"
"""

import argparse
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.simple_transaction_logger import SimpleTransactionLogger


def main():
    parser = argparse.ArgumentParser(
        description='Log a charity transfer to update balance tracking',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Log a simple transfer
  python scripts/log_charity_transfer.py \\
    --amount 156.40 \\
    --charity "Red Cross" \\
    --date "2025-12-31" \\
    --proof "PayPal TX: 12AB34CD56EF78"
  
  # Split transfer (do this twice with different amounts)
  python scripts/log_charity_transfer.py \\
    --amount 93.84 \\
    --charity "Red Cross" \\
    --date "2025-12-31" \\
    --proof "PayPal TX: AAA111"
"""
    )
    
    parser.add_argument(
        '--amount',
        type=float,
        required=True,
        help='Amount transferred (e.g., 156.40)'
    )
    
    parser.add_argument(
        '--charity',
        type=str,
        required=True,
        help='Charity name or organization (e.g., "Red Cross")'
    )
    
    parser.add_argument(
        '--date',
        type=str,
        required=True,
        help='Transfer date in ISO format (e.g., "2025-12-31")'
    )
    
    parser.add_argument(
        '--proof',
        type=str,
        required=True,
        help='PayPal transaction ID or other proof of transfer'
    )
    
    args = parser.parse_args()
    
    # Validate amount
    if args.amount <= 0:
        print("❌ Error: Amount must be positive")
        sys.exit(1)
    
    # Validate date format (basic check)
    if len(args.date) != 10 or args.date.count('-') != 2:
        print("❌ Error: Date must be in YYYY-MM-DD format")
        sys.exit(1)
    
    # Initialize logger
    logger = SimpleTransactionLogger()
    
    # Get current balance
    balance_before = logger.get_charity_balance()
    
    print("="*60)
    print("💰 Logging Charity Transfer")
    print("="*60)
    print(f"Amount:      €{args.amount:.2f}")
    print(f"Charity:     {args.charity}")
    print(f"Date:        {args.date}")
    print(f"Proof:       {args.proof}")
    print()
    print(f"Balance Before: €{balance_before['current_balance']:.2f}")
    print()
    
    # Log the transfer
    try:
        logger.mark_charity_transferred(
            amount=args.amount,
            charity=args.charity,
            date=args.date,
            proof=args.proof
        )
        
        # Get new balance
        balance_after = logger.get_charity_balance()
        
        print("✅ Transfer logged successfully!")
        print()
        print(f"Balance After:  €{balance_after['current_balance']:.2f}")
        print(f"Total Transferred to Date: €{balance_after['total_transferred']:.2f}")
        
        if balance_after['current_balance'] > 0:
            print()
            print(f"⚠️  Remaining balance: €{balance_after['current_balance']:.2f}")
            print("   (You may want to transfer more)")
        else:
            print()
            print("🎉 All charity funds transferred!")
        
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error logging transfer: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
