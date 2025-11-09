from django.contrib import admin
from apps.store.models import Product, ProductSpecification
from apps.inventory.models import InventoryItem


class ProductSpecificationInline(admin.TabularInline):
    """
    Inline admin for product specifications
    """
    model = ProductSpecification
    extra = 1
    fields = ['name', 'value', 'order']
    ordering = ['order', 'name']


class InventoryItemInline(admin.StackedInline):
    """
    Inline admin for inventory management
    """
    model = InventoryItem
    extra = 1  # Changed from 0 to 1 to show form for new products
    max_num = 1
    min_num = 1  # Require at least one inventory item
    can_delete = False
    fields = ['quantity', 'low_stock_threshold', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    verbose_name = 'إدارة المخزون'
    verbose_name_plural = 'إدارة المخزون'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    إدارة المنتجات
    Product administration
    """
    list_display = [
        'name',
        'sku',
        'category',
        'brand',
        'price',
        'sale_price',
        'is_active',
        'is_featured',
        'is_new_arrival',
        'is_coming_soon',
        'created_at',
    ]
    list_filter = [
        'is_active',
        'is_featured',
        'is_new_arrival',
        'is_coming_soon',
        'category',
        'brand',
        'created_at',
    ]
    search_fields = [
        'name',
        'sku',
        'description',
        'compatible_makes',
        'compatible_models',
    ]
    prepopulated_fields = {
        'slug': ('name',)
    }
    list_editable = [
        'is_active',
        'is_featured',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    inlines = [
        ProductSpecificationInline,
        InventoryItemInline,
    ]
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': (
                'name',
                'slug',
                'sku',
                'description',
                'short_description',
            )
        }),
        ('التصنيف', {
            'fields': (
                'category',
                'brand',
            )
        }),
        ('التسعير', {
            'fields': (
                'price',
                'sale_price',
                'cost_price',
            )
        }),
        ('تفاصيل المنتج', {
            'fields': (
                'weight',
                'dimensions',
            )
        }),
        ('الصور', {
            'fields': (
                'main_image',
                'image_2',
                'image_3',
                'image_4',
            )
        }),
        ('التوافق مع المركبات', {
            'fields': (
                'compatible_brands',
                'compatible_car_models',
                'year_from',
                'year_to',
            ),
            'classes': ('collapse',),
        }),
        ('تحسين محركات البحث (SEO)', {
            'fields': (
                'meta_title',
                'meta_description',
            ),
            'classes': ('collapse',),
        }),
        ('الحالة', {
            'fields': (
                'is_active',
                'is_featured',
                'is_new_arrival',
                'is_coming_soon',
            )
        }),
        ('التواريخ', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )
    ordering = ['-created_at']

    def get_queryset(self, request):
        """
        Optimize queryset with select_related
        """
        qs = super().get_queryset(request)
        return qs.select_related('category', 'brand')
