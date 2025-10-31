from django.contrib import admin
from apps.users.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """
    إدارة العناوين
    Address administration
    """
    list_display = [
        'label',
        'user',
        'city',
        'country',
        'is_default',
        'created_at',
    ]
    list_filter = [
        'is_default',
        'country',
        'city',
        'created_at',
    ]
    search_fields = [
        'user__username',
        'user__email',
        'label',
        'full_name',
        'phone_number',
        'street',
        'city',
    ]
    list_editable = [
        'is_default',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    fieldsets = (
        ('المستخدم', {
            'fields': ('user',)
        }),
        ('معلومات العنوان', {
            'fields': (
                'label',
                'full_name',
                'phone_number',
            )
        }),
        ('العنوان التفصيلي', {
            'fields': (
                'street',
                'building_number',
                'apartment_number',
                'city',
                'state',
                'postal_code',
                'country',
                'additional_info',
            )
        }),
        ('الإعدادات', {
            'fields': ('is_default',)
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    ordering = ['-is_default', '-created_at']

    def get_queryset(self, request):
        """
        Optimize queryset with select_related
        """
        qs = super().get_queryset(request)
        return qs.select_related('user')
