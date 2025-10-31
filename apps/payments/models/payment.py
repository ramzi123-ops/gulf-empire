from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.orders.models import Order


class Payment(models.Model):
    """
    Represents a payment transaction for an order
    """
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('succeeded', _('Succeeded')),
        ('failed', _('Failed')),
        ('cancelled', _('Cancelled')),
        ('refunded', _('Refunded')),
    ]
    
    # Relationships
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name=_('Order')
    )
    
    # Stripe information
    stripe_payment_intent_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_('Stripe Payment Intent ID')
    )
    
    stripe_charge_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Stripe Charge ID')
    )
    
    # Payment details
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name=_('Amount')
    )
    
    currency = models.CharField(
        max_length=3,
        default='KWD',
        verbose_name=_('Currency')
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Payment Status')
    )
    
    # Additional information
    payment_method = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Payment Method')
    )
    
    error_message = models.TextField(
        blank=True,
        verbose_name=_('Error Message')
    )
    
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('Metadata')
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )
    
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Paid At')
    )
    
    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
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
