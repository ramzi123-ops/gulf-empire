"""
Views for static pages (About, Contact, Gallery)
"""
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def about_view(request):
    """
    عرض صفحة من نحن
    Display About Us page
    """
    context = {
        'page_title': 'من نحن',
    }
    return render(request, 'store/about.html', context)


@require_http_methods(["GET", "POST"])
def contact_view(request):
    """
    عرض صفحة اتصل بنا
    Display Contact Us page
    """
    if request.method == 'POST':
        # Handle contact form submission
        # TODO: Implement contact form handling
        pass
    
    context = {
        'page_title': 'اتصل بنا',
    }
    return render(request, 'store/contact.html', context)


@require_http_methods(["GET"])
def gallery_view(request):
    """
    عرض صفحة معرض الصور
    Display Gallery page
    """
    context = {
        'page_title': 'معرض الصور',
    }
    return render(request, 'store/gallery.html', context)
