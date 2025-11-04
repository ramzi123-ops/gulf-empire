# 🚀 START HERE - Phase 1 Implementation

## You're Ready to Setup Stripe Payments!

I've created everything you need. Follow these exact steps:

---

## ⚡ Quick Start (10 Minutes)

### Step 1: Install Dependencies (1 min)

```bash
pip install python-dotenv stripe
```

---

### Step 2: Create .env File (30 sec)

```bash
copy .env.example .env
```

---

### Step 3: Get Stripe Keys (2 min)

1. Go to: https://dashboard.stripe.com/test/apikeys
2. Copy both keys:
   - `pk_test_...` (Publishable)
   - `sk_test_...` (Secret)

---

### Step 4: Update .env (1 min)

Open `.env` and paste your keys:

```env
STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY_HERE
STRIPE_SECRET_KEY=sk_test_YOUR_KEY_HERE
```

---

### Step 5: Install Stripe CLI (3 min)

**Windows:**
```powershell
scoop bucket add stripe https://github.com/stripe/scoop-stripe-cli.git
scoop install stripe
```

**Or download:** https://github.com/stripe/stripe-cli/releases/latest

---

### Step 6: Login to Stripe CLI (30 sec)

```bash
stripe login
```

Click "Allow access" in the browser that opens.

---

### Step 7: Start Webhook Forwarding (1 min)

**Terminal 1:**
```bash
python manage.py runserver
```

**Terminal 2 (NEW window):**
```bash
stripe listen --forward-to localhost:8000/payments/webhook/stripe/
```

**Copy the `whsec_...` secret** and add to `.env`:
```env
STRIPE_WEBHOOK_SECRET=whsec_YOUR_SECRET_HERE
```

---

### Step 8: Verify Setup (30 sec)

```bash
python verify_stripe_setup.py
```

Should show all ✅ checks passed!

---

## 🧪 Test Your First Payment (2 min)

1. Visit: http://localhost:8000
2. Add a product to cart
3. Go to checkout
4. Use test card:
   - **Card:** `4242 4242 4242 4242`
   - **Date:** `12/25`
   - **CVC:** `123`
5. Submit payment
6. Watch Terminal 2 for webhook events! 🎉

---

## 📚 Helpful Guides

| File | Purpose |
|------|---------|
| `PHASE1_CHECKLIST.md` | Step-by-step checklist |
| `STRIPE_SETUP_GUIDE.md` | Detailed Stripe setup guide |
| `INSTALL.md` | Installation instructions |
| `verify_stripe_setup.py` | Test your configuration |
| `PAYMENT_COMPLETION_PLAN.md` | Full 8-phase implementation plan |

---

## ✅ Phase 1 Complete When:

- [x] Python-dotenv installed
- [ ] `.env` file created
- [ ] Stripe keys added to `.env`
- [ ] Stripe CLI installed
- [ ] Logged into Stripe CLI
- [ ] Webhook forwarding running
- [ ] Webhook secret in `.env`
- [ ] Verification script passes
- [ ] Test payment successful

---

## 🆘 Need Help?

### Common Issues:

**Error: "No module named 'dotenv'"**
```bash
pip install python-dotenv
```

**Error: "Invalid API Key"**
- Check keys in `.env` start with `pk_test_` and `sk_test_`
- Restart Django server after updating `.env`

**Webhooks not working:**
- Make sure `stripe listen` is running
- Check Django on localhost:8000
- Verify webhook secret in `.env`

---

## 🎯 What Happens Next?

After Phase 1, you can:
- ✅ Process real test payments
- ✅ See order status updates automatically
- ✅ Test different card scenarios

**Then move to:**
- Phase 2: Advanced testing
- Phase 3: Email notifications
- Phase 7: Production deployment

---

## 🎉 You're Almost There!

Phase 1 is the foundation. Once complete, your payment system is functional!

**Let's go! Start with Step 1 above!** 🚀
