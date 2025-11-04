# 🚀 Stripe Setup Guide - Quick Start

## Step 1: Create Your .env File

```bash
# Copy the example file
cp .env.example .env
```

**Or manually:** Copy `.env.example` to `.env` in the project root.

---

## Step 2: Get Your Stripe Test API Keys

### Option A: If You DON'T Have a Stripe Account Yet

1. **Sign Up:**
   - Go to: https://dashboard.stripe.com/register
   - Enter your email and create a password
   - You'll be in **TEST MODE** by default ✅

2. **Get Your Keys:**
   - After login, you'll see: "Get your test API keys"
   - Or go to: https://dashboard.stripe.com/test/apikeys
   
3. **Copy Your Keys:**
   - **Publishable key:** Starts with `pk_test_...`
   - **Secret key:** Click "Reveal test key", starts with `sk_test_...`

### Option B: If You Already Have a Stripe Account

1. **Login:** https://dashboard.stripe.com/login

2. **Switch to Test Mode:**
   - Look at top-left toggle
   - Make sure it says "Test mode" (not "Live mode")

3. **Get Keys:**
   - Go to: https://dashboard.stripe.com/test/apikeys
   - Copy both keys

---

## Step 3: Update Your .env File

Open your `.env` file and replace these lines:

```env
# Replace these with your actual Stripe test keys
STRIPE_PUBLISHABLE_KEY=pk_test_51abc123...  # Your actual publishable key
STRIPE_SECRET_KEY=sk_test_51xyz789...       # Your actual secret key

# Keep this for now - we'll set it up in Step 4
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

**Example of what it should look like:**
```env
STRIPE_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
```

---

## Step 4: Set Up Webhook for Local Development

Webhooks tell your app when payments succeed/fail. For local development, we use **Stripe CLI**.

### 4.1 Install Stripe CLI

**Windows:**
```powershell
# Using Scoop package manager
scoop bucket add stripe https://github.com/stripe/scoop-stripe-cli.git
scoop install stripe
```

**Or download directly:**
- https://github.com/stripe/stripe-cli/releases/latest
- Download `stripe_X.X.X_windows_x86_64.zip`
- Extract and add to PATH

**Mac:**
```bash
brew install stripe/stripe-cli/stripe
```

**Linux:**
```bash
# Download the latest release
wget https://github.com/stripe/stripe-cli/releases/latest/download/stripe_linux_x86_64.tar.gz
tar -xvf stripe_linux_x86_64.tar.gz
sudo mv stripe /usr/local/bin/
```

### 4.2 Login to Stripe CLI

```bash
stripe login
```

This will:
1. Open your browser
2. Ask you to authorize Stripe CLI
3. Connect CLI to your account

### 4.3 Start Webhook Forwarding

```bash
# Start your Django development server first
python manage.py runserver

# In a NEW terminal, run:
stripe listen --forward-to localhost:8000/payments/webhook/stripe/
```

You'll see output like:
```
> Ready! Your webhook signing secret is whsec_abc123xyz789... (^C to quit)
```

**Copy that `whsec_...` secret** and add it to your `.env`:
```env
STRIPE_WEBHOOK_SECRET=whsec_abc123xyz789...  # The secret from Stripe CLI
```

---

## Step 5: Verify Setup

### 5.1 Check Django Settings

```bash
python manage.py shell
```

```python
from django.conf import settings

# Should show your test keys
print(settings.STRIPE_PUBLISHABLE_KEY)  # pk_test_...
print(settings.STRIPE_SECRET_KEY)        # sk_test_...
print(settings.STRIPE_WEBHOOK_SECRET)    # whsec_...

# All should start with the correct prefix
exit()
```

### 5.2 Test Stripe Connection

```python
# In Django shell
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

# Try to list payment intents (should work)
try:
    result = stripe.PaymentIntent.list(limit=1)
    print("✅ Stripe connection successful!")
    print(f"Account: {result}")
except Exception as e:
    print(f"❌ Error: {e}")
```

---

## ✅ Setup Complete Checklist

- [ ] Stripe account created (test mode)
- [ ] Test API keys copied
- [ ] `.env` file created and updated
- [ ] Stripe CLI installed
- [ ] Webhook forwarding running
- [ ] Webhook secret added to `.env`
- [ ] Django settings verified
- [ ] Stripe connection tested

---

## 🧪 Next Step: Test a Payment

Once setup is complete, you can test the payment flow:

1. **Start Django server:**
   ```bash
   python manage.py runserver
   ```

2. **Start Stripe webhook forwarding** (new terminal):
   ```bash
   stripe listen --forward-to localhost:8000/payments/webhook/stripe/
   ```

3. **Visit your site:** http://localhost:8000
4. **Add a product to cart**
5. **Go to checkout**
6. **Use test card:** `4242 4242 4242 4242`
   - Any future date
   - Any 3-digit CVC
   - Any ZIP code

---

## 🎯 Test Card Numbers

| Card Number | Scenario |
|-------------|----------|
| `4242 4242 4242 4242` | ✅ Success |
| `4000 0000 0000 9995` | ❌ Insufficient funds |
| `4000 0000 0000 0002` | ❌ Card declined |
| `4000 0025 0000 3155` | 🔐 Requires 3D Secure |

**All test cards:**
- Expiry: Any future date (e.g., 12/25)
- CVC: Any 3 digits (e.g., 123)
- ZIP: Any 5 digits (e.g., 12345)

---

## 🐛 Troubleshooting

### Error: "Invalid API Key"
- ✅ Check `.env` has correct keys
- ✅ Restart Django server after updating `.env`
- ✅ Make sure keys start with `pk_test_` and `sk_test_`

### Webhooks Not Working
- ✅ Make sure `stripe listen` is running
- ✅ Check Django server is on port 8000
- ✅ Verify webhook secret in `.env`

### Connection Refused
- ✅ Check Django server is running on localhost:8000
- ✅ Check no firewall blocking

---

## 📚 References

- **Stripe Dashboard:** https://dashboard.stripe.com
- **API Keys:** https://dashboard.stripe.com/test/apikeys
- **Webhooks:** https://dashboard.stripe.com/test/webhooks
- **Test Cards:** https://stripe.com/docs/testing
- **Stripe CLI:** https://stripe.com/docs/stripe-cli

---

## 🔒 Security Reminders

- ✅ Never commit `.env` to git
- ✅ Use test keys for development
- ✅ Use live keys only in production
- ✅ Keep secret keys secret!
- ✅ Rotate keys if exposed

---

**🎉 Once you complete this setup, you're ready to test payments!**
