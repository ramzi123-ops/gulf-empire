"""
Check if Stripe keys are configured correctly
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings

print("=" * 60)
print("STRIPE CONFIGURATION CHECK")
print("=" * 60)

# Check publishable key
pub_key = settings.STRIPE_PUBLISHABLE_KEY
if pub_key.startswith('pk_test_'):
    print(f"\n✅ Publishable Key: {pub_key[:20]}... (OK)")
else:
    print(f"\n❌ Publishable Key: {pub_key}")
    print("   ERROR: Should start with 'pk_test_'")

# Check secret key
sec_key = settings.STRIPE_SECRET_KEY
if sec_key.startswith('sk_test_'):
    print(f"✅ Secret Key: {sec_key[:20]}... (OK)")
else:
    print(f"❌ Secret Key: {sec_key}")
    print("   ERROR: Should start with 'sk_test_'")

# Check webhook secret
webhook_key = settings.STRIPE_WEBHOOK_SECRET
if webhook_key.startswith('whsec_'):
    print(f"✅ Webhook Secret: {webhook_key[:20]}... (OK)")
else:
    print(f"⚠️  Webhook Secret: {webhook_key}")
    print("   WARNING: Should start with 'whsec_'")

print("\n" + "=" * 60)
print("RECOMMENDATIONS")
print("=" * 60)

if not pub_key.startswith('pk_test_'):
    print("\n❌ Fix your .env file:")
    print("   STRIPE_PUBLISHABLE_KEY should start with 'pk_test_'")
    print("   Get it from: https://dashboard.stripe.com/test/apikeys")

if not sec_key.startswith('sk_test_'):
    print("\n❌ Fix your .env file:")
    print("   STRIPE_SECRET_KEY should start with 'sk_test_'")
    print("   Get it from: https://dashboard.stripe.com/test/apikeys")

if not webhook_key.startswith('whsec_'):
    print("\n⚠️  Update your .env file:")
    print("   STRIPE_WEBHOOK_SECRET=whsec_7d135b42f43d462f0fa9ebf2aea190cd6bd9d2e648ac44cb977f9df132266412")

if pub_key.startswith('pk_test_') and sec_key.startswith('sk_test_'):
    print("\n✅ All keys look good!")
    print("\nIf card input is still disabled:")
    print("1. Open browser console (F12)")
    print("2. Look for JavaScript errors")
    print("3. Hard refresh the page (Ctrl+F5)")
    print("4. Check if Stripe.js loaded: https://js.stripe.com/v3/")

print("\n" + "=" * 60)
