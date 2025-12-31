# UMAJA Payment System Setup Guide

Complete guide to setting up and running the UMAJA payment and revenue system.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [PayPal Configuration](#paypal-configuration)
3. [Environment Setup](#environment-setup)
4. [Email Configuration](#email-configuration)
5. [Testing in Sandbox Mode](#testing-in-sandbox-mode)
6. [Going Live](#going-live)
7. [Troubleshooting](#troubleshooting)
8. [API Usage](#api-usage)

---

## Prerequisites

### Required

- Python 3.11+
- PayPal Business Account
- Email account with SMTP access (Gmail recommended)
- Public server URL (for webhooks in production)

### Optional

- Gumroad account (alternative to PayPal direct integration)

---

## PayPal Configuration

### Step 1: Create PayPal Developer Account

1. Go to [PayPal Developer](https://developer.paypal.com/)
2. Sign in with your PayPal account
3. Navigate to **Dashboard**

### Step 2: Create Sandbox App

1. Click **Apps & Credentials**
2. Select **Sandbox** tab
3. Click **Create App**
4. Enter app name (e.g., "UMAJA-Core")
5. Select app type: **Merchant**
6. Click **Create App**

### Step 3: Get API Credentials

1. In your app dashboard, find:
   - **Client ID** (copy this)
   - **Secret** (click "Show" and copy)
2. Save these credentials securely

### Step 4: Create Sandbox Accounts

1. Go to **Sandbox → Accounts**
2. Create 3 **Business** accounts:
   - Charity account
   - Operations account
   - Upgrades account
3. Note the email addresses for each account

### Step 5: Enable Payouts

1. In your app settings, scroll to **Features**
2. Enable **Payouts** feature
3. Save changes

---

## Environment Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/harrie19/UMAJA-Core.git
cd UMAJA-Core
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

1. Copy the example file:

```bash
cp .env.example .env
```

2. Edit `.env` with your credentials:

```env
# ===== PAYMENT PROCESSING =====
PAYPAL_MODE=sandbox
PAYPAL_CLIENT_ID=your_client_id_here
PAYPAL_SECRET=your_secret_here

# ===== REVENUE DISTRIBUTION ACCOUNTS =====
CHARITY_PAYPAL_EMAIL=charity-sandbox@business.example.com
OPERATIONS_PAYPAL_EMAIL=operations-sandbox@business.example.com
UPGRADES_PAYPAL_EMAIL=upgrades-sandbox@business.example.com

# ===== EMAIL DELIVERY =====
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=noreply@yourdomain.com

# ===== WEB SERVER =====
SERVER_URL=http://localhost:5000
WEBHOOK_SECRET=generate_random_secret_here

# ===== APPLICATION =====
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
```

### Step 4: Generate Webhook Secret

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output to `WEBHOOK_SECRET` in `.env`.

---

## Email Configuration

### Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication**
   - Go to Google Account settings
   - Security → 2-Step Verification
   - Enable it

2. **Generate App Password**
   - Go to Security → App passwords
   - Select "Mail" and your device
   - Copy the 16-character password
   - Use this as `SMTP_PASSWORD` in `.env`

3. **Configure .env**

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
FROM_EMAIL=your.email@gmail.com
```

### Alternative: Other Email Providers

**Outlook/Office 365:**
```env
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
```

**SendGrid:**
```env
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your_sendgrid_api_key
```

---

## Testing in Sandbox Mode

### Step 1: Verify Configuration

```bash
python src/auto_revenue_system.py
```

Expected output:
```
✅ System Status: Ready
Components:
  ✅ text_generator
  ✅ quality_analyzer
  ✅ payment_processor
  ✅ revenue_distributor
  ✅ email_sender
```

### Step 2: Start API Server

```bash
python api/server.py
```

Server will start on `http://localhost:5000`

### Step 3: Test Purchase Flow

**Create a purchase:**

```bash
curl -X POST http://localhost:5000/api/purchase \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "topic": "artificial intelligence",
    "length": "short",
    "noise_level": 0.3
  }'
```

**Response:**
```json
{
  "success": true,
  "text_id": "abc-123",
  "payment_id": "PAY-xyz789",
  "approval_url": "https://www.sandbox.paypal.com/...",
  "amount": 1.50,
  "preview": "Consider the deeper implications of artificial intelligence..."
}
```

### Step 4: Complete Payment

1. Open the `approval_url` in browser
2. Log in with a sandbox **personal** account
3. Approve the payment
4. You'll be redirected to success page
5. Check your email for the generated text

### Step 5: Verify Distribution

```bash
python -c "
from src.transaction_logger import TransactionLogger
logger = TransactionLogger()
transactions = logger.get_all_transactions()
for tx in transactions:
    print(f'Transaction: {tx[\"transaction_id\"]}')
    print(f'  Charity: \${tx.get(\"charity_amount\", 0):.2f}')
    print(f'  Operations: \${tx.get(\"operations_amount\", 0):.2f}')
    print(f'  Upgrades: \${tx.get(\"upgrades_amount\", 0):.2f}')
    print()
"
```

### Step 6: Check Sandbox Accounts

1. Log in to [PayPal Sandbox](https://www.sandbox.paypal.com/)
2. Check each business account
3. Verify funds were received according to distribution (40% / 30% / 30%)

---

## Going Live

### Step 1: Switch to Live Credentials

1. Go to [PayPal Developer](https://developer.paypal.com/)
2. Navigate to **Apps & Credentials**
3. Select **Live** tab
4. Create a new app or use existing
5. Copy **Live** Client ID and Secret

### Step 2: Update Environment

```env
PAYPAL_MODE=live
PAYPAL_CLIENT_ID=your_live_client_id
PAYPAL_SECRET=your_live_secret

CHARITY_PAYPAL_EMAIL=charity@real-charity.org
OPERATIONS_PAYPAL_EMAIL=operations@yourdomain.com
UPGRADES_PAYPAL_EMAIL=upgrades@yourdomain.com

SERVER_URL=https://yourdomain.com
ENVIRONMENT=production
DEBUG=False
```

### Step 3: Configure Webhooks (Production Only)

1. In PayPal Dashboard, go to your Live app
2. Scroll to **Webhooks**
3. Click **Add Webhook**
4. Enter webhook URL: `https://yourdomain.com/webhook/paypal`
5. Select events to subscribe to:
   - `PAYMENT.SALE.COMPLETED`
   - `PAYMENT.SALE.REFUNDED`
   - `PAYMENT.SALE.REVERSED`
6. Save webhook

### Step 4: Deploy to Production

**Using systemd (Linux):**

Create `/etc/systemd/system/umaja-api.service`:

```ini
[Unit]
Description=UMAJA Payment API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/UMAJA-Core
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python api/server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl enable umaja-api
sudo systemctl start umaja-api
```

**Using Docker:**

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "api/server.py"]
```

Build and run:
```bash
docker build -t umaja-api .
docker run -p 5000:5000 --env-file .env umaja-api
```

### Step 5: Set Up Reverse Proxy

**Nginx configuration:**

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Step 6: Enable SSL

```bash
sudo certbot --nginx -d yourdomain.com
```

---

## Troubleshooting

### Issue: "PayPal not configured"

**Solution:**
1. Check `.env` file exists
2. Verify `PAYPAL_CLIENT_ID` and `PAYPAL_SECRET` are set
3. Ensure no extra spaces in credentials
4. Restart server after changing `.env`

### Issue: "SMTP authentication failed"

**Solution:**
1. For Gmail, use App Password, not regular password
2. Enable "Less secure app access" or use OAuth2
3. Check SMTP host and port are correct
4. Verify username is full email address

### Issue: "Payment creation failed"

**Solution:**
1. Check PayPal credentials are correct
2. Verify PayPal mode matches credentials (sandbox vs live)
3. Check internet connectivity
4. Review PayPal developer logs

### Issue: "Distribution failed"

**Solution:**
1. Verify all three PayPal emails are set in `.env`
2. Ensure accounts are verified PayPal business accounts
3. Check payout feature is enabled in PayPal app
4. Review transaction logs: `cat data/transactions.json`

### Issue: "Email not delivered"

**Solution:**
1. Check spam folder
2. Verify SMTP credentials
3. Test SMTP connection:
   ```bash
   python -c "from src.email_sender import EmailSender; s = EmailSender(); print(s.configured)"
   ```
4. Check email server logs

---

## API Usage

### Create Purchase

**Endpoint:** `POST /api/purchase`

**Request:**
```json
{
  "email": "customer@example.com",
  "topic": "machine learning",
  "length": "short",
  "noise_level": 0.4
}
```

**Response:**
```json
{
  "success": true,
  "text_id": "550e8400-e29b-41d4-a716-446655440000",
  "payment_id": "PAY-1234567890",
  "approval_url": "https://www.paypal.com/checkoutnow?token=...",
  "amount": 1.85,
  "word_count": 127,
  "quality": "excellent",
  "preview": "Consider the deeper implications of machine learning...",
  "message": "Please complete payment via the approval URL"
}
```

### Check Transaction Status

**Endpoint:** `GET /api/status/<transaction_id>`

**Response:**
```json
{
  "success": true,
  "transaction": {
    "transaction_id": "TX_20251231120000",
    "status": "completed",
    "amount": 1.85,
    "charity_amount": 0.74,
    "operations_amount": 0.56,
    "upgrades_amount": 0.55,
    "timestamp": "2025-12-31T12:00:00Z"
  }
}
```

### Get System Status

**Endpoint:** `GET /api/system/status`

**Response:**
```json
{
  "ready": true,
  "components": {
    "text_generator": true,
    "quality_analyzer": true,
    "payment_processor": true,
    "revenue_distributor": true,
    "email_sender": true
  },
  "distribution_summary": {
    "total_transactions": 42,
    "total_distributed": 125.50,
    "total_charity": 50.20,
    "total_operations": 37.65,
    "total_upgrades": 37.65
  }
}
```

---

## Monthly Reporting

Generate tax and accounting reports:

```bash
python -c "
from src.transaction_logger import TransactionLogger
logger = TransactionLogger()

# Get December 2025 report
report = logger.get_monthly_report(12, 2025)

print(f'Month: {report[\"month\"]}/{report[\"year\"]}')
print(f'Total Revenue: \${report[\"total_revenue\"]:.2f}')
print(f'Total Charity: \${report[\"total_charity\"]:.2f}')
print(f'Transactions: {report[\"transaction_count\"]}')

# Export to CSV
csv_file = logger.export_csv('2025-01-01', '2025-12-31')
print(f'Exported to: {csv_file}')
"
```

---

## Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore`
2. **Rotate webhook secret** regularly
3. **Use HTTPS** in production
4. **Enable PayPal IPN verification** for webhooks
5. **Monitor transaction logs** for suspicious activity
6. **Backup `data/transactions.json`** regularly
7. **Use strong SMTP passwords**
8. **Limit API access** with rate limiting in production

---

## Support

- **Documentation:** [docs/](https://github.com/harrie19/UMAJA-Core/docs)
- **Issues:** [GitHub Issues](https://github.com/harrie19/UMAJA-Core/issues)
- **PayPal Support:** [developer.paypal.com/support](https://developer.paypal.com/support/)

---

**Last Updated:** December 31, 2025  
**Version:** 1.0.0
