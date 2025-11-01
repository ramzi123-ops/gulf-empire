from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    إدارة المستخدمين
    Custom User administration
    """
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'is_staff',
        'is_active',
        'date_joined',
    ]
    list_filter = [
        'is_staff',
        'is_superuser',
        'is_active',
        'date_joined',
    ]
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number',
    ]
    ordering = ['-date_joined']
    
    # Extend the default fieldsets to include phone_number
    fieldsets = BaseUserAdmin.fieldsets + (
        ('معلومات إضافية', {
            'fields': ('phone_number',)
        }),
    )
    
    # For adding new users
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('معلومات إضافية', {
            'fields': ('phone_number',)
        }),
    )
