from django.db import models
from django.conf import settings
from apps.store.models import Product


class Cart(models.Model):
    """
    سلة التسوق
    Shopping Cart
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='carts',
        verbose_name="المستخدم"
    )
    session_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="معرف الجلسة",
        help_text="للمستخدمين غير المسجلين"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاريخ التحديث"
    )

    class Meta:
        verbose_name = "سلة تسوق"
        verbose_name_plural = "سلال التسوق"
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['session_id']),
        ]

    def __str__(self):
        if self.user:
            return f"سلة {self.user.username}"
        return f"سلة ضيف ({self.session_id[:10]}...)"

    @property
    def total_items(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        """Calculate cart subtotal"""
        return sum(item.total_price for item in self.items.all())

    @property
    def total(self):
        """Calculate cart total (can include shipping, taxes, etc.)"""
        # For now, just return subtotal
        # In future, add shipping and tax calculations
        return self.subtotal

    def clear(self):
        """Remove all items from cart"""
        self.items.all().delete()


class CartItem(models.Model):
    """
    عنصر في سلة التسوق
    Cart Item
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="السلة"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="المنتج"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="الكمية"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإضافة"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاريخ التحديث"
    )

    class Meta:
        verbose_name = "عنصر في السلة"
        verbose_name_plural = "عناصر السلة"
        unique_together = ['cart', 'product']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def unit_price(self):
        """Get the unit price (sale price if available, otherwise regular price)"""
        return self.product.final_price

    @property
    def total_price(self):
        """Calculate total price for this cart item"""
        return self.unit_price * self.quantity

    def increase_quantity(self, amount=1):
        """Increase quantity by specified amount"""
        self.quantity += amount
        self.save()

    def decrease_quantity(self, amount=1):
        """Decrease quantity by specified amount"""
        if self.quantity > amount:
            self.quantity -= amount
            self.save()
        else:
            self.delete()
