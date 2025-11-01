from django.contrib import admin
from apps.orders.models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """
    Inline admin for cart items
    """
    model = CartItem
    extra = 0
    fields = ['product', 'quantity', 'unit_price', 'total_price']
    readonly_fields = ['unit_price', 'total_price']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    إدارة سلة التسوق
    Shopping Cart administration
    """
    list_display = [
        'id',
        'user',
        'session_id',
        'total_items',
        'total',
        'created_at',
    ]
    list_filter = [
        'created_at',
        'updated_at',
    ]
    search_fields = [
        'user__email',
        'session_id',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'total_items',
        'subtotal',
        'total',
    ]
    inlines = [CartItemInline]
    
    fieldsets = (
        ('معلومات السلة', {
            'fields': ('user', 'session_id')
        }),
        ('الإحصائيات', {
            'fields': ('total_items', 'subtotal', 'total')
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ['-updated_at']
    
    def get_queryset(self, request):
        """
        Optimize queryset with select_related
        """
        qs = super().get_queryset(request)
        return qs.select_related('user').prefetch_related('items__product')
