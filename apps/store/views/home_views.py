from django.shortcuts import render
from django.db.models import Count, Sum, Q
from django.utils import timezone
from apps.store.models import Product, Category, Brand, Advertisement, Gallery


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
    
    # Get active advertisements by placement
    now = timezone.now()
    ad_filter = Q(is_active=True) & (
        Q(start_date__isnull=True) | Q(start_date__lte=now)
    ) & (
        Q(end_date__isnull=True) | Q(end_date__gte=now)
    )
    
    hero_ads = Advertisement.objects.filter(
        ad_filter, placement='hero'
    ).order_by('display_order')[:5]
    
    sidebar_ads = Advertisement.objects.filter(
        ad_filter, placement='sidebar'
    ).order_by('display_order')[:3]
    
    middle_ads = Advertisement.objects.filter(
        ad_filter, placement='middle'
    ).order_by('display_order')[:2]
    
    footer_ads = Advertisement.objects.filter(
        ad_filter, placement='footer'
    ).order_by('display_order')[:3]
    
    popup_ads = Advertisement.objects.filter(
        ad_filter, placement='popup'
    ).order_by('display_order')[:1]
    
    # Get featured gallery images
    featured_gallery = Gallery.objects.filter(
        is_active=True,
        is_featured=True
    ).order_by('display_order')[:6]
    
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
        'hero_ads': hero_ads,
        'sidebar_ads': sidebar_ads,
        'middle_ads': middle_ads,
        'footer_ads': footer_ads,
        'popup_ads': popup_ads,
        'featured_gallery': featured_gallery,
    }
    
    return render(request, 'store/home.html', context)
