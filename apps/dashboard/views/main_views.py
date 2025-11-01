from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta

from apps.orders.models import Order
from apps.users.models import User
from apps.store.models import Product


@staff_member_required
def dashboard_home(request):
    """
    Main dashboard home view showing key metrics and statistics
    """
    
    # Get date ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Order statistics
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    confirmed_orders = Order.objects.filter(status='confirmed').count()
    processing_orders = Order.objects.filter(status='processing').count()
    shipped_orders = Order.objects.filter(status='shipped').count()
    delivered_orders = Order.objects.filter(status='delivered').count()
    
    # Recent orders (this week)
    recent_orders = Order.objects.filter(
        created_at__gte=week_ago
    ).count()
    
    # Revenue statistics
    total_revenue = Order.objects.filter(
        payment_status='paid'
    ).aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    weekly_revenue = Order.objects.filter(
        payment_status='paid',
        created_at__gte=week_ago
    ).aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    monthly_revenue = Order.objects.filter(
        payment_status='paid',
        created_at__gte=month_ago
    ).aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    # Customer statistics
    total_customers = User.objects.filter(is_staff=False).count()
    new_customers_week = User.objects.filter(
        is_staff=False,
        date_joined__gte=week_ago
    ).count()
    
    # Product statistics
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    low_stock_products = Product.objects.filter(
        stock_quantity__lte=10,
        stock_quantity__gt=0
    ).count()
    out_of_stock = Product.objects.filter(stock_quantity=0).count()
    
    # Recent orders for display
    latest_orders = Order.objects.select_related(
        'user', 'address'
    ).order_by('-created_at')[:10]
    
    context = {
        # Order stats
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'processing_orders': processing_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,
        'recent_orders_count': recent_orders,
        
        # Revenue stats
        'total_revenue': total_revenue,
        'weekly_revenue': weekly_revenue,
        'monthly_revenue': monthly_revenue,
        
        # Customer stats
        'total_customers': total_customers,
        'new_customers_week': new_customers_week,
        
        # Product stats
        'total_products': total_products,
        'active_products': active_products,
        'low_stock_products': low_stock_products,
        'out_of_stock': out_of_stock,
        
        # Latest orders
        'latest_orders': latest_orders,
    }
    
    return render(request, 'dashboard/home.html', context)
