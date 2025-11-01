from django.db import models
from apps.orders.models import Order


class Payment(models.Model):
    """
    Represents a payment transaction for an order
    """
    
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('processing', 'قيد المعالجة'),
        ('succeeded', 'نجح'),
        ('failed', 'فشل'),
        ('cancelled', 'ملغي'),
        ('refunded', 'مسترد'),
    ]
    
    # Relationships
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='الطلب'
    )
    
    # Stripe information
    stripe_payment_intent_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='معرف نية الدفع Stripe'
    )
    
    stripe_charge_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='معرف الشحنة Stripe'
    )
    
    # Payment details
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name='المبلغ'
    )
    
    currency = models.CharField(
        max_length=3,
        default='KWD',
        verbose_name='العملة'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='حالة الدفع'
    )
    
    # Additional information
    payment_method = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='طريقة الدفع'
    )
    
    error_message = models.TextField(
        blank=True,
        verbose_name='رسالة الخطأ'
    )
    
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='البيانات الوصفية'
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاريخ التحديث'
    )
    
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='تاريخ الدفع'
    )
    
    class Meta:
        verbose_name = 'دفعة'
        verbose_name_plural = 'المدفوعات'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['stripe_payment_intent_id']),
            models.Index(fields=['order', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Payment for Order #{self.order.order_number} - {self.status}"
    
    def is_successful(self):
        """Check if payment was successful"""
        return self.status == 'succeeded'
    
    def can_refund(self):
        """Check if payment can be refunded"""
        return self.status == 'succeeded' and not self.is_refunded()
    
    def is_refunded(self):
        """Check if payment has been refunded"""
        return self.status == 'refunded'
