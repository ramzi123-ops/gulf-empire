from django.contrib import admin
from apps.store.models import Category, Brand


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    إدارة الفئات
    Category administration
    """
    list_display = [
        'name',
        'parent',
        'is_active',
        'show_in_menu',
        'menu_order',
        'created_at',
    ]
    list_filter = [
        'is_active',
        'show_in_menu',
        'created_at',
    ]
    search_fields = [
        'name',
        'description',
    ]
    prepopulated_fields = {
        'slug': ('name',)
    }
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('name', 'slug', 'description', 'parent')
        }),
        ('إعدادات القائمة الرئيسية', {
            'fields': ('show_in_menu', 'menu_order', 'icon'),
            'description': 'تحكم في عرض الفئة في القائمة الرئيسية (Mega Menu)'
        }),
        ('الحالة', {
            'fields': ('is_active',)
        }),
    )
    ordering = ['menu_order', 'name']
    list_editable = ['show_in_menu', 'menu_order']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """
    إدارة العلامات التجارية
    Brand administration
    """
    list_display = [
        'name',
        'is_active',
        'show_in_navbar',
        'created_at',
    ]
    list_filter = [
        'is_active',
        'show_in_navbar',
        'created_at',
    ]
    search_fields = [
        'name',
        'description',
    ]
    prepopulated_fields = {
        'slug': ('name',)
    }
    fieldsets = (
        ('المعلومات الأساسية', {
            'fields': ('name', 'slug', 'logo', 'description')
        }),
        ('الحالة والعرض', {
            'fields': ('is_active', 'show_in_navbar')
        }),
    )
    ordering = ['name']
