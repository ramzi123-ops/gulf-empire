from django.db import models
from django.utils.translation import gettext_lazy as _
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
        verbose_name=_('Product')
    )
    
    # Stock fields
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Quantity'),
        help_text=_('Current stock quantity')
    )
    
    low_stock_threshold = models.PositiveIntegerField(
        default=10,
        verbose_name=_('Low Stock Threshold'),
        help_text=_('Minimum quantity before low stock alert')
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
        verbose_name = _('Inventory Item')
        verbose_name_plural = _('Inventory Items')
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
            return _('Out of Stock')
        elif self.is_low_stock():
            return _('Low Stock')
        else:
            return _('In Stock')
    
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
