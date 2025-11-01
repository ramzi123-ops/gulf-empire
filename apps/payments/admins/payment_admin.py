from django.contrib import admin
from apps.payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    إدارة المدفوعات
    Payment administration
    """
    list_display = [
        'id',
        'order',
        'amount',
        'currency',
        'payment_method',
        'status',
        'created_at',
    ]
    list_filter = [
        'payment_method',
        'status',
        'currency',
        'created_at',
    ]
    search_fields = [
        'stripe_payment_intent_id',
        'stripe_charge_id',
        'order__order_number',
        'order__user__email',
    ]
    readonly_fields = [
        'stripe_payment_intent_id',
        'stripe_charge_id',
        'created_at',
        'updated_at',
        'paid_at',
    ]
    
    fieldsets = (
        ('معلومات الدفع', {
            'fields': ('order', 'stripe_payment_intent_id', 'stripe_charge_id')
        }),
        ('تفاصيل الدفع', {
            'fields': ('amount', 'currency', 'payment_method', 'status')
        }),
        ('معلومات إضافية', {
            'fields': ('error_message', 'metadata'),
            'classes': ('collapse',),
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at', 'paid_at'),
            'classes': ('collapse',),
        }),
    )
    
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        """
        Optimize queryset with select_related
        """
        qs = super().get_queryset(request)
        return qs.select_related('order', 'order__user')
