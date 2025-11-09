from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from .taxonomy import Brand


class CarModel(models.Model):
    """
    موديل السيارة (مثل: كامري، التيما، إلنترا)
    Car Model (e.g., Camry, Altima, Elantra)
    """
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='car_models',
        verbose_name="الماركة"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="اسم الموديل"
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name="رابط الموديل (Slug)",
        help_text="يتم إنشاؤه تلقائياً من الماركة والموديل"
    )
    year_from = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year + 5)
        ],
        verbose_name="من سنة"
    )
    year_to = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year + 5)
        ],
        null=True,
        blank=True,
        verbose_name="إلى سنة",
        help_text="اتركه فارغاً إذا كان الموديل لا يزال يُنتج"
    )
    generation = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="الجيل",
        help_text="مثل: الجيل الثالث، الجيل الرابع"
    )
    body_type = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="نوع الهيكل",
        help_text="مثل: سيدان، هاتشباك، SUV"
    )
    engine_types = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="أنواع المحركات",
        help_text="مثل: 1.6L, 2.0L, 2.4L"
    )
    image = models.ImageField(
        upload_to='car_models/',
        null=True,
        blank=True,
        verbose_name="صورة الموديل"
    )
    description = models.TextField(
        blank=True,
        verbose_name="الوصف"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط"
    )
    show_in_navbar = models.BooleanField(
        default=False,
        verbose_name="إظهار في شريط التنقل",
        help_text="حدد هذا الخيار لإظهار الموديل في شريط التنقل العلوي"
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
        verbose_name = "موديل السيارة"
        verbose_name_plural = "موديلات السيارات"
        ordering = ['brand__name', 'name', '-year_from']
        unique_together = ['brand', 'name', 'year_from']
        indexes = [
            models.Index(fields=['brand', 'is_active']),
            models.Index(fields=['year_from', 'year_to']),
        ]

    def __str__(self):
        year_range = f"{self.year_from}"
        if self.year_to:
            year_range += f"-{self.year_to}"
        else:
            year_range += "+"
        return f"{self.brand.name} {self.name} ({year_range})"

    def save(self, *args, **kwargs):
        if not self.slug:
            year_range = f"{self.year_from}"
            if self.year_to:
                year_range += f"-{self.year_to}"
            slug_text = f"{self.brand.name}-{self.name}-{year_range}"
            self.slug = slugify(slug_text, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        """Get full car model name with brand"""
        return f"{self.brand.name} {self.name}"

    @property
    def year_range_display(self):
        """Get formatted year range for display"""
        if self.year_to:
            return f"{self.year_from} - {self.year_to}"
        return f"{self.year_from} - الآن"

    def is_current_model(self):
        """Check if this model is still in production"""
        return self.year_to is None or self.year_to >= datetime.now().year


