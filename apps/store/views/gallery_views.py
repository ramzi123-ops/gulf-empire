from django.shortcuts import render
from django.core.paginator import Paginator
from apps.store.models import Gallery


def gallery_list(request):
    """
    معرض الصور
    Gallery page with filtering
    """
    # Get all active gallery images
    gallery_items = Gallery.objects.filter(is_active=True).order_by('display_order', '-created_at')
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        gallery_items = gallery_items.filter(category=category)
    
    # Pagination
    paginator = Paginator(gallery_items, 12)  # 12 images per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter
    categories = Gallery.CATEGORY_CHOICES
    
    context = {
        'gallery_items': page_obj,
        'categories': categories,
        'current_category': category,
    }
    
    return render(request, 'store/gallery.html', context)
