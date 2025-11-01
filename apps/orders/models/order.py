from django.db import models
from django.conf import settings
from apps.store.models import Product
from apps.users.models import Address


class Order(models.Model):
    """
    Represents a customer order
    """
    
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('confirmed', 'مؤكد'),
        ('processing', 'قيد المعالجة'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التوصيل'),
        ('cancelled', 'ملغي'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('paid', 'مدفوع'),
        ('failed', 'فشل'),
        ('refunded', 'مسترد'),
    ]
    
    # Relationships
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='المستخدم'
    )
    
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name='عنوان التوصيل'
    )
    
    # Order details
    order_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='رقم الطلب'
    )
    
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name='السعر الإجمالي'
    )
    
    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=0,
        verbose_name='تكلفة الشحن'
    )
    
    # Status fields
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='حالة الطلب'
    )
    
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name='حالة الدفع'
    )
    
    # Additional information
    notes = models.TextField(
        blank=True,
        verbose_name='ملاحظات الطلب'
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
    
    class Meta:
        verbose_name = 'طلب'
        verbose_name_plural = 'الطلبات'
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
        verbose_name='الطلب'
    )
    
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='المنتج'
    )
    
    # Item details (snapshot at time of order)
    product_name = models.CharField(
        max_length=200,
        verbose_name='اسم المنتج'
    )
    
    product_sku = models.CharField(
        max_length=100,
        verbose_name='رمز المنتج'
    )
    
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='الكمية'
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        verbose_name='سعر الوحدة'
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإضافة'
    )
    
    class Meta:
        verbose_name = 'عنصر الطلب'
        verbose_name_plural = 'عناصر الطلب'
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
