from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Advertisement(models.Model):
    """
    الإعلانات (البانرات)
    Advertisement/Banner model for homepage sliders and promotional banners
    """
    PLACEMENT_CHOICES = [
        ('hero', 'البانر الرئيسي (Hero)'),
        ('sidebar', 'الشريط الجانبي'),
        ('middle', 'منتصف الصفحة'),
        ('footer', 'أسفل الصفحة'),
        ('popup', 'نافذة منبثقة'),
    ]
    
    title = models.CharField(
        max_length=200,
        verbose_name="العنوان"
    )
    subtitle = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="العنوان الفرعي"
    )
    description = models.TextField(
        blank=True,
        verbose_name="الوصف"
    )
    image = models.ImageField(
        upload_to='advertisements/',
        verbose_name="الصورة",
        help_text="يُفضل استخدام صور بحجم 1920x600 للبانر الرئيسي"
    )
    mobile_image = models.ImageField(
        upload_to='advertisements/',
        blank=True,
        null=True,
        verbose_name="صورة الموبايل",
        help_text="صورة مخصصة للأجهزة المحمولة (اختياري)"
    )
    
    # Link settings
    link_url = models.URLField(
        blank=True,
        verbose_name="رابط الإعلان",
        help_text="الرابط عند الضغط على الإعلان"
    )
    link_text = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="نص الزر",
        default="تسوق الآن"
    )
    open_in_new_tab = models.BooleanField(
        default=False,
        verbose_name="فتح في تبويب جديد"
    )
    
    # Display settings
    placement = models.CharField(
        max_length=20,
        choices=PLACEMENT_CHOICES,
        default='hero',
        verbose_name="موقع العرض"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتيب العرض",
        help_text="الترتيب في حالة وجود أكثر من إعلان (الأقل يظهر أولاً)"
    )
    
    # Date range
    start_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="تاريخ البدء",
        help_text="تاريخ بدء عرض الإعلان (اختياري)"
    )
    end_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="تاريخ الانتهاء",
        help_text="تاريخ انتهاء عرض الإعلان (اختياري)"
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط"
    )
    
    # Analytics
    click_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="عدد النقرات"
    )
    view_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="عدد المشاهدات"
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
        verbose_name = "إعلان"
        verbose_name_plural = "الإعلانات"
        ordering = ['placement', 'display_order', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_placement_display()})"
    
    def increment_view(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    def increment_click(self):
        """Increment click count"""
        self.click_count += 1
        self.save(update_fields=['click_count'])


class Gallery(models.Model):
    """
    معرض الصور
    Gallery model for showcasing images (projects, workshops, events, etc.)
    """
    CATEGORY_CHOICES = [
        ('workshop', 'ورشة العمل'),
        ('products', 'المنتجات'),
        ('events', 'الفعاليات'),
        ('customers', 'العملاء'),
        ('team', 'الفريق'),
        ('other', 'أخرى'),
    ]
    
    title = models.CharField(
        max_length=200,
        verbose_name="العنوان"
    )
    description = models.TextField(
        blank=True,
        verbose_name="الوصف"
    )
    image = models.ImageField(
        upload_to='gallery/',
        verbose_name="الصورة"
    )
    thumbnail = models.ImageField(
        upload_to='gallery/thumbnails/',
        blank=True,
        null=True,
        verbose_name="الصورة المصغرة",
        help_text="سيتم إنشاؤها تلقائياً إذا تُركت فارغة"
    )
    
    # Categorization
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name="الفئة"
    )
    tags = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="الوسوم",
        help_text="افصل بين الوسوم بفاصلة (مثال: سيارات، قطع غيار، تويوتا)"
    )
    
    # Display settings
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتيب العرض"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="مميز",
        help_text="عرض في الصفحة الرئيسية"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط"
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
        verbose_name = "صورة معرض"
        verbose_name_plural = "معرض الصور"
        ordering = ['display_order', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
