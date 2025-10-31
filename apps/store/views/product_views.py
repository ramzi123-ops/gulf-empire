from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from apps.store.models import Product, Category, Brand


def product_list(request):
    """
    عرض قائمة المنتجات
    Display list of active products
    """
    # Get only active products with stock
    products = Product.objects.filter(
        is_active=True
    ).select_related('category', 'brand').order_by('-created_at')

    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Filter by brand
    brand_slug = request.GET.get('brand')
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(sku__icontains=search_query) |
            Q(compatible_makes__icontains=search_query) |
            Q(compatible_models__icontains=search_query)
        )

    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Filter by features
    if request.GET.get('featured') == 'true':
        products = products.filter(is_featured=True)
    if request.GET.get('new_arrival') == 'true':
        products = products.filter(is_new_arrival=True)
    if request.GET.get('on_sale') == 'true':
        products = products.filter(sale_price__isnull=False)

    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name_asc': 'name',
        'name_desc': '-name',
        'newest': '-created_at',
        'oldest': 'created_at',
    }
    products = products.order_by(valid_sorts.get(sort_by, '-created_at'))

    # Get all categories and brands for filter sidebar
    categories = Category.objects.filter(is_active=True, parent__isnull=True)
    brands = Brand.objects.filter(is_active=True)

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'current_category': category_slug,
        'current_brand': brand_slug,
        'search_query': search_query,
    }

    # Check if this is an HTMX request
    if request.htmx:
        return render(request, 'store/partials/product_grid.html', context)

    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    """
    عرض تفاصيل المنتج
    Display single product details
    """
    product = get_object_or_404(
        Product.objects.select_related('category', 'brand').prefetch_related('specifications'),
        slug=slug,
        is_active=True
    )

    # Get related products (same category, excluding current product)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id).select_related('category', 'brand')[:4]

    # Collect all product images
    product_images = [product.main_image]
    if product.image_2:
        product_images.append(product.image_2)
    if product.image_3:
        product_images.append(product.image_3)
    if product.image_4:
        product_images.append(product.image_4)

    context = {
        'product': product,
        'related_products': related_products,
        'product_images': product_images,
    }

    return render(request, 'store/product_detail.html', context)
