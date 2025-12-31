# 🚀 Quick Start - 5 Minutes to First Sale

Get your UMAJA payment system up and running in just 5 minutes!

## Step 1: Get PayPal API Keys (2 min)

1. Go to https://developer.paypal.com/dashboard
2. Log in with your normal PayPal account
3. Click "Apps & Credentials"
4. Click "Create App"
5. Give it a name (e.g., "UMAJA-Payment-System")
6. Copy the following credentials:
   - **Client ID** (visible immediately)
   - **Secret** (click "Show" to reveal)

### Important Notes:
- Start with **Sandbox** mode for testing
- Switch to **Live** mode when ready for real payments
- All payments go to YOUR PayPal account (no complex setup!)

---

## Step 2: Configure Environment (1 min)

```bash
# Copy the example environment file
cp .env.example .env

# Edit the file
nano .env
# or use your favorite editor
```

Paste your PayPal credentials:

```env
# Your PayPal Account (REQUIRED)
PAYPAL_EMAIL=your-real@paypal.com

# PayPal API Credentials
PAYPAL_CLIENT_ID=paste-your-client-id-here
PAYPAL_SECRET=paste-your-secret-here
PAYPAL_MODE=sandbox  # Use 'sandbox' for testing, 'live' for production

# Optional: Charity info for your records
CHARITY_NAME=Your Favorite Charity
CHARITY_WEBSITE=https://charity.org
```

**That's it!** The other settings have sensible defaults.

---

## Step 3: Install Dependencies & Start Server (1 min)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the server
python api/simple_server.py
```

You should see:
```
🚀 UMAJA Simple Payment Server Starting...
Server URL: http://localhost:5000
Dashboard: http://localhost:5000/
```

---

## Step 4: Create Your First Sale (1 min)

### Option A: Using the Web Dashboard

1. Open your browser to: http://localhost:5000
2. Fill in the "Create New Sale" form:
   - Customer Email: `customer@example.com`
   - Topic: `AI ethics`
   - Length: `Short`
3. Click "Create Payment Link"
4. Copy the payment URL and share it with your customer!

### Option B: Using cURL (for automation)

```bash
curl -X POST http://localhost:5000/api/create-sale \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "topic": "AI ethics",
    "length": "short"
  }'
```

**Response:**
```json
{
  "success": true,
  "payment_url": "https://www.sandbox.paypal.com/checkoutnow?token=...",
  "amount": 1.27,
  "text_preview": "Consider the deeper implications of AI ethics...",
  "payment_id": "PAYID-XXXXX"
}
```

---

## Step 5: Test the Payment Flow

1. **Share the payment URL** with your test customer (or open it yourself in a new browser tab)
2. **Log in to PayPal Sandbox** using test credentials:
   - Go to: https://developer.paypal.com/developer/accounts/
   - Use a test buyer account (or create one)
3. **Complete the payment**
4. **Customer gets redirected** to success page with their text!
5. **Check your dashboard**: http://localhost:5000

You'll see:
- Total sales updated
- Your income (30%) calculated
- Charity reserve (40%) tracked
- Transaction logged

---

## Step 6: Check Your Dashboard

Open http://localhost:5000 to see:

- **Total Sales**: All money received in YOUR PayPal
- **Your Income**: 30% operations earnings
- **Charity Reserve**: 40% to transfer (you decide when)
- **Upgrades Fund**: 30% for reinvestment
- **Recent Transactions**: List of all sales

---

## 🎉 Done!

You now have a working payment system where:
- ✅ ALL money goes to YOUR one PayPal account
- ✅ System tracks internal allocation (40% charity, 30% ops, 30% upgrades)
- ✅ You get monthly reports
- ✅ You manually transfer charity portion when ready

---

## Next Steps

### For Testing (Sandbox Mode)

1. Use PayPal's test accounts to simulate payments
2. Test the full flow: create sale → pay → deliver text
3. Check the dashboard and reports

### For Production (Live Mode)

1. Get your **Live** API credentials from PayPal
2. Update `.env`:
   ```env
   PAYPAL_MODE=live
   PAYPAL_CLIENT_ID=your-live-client-id
   PAYPAL_SECRET=your-live-secret
   ```
3. Restart the server
4. Start making real sales! 💰

---

## Common Commands

```bash
# Start server
python api/simple_server.py

# View dashboard
open http://localhost:5000

# Check charity balance
curl http://localhost:5000/api/reports/charity

# Get monthly report
curl http://localhost:5000/api/reports/monthly/2025/12

# Export tax report
curl http://localhost:5000/api/reports/tax/2025
```

---

## Troubleshooting

### "Payment creation failed"
- Check your PayPal API credentials in `.env`
- Make sure you're using the right mode (sandbox/live)
- Verify your PayPal developer account is set up

### "Module not found"
- Run: `pip install -r requirements.txt`

### "Port already in use"
- Change the port in `.env`: `SERVER_URL=http://localhost:8000`
- Or stop other services using port 5000

### "PayPal sandbox not working"
- Use test credentials from PayPal Developer Dashboard
- Make sure `PAYPAL_MODE=sandbox` in `.env`

---

## Need Help?

- Check the full documentation in `docs/`
- Review the code in `src/` and `api/`
- File an issue on GitHub

---

**Congratulations!** You're now running a simplified payment system that's:
- Easy to manage (one PayPal account)
- Transparent (full tracking and reporting)
- Charitable (40% automatically allocated)
- Professional (automated text delivery)

Time to make your first real sale! 🚀
