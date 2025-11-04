"""
Quick script to check order and payment status
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.orders.models import Order
from apps.payments.models import Payment

print("=" * 60)
print("ORDER STATUS CHECK")
print("=" * 60)

# Get recent orders
orders = Order.objects.all().order_by('-created_at')[:5]

if not orders:
    print("\n❌ No orders found")
else:
    print(f"\n📦 Last {orders.count()} Orders:\n")
    
    for order in orders:
        print(f"{'='*60}")
        print(f"Order #{order.order_number}")
        print(f"{'='*60}")
        print(f"  User: {order.user.username}")
        print(f"  Created: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Total: {order.total_price} SAR")
        print(f"  Status: {order.get_status_display()}")
        print(f"  Payment Status: {order.get_payment_status_display()}")
        
        # Check payment record
        payments = Payment.objects.filter(order=order)
        if payments.exists():
            print(f"\n  💳 Payments:")
            for payment in payments:
                print(f"    - ID: {payment.id}")
                print(f"      Status: {payment.get_status_display()}")
                print(f"      Amount: {payment.amount} SAR")
                print(f"      Stripe Intent: {payment.stripe_payment_intent_id}")
                if payment.error_message:
                    print(f"      ⚠️  Error: {payment.error_message}")
        else:
            print(f"\n  ❌ No payment records")
        
        print()

print("=" * 60)
print("SUMMARY")
print("=" * 60)

# Count by status
pending = Order.objects.filter(status='pending').count()
confirmed = Order.objects.filter(status='confirmed').count()
paid = Order.objects.filter(payment_status='paid').count()
failed = Order.objects.filter(payment_status='failed').count()

print(f"  Pending Orders: {pending}")
print(f"  Confirmed Orders: {confirmed}")
print(f"  Paid Orders: {paid}")
print(f"  Failed Payments: {failed}")

print("\n" + "=" * 60)
