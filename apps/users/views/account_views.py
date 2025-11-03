from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from apps.users.models import Address, Profile
from apps.orders.models import Order


@login_required
def profile_view(request):
    """
    الملف الشخصي للمستخدم مع سجل الطلبات
    User profile with order history
    """
    # Get or create user profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Handle profile update
    if request.method == 'POST':
        # Update user info
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        
        # Update profile info
        profile.bio = request.POST.get('bio', profile.bio)
        date_of_birth = request.POST.get('date_of_birth')
        if date_of_birth:
            profile.date_of_birth = date_of_birth
        
        profile.newsletter_subscribed = request.POST.get('newsletter_subscribed') == 'on'
        profile.sms_notifications = request.POST.get('sms_notifications') == 'on'
        profile.email_notifications = request.POST.get('email_notifications') == 'on'
        
        # Handle avatar upload
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        messages.success(request, 'تم تحديث الملف الشخصي بنجاح')
        return redirect('users:profile')
    
    # Get user orders with pagination
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(orders, 10)  # 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate order statistics
    total_orders = orders.count()
    completed_orders = orders.filter(status='delivered').count()
    pending_orders = orders.filter(status__in=['pending', 'processing', 'shipped']).count()
    cancelled_orders = orders.filter(status='cancelled').count()
    
    context = {
        'profile': profile,
        'orders': page_obj,
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'cancelled_orders': cancelled_orders,
    }
    
    return render(request, 'users/profile.html', context)


@login_required
def manage_addresses(request):
    """
    إدارة دفتر العناوين
    Manage user addresses
    """
    addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')
    
    context = {
        'addresses': addresses,
    }
    
    return render(request, 'users/address_book.html', context)


@login_required
def add_address(request):
    """
    إضافة عنوان جديد
    Add a new address
    """
    if request.method == 'GET':
        # Return the empty form
        return render(request, 'users/partials/address_form.html', {'action': 'add'})
    
    elif request.method == 'POST':
        # Get form data
        label = request.POST.get('label')
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        street = request.POST.get('street')
        building_number = request.POST.get('building_number', '')
        apartment_number = request.POST.get('apartment_number', '')
        city = request.POST.get('city')
        state = request.POST.get('state', '')
        postal_code = request.POST.get('postal_code', '')
        country = request.POST.get('country', 'السعودية')
        additional_info = request.POST.get('additional_info', '')
        is_default = request.POST.get('is_default') == 'on'
        
        # Validate required fields
        if not all([label, full_name, phone_number, street, city]):
            messages.error(request, 'يرجى ملء جميع الحقول المطلوبة')
            return render(request, 'users/partials/address_form.html', {
                'action': 'add',
                'errors': ['يرجى ملء جميع الحقول المطلوبة']
            })
        
        # Create address
        Address.objects.create(
            user=request.user,
            label=label,
            full_name=full_name,
            phone_number=phone_number,
            street=street,
            building_number=building_number,
            apartment_number=apartment_number,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            additional_info=additional_info,
            is_default=is_default
        )
        
        messages.success(request, 'تمت إضافة العنوان بنجاح')
        
        # If HTMX request, return updated address list and clear form
        if request.htmx:
            addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')
            response = render(request, 'users/partials/address_list.html', {'addresses': addresses})
            # Add header to trigger form container clearing
            response['HX-Trigger'] = 'addressAdded'
            return response
        
        return redirect('users:manage_addresses')


@login_required
def edit_address(request, address_id):
    """
    تعديل عنوان موجود
    Edit an existing address
    """
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == 'GET':
        # Return the form with address data
        return render(request, 'users/partials/address_form.html', {
            'action': 'edit',
            'address': address,
        })
    
    elif request.method == 'POST':
        # Update address
        address.label = request.POST.get('label', address.label)
        address.full_name = request.POST.get('full_name', address.full_name)
        address.phone_number = request.POST.get('phone_number', address.phone_number)
        address.street = request.POST.get('street', address.street)
        address.building_number = request.POST.get('building_number', '')
        address.apartment_number = request.POST.get('apartment_number', '')
        address.city = request.POST.get('city', address.city)
        address.state = request.POST.get('state', '')
        address.postal_code = request.POST.get('postal_code', '')
        address.country = request.POST.get('country', 'السعودية')
        address.additional_info = request.POST.get('additional_info', '')
        address.is_default = request.POST.get('is_default') == 'on'
        
        # Validate required fields
        if not all([address.label, address.full_name, address.phone_number, address.street, address.city]):
            messages.error(request, 'يرجى ملء جميع الحقول المطلوبة')
            return render(request, 'users/partials/address_form.html', {
                'action': 'edit',
                'address': address,
                'errors': ['يرجى ملء جميع الحقول المطلوبة']
            })
        
        address.save()
        messages.success(request, 'تم تحديث العنوان بنجاح')
        
        # If HTMX request, return updated address list and clear form
        if request.htmx:
            addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')
            response = render(request, 'users/partials/address_list.html', {'addresses': addresses})
            response['HX-Trigger'] = 'addressUpdated'
            return response
        
        return redirect('users:manage_addresses')


@login_required
@require_http_methods(["DELETE", "POST"])  # Support both DELETE and POST for compatibility
def delete_address(request, address_id):
    """
    حذف عنوان
    Delete an address
    """
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    
    messages.success(request, 'تم حذف العنوان بنجاح')
    
    # If HTMX request, return updated address list
    if request.htmx:
        addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')
        return render(request, 'users/partials/address_list.html', {'addresses': addresses})
    
    return redirect('users:manage_addresses')
