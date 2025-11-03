from django.contrib import admin
from apps.store.models import Advertisement, Gallery


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    """
    إدارة الإعلانات
    Advertisement administration
    """
    list_display = [
        'title',
        'placement',
        'display_order',
        'is_active',
        'start_date',
        'end_date',
        'view_count',
        'click_count',
        'created_at',
    ]
    list_filter = [
        'is_active',
        'placement',
        'created_at',
        'start_date',
        'end_date',
    ]
    search_fields = [
        'title',
        'subtitle',
        'description',
    ]
    list_editable = [
        'is_active',
        'display_order',
    ]
    readonly_fields = [
        'view_count',
        'click_count',
        'created_at',
        'updated_at',
    ]
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': (
                'title',
                'subtitle',
                'description',
            )
        }),
        ('الصور', {
            'fields': (
                'image',
                'mobile_image',
            )
        }),
        ('إعدادات الرابط', {
            'fields': (
                'link_url',
                'link_text',
                'open_in_new_tab',
            )
        }),
        ('إعدادات العرض', {
            'fields': (
                'placement',
                'display_order',
                'is_active',
            )
        }),
        ('فترة العرض', {
            'fields': (
                'start_date',
                'end_date',
            ),
            'classes': ('collapse',),
        }),
        ('الإحصائيات', {
            'fields': (
                'view_count',
                'click_count',
            ),
            'classes': ('collapse',),
        }),
        ('التواريخ', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )
    ordering = ['placement', 'display_order', '-created_at']

    def get_queryset(self, request):
        """
        Add custom annotations if needed
        """
        qs = super().get_queryset(request)
        return qs


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """
    إدارة معرض الصور
    Gallery administration
    """
    list_display = [
        'title',
        'category',
        'is_featured',
        'is_active',
        'display_order',
        'created_at',
    ]
    list_filter = [
        'is_active',
        'is_featured',
        'category',
        'created_at',
    ]
    search_fields = [
        'title',
        'description',
        'tags',
    ]
    list_editable = [
        'is_featured',
        'is_active',
        'display_order',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': (
                'title',
                'description',
            )
        }),
        ('الصور', {
            'fields': (
                'image',
                'thumbnail',
            )
        }),
        ('التصنيف', {
            'fields': (
                'category',
                'tags',
            )
        }),
        ('إعدادات العرض', {
            'fields': (
                'display_order',
                'is_featured',
                'is_active',
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
    ordering = ['display_order', '-created_at']

    def get_queryset(self, request):
        """
        Optimize queryset if needed
        """
        qs = super().get_queryset(request)
        return qs
