from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.store.models import Product
from apps.users.models import Address


class Order(models.Model):
    """
    Represents a customer order
    """
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('processing', _('Processing')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('paid', _('Paid')),
        ('failed', _('Failed')),
        ('refunded', _('Refunded')),
    ]
    
    # Relationships
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('User')
    )
    
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('Delivery Address')
    )
    
    # Order details
    order_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Order Number')
    )
    
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name=_('Total Price')
    )
    
    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=0,
        verbose_name=_('Shipping Cost')
    )
    
    # Status fields
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Order Status')
    )
    
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name=_('Payment Status')
    )
    
    # Additional information
    notes = models.TextField(
        blank=True,
        verbose_name=_('Order Notes')
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
    
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['order_number']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Order #{self.order_number}"
    
    def save(self, *args, **kwargs):
        """Generate order number if not set"""
        if not self.order_number:
            import uuid
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            unique_id = str(uuid.uuid4())[:8].upper()
            self.order_number = f"ORD-{timestamp}-{unique_id}"
        super().save(*args, **kwargs)
    
    def get_subtotal(self):
        """Calculate subtotal (without shipping)"""
        return sum(item.get_total_price() for item in self.items.all())
    
    def get_total_items(self):
        """Get total number of items in order"""
        return sum(item.quantity for item in self.items.all())
    
    def can_cancel(self):
        """Check if order can be cancelled"""
        return self.status in ['pending', 'confirmed']
    
    def cancel(self):
        """Cancel the order"""
        if self.can_cancel():
            self.status = 'cancelled'
            self.save()
            return True
        return False


class OrderItem(models.Model):
    """
    Represents a single item in an order
    """
    
    # Relationships
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Order')
    )
    
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name=_('Product')
    )
    
    # Item details (snapshot at time of order)
    product_name = models.CharField(
        max_length=200,
        verbose_name=_('Product Name')
    )
    
    product_sku = models.CharField(
        max_length=100,
        verbose_name=_('Product SKU')
    )
    
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_('Quantity')
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name=_('Unit Price')
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    
    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
        ordering = ['id']
        indexes = [
            models.Index(fields=['order', 'product']),
        ]
    
    def __str__(self):
        return f"{self.quantity}x {self.product_name} (Order #{self.order.order_number})"
    
    def get_total_price(self):
        """Calculate total price for this item"""
        return self.quantity * self.price
    
    def save(self, *args, **kwargs):
        """Capture product details at time of order"""
        if not self.product_name:
            self.product_name = self.product.name
        if not self.product_sku:
            self.product_sku = self.product.sku
        if not self.price:
            self.price = self.product.get_price()
        super().save(*args, **kwargs)
