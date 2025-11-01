from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from apps.store.models import Product
from apps.orders.models import CartItem
from apps.orders.utils import get_cart


@require_POST
def add_to_cart(request, product_id):
    """
    إضافة منتج إلى السلة
    Add a product to the shopping cart
    
    Args:
        request: Django HttpRequest object
        product_id: Product ID to add to cart
        
    Returns:
        Rendered cart_icon.html partial with OOB swap
    """
    # Get the product
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Check if product has stock using inventory system
    if not product.has_stock:
        # Return HTMX OOB error toast
        error_html = '''
        <div hx-swap-oob="true" id="toast-message" 
             class="fixed top-4 start-4 z-50 flex items-center gap-3 bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg shadow-lg">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
            </svg>
            <span class="font-semibold">عذراً، هذا المنتج غير متوفر حالياً</span>
        </div>
        '''
        return HttpResponse(error_html)
    
    # Get or create the cart
    cart = get_cart(request)
    
    # Get quantity from request (default to 1)
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1
    
    # Check stock availability using inventory system
    cart_item = cart.items.filter(product=product).first()
    quantity_in_cart = cart_item.quantity if cart_item else 0
    new_total = quantity_in_cart + quantity
    
    # Validate against inventory stock
    if new_total > product.stock:
        # Return HTMX OOB error toast
        error_html = '''
        <div hx-swap-oob="true" id="toast-message" 
             class="fixed top-4 start-4 z-50 flex items-center gap-3 bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg shadow-lg">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
            </svg>
            <span class="font-semibold">لا توجد كمية كافية في المخزون</span>
        </div>
        '''
        return HttpResponse(error_html)
    
    # Add or update cart item
    if cart_item:
        cart_item.increase_quantity(quantity)
        messages.success(request, f'تم تحديث كمية {product.name} في السلة')
    else:
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity
        )
        messages.success(request, f'تمت إضافة {product.name} إلى السلة')
    
    # Return updated cart icon with OOB swap
    return render(request, 'partials/cart_icon.html', {
        'cart': cart
    })


@require_POST
def update_cart_item(request, item_id):
    """
    تحديث كمية منتج في السلة
    Update quantity of a cart item
    
    Args:
        request: Django HttpRequest object
        item_id: CartItem ID to update
        
    Returns:
        Rendered cart partial
    """
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    # Get action (increase, decrease, or set)
    action = request.POST.get('action', 'set')
    
    if action == 'increase':
        # Check against inventory stock
        if cart_item.quantity < cart_item.product.stock:
            cart_item.increase_quantity(1)
            messages.success(request, 'تم تحديث الكمية')
        else:
            messages.error(request, 'لا توجد كمية كافية في المخزون')
    
    elif action == 'decrease':
        cart_item.decrease_quantity(1)
        if cart_item.quantity > 0:
            messages.success(request, 'تم تحديث الكمية')
        else:
            messages.success(request, 'تم حذف المنتج من السلة')
    
    else:  # set quantity
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                cart_item.delete()
                messages.success(request, 'تم حذف المنتج من السلة')
            elif quantity > cart_item.product.stock:
                messages.error(request, f'لا توجد كمية كافية في المخزون')
            else:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'تم تحديث الكمية')
        except (ValueError, TypeError):
            messages.error(request, 'كمية غير صالحة')
    
    # Return updated cart icon with OOB swap
    return render(request, 'partials/cart_icon.html', {
        'cart': cart
    })


@require_POST
def remove_from_cart(request, item_id):
    """
    حذف منتج من السلة
    Remove a product from the cart
    
    Args:
        request: Django HttpRequest object
        item_id: CartItem ID to remove
        
    Returns:
        Rendered cart partial
    """
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    product_name = cart_item.product.name
    cart_item.delete()
    
    messages.success(request, f'تم حذف {product_name} من السلة')
    
    # Return updated cart icon with OOB swap
    return render(request, 'partials/cart_icon.html', {
        'cart': cart
    })


def view_cart(request):
    """
    عرض سلة التسوق
    View the shopping cart
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Rendered cart page
    """
    cart = get_cart(request)
    
    context = {
        'cart': cart,
    }
    
    return render(request, 'orders/cart.html', context)
