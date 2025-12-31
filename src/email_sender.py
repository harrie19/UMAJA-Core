"""
Email Sender for UMAJA-Core
Sends generated texts and receipts to customers via SMTP
"""

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailSender:
    """
    Handles email delivery via SMTP.
    """
    
    def __init__(self):
        """
        Initialize email sender.
        
        Environment variables required:
        - SMTP_HOST: SMTP server hostname
        - SMTP_PORT: SMTP server port
        - SMTP_USER: SMTP username
        - SMTP_PASSWORD: SMTP password
        - FROM_EMAIL: Sender email address
        """
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', self.smtp_user)
        
        # Check configuration
        self.configured = self._check_configuration()
    
    def _check_configuration(self) -> bool:
        """Check if SMTP is configured."""
        if not self.smtp_user or not self.smtp_password:
            logger.warning("SMTP not configured. Set SMTP_USER and SMTP_PASSWORD in .env")
            return False
        
        logger.info("Email sender configured successfully")
        return True
    
    def _send_email(self, to_email: str, subject: str, 
                   html_content: str, text_content: str = None) -> bool:
        """
        Send an email via SMTP.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email content
            text_content: Plain text fallback content
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.configured:
            logger.error("Cannot send email - SMTP not configured")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add plain text version if provided
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            # Add HTML version
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Connect to SMTP server and send
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                # Use starttls with certificate verification
                context = __import__('ssl').create_default_context()
                server.starttls(context=context)
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def send_text_delivery(self, recipient_email: str, text_data: Dict, 
                          transaction_id: str) -> bool:
        """
        Send generated text to customer.
        
        Args:
            recipient_email: Customer email address
            text_data: Generated text data containing:
                - text: Generated text content
                - word_count: Word count
                - metadata: Additional metadata
            transaction_id: Transaction identifier
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            text_content = text_data.get('text', '')
            word_count = text_data.get('word_count', 0)
            metadata = text_data.get('metadata', {})
            
            # Create HTML email
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 30px;
                        border-radius: 10px;
                        text-align: center;
                        margin-bottom: 30px;
                    }}
                    .content {{
                        background: #f9f9f9;
                        padding: 30px;
                        border-radius: 10px;
                        border: 1px solid #e0e0e0;
                        margin-bottom: 30px;
                    }}
                    .text-content {{
                        background: white;
                        padding: 20px;
                        border-left: 4px solid #667eea;
                        margin: 20px 0;
                        line-height: 1.8;
                    }}
                    .metadata {{
                        background: #f0f0f0;
                        padding: 15px;
                        border-radius: 5px;
                        margin-top: 20px;
                    }}
                    .footer {{
                        text-align: center;
                        color: #666;
                        font-size: 0.9em;
                        padding-top: 20px;
                        border-top: 1px solid #e0e0e0;
                    }}
                    .distribution {{
                        background: #e8f5e9;
                        padding: 20px;
                        border-radius: 5px;
                        margin: 20px 0;
                    }}
                    .distribution-item {{
                        display: flex;
                        justify-content: space-between;
                        padding: 5px 0;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🎨 Your UMAJA Generated Text</h1>
                    <p>Thank you for your purchase!</p>
                </div>
                
                <div class="content">
                    <h2>Your Generated Text</h2>
                    <div class="text-content">
                        {text_content}
                    </div>
                    
                    <div class="metadata">
                        <h3>📊 Text Details</h3>
                        <p><strong>Word Count:</strong> {word_count}</p>
                        <p><strong>Topic:</strong> {metadata.get('topic', 'N/A')}</p>
                        <p><strong>Quality Score:</strong> {metadata.get('coherence_score', 'N/A')}</p>
                        <p><strong>Transaction ID:</strong> {transaction_id}</p>
                    </div>
                    
                    <div class="distribution">
                        <h3>💚 Transparent Revenue Distribution</h3>
                        <p>Your payment is distributed as follows:</p>
                        <div class="distribution-item">
                            <span>🎗️ Charity Support</span>
                            <span><strong>40%</strong></span>
                        </div>
                        <div class="distribution-item">
                            <span>⚙️ Operations & Maintenance</span>
                            <span><strong>30%</strong></span>
                        </div>
                        <div class="distribution-item">
                            <span>🚀 Platform Upgrades</span>
                            <span><strong>30%</strong></span>
                        </div>
                        <p style="margin-top: 15px; font-size: 0.9em;">
                            Thank you for supporting both innovation and charity!
                        </p>
                    </div>
                </div>
                
                <div class="footer">
                    <p>UMAJA - Where AI Meets Social Good</p>
                    <p>Transaction ID: {transaction_id}</p>
                    <p>Generated on {datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')}</p>
                </div>
            </body>
            </html>
            """
            
            # Plain text version
            plain_text = f"""
UMAJA Generated Text
====================

{text_content}

---

Text Details:
- Word Count: {word_count}
- Topic: {metadata.get('topic', 'N/A')}
- Quality Score: {metadata.get('coherence_score', 'N/A')}
- Transaction ID: {transaction_id}

Revenue Distribution:
- Charity Support: 40%
- Operations & Maintenance: 30%
- Platform Upgrades: 30%

Thank you for supporting UMAJA!
            """
            
            subject = f"Your UMAJA Generated Text - {transaction_id}"
            
            return self._send_email(recipient_email, subject, html_content, plain_text)
            
        except Exception as e:
            logger.error(f"Error sending text delivery email: {e}")
            return False
    
    def send_receipt(self, recipient_email: str, payment_details: Dict) -> bool:
        """
        Send payment receipt to customer.
        
        Args:
            recipient_email: Customer email address
            payment_details: Payment details containing:
                - amount: Payment amount
                - transaction_id: Transaction ID
                - timestamp: Payment timestamp
                
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            amount = payment_details.get('amount', 0.0)
            transaction_id = payment_details.get('transaction_id', 'N/A')
            timestamp = payment_details.get('timestamp', datetime.utcnow().isoformat())
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    .header {{
                        background: #4CAF50;
                        color: white;
                        padding: 20px;
                        text-align: center;
                        border-radius: 5px;
                    }}
                    .content {{
                        padding: 20px;
                        border: 1px solid #e0e0e0;
                        margin-top: 20px;
                    }}
                    .amount {{
                        font-size: 2em;
                        color: #4CAF50;
                        text-align: center;
                        margin: 20px 0;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>✅ Payment Receipt</h1>
                </div>
                <div class="content">
                    <p>Thank you for your payment!</p>
                    <div class="amount">${amount:.2f} USD</div>
                    <p><strong>Transaction ID:</strong> {transaction_id}</p>
                    <p><strong>Date:</strong> {timestamp}</p>
                    <p>Your text will be delivered shortly.</p>
                </div>
            </body>
            </html>
            """
            
            plain_text = f"""
Payment Receipt
===============

Thank you for your payment!

Amount: ${amount:.2f} USD
Transaction ID: {transaction_id}
Date: {timestamp}

Your text will be delivered shortly.
            """
            
            subject = f"Payment Receipt - {transaction_id}"
            
            return self._send_email(recipient_email, subject, html_content, plain_text)
            
        except Exception as e:
            logger.error(f"Error sending receipt: {e}")
            return False


if __name__ == "__main__":
    # Example usage
    sender = EmailSender()
    
    if sender.configured:
        print("✅ Email sender configured")
        print(f"SMTP Host: {sender.smtp_host}:{sender.smtp_port}")
        print(f"From: {sender.from_email}")
    else:
        print("⚠️  Email sender not configured")
        print("Set SMTP_USER and SMTP_PASSWORD in .env")
