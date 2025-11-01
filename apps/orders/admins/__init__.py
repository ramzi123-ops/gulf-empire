"""
Orders App Admin Registration

App Name: orders
Model Files: cart.py, order.py
Admin Files: cart_admin.py, order_admin.py

All admin classes use @admin.register() decorators and self-register on import.
"""

# Import admin classes (they self-register via @admin.register() decorators)
from .cart_admin import CartAdmin, CartItemInline
from .order_admin import OrderAdmin, OrderItemInline

__all__ = [
    'CartAdmin',
    'CartItemInline',
    'OrderAdmin',
    'OrderItemInline',
]
