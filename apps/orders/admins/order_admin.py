from django.contrib import admin
from apps.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Inline admin for order items
    """
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_sku', 'price', 'quantity', 'get_total_price']
    fields = ['product', 'product_name', 'product_sku', 'quantity', 'price', 'get_total_price']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    إدارة الطلبات
    Order administration
    """
    list_display = [
        'order_number',
        'user',
        'total_price',
        'status',
        'payment_status',
        'created_at',
    ]
    list_filter = [
        'status',
        'payment_status',
        'created_at',
    ]
    search_fields = [
        'order_number',
        'user__email',
        'user__first_name',
        'user__last_name',
    ]
    readonly_fields = [
        'order_number',
        'created_at',
        'updated_at',
        'get_subtotal',
        'get_total_items',
    ]
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('معلومات الطلب', {
            'fields': ('order_number', 'user', 'address')
        }),
        ('التسعير', {
            'fields': ('total_price', 'shipping_cost', 'get_subtotal')
        }),
        ('الحالة', {
            'fields': ('status', 'payment_status')
        }),
        ('ملاحظات', {
            'fields': ('notes',),
            'classes': ('collapse',),
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
        return qs.select_related('user', 'address')
