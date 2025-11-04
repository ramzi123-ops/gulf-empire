# ✅ Phase 1 Setup Checklist

## Quick Reference - Do This Now!

### 📝 Step-by-Step Instructions

#### 1️⃣ Create Your .env File (1 minute)

```bash
# Copy the template
copy .env.example .env
```

---

#### 2️⃣ Get Stripe Test Keys (3 minutes)

**Go to:** https://dashboard.stripe.com/test/apikeys

**You'll see two keys:**
- `pk_test_...` ← Publishable key (safe to use in frontend)
- `sk_test_...` ← Secret key (NEVER expose publicly)

**Copy them!**

---

#### 3️⃣ Update .env File (1 minute)

Open `.env` and paste your keys:

```env
STRIPE_PUBLISHABLE_KEY=pk_test_51QK...  # Paste your actual key
STRIPE_SECRET_KEY=sk_test_51QK...       # Paste your actual key
```

Save the file!

---

#### 4️⃣ Install Stripe CLI (5 minutes)

**Windows (using Scoop):**
```powershell
scoop bucket add stripe https://github.com/stripe/scoop-stripe-cli.git
scoop install stripe
```

**Or download:** https://github.com/stripe/stripe-cli/releases/latest

---

#### 5️⃣ Login to Stripe CLI (30 seconds)

```bash
stripe login
```

This will open your browser → Click "Allow access"

---

#### 6️⃣ Get Webhook Secret (1 minute)

```bash
# Start Django server first
python manage.py runserver

# In NEW terminal:
stripe listen --forward-to localhost:8000/payments/webhook/stripe/
```

**Copy the `whsec_...` secret** from the output!

Add it to `.env`:
```env
STRIPE_WEBHOOK_SECRET=whsec_abc123...  # Paste the secret
```

---

#### 7️⃣ Verify Setup (30 seconds)

```bash
python verify_stripe_setup.py
```

You should see all ✅ checks pass!

---

## 🎯 Final Checklist

- [ ] `.env` file created
- [ ] Stripe publishable key added
- [ ] Stripe secret key added
- [ ] Stripe CLI installed
- [ ] Logged into Stripe CLI
- [ ] Webhook forwarding running
- [ ] Webhook secret added to `.env`
- [ ] Verification script passed

---

## 🧪 Test It Works!

1. **Keep two terminals open:**
   - Terminal 1: `python manage.py runserver`
   - Terminal 2: `stripe listen --forward-to localhost:8000/payments/webhook/stripe/`

2. **Visit:** http://localhost:8000

3. **Add product → Checkout → Use test card:**
   - Card: `4242 4242 4242 4242`
   - Date: `12/25` (any future date)
   - CVC: `123` (any 3 digits)

4. **Watch Terminal 2** - You should see webhook events! 🎉

---

## ❓ Need Help?

- **Full Guide:** `STRIPE_SETUP_GUIDE.md`
- **Full Plan:** `PAYMENT_COMPLETION_PLAN.md`
- **Stripe Docs:** https://stripe.com/docs

---

## ⏱️ Total Time: ~10 minutes

You're doing great! Once this is done, your payment system is ready for testing! 🚀
