from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.translation import gettext as _
from django.conf import settings
import stripe

from apps.orders.models import Cart, Order, OrderItem
from apps.payments.models import Payment
from apps.users.models import Address

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    """
    Checkout view - handles order creation and payment initiation
    Collects delivery address and contact information
    """
    
    # Get or create cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if cart is empty
    if not cart.items.exists():
        return redirect('store:product_list')
    
    # GET request - show checkout page
    if request.method == 'GET':
        # Get user's saved addresses
        user_addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')
        
        context = {
            'cart': cart,
            'user_addresses': user_addresses,
        }
        
        return render(request, 'orders/checkout.html', context)
    
    # POST request - create order
    elif request.method == 'POST':
        order_notes = request.POST.get('notes', '').strip()
        
        # Get delivery address fields
        full_name = request.POST.get('full_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        street = request.POST.get('street', '').strip()
        additional_info = request.POST.get('additional_info', '').strip()
        
        # Validate required fields
        if not all([full_name, phone_number, city, street]):
            from django.contrib import messages
            messages.error(request, 'الرجاء تعبئة جميع الحقول المطلوبة')
            return redirect('orders:checkout')
        
        try:
            # CRITICAL: Validate stock availability before creating order
            stock_errors = []
            for cart_item in cart.items.all():
                product = cart_item.product
                if not product.has_stock:
                    stock_errors.append(f'{product.name} - نفد من المخزون')
                elif cart_item.quantity > product.stock:
                    stock_errors.append(
                        f'{product.name} - المتوفر فقط {product.stock} قطعة'
                    )
            
            if stock_errors:
                # Stock validation failed - redirect back to cart with errors
                from django.contrib import messages
                for error in stock_errors:
                    messages.error(request, error)
                messages.error(request, 'الرجاء تحديث السلة قبل المتابعة')
                return redirect('orders:cart')
            
            # Create order within a transaction
            with transaction.atomic():
                # Create delivery address
                delivery_address = Address.objects.create(
                    user=request.user,
                    label="طلب",  # Order address
                    full_name=full_name,
                    phone_number=phone_number,
                    street=street,
                    city=city,
                    state=state,
                    additional_info=additional_info,
                    country="السعودية",
                    is_default=False
                )
                
                # Calculate totals (no shipping cost)
                total = cart.subtotal
                
                # Create the order
                order = Order.objects.create(
                    user=request.user,
                    address=delivery_address,  # Link delivery address
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
