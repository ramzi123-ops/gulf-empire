from django.shortcuts import render
from django.db.models import Count, Sum, Q
from apps.store.models import Product, Category, Brand


def home(request):
    """
    الصفحة الرئيسية
    Homepage with featured sections
    """
    # Get active categories (top-level only)
    categories = Category.objects.filter(
        is_active=True,
        parent__isnull=True
    ).order_by('name')[:8]
    
    # Get active brands with logos
    brands = Brand.objects.filter(
        is_active=True,
        logo__isnull=False
    ).order_by('name')[:12]
    
    # Get featured products (مميز)
    featured_products = Product.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related('category', 'brand').order_by('-created_at')[:8]
    
    # Get featured products WITH discount (مميز مع خصم)
    featured_sale_products = Product.objects.filter(
        is_active=True,
        is_featured=True,
        sale_price__isnull=False
    ).select_related('category', 'brand').order_by('-created_at')[:8]
    
    # Get new arrivals (وصل حديثاً)
    new_arrivals = Product.objects.filter(
        is_active=True,
        is_new_arrival=True
    ).select_related('category', 'brand').order_by('-created_at')[:8]
    
    # Get products on sale (العروض)
    sale_products = Product.objects.filter(
        is_active=True,
        sale_price__isnull=False
    ).select_related('category', 'brand').order_by('-created_at')[:8]
    
    # Get most sold products (based on order items - will show all for now)
    # TODO: Update when order statistics are available
    most_sold_products = Product.objects.filter(
        is_active=True
    ).select_related('category', 'brand').order_by('-created_at')[:8]
    
    # Get coming soon products (قريباً)
    coming_soon_products = Product.objects.filter(
        is_active=True,
        is_coming_soon=True
    ).select_related('category', 'brand').order_by('-created_at')[:8]
    
    # Get all products for "Shop All" section
    all_products = Product.objects.filter(
        is_active=True
    ).select_related('category', 'brand').order_by('-created_at')[:12]
    
    context = {
        'categories': categories,
        'brands': brands,
        'featured_products': featured_products,
        'featured_sale_products': featured_sale_products,
        'new_arrivals': new_arrivals,
        'sale_products': sale_products,
        'most_sold_products': most_sold_products,
        'coming_soon_products': coming_soon_products,
        'all_products': all_products,
    }
    
    return render(request, 'store/home.html', context)
