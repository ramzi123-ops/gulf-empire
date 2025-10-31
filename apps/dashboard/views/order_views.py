from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.translation import gettext as _

from apps.orders.models import Order


@staff_member_required
def dashboard_order_list(request):
    """
    Display list of all orders with filtering and search
    """
    
    # Get all orders
    orders = Order.objects.select_related(
        'user', 'address'
    ).prefetch_related('items').order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Filter by payment status
    payment_filter = request.GET.get('payment_status')
    if payment_filter:
        orders = orders.filter(payment_status=payment_filter)
    
    # Search by order number or customer email
    search_query = request.GET.get('search')
    if search_query:
        orders = orders.filter(
            Q(order_number__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(orders, 20)  # 20 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get status counts for filter badges
    status_counts = {
        'all': Order.objects.count(),
        'pending': Order.objects.filter(status='pending').count(),
        'confirmed': Order.objects.filter(status='confirmed').count(),
        'processing': Order.objects.filter(status='processing').count(),
        'shipped': Order.objects.filter(status='shipped').count(),
        'delivered': Order.objects.filter(status='delivered').count(),
        'cancelled': Order.objects.filter(status='cancelled').count(),
    }
    
    context = {
        'page_obj': page_obj,
        'status_counts': status_counts,
        'current_status': status_filter,
        'current_payment': payment_filter,
        'search_query': search_query,
    }
    
    return render(request, 'dashboard/order_list.html', context)


@staff_member_required
def dashboard_order_detail(request, order_id):
    """
    Display order details and allow status updates
    Role-based: Only 'Store Manager' can update order status
    """
    
    # Get the order
    order = get_object_or_404(
        Order.objects.select_related('user', 'address').prefetch_related('items__product', 'payments'),
        id=order_id
    )
    
    # Check if user can update status (Store Manager only)
    can_update_status = request.user.groups.filter(name='Store Manager').exists()
    
    # Handle status update via POST
    if request.method == 'POST':
        # Verify user has permission to update status
        if not can_update_status:
            messages.error(request, 'ليس لديك صلاحية لتحديث حالة الطلب.')
            return redirect('dashboard:order_detail', order_id=order.id)
        
        new_status = request.POST.get('status')
        
        # Validate status
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status in valid_statuses:
            old_status = order.status
            order.status = new_status
            order.save()
            
            messages.success(
                request,
                f'تم تحديث حالة الطلب من "{old_status}" إلى "{new_status}"'
            )
            
            # TODO: Send status update email to customer
            # send_order_status_update_email(order, old_status, new_status)
            
            return redirect('dashboard:order_detail', order_id=order.id)
        else:
            messages.error(request, 'الحالة المختارة غير صحيحة.')
    
    # Get order status history (if tracking model exists)
    # For now, we'll just show current status
    
    context = {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
        'can_update_status': can_update_status,
    }
    
    return render(request, 'dashboard/order_detail.html', context)
