# 📦 Installation Instructions

## Quick Setup (First Time)

### 1. Install Python Dependencies

```bash
# Install required packages
pip install python-dotenv stripe django
```

**Or if you have requirements.txt:**
```bash
pip install -r requirements.txt
```

---

### 2. Create .env File

```bash
# Copy the template
copy .env.example .env
```

Then edit `.env` with your actual Stripe keys (see PHASE1_CHECKLIST.md)

---

### 3. Run Database Migrations

```bash
python manage.py migrate
```

---

### 4. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

---

### 5. Verify Setup

```bash
python verify_stripe_setup.py
```

---

## 🚀 Running the Project

### Development Mode

**Terminal 1 - Django Server:**
```bash
python manage.py runserver
```

**Terminal 2 - Stripe Webhooks:**
```bash
stripe listen --forward-to localhost:8000/payments/webhook/stripe/
```

**Visit:** http://localhost:8000

---

## 📦 Required Packages

```txt
Django>=5.2
stripe>=5.0.0
python-dotenv>=1.0.0
```

---

## ✅ Verify Installation

Run the verification script:
```bash
python verify_stripe_setup.py
```

You should see all ✅ checks pass!

---

## 🐛 Troubleshooting

### ModuleNotFoundError: No module named 'dotenv'
```bash
pip install python-dotenv
```

### ModuleNotFoundError: No module named 'stripe'
```bash
pip install stripe
```

### Stripe CLI not found
Follow instructions in STRIPE_SETUP_GUIDE.md to install Stripe CLI

---

## 📚 Next Steps

1. ✅ Follow PHASE1_CHECKLIST.md to setup Stripe
2. 🧪 Test payment with test cards
3. 📧 Setup email notifications (Phase 3)
4. 🚀 Deploy to production (Phase 7)

See **PAYMENT_COMPLETION_PLAN.md** for full implementation guide.
