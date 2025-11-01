from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils.translation import gettext as _
from django.conf import settings
import stripe

from apps.orders.models import Cart, Order, OrderItem
from apps.users.models import Address
from apps.payments.models import Payment

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    """
    Checkout view - handles address selection and order creation
    """
    
    # Get or create cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if cart is empty
    if not cart.items.exists():
        messages.warning(request, _('Your cart is empty. Please add items before checking out.'))
        return redirect('store:product_list')
    
    # GET request - show checkout page
    if request.method == 'GET':
        # Get user's addresses
        addresses = Address.objects.filter(user=request.user)
        
        # Check if user has at least one address
        if not addresses.exists():
            messages.warning(request, _('Please add a delivery address before checking out.'))
            return redirect('users:add_address')
        
        context = {
            'cart': cart,
            'addresses': addresses,
            'default_address': addresses.filter(is_default=True).first(),
        }
        
        return render(request, 'orders/checkout.html', context)
    
    # POST request - create order
    elif request.method == 'POST':
        address_id = request.POST.get('address_id')
        order_notes = request.POST.get('notes', '').strip()
        
        # Validate address selection
        if not address_id:
            messages.error(request, _('Please select a delivery address.'))
            return redirect('orders:checkout')
        
        # Get the selected address
        address = get_object_or_404(Address, id=address_id, user=request.user)
        
        try:
            # Create order within a transaction
            with transaction.atomic():
                # Calculate totals
                subtotal = cart.get_subtotal()
                shipping_cost = cart.get_shipping_cost()
                total = cart.get_total()
                
                # Create the order
                order = Order.objects.create(
                    user=request.user,
                    address=address,
                    total_price=total,
                    shipping_cost=shipping_cost,
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
            messages.error(request, _('An error occurred while creating your order. Please try again.'))
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Checkout error: {str(e)}')
            return redirect('orders:checkout')
