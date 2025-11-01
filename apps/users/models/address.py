from django.db import models
from django.conf import settings


class Address(models.Model):
    """
    عنوان المستخدم
    User Address model
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name="المستخدم"
    )
    label = models.CharField(
        max_length=100,
        verbose_name="تسمية العنوان",
        help_text="مثال: المنزل، العمل، الشركة"
    )
    full_name = models.CharField(
        max_length=200,
        verbose_name="الاسم الكامل",
        help_text="اسم المستلم"
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name="رقم الهاتف"
    )
    street = models.CharField(
        max_length=500,
        verbose_name="الشارع والعنوان التفصيلي"
    )
    building_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="رقم المبنى"
    )
    apartment_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="رقم الشقة"
    )
    city = models.CharField(
        max_length=100,
        verbose_name="المدينة"
    )
    state = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="المحافظة/الولاية"
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="الرمز البريدي"
    )
    country = models.CharField(
        max_length=100,
        default="السعودية",
        verbose_name="الدولة"
    )
    additional_info = models.TextField(
        blank=True,
        verbose_name="معلومات إضافية",
        help_text="إرشادات التوصيل أو علامات مميزة"
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name="العنوان الافتراضي"
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
        verbose_name = "عنوان"
        verbose_name_plural = "العناوين"
        ordering = ['-is_default', '-created_at']
        indexes = [
            models.Index(fields=['user', 'is_default']),
        ]

    def __str__(self):
        return f"{self.label} - {self.user.username}"

    def save(self, *args, **kwargs):
        """
        If this address is set as default, unset all other default addresses for this user
        """
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    @property
    def full_address(self):
        """Return formatted full address"""
        parts = [
            self.street,
            f"مبنى {self.building_number}" if self.building_number else None,
            f"شقة {self.apartment_number}" if self.apartment_number else None,
            self.city,
            self.state,
            self.postal_code,
            self.country,
        ]
        return ", ".join(filter(None, parts))
