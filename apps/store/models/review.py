from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from .product import Product


class Review(models.Model):
    """
    مراجعة المنتج
    Product Review
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="المنتج"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="المستخدم"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="التقييم",
        help_text="من 1 إلى 5 نجوم"
    )
    comment = models.TextField(
        verbose_name="التعليق"
    )
    is_verified_purchase = models.BooleanField(
        default=False,
        verbose_name="مشتري موثق",
        help_text="هل اشترى المستخدم هذا المنتج؟"
    )
    is_approved = models.BooleanField(
        default=True,
        verbose_name="موافق عليه",
        help_text="يجب الموافقة على المراجعة قبل عرضها"
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
        verbose_name = "مراجعة"
        verbose_name_plural = "المراجعات"
        ordering = ['-created_at']
        unique_together = ['product', 'user']  # One review per user per product
        indexes = [
            models.Index(fields=['product', 'is_approved']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"

    @property
    def stars_filled(self):
        """Return range for filled stars"""
        return range(self.rating)

    @property
    def stars_empty(self):
        """Return range for empty stars"""
        return range(5 - self.rating)
