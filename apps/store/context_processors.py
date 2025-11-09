"""
Context processors for the store app
"""
from apps.store.models.taxonomy import Category


def menu_categories(request):
    """
    Make menu categories available in all templates
    """
    categories = Category.objects.filter(
        is_active=True,
        show_in_menu=True
    ).order_by('menu_order', 'name').prefetch_related('children')
    
    return {
        'menu_categories': categories
    }
