"""
Order management views - order detail, tracking, etc.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

from apps.orders.models import Order


@login_required
def order_detail(request, order_id):
    """
    Display order detail page with items, status, and payment information
    """
    
    # Get order - ensure user can only see their own orders
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    
    return render(request, 'orders/order_detail.html', context)


@login_required
def order_list(request):
    """
    Display list of user's orders
    """
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'orders/order_list.html', context)
