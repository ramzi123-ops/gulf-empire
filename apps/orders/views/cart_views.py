from django.shortcuts import render, get_object_or_404
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
        # Return empty response - product not available
        return HttpResponse('')
    
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
        # Return empty response - insufficient stock
        return HttpResponse('')
    
    # Add or update cart item
    if cart_item:
        cart_item.increase_quantity(quantity)
    else:
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity
        )
    
    # Return updated cart icon only
    from django.urls import reverse
    cart_url = reverse('orders:cart')
    response_html = f'''
    <div id="mini-cart" hx-swap-oob="true" class="relative">
        <a href="{cart_url}" class="text-primary hover:text-primary-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
            <span class="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                {cart.total_items}
            </span>
        </a>
    </div>
    '''
    return HttpResponse(response_html)


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
    item_was_deleted = False
    
    if action == 'increase':
        # Check against inventory stock
        if cart_item.quantity < cart_item.product.stock:
            cart_item.increase_quantity(1)
    
    elif action == 'decrease':
        # decrease_quantity will delete the item if quantity reaches 0
        cart_item.decrease_quantity(1)
        # Check if item still exists (not deleted)
        item_was_deleted = not CartItem.objects.filter(id=item_id).exists()
    
    else:  # set quantity
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                cart_item.delete()
                item_was_deleted = True
            elif quantity <= cart_item.product.stock:
                cart_item.quantity = quantity
                cart_item.save()
        except (ValueError, TypeError):
            pass
    
    # Refresh cart to get updated values
    cart.refresh_from_db()
    
    # Build response with cart totals and OOB swaps
    from django.template.loader import render_to_string
    from django.urls import reverse
    
    cart_totals_html = render_to_string('orders/partials/cart_totals.html', {'cart': cart}, request=request)
    
    # If item was deleted, remove the row + update cart totals and mini-cart
    if item_was_deleted:
        # Update mini-cart icon
        cart_url = reverse('orders:cart')
        oob_mini_cart = f'''
        <div id="mini-cart" hx-swap-oob="true" class="relative">
            <a href="{cart_url}" class="text-primary hover:text-primary-600">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path>
                </svg>
                <span class="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                    {cart.total_items}
                </span>
            </a>
        </div>
        '''
        # OOB swap to remove the cart row
        oob_remove_row = f'<div id="cart-item-{item_id}" hx-swap-oob="delete"></div>'
        
        # Add OOB swap to cart totals
        cart_totals_with_oob = cart_totals_html.replace('<div id="cart-totals"', '<div id="cart-totals" hx-swap-oob="true"')
        return HttpResponse(cart_totals_with_oob + oob_mini_cart + oob_remove_row)
    
    # Otherwise, item still exists - update quantity and total
    cart_item.refresh_from_db()
    
    # Add OOB swaps for the updated quantity and total
    oob_quantity = f'<span id="quantity-{cart_item.id}" hx-swap-oob="true" class="w-12 text-center font-medium">{cart_item.quantity}</span>'
    oob_total = f'<span id="total-{cart_item.id}" hx-swap-oob="true" class="text-base font-bold text-primary">{cart_item.total_price} <span class="riyal-icon">&#xE900;</span></span>'
    
    # Update mini-cart icon
    cart_url = reverse('orders:cart')
    oob_mini_cart = f'''
    <div id="mini-cart" hx-swap-oob="true" class="relative">
        <a href="{cart_url}" class="text-primary hover:text-primary-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
            <span class="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                {cart.total_items}
            </span>
        </a>
    </div>
    '''
    
    return HttpResponse(cart_totals_html + oob_quantity + oob_total + oob_mini_cart)


@require_POST
def remove_from_cart(request, item_id):
    """
    حذف منتج من السلة
    Remove a product from the cart
    
    Args:
        request: Django HttpRequest object
        item_id: CartItem ID to remove
        
    Returns:
        Empty response for row removal + OOB swap for cart totals
    """
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    cart_item.delete()
    
    # Refresh cart to get updated values
    cart.refresh_from_db()
    
    # Return empty response for the deleted row + OOB swap for cart totals
    from django.template.loader import render_to_string
    from django.urls import reverse
    
    cart_totals_html = render_to_string('orders/partials/cart_totals.html', {'cart': cart}, request=request)
    
    # Add OOB swap attribute to cart totals
    cart_totals_with_oob = cart_totals_html.replace('<div id="cart-totals"', '<div id="cart-totals" hx-swap-oob="true"')
    
    # Update mini-cart icon
    cart_url = reverse('orders:cart')
    oob_mini_cart = f'''
    <div id="mini-cart" hx-swap-oob="true" class="relative">
        <a href="{cart_url}" class="text-primary hover:text-primary-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
            <span class="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                {cart.total_items}
            </span>
        </a>
    </div>
    '''
    
    return HttpResponse(cart_totals_with_oob + oob_mini_cart)


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
