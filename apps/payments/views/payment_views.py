from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.conf import settings

from apps.orders.models import Order


@login_required
def payment_process(request, order_id):
    """
    Payment processing view - displays Stripe payment form
    """
    
    # Get the order
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check if order is already paid
    if order.payment_status == 'paid':
        return redirect('users:order_detail', order_id=order.id)
    
    # Get client_secret from session
    client_secret = request.session.get('payment_intent_client_secret')
    
    if not client_secret:
        return redirect('orders:checkout')
    
    context = {
        'order': order,
        'client_secret': client_secret,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    
    return render(request, 'payments/payment.html', context)


@login_required
def payment_success(request, order_id):
    """
    Payment success view - shown after successful payment
    """
    
    # Get the order
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Clear payment session data
    if 'payment_intent_client_secret' in request.session:
        del request.session['payment_intent_client_secret']
    if 'order_id' in request.session:
        del request.session['order_id']
    
    context = {
        'order': order,
    }
    
    return render(request, 'payments/payment_success.html', context)


@login_required
def payment_cancelled(request):
    """
    Payment cancelled view - shown when user cancels payment
    """
    
    return redirect('users:account')
