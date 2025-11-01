from django.db import models
from apps.store.models import Product


class InventoryItem(models.Model):
    """
    إدارة مخزون المنتجات
    Inventory management for products
    """
    
    # Relationship
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='inventory',
        verbose_name='المنتج'
    )
    
    # Stock fields
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='الكمية',
        help_text='كمية المخزون الحالية'
    )
    
    low_stock_threshold = models.PositiveIntegerField(
        default=10,
        verbose_name='حد المخزون المنخفض',
        help_text='الحد الأدنى قبل تنبيه المخزون المنخفض'
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
        verbose_name = 'عنصر مخزون'
        verbose_name_plural = 'عناصر المخزون'
        ordering = ['product__name']
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['quantity']),
        ]
    
    def __str__(self):
        return f"Inventory: {self.product.name} - {self.quantity} units"
    
    def is_low_stock(self):
        """
        Check if inventory is below low stock threshold
        """
        return 0 < self.quantity <= self.low_stock_threshold
    
    def is_out_of_stock(self):
        """
        Check if inventory is out of stock
        """
        return self.quantity == 0
    
    def get_stock_status(self):
        """
        Get readable stock status
        """
        if self.is_out_of_stock():
            return 'نفد المخزون'
        elif self.is_low_stock():
            return 'مخزون منخفض'
        else:
            return 'متوفر'
    
    def add_stock(self, quantity):
        """
        Add stock quantity
        """
        if quantity > 0:
            self.quantity += quantity
            self.save()
            return True
        return False
    
    def remove_stock(self, quantity):
        """
        Remove stock quantity
        """
        if quantity > 0 and self.quantity >= quantity:
            self.quantity -= quantity
            self.save()
            return True
        return False
