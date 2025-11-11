from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.translation import gettext as _
from django.conf import settings
import stripe

from apps.orders.models import Cart, Order, OrderItem
from apps.payments.models import Payment

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    """
    Checkout view - handles order creation and payment initiation
    No shipping/address required (digital or in-store pickup)
    """
    
    # Get or create cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if cart is empty
    if not cart.items.exists():
        return redirect('store:product_list')
    
    # GET request - show checkout page
    if request.method == 'GET':
        context = {
            'cart': cart,
        }
        
        return render(request, 'orders/checkout.html', context)
    
    # POST request - create order
    elif request.method == 'POST':
        order_notes = request.POST.get('notes', '').strip()
        
        try:
            # Create order within a transaction
            with transaction.atomic():
                # Calculate totals (no shipping cost)
                total = cart.subtotal
                
                # Create the order
                order = Order.objects.create(
                    user=request.user,
                    address=None,  # No shipping address needed
                    total_price=total,
                    shipping_cost=0,  # No shipping
                    notes=order_notes,
                    status='pending',
                    payment_status='pending'
                )
                
                # Create order items from cart items
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        product_name=cart_item.product.name,
                        product_sku=cart_item.product.sku,
                        quantity=cart_item.quantity,
                        price=cart_item.unit_price
                    )
                
                # Create Stripe PaymentIntent
                amount_in_fils = int(total * 1000)  # Convert SAR to fils (1 SAR = 1000 fils)
                
                payment_intent = stripe.PaymentIntent.create(
                    amount=amount_in_fils,
                    currency='SAR',
                    metadata={
                        'order_id': order.id,
                        'order_number': order.order_number,
                        'user_id': request.user.id,
                    },
                    description=f'Order #{order.order_number}'
                )
                
                # Create Payment record
                Payment.objects.create(
                    order=order,
                    stripe_payment_intent_id=payment_intent.id,
                    amount=total,
                    currency='SAR',
                    status='pending',
                    metadata={
                        'payment_intent': payment_intent.id,
                        'client_secret': payment_intent.client_secret,
                    }
                )
                
                # Store client_secret in session for payment page
                request.session['payment_intent_client_secret'] = payment_intent.client_secret
                request.session['order_id'] = order.id
                
                # Clear the cart
                cart.items.all().delete()
                
                # Redirect to payment page
                return redirect('payments:payment_process', order_id=order.id)
        
        except Exception as e:
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Checkout error: {str(e)}')
            return redirect('orders:checkout')
