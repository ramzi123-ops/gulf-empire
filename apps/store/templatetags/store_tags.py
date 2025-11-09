from django import template
from django.db.models import Prefetch
from apps.store.models import Brand, CarModel

register = template.Library()


@register.inclusion_tag('partials/brands_navbar.html')
def brands_navbar():
    """
    Template tag to display brands with their car models in navbar
    """
    # Get brands that should show in navbar
    brands_with_models = Brand.objects.filter(
        is_active=True,
        show_in_navbar=True
    ).prefetch_related(
        Prefetch(
            'car_models',
            queryset=CarModel.objects.filter(
                is_active=True,
                show_in_navbar=True
            ).order_by('name', '-year_from')
        )
    ).order_by('name')
    
    return {
        'brands_with_models': brands_with_models
    }


@register.simple_tag
def get_car_models_for_brand(brand):
    """
    Get car models for a specific brand
    """
    return CarModel.objects.filter(
        brand=brand,
        is_active=True
    ).order_by('name', '-year_from')
