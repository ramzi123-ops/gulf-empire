# Payment System Completion Plan

## 📋 Project Overview
Complete the Stripe payment integration for Gulf Emperor e-commerce platform, including setup, testing, email notifications, and production deployment.

---

## 🎯 Current Status

### ✅ Completed
- [x] Payment model with Stripe integration
- [x] Order creation flow (cart → checkout → order)
- [x] Stripe PaymentIntent creation
- [x] Payment processing page with Stripe.js
- [x] Webhook endpoint for payment events
- [x] Payment status tracking (pending, succeeded, failed, refunded)
- [x] Order status updates based on payment
- [x] Success/cancelled pages
- [x] Security (signature verification, login required)

### ⏳ Pending
- [ ] Stripe account setup and API keys
- [ ] Webhook endpoint configuration
- [ ] Email notifications (confirmation, failure, refund)
- [ ] Testing with Stripe test cards
- [ ] Error handling improvements
- [ ] Admin panel for payment management
- [ ] Production deployment checklist
- [ ] Documentation for maintenance

---

## 📅 Implementation Phases

### **Phase 1: Stripe Setup & Configuration** (Est: 2 hours)

#### 1.1 Create Stripe Account
- [ ] Sign up at https://dashboard.stripe.com/register
- [ ] Complete business verification (if required)
- [ ] Enable SAR (Saudi Riyal) currency
- [ ] Configure business settings

#### 1.2 Get API Keys
- [ ] Navigate to Developers → API Keys
- [ ] Copy **Publishable key** (pk_test_...)
- [ ] Copy **Secret key** (sk_test_...)
- [ ] Store in `.env` file (never commit to git)

**`.env` file:**
```env
# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_51...
STRIPE_SECRET_KEY=sk_test_51...
STRIPE_WEBHOOK_SECRET=whsec_...  # Will get this in step 1.3
```

#### 1.3 Configure Webhook Endpoint
- [ ] Go to Developers → Webhooks
- [ ] Click "Add endpoint"
- [ ] Enter URL: `https://yourdomain.com/payments/webhook/stripe/`
- [ ] Select events to listen:
  - [x] `payment_intent.succeeded`
  - [x] `payment_intent.payment_failed`
  - [x] `charge.succeeded`
  - [x] `charge.refunded`
- [ ] Copy **Signing secret** (whsec_...)
- [ ] Add to `.env` file

#### 1.4 Update Settings
```python
# config/settings.py - Verify these are reading from environment
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
```

---

### **Phase 2: Local Testing** (Est: 3 hours)

#### 2.1 Install Stripe CLI
```bash
# Download from: https://stripe.com/docs/stripe-cli
# Or use package manager:
# Windows: scoop install stripe
# Mac: brew install stripe/stripe-cli/stripe
# Linux: https://github.com/stripe/stripe-cli/releases

# Login to Stripe
stripe login

# Forward webhooks to local server
stripe listen --forward-to localhost:8000/payments/webhook/stripe/
```

#### 2.2 Test Payment Flow
**Test Cards:** https://stripe.com/docs/testing

| Card Number | Scenario | CVV | Date |
|-------------|----------|-----|------|
| 4242 4242 4242 4242 | Success | Any 3 digits | Any future |
| 4000 0000 0000 9995 | Declined (insufficient funds) | Any 3 digits | Any future |
| 4000 0000 0000 0002 | Declined (card declined) | Any 3 digits | Any future |
| 4000 0025 0000 3155 | Requires authentication (3D Secure) | Any 3 digits | Any future |

**Test Checklist:**
- [ ] Add product to cart
- [ ] Proceed to checkout
- [ ] Select/create delivery address
- [ ] Submit order (creates PaymentIntent)
- [ ] Enter test card details
- [ ] Submit payment
- [ ] Verify webhook received in Stripe CLI
- [ ] Check order status updated to "confirmed"
- [ ] Check payment status updated to "succeeded"
- [ ] Verify cart is cleared
- [ ] Test success page displays correctly

**Error Scenarios:**
- [ ] Test declined card
- [ ] Test insufficient funds
- [ ] Test expired card
- [ ] Verify error messages display
- [ ] Check payment status = "failed"
- [ ] Order status remains "pending"

---

### **Phase 3: Email Notifications** (Est: 4 hours)

#### 3.1 Email Backend Setup

**Development (Console):**
```python
# config/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**Production (SMTP):**
```python
# config/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@gulfemperor.com')
```

**Add to `.env`:**
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Gulf Emperor <noreply@gulfemperor.com>
```

#### 3.2 Create Email Templates

**File: `apps/payments/emails.py`**
```python
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_order_confirmation_email(order):
    """Send order confirmation email to customer"""
    try:
        subject = f'تأكيد الطلب #{order.order_number} - إمبراطور الخليج'
        
        # Render email template
        html_message = render_to_string('payments/emails/order_confirmation.html', {
            'order': order,
            'user': order.user,
        })
        
        plain_message = f"""
        شكراً لطلبك من إمبراطور الخليج!
        
        رقم الطلب: {order.order_number}
        المبلغ الإجمالي: {order.total_price} ر.س
        حالة الدفع: مدفوع
        
        سيتم شحن طلبك قريباً.
        
        مع تحيات،
        فريق إمبراطور الخليج
        """
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f'Order confirmation email sent to {order.user.email}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send order confirmation email: {str(e)}')
        return False


def send_payment_failed_email(order):
    """Send payment failed notification"""
    try:
        subject = f'فشل الدفع للطلب #{order.order_number}'
        
        plain_message = f"""
        عذراً، فشلت عملية الدفع للطلب #{order.order_number}.
        
        يمكنك المحاولة مرة أخرى من خلال حسابك.
        
        إذا استمرت المشكلة، يرجى التواصل معنا.
        
        مع تحيات،
        فريق إمبراطور الخليج
        """
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            fail_silently=False,
        )
        
        logger.info(f'Payment failed email sent to {order.user.email}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send payment failed email: {str(e)}')
        return False


def send_refund_confirmation_email(order):
    """Send refund confirmation email"""
    try:
        subject = f'تأكيد استرداد المبلغ للطلب #{order.order_number}'
        
        plain_message = f"""
        تم استرداد مبلغ الطلب #{order.order_number} بنجاح.
        
        المبلغ: {order.total_price} ر.س
        
        سيظهر المبلغ في حسابك البنكي خلال 5-10 أيام عمل.
        
        مع تحيات،
        فريق إمبراطور الخليج
        """
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.user.email],
            fail_silently=False,
        )
        
        logger.info(f'Refund confirmation email sent to {order.user.email}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send refund email: {str(e)}')
        return False
```

#### 3.3 Create HTML Email Template

**File: `apps/payments/templates/payments/emails/order_confirmation.html`**
```html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تأكيد الطلب</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #1e40af; color: white; padding: 20px; text-align: center; }
        .content { background: #f9fafb; padding: 20px; }
        .order-summary { background: white; padding: 15px; margin: 20px 0; border-radius: 8px; }
        .total { font-size: 24px; font-weight: bold; color: #1e40af; }
        .footer { text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>شكراً لطلبك! 🎉</h1>
        </div>
        
        <div class="content">
            <p>مرحباً {{ user.get_full_name }},</p>
            
            <p>تم استلام طلبك بنجاح وجاري تجهيزه للشحن.</p>
            
            <div class="order-summary">
                <h2>تفاصيل الطلب</h2>
                <p><strong>رقم الطلب:</strong> {{ order.order_number }}</p>
                <p><strong>التاريخ:</strong> {{ order.created_at|date:"d/m/Y - h:i A" }}</p>
                <p><strong>عدد المنتجات:</strong> {{ order.get_total_items }}</p>
                <p><strong>المبلغ الفرعي:</strong> {{ order.get_subtotal }} ر.س</p>
                <p><strong>تكلفة الشحن:</strong> {{ order.shipping_cost }} ر.س</p>
                <p class="total">المجموع الكلي: {{ order.total_price }} ر.س</p>
            </div>
            
            <h3>عنوان التوصيل:</h3>
            <p>
                {{ order.address.full_name }}<br>
                {{ order.address.street_address }}<br>
                {{ order.address.city }}, {{ order.address.state }}<br>
                {{ order.address.phone_number }}
            </p>
            
            <p>يمكنك تتبع حالة طلبك من خلال <a href="#">حسابك</a>.</p>
        </div>
        
        <div class="footer">
            <p>مع تحيات فريق إمبراطور الخليج</p>
            <p>للاستفسارات: support@gulfemperor.com</p>
        </div>
    </div>
</body>
</html>
```

#### 3.4 Update Webhook Handlers

**File: `apps/payments/views/webhook_views.py`**

Update the TODO comments:
```python
# Line 118 - Import emails module at top
from apps.payments.emails import (
    send_order_confirmation_email,
    send_payment_failed_email,
    send_refund_confirmation_email
)

# Line 117-118 - Replace TODO
send_order_confirmation_email(order)

# Line 157-158 - Replace TODO
send_payment_failed_email(order)

# Line 220-221 - Replace TODO
send_refund_confirmation_email(order)
```

#### 3.5 Test Emails
- [ ] Trigger successful payment
- [ ] Check console/inbox for confirmation email
- [ ] Verify email contains correct order details
- [ ] Test failed payment email
- [ ] Test refund email (using Stripe dashboard to issue refund)

---

### **Phase 4: Admin Panel Enhancements** (Est: 2 hours)

#### 4.1 Payment Admin

**File: `apps/payments/admins/payment_admin.py`**

Enhance with:
- [ ] List display: order number, amount, status, created_at
- [ ] Filters: status, created_at, currency
- [ ] Search: order number, stripe_payment_intent_id
- [ ] Read-only fields: stripe IDs, timestamps
- [ ] Actions: Issue refund
- [ ] Inline view of related order

```python
from django.contrib import admin
from apps.payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_order_number', 'amount', 'currency', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['order__order_number', 'stripe_payment_intent_id', 'stripe_charge_id']
    readonly_fields = ['stripe_payment_intent_id', 'stripe_charge_id', 'created_at', 'updated_at', 'paid_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order',)
        }),
        ('Payment Details', {
            'fields': ('amount', 'currency', 'status', 'payment_method')
        }),
        ('Stripe Information', {
            'fields': ('stripe_payment_intent_id', 'stripe_charge_id')
        }),
        ('Additional Information', {
            'fields': ('error_message', 'metadata')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'paid_at')
        }),
    )
    
    def get_order_number(self, obj):
        return obj.order.order_number
    get_order_number.short_description = 'Order Number'
    get_order_number.admin_order_field = 'order__order_number'
```

#### 4.2 Order Admin Enhancement

**File: `apps/orders/admins/order_admin.py`**

Add payment status to list display:
```python
list_display = ['order_number', 'user', 'total_price', 'status', 'payment_status', 'created_at']
list_filter = ['status', 'payment_status', 'created_at']
```

---

### **Phase 5: Error Handling & UX Improvements** (Est: 3 hours)

#### 5.1 Enhanced Error Messages

**File: `apps/orders/views/checkout_views.py`**

```python
# Line 129-135 - Improve error handling
except stripe.error.CardError as e:
    # Card was declined
    messages.error(request, f'تم رفض البطاقة: {e.user_message}')
    logger.error(f'Card error: {str(e)}')
except stripe.error.InvalidRequestError as e:
    # Invalid parameters
    messages.error(request, 'خطأ في معالجة الدفع. يرجى المحاولة لاحقاً.')
    logger.error(f'Invalid request: {str(e)}')
except stripe.error.AuthenticationError as e:
    # Authentication with Stripe failed
    messages.error(request, 'خطأ في الاتصال بخدمة الدفع.')
    logger.error(f'Stripe authentication failed: {str(e)}')
except Exception as e:
    messages.error(request, 'حدث خطأ غير متوقع. يرجى المحاولة لاحقاً.')
    logger.error(f'Checkout error: {str(e)}')
```

#### 5.2 Payment Retry Mechanism

**File: `apps/users/templates/users/order_detail.html`**

Add retry button for failed payments:
```html
{% if order.payment_status == 'failed' %}
<div class="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
    <p class="text-red-700 mb-2">فشلت عملية الدفع</p>
    <a href="{% url 'payments:payment_process' order.id %}" 
       class="btn btn-primary">
        المحاولة مرة أخرى
    </a>
</div>
{% endif %}
```

#### 5.3 Loading States

**File: `apps/payments/templates/payments/payment.html`**

Already implemented:
- [x] Submit button disabled during processing
- [x] Loading spinner
- [x] Real-time card validation

#### 5.4 Session Expiry Handling

**File: `apps/payments/views/payment_views.py`**

```python
# Line 27-29 - Add better error handling
if not client_secret:
    messages.error(request, 'انتهت جلسة الدفع. يرجى إنشاء طلب جديد.')
    logger.warning(f'Payment session expired for order {order_id}')
    return redirect('orders:cart')
```

---

### **Phase 6: Security Audit** (Est: 2 hours)

#### 6.1 Security Checklist
- [x] **Webhook signature verification** - Implemented
- [x] **CSRF protection** - Exempt only webhook endpoint
- [x] **Login required** - All payment views protected
- [x] **Order ownership validation** - User can only access their orders
- [x] **No card data stored** - Only Stripe IDs
- [ ] **HTTPS enforcement** - Required for production
- [ ] **Environment variables** - Keys not in code
- [ ] **Rate limiting** - Consider for webhook endpoint
- [ ] **Logging** - Sensitive data not logged

#### 6.2 Production Settings

**File: `config/settings.py`**

```python
if not DEBUG:
    # Enforce HTTPS
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Security headers
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
```

---

### **Phase 7: Production Deployment** (Est: 4 hours)

#### 7.1 Pre-Deployment Checklist

**Environment:**
- [ ] All `.env` variables set on production server
- [ ] Database migrations run
- [ ] Static files collected
- [ ] HTTPS/SSL certificate installed
- [ ] Domain configured

**Stripe:**
- [ ] Switch to live API keys (pk_live_..., sk_live_...)
- [ ] Update webhook endpoint to production URL
- [ ] Verify webhook signing secret
- [ ] Enable live mode in Stripe dashboard

#### 7.2 Deployment Steps

```bash
# 1. Pull latest code
git pull origin main

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. Restart application server
# (depends on your hosting: gunicorn, uwsgi, etc.)
sudo systemctl restart gunicorn

# 6. Test deployment
python manage.py check --deploy
```

#### 7.3 Post-Deployment Verification

**Test in Production:**
- [ ] Test payment with real card (small amount)
- [ ] Verify webhook receives events
- [ ] Check order status updates
- [ ] Verify email sent
- [ ] Test with different card types
- [ ] Verify admin panel access

**Monitoring:**
- [ ] Set up error tracking (Sentry, Rollbar)
- [ ] Monitor Stripe dashboard for events
- [ ] Check application logs
- [ ] Set up uptime monitoring
- [ ] Configure email alerts for failed payments

---

### **Phase 8: Documentation** (Est: 2 hours)

#### 8.1 User Documentation

Create `docs/USER_GUIDE.md`:
- How to make a purchase
- Payment methods accepted
- Refund policy
- Order tracking
- FAQ

#### 8.2 Developer Documentation

Create `docs/PAYMENT_SYSTEM.md`:
- Architecture overview
- Payment flow diagram
- Webhook event handling
- Error codes and handling
- Testing procedures
- Maintenance tasks

#### 8.3 Troubleshooting Guide

Create `docs/TROUBLESHOOTING.md`:
- Common issues
- Webhook debugging
- Payment failures
- Email not sending
- Stripe dashboard reference

---

## 🧪 Testing Strategy

### Unit Tests
```python
# apps/payments/tests.py
from django.test import TestCase
from apps.payments.models import Payment
from apps.orders.models import Order

class PaymentModelTests(TestCase):
    def test_payment_creation(self):
        # Test payment record creation
        pass
    
    def test_successful_payment_status(self):
        # Test is_successful() method
        pass
    
    def test_refund_eligibility(self):
        # Test can_refund() method
        pass
```

### Integration Tests
```python
# apps/payments/tests_integration.py
from django.test import TestCase, Client
from unittest.mock import patch, Mock

class CheckoutIntegrationTests(TestCase):
    @patch('stripe.PaymentIntent.create')
    def test_checkout_creates_payment_intent(self, mock_create):
        # Test full checkout flow
        pass
```

### Webhook Tests
```python
# apps/payments/tests_webhooks.py
from django.test import TestCase, Client
import stripe

class WebhookTests(TestCase):
    def test_payment_succeeded_webhook(self):
        # Test webhook handling
        pass
```

---

## 📊 Monitoring & Maintenance

### Key Metrics to Track
1. **Payment Success Rate** - Target: >95%
2. **Average Payment Time** - Target: <10 seconds
3. **Webhook Delivery Rate** - Target: 100%
4. **Failed Payment Rate** - Track reasons
5. **Refund Rate** - Business metric

### Daily Tasks
- [ ] Check Stripe dashboard for anomalies
- [ ] Review failed payments
- [ ] Monitor webhook logs
- [ ] Check email delivery

### Weekly Tasks
- [ ] Review payment analytics
- [ ] Check for declined patterns
- [ ] Update test cases
- [ ] Review error logs

### Monthly Tasks
- [ ] Reconcile Stripe payouts with database
- [ ] Update documentation
- [ ] Review security practices
- [ ] Performance optimization

---

## 🚨 Rollback Plan

If issues arise in production:

1. **Disable Payment Processing**
   ```python
   # Temporarily redirect checkout to maintenance page
   # in urls.py or view
   ```

2. **Switch to Manual Processing**
   - Accept orders without immediate payment
   - Process payments manually via Stripe dashboard
   - Update order status manually

3. **Revert Code**
   ```bash
   git revert <commit-hash>
   git push origin main
   # Redeploy
   ```

---

## 📞 Support Contacts

- **Stripe Support:** https://support.stripe.com
- **Stripe Status:** https://status.stripe.com
- **Emergency Contact:** [Your tech lead]

---

## ✅ Final Checklist

Before going live:
- [ ] All test payments successful
- [ ] Webhooks working correctly
- [ ] Emails sending properly
- [ ] Admin panel accessible
- [ ] Error handling tested
- [ ] Security audit passed
- [ ] Documentation complete
- [ ] Team trained
- [ ] Backup plan ready
- [ ] Monitoring configured

---

## 📈 Success Criteria

Payment system is considered complete when:
1. ✅ Test payment completes successfully
2. ✅ Order status updates automatically
3. ✅ Customer receives confirmation email
4. ✅ Admin can view payment in dashboard
5. ✅ Webhooks process correctly
6. ✅ Failed payments handled gracefully
7. ✅ Production deployment successful
8. ✅ No critical bugs for 7 days

---

**Estimated Total Time:** 22 hours (~3 working days)

**Priority Order:**
1. Phase 1 (Setup) - CRITICAL
2. Phase 2 (Testing) - CRITICAL
3. Phase 7 (Deployment) - HIGH
4. Phase 3 (Emails) - HIGH
5. Phase 5 (Error Handling) - MEDIUM
6. Phase 4 (Admin) - MEDIUM
7. Phase 6 (Security) - MEDIUM
8. Phase 8 (Documentation) - LOW

---

*Last Updated: November 4, 2025*
*Project: Gulf Emperor E-commerce*
*Developer: [Your Name]*
