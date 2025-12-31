# How to Handle Charity Transfers

The UMAJA system automatically tracks how much money should go to charity (40% of all sales), but **you** decide when and how to actually transfer it. This guide explains the process.

---

## Understanding the System

### How It Works

1. **Customer pays**: Money goes to YOUR PayPal account
2. **System tracks**: Internally allocates 40% for charity
3. **You see balance**: Dashboard shows "Charity Reserve"
4. **You transfer**: Monthly (or whenever you want)
5. **You log it**: Record the transfer in the system

### Why This Approach?

- ✅ **Simple**: No complex multi-account setup
- ✅ **Flexible**: You choose which charity and when
- ✅ **Tax-friendly**: You can claim deductions
- ✅ **Transparent**: Full tracking and proof
- ✅ **Control**: All money in your account first

---

## Monthly Transfer Process

### Step 1: Check Your Dashboard

Open your dashboard at http://localhost:5000

Look at the **"Charity Reserve"** card:
```
Charity Reserve (40%)
€156.40
Recommended to transfer
```

Or via API:
```bash
curl http://localhost:5000/api/reports/charity
```

Response:
```json
{
  "total_reserved": 156.40,
  "total_transferred": 0.00,
  "current_balance": 156.40,
  "last_transfer_date": null
}
```

### Step 2: Choose Your Charity

You can:
- Transfer to **one charity** (e.g., Red Cross)
- **Split between multiple** charities
- Change charities each month

Popular options:
- Red Cross / Red Crescent
- UNICEF
- Doctors Without Borders
- Local food banks
- Educational charities
- Environmental organizations

### Step 3: Transfer the Money

Use PayPal's **"Send Money"** feature:

1. Log in to PayPal.com
2. Click **"Send & Request"**
3. Enter charity's email or search for their organization
4. Enter amount: €156.40
5. Add note: "UMAJA charity allocation for [Month Year]"
6. Send!

**Important**: Save the transaction details:
- PayPal Transaction ID
- Date of transfer
- Amount
- Charity name

### Step 4: Log the Transfer

Record it in the UMAJA system so tracking stays accurate:

```bash
python scripts/log_charity_transfer.py \
  --amount 156.40 \
  --charity "Red Cross" \
  --date "2025-12-31" \
  --proof "PayPal Transaction ID: 12AB34CD56EF78"
```

Or manually edit `data/transactions.json` (not recommended).

### Step 5: Verify

Check the dashboard again. The "Charity Reserve" should now show:
```
Charity Reserve (40%)
€0.00
```

And your transfer history will be recorded.

---

## Transfer Frequency

### Recommended: Monthly

Transfer at the end of each month:
- Easy to remember
- Manageable amounts
- Good for accounting

### Alternative: Quarterly

If you have lower volume:
- Transfer every 3 months
- Larger but less frequent
- Still maintains transparency

### Minimum: Annually

At minimum, transfer once per year:
- Before tax filing deadline
- Good for year-end giving
- Get full tax deduction

---

## Tax Benefits

### Deductions

- Charity transfers are **tax-deductible**
- Save PayPal transaction confirmations
- Get receipts from charities
- Include in your tax filing

### Documentation

The system generates:

1. **Annual Tax Report**:
   ```bash
   curl http://localhost:5000/api/reports/tax/2025
   ```

2. **Monthly Reports**:
   ```bash
   curl http://localhost:5000/api/reports/monthly/2025/12
   ```

3. **Transaction Log**:
   Located at `data/transactions.json`

Keep these for your records!

---

## Transparency & Trust

### Show Your Customers

On your website, you can show:
- "40% of every purchase supports [Charity Name]"
- Link to quarterly transparency reports
- Total amount donated to date

### Publish Reports

Consider publishing:
- Quarterly donation summaries
- Charity receipts (redact personal info)
- Impact statements from charities

Example transparency page:
```markdown
# Our Charitable Giving

## 2025 Donations
- Q1: €458.30 to Red Cross
- Q2: €612.50 to UNICEF
- Q3: €534.20 to Doctors Without Borders
- Q4: €[pending]

Total: €1,605.00

All donations verified via PayPal transaction records.
```

---

## Script Reference

### Log Charity Transfer

```bash
python scripts/log_charity_transfer.py \
  --amount <amount> \
  --charity "<charity_name>" \
  --date "<YYYY-MM-DD>" \
  --proof "<transaction_id>"
```

**Parameters:**
- `--amount`: Amount transferred (e.g., 156.40)
- `--charity`: Charity name (e.g., "Red Cross")
- `--date`: Transfer date in ISO format (e.g., "2025-12-31")
- `--proof`: PayPal transaction ID or other proof

**Example:**
```bash
python scripts/log_charity_transfer.py \
  --amount 156.40 \
  --charity "Red Cross" \
  --date "2025-12-31" \
  --proof "PayPal TX: 12AB34CD56EF78"
```

**Output:**
```
✅ Logged €156.40 transfer to Red Cross
📊 New charity balance: €0.00
```

---

## Multiple Charity Example

Want to split your donation?

**Transfer 1: 60% to Charity A**
```bash
# €156.40 × 0.6 = €93.84
python scripts/log_charity_transfer.py \
  --amount 93.84 \
  --charity "Red Cross" \
  --date "2025-12-31" \
  --proof "PayPal TX: AAA111"
```

**Transfer 2: 40% to Charity B**
```bash
# €156.40 × 0.4 = €62.56
python scripts/log_charity_transfer.py \
  --amount 62.56 \
  --charity "UNICEF" \
  --date "2025-12-31" \
  --proof "PayPal TX: BBB222"
```

---

## Best Practices

### ✅ Do This

- Transfer regularly (monthly is best)
- Keep all PayPal confirmations
- Get receipts from charities
- Log transfers immediately
- Use clear, descriptive notes in PayPal

### ❌ Avoid This

- Don't let balance accumulate too long
- Don't forget to log transfers
- Don't lose transaction proofs
- Don't skip months without reason

---

## FAQ

### Q: What if I forget to transfer one month?

**A:** No problem! The balance accumulates. Transfer double next month, or catch up when you remember.

### Q: Can I transfer less than the recommended amount?

**A:** Yes, but you should eventually transfer the full amount. The system tracks the cumulative balance.

### Q: What if I want to change charities?

**A:** Completely fine! You can pick different charities each month. Just log each transfer correctly.

### Q: Do I have to use the exact amount shown?

**A:** Close enough is fine. PayPal fees might create small differences. Log the actual amount you transferred.

### Q: Can I transfer more than the recommended amount?

**A:** Absolutely! If you want to donate extra from your personal funds, that's great. Just log the actual amount.

---

## Support

Need help with charity transfers?
- Check transaction logs: `data/transactions.json`
- Review API documentation
- Contact charity directly for receipts
- Keep good records for taxes

---

**Remember**: The charity transfer system is designed to be simple and flexible. You're in control, but the system helps you stay organized and accountable.

Happy giving! 🎁
