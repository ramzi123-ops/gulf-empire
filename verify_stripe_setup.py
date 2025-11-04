#!/usr/bin/env python
"""
Stripe Setup Verification Script
Run this to verify your Stripe configuration is correct
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
import stripe


def print_success(message):
    print(f"✅ {message}")


def print_error(message):
    print(f"❌ {message}")


def print_warning(message):
    print(f"⚠️  {message}")


def print_info(message):
    print(f"ℹ️  {message}")


def verify_stripe_keys():
    """Verify Stripe API keys are configured"""
    print("\n" + "="*60)
    print("🔑 Verifying Stripe API Keys")
    print("="*60)
    
    # Check Publishable Key
    pub_key = getattr(settings, 'STRIPE_PUBLISHABLE_KEY', None)
    if pub_key and pub_key.startswith('pk_test_'):
        print_success(f"Publishable Key: {pub_key[:20]}...")
    elif pub_key and pub_key.startswith('pk_live_'):
        print_warning(f"Live Key Detected: {pub_key[:20]}... (Use test keys for development!)")
    else:
        print_error("Publishable Key: Not configured or invalid")
        return False
    
    # Check Secret Key
    secret_key = getattr(settings, 'STRIPE_SECRET_KEY', None)
    if secret_key and secret_key.startswith('sk_test_'):
        print_success(f"Secret Key: {secret_key[:20]}...")
    elif secret_key and secret_key.startswith('sk_live_'):
        print_warning(f"Live Key Detected: {secret_key[:20]}... (Use test keys for development!)")
    else:
        print_error("Secret Key: Not configured or invalid")
        return False
    
    # Check Webhook Secret
    webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', None)
    if webhook_secret and webhook_secret.startswith('whsec_'):
        print_success(f"Webhook Secret: {webhook_secret[:20]}...")
    else:
        print_warning("Webhook Secret: Not configured (Run 'stripe listen' to get it)")
    
    return True


def test_stripe_connection():
    """Test connection to Stripe API"""
    print("\n" + "="*60)
    print("🌐 Testing Stripe API Connection")
    print("="*60)
    
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # Try to retrieve account information
        account = stripe.Account.retrieve()
        print_success(f"Connected to Stripe account")
        print_info(f"   Account ID: {account.id}")
        print_info(f"   Country: {account.country}")
        print_info(f"   Default Currency: {account.default_currency.upper()}")
        
        # Try to list payment intents (should work even if empty)
        payment_intents = stripe.PaymentIntent.list(limit=1)
        print_success(f"API calls working correctly")
        
        return True
        
    except stripe.error.AuthenticationError as e:
        print_error(f"Authentication failed: {str(e)}")
        print_info("   Check your STRIPE_SECRET_KEY in .env file")
        return False
        
    except Exception as e:
        print_error(f"Connection failed: {str(e)}")
        return False


def verify_webhook_endpoint():
    """Verify webhook endpoint is configured"""
    print("\n" + "="*60)
    print("🔗 Verifying Webhook Configuration")
    print("="*60)
    
    webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', None)
    
    if not webhook_secret or not webhook_secret.startswith('whsec_'):
        print_warning("Webhook secret not configured")
        print_info("   For local development, run:")
        print_info("   stripe listen --forward-to localhost:8000/payments/webhook/stripe/")
        print_info("   Then copy the webhook secret to your .env file")
        return False
    
    print_success("Webhook secret configured")
    print_info("   Make sure 'stripe listen' is running during development")
    
    return True


def check_database():
    """Check if payment models are migrated"""
    print("\n" + "="*60)
    print("🗄️  Checking Database")
    print("="*60)
    
    try:
        from apps.payments.models import Payment
        from apps.orders.models import Order
        
        # Try to query (will fail if migrations not run)
        payment_count = Payment.objects.count()
        order_count = Order.objects.count()
        
        print_success(f"Payment model: {payment_count} records")
        print_success(f"Order model: {order_count} records")
        print_info("   Database migrations are up to date")
        
        return True
        
    except Exception as e:
        print_error(f"Database error: {str(e)}")
        print_info("   Run: python manage.py migrate")
        return False


def print_next_steps():
    """Print next steps"""
    print("\n" + "="*60)
    print("🚀 Next Steps")
    print("="*60)
    print()
    print("1. Start Django development server:")
    print("   python manage.py runserver")
    print()
    print("2. Start Stripe webhook forwarding (in new terminal):")
    print("   stripe listen --forward-to localhost:8000/payments/webhook/stripe/")
    print()
    print("3. Test payment flow:")
    print("   - Visit: http://localhost:8000")
    print("   - Add product to cart")
    print("   - Proceed to checkout")
    print("   - Use test card: 4242 4242 4242 4242")
    print()
    print("4. Monitor webhook events in the Stripe CLI terminal")
    print()


def main():
    """Main verification function"""
    print("\n" + "="*70)
    print("🎯 Gulf Emperor - Stripe Setup Verification")
    print("="*70)
    
    all_checks_passed = True
    
    # Run all checks
    if not verify_stripe_keys():
        all_checks_passed = False
    
    if not test_stripe_connection():
        all_checks_passed = False
    
    if not verify_webhook_endpoint():
        all_checks_passed = False
    
    if not check_database():
        all_checks_passed = False
    
    # Print summary
    print("\n" + "="*70)
    if all_checks_passed:
        print("✅ ALL CHECKS PASSED! Your Stripe setup is ready!")
        print_next_steps()
    else:
        print("⚠️  SOME CHECKS FAILED - Please fix the issues above")
        print("\nFor help, see:")
        print("- STRIPE_SETUP_GUIDE.md")
        print("- PAYMENT_COMPLETION_PLAN.md")
    print("="*70 + "\n")
    
    return 0 if all_checks_passed else 1


if __name__ == '__main__':
    sys.exit(main())
