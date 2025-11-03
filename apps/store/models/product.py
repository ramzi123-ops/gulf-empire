from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from decimal import Decimal
from .taxonomy import Category, Brand


class Product(models.Model):
    """
    المنتج الرئيسي (قطع غيار السيارات)
    Main Product model (automotive parts)
    """
    # Basic Information
    name = models.CharField(
        max_length=300,
        verbose_name="اسم المنتج"
    )
    slug = models.SlugField(
        max_length=300,
        unique=True,
        verbose_name="الاسم اللطيف",
        help_text="يتم إنشاؤه تلقائياً من الاسم"
    )
    sku = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="رمز المنتج (SKU)"
    )
    description = models.TextField(
        verbose_name="الوصف"
    )
    short_description = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="وصف مختصر"
    )

    # Taxonomy
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name="الفئة"
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name="العلامة التجارية"
    )

    # Pricing
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="السعر"
    )
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="سعر التخفيض"
    )
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="سعر التكلفة",
        help_text="للاستخدام الداخلي فقط"
    )

    # Inventory
    stock_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="الكمية المتوفرة"
    )
    low_stock_threshold = models.PositiveIntegerField(
        default=5,
        verbose_name="حد المخزون المنخفض"
    )

    # Product Details
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="الوزن (كجم)"
    )
    dimensions = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="الأبعاد",
        help_text="مثال: 10x5x3 سم"
    )

    # Images
    main_image = models.ImageField(
        upload_to='products/',
        verbose_name="الصورة الرئيسية"
    )
    image_2 = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True,
        verbose_name="الصورة الثانية"
    )
    image_3 = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True,
        verbose_name="الصورة الثالثة"
    )
    image_4 = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True,
        verbose_name="الصورة الرابعة"
    )

    # Vehicle Compatibility (for automotive parts)
    compatible_makes = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="الماركات المتوافقة",
        help_text="مثال: تويوتا، نيسان، هيونداي"
    )
    compatible_models = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="الموديلات المتوافقة",
        help_text="مثال: كامري 2015-2020، التيما 2018-2022"
    )
    year_from = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="من سنة"
    )
    year_to = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="إلى سنة"
    )

    # SEO
    meta_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="عنوان الميتا"
    )
    meta_description = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="وصف الميتا"
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="مميز"
    )
    is_new_arrival = models.BooleanField(
        default=False,
        verbose_name="وصل حديثاً"
    )
    is_coming_soon = models.BooleanField(
        default=False,
        verbose_name="قريباً",
        help_text="المنتجات القادمة قريباً"
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاريخ التحديث"
    )

    class Meta:
        verbose_name = "منتج"
        verbose_name_plural = "المنتجات"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['sku']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['brand', 'is_active']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def stock(self):
        """
        Get inventory quantity from InventoryItem
        Falls back to stock_quantity if no inventory item exists
        """
        try:
            return self.inventory.quantity
        except:
            return 0
    
    @property
    def has_stock(self):
        """
        Check if product has stock available
        """
        return self.stock > 0
    
    @property
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock_quantity > 0

    @property
    def is_low_stock(self):
        """Check if product is low in stock"""
        return 0 < self.stock_quantity <= self.low_stock_threshold

    @property
    def final_price(self):
        """Return the sale price if available, otherwise regular price"""
        return self.sale_price if self.sale_price else self.price

    @property
    def discount_percentage(self):
        """Calculate discount percentage if sale price is set"""
        if self.sale_price and self.price > self.sale_price:
            return int(((self.price - self.sale_price) / self.price) * 100)
        return 0


class ProductSpecification(models.Model):
    """
    مواصفات المنتج (مثل: قوة المحرك، الضمان، المنشأ)
    Product Specification (e.g., engine power, warranty, origin)
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='specifications',
        verbose_name="المنتج"
    )
    name = models.CharField(
        max_length=200,
        verbose_name="اسم المواصفة"
    )
    value = models.CharField(
        max_length=500,
        verbose_name="القيمة"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="الترتيب"
    )

    class Meta:
        verbose_name = "مواصفة المنتج"
        verbose_name_plural = "مواصفات المنتجات"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"
