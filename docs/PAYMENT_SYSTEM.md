# UMAJA Payment System - Implementation Summary

## 🎉 What's New

A **simplified single-PayPal-account revenue system** has been added to UMAJA-Core! This system allows you to accept payments for generated texts with automatic internal tracking of charity allocations.

---

## ✨ Key Features

### Simple & Straightforward
- ✅ **ONE PayPal account** - All money goes to YOUR account
- ✅ **No complex payouts** - You control when to transfer charity funds
- ✅ **Internal tracking** - System calculates 40% charity, 30% operations, 30% upgrades
- ✅ **Beautiful dashboard** - See revenue, income, and charity balance at a glance

### Complete Payment Flow
1. **Generate payment link** → Customer receives PayPal URL
2. **Customer pays** → Money goes to your PayPal account
3. **Text delivered** → Automatic delivery on payment completion
4. **Transaction logged** → Full tracking with allocation breakdown

### Reporting & Transparency
- 📊 Monthly revenue reports
- 💰 Charity balance tracking
- 📄 Tax-ready exports
- 🎁 Transfer history for transparency

---

## 🚀 Quick Start

### 1. Get PayPal API Credentials
```bash
# Visit https://developer.paypal.com/dashboard
# Create an app and copy your Client ID and Secret
```

### 2. Configure
```bash
cp .env.example .env
# Edit .env and add your PayPal credentials
```

### 3. Install & Run
```bash
pip install -r requirements.txt
python api/simple_server.py
```

### 4. Open Dashboard
```
http://localhost:5000
```

**Full guide**: See [docs/QUICK_START.md](docs/QUICK_START.md)

---

## 📁 New Files Added

### Core Payment Components
```
src/
├── simple_payment_processor.py    # PayPal integration
├── simple_transaction_logger.py   # Transaction tracking & allocation
└── simple_text_seller.py          # Complete purchase flow
```

### API & UI
```
api/
└── simple_server.py               # Flask server with REST API

templates/
└── dashboard.html                 # Seller dashboard UI
```

### Documentation
```
docs/
├── QUICK_START.md                 # 5-minute setup guide
└── CHARITY_TRANSFERS.md           # How to handle charity transfers
```

### Helper Scripts
```
scripts/
└── log_charity_transfer.py        # CLI tool for logging transfers
```

---

## 🎯 How It Works

### Payment Creation
```python
from src.simple_text_seller import SimpleTextSeller

seller = SimpleTextSeller()

# Create a sale
result = seller.create_purchase_link(
    customer_email="customer@example.com",
    topic="AI ethics",
    length="short",
    noise_level=0.4
)

# Share payment URL with customer
print(f"Payment URL: {result['payment_url']}")
```

### API Endpoints

**Create Sale**:
```bash
curl -X POST http://localhost:5000/api/create-sale \
  -H "Content-Type: application/json" \
  -d '{"email":"customer@example.com","topic":"AI ethics","length":"short"}'
```

**Check Payment**:
```bash
curl http://localhost:5000/api/check-payment/<payment_id>
```

**Get Charity Balance**:
```bash
curl http://localhost:5000/api/reports/charity
```

**Monthly Report**:
```bash
curl http://localhost:5000/api/reports/monthly/2025/12
```

---

## 💰 Fund Allocation

Every sale is automatically split:
- **40% → Charity** (you transfer manually)
- **30% → Operations** (your income)
- **30% → Upgrades** (reinvestment fund)

Example: €10.00 sale
- €4.00 reserved for charity
- €3.00 your income
- €3.00 for upgrades

---

## 🎁 Charity Transfers

### Check Balance
```bash
curl http://localhost:5000/api/reports/charity
```

### Transfer & Log
```bash
# 1. Use PayPal to send money to charity
# 2. Log the transfer:
python scripts/log_charity_transfer.py \
  --amount 156.40 \
  --charity "Red Cross" \
  --date "2025-12-31" \
  --proof "PayPal TX: 12345"
```

**Full guide**: See [docs/CHARITY_TRANSFERS.md](docs/CHARITY_TRANSFERS.md)

---

## 📊 Dashboard Features

Access at `http://localhost:5000`

### Stats Cards
- **Total Sales** - All revenue received
- **Your Income (30%)** - Operations earnings
- **Charity Reserve (40%)** - Amount to transfer
- **Upgrades Fund (30%)** - Reinvestment amount

### Recent Transactions
View last 10 sales with:
- Date and payment ID
- Amount and charity allocation
- Customer email

### Create New Sale
Built-in form to generate payment links:
- Enter customer email
- Specify topic
- Choose length (short/long)
- Set noise level
- Get instant payment URL

---

## 🔒 Security

### Built-in Protection
✅ PayPal API authentication
✅ Environment variable configuration
✅ Input validation on all endpoints
✅ No SQL injection risks (using JSON storage)

### Passed Security Checks
- ✅ CodeQL analysis: 0 vulnerabilities
- ✅ No exposed credentials
- ✅ Secure payment processing

---

## 🧪 Testing

All payment components tested:
```bash
# Transaction logging
✅ Allocation calculation (40/30/30)
✅ Balance tracking
✅ Transfer recording

# Reporting
✅ Monthly reports
✅ Tax exports
✅ Recent transactions

# Integration
✅ Payment processor config
✅ Distribution engine compatibility
✅ Flask API routes
```

---

## 📝 Configuration

### Required `.env` Variables
```env
# PayPal (REQUIRED)
PAYPAL_EMAIL=your-paypal@example.com
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_SECRET=your_secret
PAYPAL_MODE=sandbox  # or 'live'

# Optional
CHARITY_NAME=Your Favorite Charity
CHARITY_WEBSITE=https://charity.org
SERVER_URL=http://localhost:5000
```

### Optional Email Notifications
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@umaja.dev
```

---

## 📖 API Documentation

### Create Sale
```
POST /api/create-sale
Content-Type: application/json

{
  "email": "customer@example.com",
  "topic": "AI ethics",
  "length": "short",        # or "long"
  "noise_level": 0.4        # 0.0 to 1.0
}

Response:
{
  "success": true,
  "payment_url": "https://paypal.com/...",
  "amount": 1.27,
  "text_preview": "Consider the deeper...",
  "payment_id": "PAYID-..."
}
```

### Check Payment
```
GET /api/check-payment/<payment_id>

Response:
{
  "success": true,
  "status": "delivered",
  "text": "Full generated text...",
  "message": "Text delivered successfully"
}
```

### Get Dashboard Data
```
GET /api/dashboard

Response:
{
  "total_revenue": 156.40,
  "your_income": 46.92,
  "charity_owed": 62.56,
  "recent_transactions": [...]
}
```

### Charity Report
```
GET /api/reports/charity

Response:
{
  "total_reserved": 156.40,
  "total_transferred": 0.00,
  "current_balance": 156.40,
  "last_transfer_date": null
}
```

### Monthly Report
```
GET /api/reports/monthly/<year>/<month>

Response:
{
  "month": 12,
  "year": 2025,
  "total_revenue": 156.40,
  "charity_reserved": 62.56,
  "your_income": 46.92,
  "transaction_count": 15
}
```

### Tax Export
```
GET /api/reports/tax/<year>

Response:
{
  "year": 2025,
  "transactions": [...],
  "total_income": 468.20,
  "total_charity": 624.27
}
```

---

## 🎓 Usage Examples

### Example 1: Command Line Sale
```bash
# Create sale
curl -X POST http://localhost:5000/api/create-sale \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "topic": "machine learning ethics",
    "length": "long",
    "noise_level": 0.5
  }'

# Response includes payment_url to share with customer
```

### Example 2: Python Integration
```python
from src.simple_text_seller import SimpleTextSeller

seller = SimpleTextSeller()

# Create payment link
result = seller.create_purchase_link(
    customer_email="jane@example.com",
    topic="quantum computing",
    length="short",
    noise_level=0.3
)

if result['success']:
    print(f"Amount: €{result['amount']}")
    print(f"Send this URL to customer: {result['payment_url']}")
```

### Example 3: Check Payment Status
```python
# After customer pays
delivery = seller.check_and_deliver(payment_id, payer_id)

if delivery['success']:
    print("Text delivered!")
    print(delivery['text'])
```

---

## 🆘 Troubleshooting

### Payment Creation Fails
- ✅ Check PayPal API credentials in `.env`
- ✅ Verify `PAYPAL_MODE` is correct (sandbox/live)
- ✅ Ensure PayPal developer account is active

### Dashboard Won't Load
- ✅ Run `pip install -r requirements.txt`
- ✅ Check port 5000 is available
- ✅ Verify Flask is installed: `pip show flask`

### Charity Balance Incorrect
- ✅ Check `data/transactions.json` for logged sales
- ✅ Verify transfers are recorded correctly
- ✅ Run: `python scripts/log_charity_transfer.py --help`

---

## 🔄 Migration from Old System

If you had a previous payment system, this is completely new and doesn't interfere. You can run both systems side-by-side.

---

## 🎯 What's Different from Complex Version

### ❌ What We DON'T Have
- No automatic multi-account payouts
- No PayPal Mass Payout API
- No real-time charity transfers

### ✅ What We DO Have
- Simple one-account setup
- Manual charity transfer control
- Full tracking and transparency
- Much easier to understand and maintain

---

## 📞 Support

Need help?
- 📖 Read [QUICK_START.md](docs/QUICK_START.md)
- 🎁 Read [CHARITY_TRANSFERS.md](docs/CHARITY_TRANSFERS.md)
- 🐛 Check logs in `data/transactions.json`
- 💬 File an issue on GitHub

---

## 🎉 Success Stories

This system is designed for:
- ✅ Solo creators selling text content
- ✅ Small businesses starting with payments
- ✅ Anyone wanting simple, transparent charity allocation
- ✅ Creators who want full control over their money

---

## 📜 License

Same as UMAJA-Core (MIT License)

---

**Ready to start?** → [Quick Start Guide](docs/QUICK_START.md)

**Questions about charity?** → [Charity Transfers Guide](docs/CHARITY_TRANSFERS.md)
