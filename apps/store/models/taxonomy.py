from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    فئة المنتجات (مثل: زيوت، فلاتر، بطاريات)
    Product Category (e.g., oils, filters, batteries)
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="اسم الفئة"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="رابط الفئة (Slug)",
        help_text="يتم إنشاؤه تلقائياً من الاسم"
    )
    description = models.TextField(
        blank=True,
        verbose_name="الوصف"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="الفئة الأب"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط"
    )
    show_in_menu = models.BooleanField(
        default=False,
        verbose_name="إظهار في القائمة الرئيسية",
        help_text="حدد هذا الخيار لإظهار الفئة في القائمة الرئيسية (Mega Menu)"
    )
    menu_order = models.IntegerField(
        default=0,
        verbose_name="ترتيب القائمة",
        help_text="ترتيب عرض الفئة في القائمة الرئيسية (الأصغر أولاً)"
    )
    icon = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="رمز الأيقونة",
        help_text="اسم أيقونة SVG أو Emoji (اختياري)"
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
        verbose_name = "فئة"
        verbose_name_plural = "الفئات"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Brand(models.Model):
    """
    العلامة التجارية للمنتجات (مثل: تويوتا، نيسان، هيونداي)
    Product Brand (e.g., Toyota, Nissan, Hyundai)
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="اسم العلامة التجارية"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="رابط العلامة التجارية (Slug)",
        help_text="يتم إنشاؤه تلقائياً من الاسم"
    )
    logo = models.ImageField(
        upload_to='brands/',
        null=True,
        blank=True,
        verbose_name="الشعار"
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
        help_text="حدد هذا الخيار لإظهار العلامة التجارية في شريط التنقل العلوي"
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
        verbose_name = "علامة تجارية"
        verbose_name_plural = "العلامات التجارية"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
