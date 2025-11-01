from django.contrib import admin
from apps.store.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    إدارة المراجعات
    Review administration
    """
    list_display = [
        'product',
        'user',
        'rating',
        'is_verified_purchase',
        'is_approved',
        'created_at',
    ]
    list_filter = [
        'rating',
        'is_verified_purchase',
        'is_approved',
        'created_at',
    ]
    search_fields = [
        'product__name',
        'user__username',
        'comment',
    ]
    list_editable = [
        'is_approved',
        'is_verified_purchase',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    fieldsets = (
        ('معلومات المراجعة', {
            'fields': ('product', 'user', 'rating', 'comment')
        }),
        ('الحالة', {
            'fields': ('is_approved', 'is_verified_purchase')
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        """
        Optimize queryset with select_related
        """
        qs = super().get_queryset(request)
        return qs.select_related('product', 'user')
