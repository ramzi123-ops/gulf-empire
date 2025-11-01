"""
Payments App Admin Registration

App Name: payments
Model Files: payment.py
Admin Files: payment_admin.py

All admin classes use @admin.register() decorators and self-register on import.
"""

# Import admin classes (they self-register via @admin.register() decorators)
from .payment_admin import PaymentAdmin

__all__ = [
    'PaymentAdmin',
]
