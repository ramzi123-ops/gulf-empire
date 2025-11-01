from django.contrib import admin
from apps.inventory.models import InventoryItem


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    """
    إدارة المخزون
    Inventory Item administration
    """
    list_display = [
        'product',
        'quantity',
        'low_stock_threshold',
        'get_stock_status',
        'updated_at',
    ]
    list_filter = [
        'updated_at',
        'created_at',
    ]
    search_fields = [
        'product__name',
        'product__sku',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'get_stock_status',
    ]
    
    fieldsets = (
        ('معلومات المنتج', {
            'fields': ('product',)
        }),
        ('المخزون', {
            'fields': ('quantity', 'low_stock_threshold', 'get_stock_status')
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ['product__name']
    
    def get_queryset(self, request):
        """
        Optimize queryset with select_related
        """
        qs = super().get_queryset(request)
        return qs.select_related('product')
    
    def get_stock_status(self, obj):
        """Display stock status with color"""
        status = obj.get_stock_status()
        if obj.is_out_of_stock():
            color = 'red'
        elif obj.is_low_stock():
            color = 'orange'
        else:
            color = 'green'
        return f'<span style="color: {color}; font-weight: bold;">{status}</span>'
    
    get_stock_status.short_description = 'حالة المخزون'
    get_stock_status.allow_tags = True
