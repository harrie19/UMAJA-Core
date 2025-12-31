# UMAJA-Core

[![Build Status](https://github.com/harrie19/UMAJA-Core/workflows/CI/badge.svg)](https://github.com/harrie19/UMAJA-Core/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/harrie19/UMAJA-Core/releases)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**UMAJA-Core** is an AI-powered text generation platform with integrated payment processing and transparent revenue distribution. Generate high-quality reflective texts while automatically supporting charity.

---

## ✨ Features

- 🤖 **AI Text Generation** - Generate reflective texts using sentence transformers
- 📊 **Quality Analysis** - Semantic coherence checking and scoring
- 💳 **Payment Processing** - Integrated PayPal payment system
- 💰 **Revenue Distribution** - Transparent 40% charity / 30% operations / 30% upgrades split
- 📧 **Email Delivery** - Automatic text delivery to customers
- 📝 **Transaction Logging** - Complete audit trail and financial reporting
- 🔒 **Production Ready** - Battle-tested payment and distribution system

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PayPal Business Account
- Email account with SMTP access

### Installation

```bash
# Clone the repository
git clone https://github.com/harrie19/UMAJA-Core.git
cd UMAJA-Core

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials
```

### Configuration

See detailed setup guide: **[docs/PAYMENT_SETUP.md](docs/PAYMENT_SETUP.md)**

Quick configuration:
1. Get PayPal API credentials (Client ID and Secret)
2. Set up three PayPal business accounts for distribution
3. Configure SMTP for email delivery
4. Update `.env` with all credentials

### Run the Server

```bash
python api/server.py
```

Server starts on `http://localhost:5000`

### Create a Purchase

```bash
curl -X POST http://localhost:5000/api/purchase \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "topic": "artificial intelligence",
    "length": "short"
  }'
```

---

## 💰 Revenue Distribution

Every payment is automatically split:
- **40%** → Charity (configurable charity organization)
- **30%** → Operations (platform maintenance)
- **30%** → Upgrades (feature development)

All transactions are logged in `data/transactions.json` for complete transparency.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              API Layer (Flask REST API)             │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│        AutoRevenueSystem (Main Orchestrator)        │
└─┬────────┬────────┬────────┬────────┬────────┬─────┘
  │        │        │        │        │        │
┌─▼──┐  ┌─▼──┐  ┌──▼──┐  ┌──▼──┐  ┌──▼──┐  ┌─▼──┐
│Text│  │Anal│  │Pay- │  │Rev- │  │Log- │  │Email│
│Gen │  │yzer│  │ment │  │enue │  │ger  │  │Send│
└────┘  └────┘  └─────┘  └─────┘  └─────┘  └────┘
```

---

## 📦 Components

### Core Modules

- **RauschenGenerator** - AI text generation with noise variation
- **VektorAnalyzer** - Semantic quality analysis
- **PaymentProcessor** - PayPal SDK integration
- **RevenueDistributor** - Automated fund distribution
- **TransactionLogger** - Transaction logging and reporting
- **EmailSender** - SMTP email delivery
- **AutoRevenueSystem** - Main orchestration class
- **Flask API** - REST API server

### Usage Example

```python
from src.auto_revenue_system import AutoRevenueSystem

# Initialize system
system = AutoRevenueSystem()

# Create a purchase
result = system.process_text_purchase(
    customer_email='customer@example.com',
    topic='quantum computing',
    length='short',
    noise_level=0.3
)

# Returns payment URL for customer
print(result['approval_url'])

# After payment approval, system automatically:
# 1. Distributes funds (40% charity, 30% ops, 30% upgrades)
# 2. Logs transaction
# 3. Emails text to customer
```

---

## 📖 API Endpoints

### POST /api/purchase
Create a text purchase and payment request.

**Request:**
```json
{
  "email": "customer@example.com",
  "topic": "machine learning",
  "length": "short",
  "noise_level": 0.3
}
```

**Response:**
```json
{
  "success": true,
  "payment_id": "PAY-123",
  "approval_url": "https://paypal.com/...",
  "amount": 1.50,
  "preview": "Consider the deeper..."
}
```

### GET /api/status/<transaction_id>
Check transaction status.

### GET /api/system/status
Get system health and statistics.

### POST /webhook/paypal
PayPal webhook endpoint (for automated payment processing).

---

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Test individual components
python src/payment_processor.py
python src/transaction_logger.py
python src/auto_revenue_system.py

# Test API server
python api/server.py
```

---

## 📊 Financial Reporting

Generate monthly reports:

```python
from src.transaction_logger import TransactionLogger

logger = TransactionLogger()

# Monthly report
report = logger.get_monthly_report(month=12, year=2025)
print(f"Revenue: ${report['total_revenue']}")
print(f"Charity: ${report['total_charity']}")

# Export to CSV
logger.export_csv('2025-01-01', '2025-12-31', 'report.csv')
```

---

## 📝 Documentation

- **[Payment Setup Guide](docs/PAYMENT_SETUP.md)** - Complete setup instructions
- **[API Documentation](#-api-endpoints)** - REST API reference
- **[Architecture](#-architecture)** - System design overview

---

## 🛠️ Development

### Project Structure

```
UMAJA-Core/
├── src/
│   ├── rauschen_generator.py      # Text generation
│   ├── vektor_analyzer.py         # Quality analysis
│   ├── payment_processor.py       # PayPal integration
│   ├── revenue_distributor.py     # Fund distribution
│   ├── transaction_logger.py      # Transaction logging
│   ├── email_sender.py            # Email delivery
│   ├── webhook_handler.py         # Webhook processing
│   └── auto_revenue_system.py     # Main orchestrator
├── api/
│   └── server.py                  # Flask API server
├── data/
│   ├── transactions.json          # Transaction log
│   └── theme_database.json        # Theme data
├── docs/
│   └── PAYMENT_SETUP.md           # Setup guide
├── .env.example                   # Environment template
├── requirements.txt               # Dependencies
└── README.md                      # This file
```

### Environment Variables

```env
# PayPal
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_SECRET=your_secret

# Distribution Accounts
CHARITY_PAYPAL_EMAIL=charity@example.com
OPERATIONS_PAYPAL_EMAIL=ops@example.com
UPGRADES_PAYPAL_EMAIL=upgrades@example.com

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=noreply@yourdomain.com

# Server
SERVER_URL=https://yourdomain.com
WEBHOOK_SECRET=random_secret_here
```

---

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💬 Support

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/harrie19/UMAJA-Core/issues)
- **PayPal Help:** [developer.paypal.com](https://developer.paypal.com/support/)

---

## 🎯 Roadmap

- [x] AI text generation
- [x] Quality analysis
- [x] PayPal payment processing
- [x] Automated revenue distribution
- [x] Email delivery
- [x] Transaction logging
- [x] REST API
- [ ] Gumroad integration (alternative payment)
- [ ] Stripe payment support
- [ ] Multi-language support
- [ ] Admin dashboard
- [ ] Analytics and insights

---

Made with ❤️ by [harrie19](https://github.com/harrie19) and [contributors](https://github.com/harrie19/UMAJA-Core/graphs/contributors)
