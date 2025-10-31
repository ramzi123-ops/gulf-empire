# Stripe Webhook Setup Guide

This guide explains how to set up and test the Stripe webhook endpoint for handling payment events.

## Overview

The webhook endpoint is located at: `/payments/webhook/stripe/`

It handles the following Stripe events:
- `payment_intent.succeeded` - Updates order to "Paid" and "Confirmed"
- `payment_intent.payment_failed` - Marks payment and order as failed
- `charge.succeeded` - Records charge ID for additional tracking
- `charge.refunded` - Updates order to refunded/cancelled status

## Setup Instructions

### 1. Get Your Stripe Keys

Visit the [Stripe Dashboard](https://dashboard.stripe.com/apikeys) and copy your keys:

- **Publishable Key** (starts with `pk_test_` or `pk_live_`)
- **Secret Key** (starts with `sk_test_` or `sk_live_`)

### 2. Configure Environment Variables

Add these to your environment variables or `.env` file:

```bash
STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

### 3. Testing Locally with Stripe CLI

#### Install Stripe CLI

**Windows (using Scoop):**
```powershell
scoop install stripe
```

**macOS (using Homebrew):**
```bash
brew install stripe/stripe-cli/stripe
```

**Linux:**
Download from: https://github.com/stripe/stripe-cli/releases

#### Login to Stripe

```bash
stripe login
```

#### Forward Webhooks to Local Server

Start your Django development server:
```bash
python manage.py runserver
```

In another terminal, forward webhooks:
```bash
stripe listen --forward-to localhost:8000/payments/webhook/stripe/
```

This command will output a webhook signing secret. Copy it and add to your environment:
```bash
STRIPE_WEBHOOK_SECRET=whsec_...
```

#### Test the Webhook

Trigger a test payment event:
```bash
stripe trigger payment_intent.succeeded
```

You should see the webhook event logged in your Django console.

### 4. Production Setup

#### Create a Webhook Endpoint in Stripe Dashboard

1. Go to [Stripe Webhooks](https://dashboard.stripe.com/webhooks)
2. Click **"Add endpoint"**
3. Enter your endpoint URL: `https://yourdomain.com/payments/webhook/stripe/`
4. Select events to listen to:
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
   - `charge.succeeded`
   - `charge.refunded`
5. Click **"Add endpoint"**
6. Copy the **Signing secret** (starts with `whsec_`)
7. Add it to your production environment variables

## Webhook Flow

### Successful Payment Flow

1. Customer completes payment on frontend
2. Stripe sends `payment_intent.succeeded` webhook
3. Webhook handler:
   - Finds Payment record by `stripe_payment_intent_id`
   - Updates Payment status to `'succeeded'`
   - Records `paid_at` timestamp
   - Stores charge ID
   - Updates Order `payment_status` to `'paid'`
   - Updates Order `status` to `'confirmed'`
   - Logs success

### Failed Payment Flow

1. Payment fails on Stripe
2. Stripe sends `payment_intent.payment_failed` webhook
3. Webhook handler:
   - Finds Payment record
   - Updates Payment status to `'failed'`
   - Stores error message
   - Updates Order `payment_status` to `'failed'`
   - Logs warning

### Refund Flow

1. Refund issued in Stripe Dashboard
2. Stripe sends `charge.refunded` webhook
3. Webhook handler:
   - Finds Payment record
   - Updates Payment status to `'refunded'`
   - Updates Order `payment_status` to `'refunded'`
   - Updates Order `status` to `'cancelled'`
   - Logs refund

## Security

The webhook endpoint:
- Is marked with `@csrf_exempt` (required for external webhooks)
- Verifies webhook signature using `stripe.Webhook.construct_event()`
- Returns 400/500 errors for invalid requests
- Logs all events for monitoring

## Monitoring

Check your logs for webhook events:
```bash
# View recent webhook events
tail -f logs/django.log | grep "Stripe webhook"

# Check for errors
tail -f logs/django.log | grep "Error handling"
```

## Troubleshooting

### Webhook Not Receiving Events

1. Check endpoint URL is correct
2. Verify webhook secret matches
3. Check firewall/security settings allow Stripe IPs
4. View webhook logs in Stripe Dashboard

### Signature Verification Failed

- Ensure `STRIPE_WEBHOOK_SECRET` is correct
- Check you're using the right secret (test vs live mode)
- Verify no middleware is modifying request body

### Payment Not Updating Order

1. Check Payment record exists with matching `stripe_payment_intent_id`
2. Verify Order is linked to Payment
3. Check database transaction didn't fail
4. Review error logs

## Test Card Numbers

Use these in test mode:

| Card Number         | Description            |
|---------------------|------------------------|
| 4242 4242 4242 4242 | Succeeds               |
| 4000 0000 0000 0002 | Declined               |
| 4000 0025 0000 3155 | Requires authentication|

**Expiry:** Any future date  
**CVC:** Any 3 digits  
**ZIP:** Any 5 digits

## Resources

- [Stripe Webhooks Documentation](https://stripe.com/docs/webhooks)
- [Stripe CLI Documentation](https://stripe.com/docs/stripe-cli)
- [Testing Webhooks](https://stripe.com/docs/webhooks/test)
- [Webhook Event Types](https://stripe.com/docs/api/events/types)
