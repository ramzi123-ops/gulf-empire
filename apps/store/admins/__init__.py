"""
Store App Admin Registration

This file is the entry point for Django's admin autodiscovery.
All admin classes are imported here to ensure they are registered.

Note: Admin classes use @admin.register() decorators in their respective files,
so registration happens automatically when they are imported.
"""

# Import admin classes (they self-register via @admin.register() decorators)
from .taxonomy_admin import CategoryAdmin, BrandAdmin
from .product_admin import ProductAdmin, ProductSpecificationInline
from .review_admin import ReviewAdmin

# Explicitly export all admin classes
__all__ = [
    'CategoryAdmin',
    'BrandAdmin',
    'ProductAdmin',
    'ProductSpecificationInline',
    'ReviewAdmin',
]
