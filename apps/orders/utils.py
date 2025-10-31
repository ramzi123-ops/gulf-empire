from apps.orders.models import Cart


def get_cart(request):
    """
    الحصول على سلة التسوق أو إنشاؤها
    Get or create shopping cart for authenticated users or guest users
    
    For authenticated users: Uses request.user
    For guest users: Uses request.session
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Cart: The user's cart or a newly created cart
    """
    if request.user.is_authenticated:
        # Get or create cart for authenticated user
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            session_id=None  # Authenticated users don't need session_id
        )
        
        # If user just logged in and had a guest cart, merge it
        if created:
            session_key = request.session.session_key
            if session_key:
                # Look for existing guest cart with this session
                try:
                    guest_cart = Cart.objects.get(
                        user=None,
                        session_id=session_key
                    )
                    # Merge guest cart items into user cart
                    for guest_item in guest_cart.items.all():
                        # Check if product already exists in user cart
                        existing_item = cart.items.filter(product=guest_item.product).first()
                        if existing_item:
                            # Increase quantity if product already in cart
                            existing_item.quantity += guest_item.quantity
                            existing_item.save()
                        else:
                            # Move item to user cart
                            guest_item.cart = cart
                            guest_item.save()
                    
                    # Delete the guest cart
                    guest_cart.delete()
                except Cart.DoesNotExist:
                    pass
        
        return cart
    
    else:
        # Get or create cart for guest user using session
        if not request.session.session_key:
            # Create session if it doesn't exist
            request.session.create()
        
        session_key = request.session.session_key
        
        cart, created = Cart.objects.get_or_create(
            user=None,
            session_id=session_key
        )
        
        return cart


def get_cart_item_count(request):
    """
    الحصول على عدد العناصر في السلة
    Get total number of items in the cart
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        int: Total number of items in cart
    """
    cart = get_cart(request)
    return cart.total_items


def clear_cart(request):
    """
    تفريغ سلة التسوق
    Clear all items from the cart
    
    Args:
        request: Django HttpRequest object
    """
    cart = get_cart(request)
    cart.clear()
