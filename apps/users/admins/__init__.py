"""
Users App Admin Registration

App Name: users
Model Files: user.py, profile.py, address.py
Admin Files: user_admin.py, profile_admin.py, address_admin.py

All admin classes use @admin.register() decorators and self-register on import.
"""

# Import admin classes (they self-register via @admin.register() decorators)
from .user_admin import UserAdmin
from .profile_admin import ProfileAdmin
from .address_admin import AddressAdmin

__all__ = [
    'UserAdmin',
    'ProfileAdmin',
    'AddressAdmin',
]
