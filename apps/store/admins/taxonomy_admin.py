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
        'created_at',
    ]
    list_filter = [
        'is_active',
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
        ('الحالة', {
            'fields': ('is_active',)
        }),
    )
    ordering = ['name']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """
    إدارة العلامات التجارية
    Brand administration
    """
    list_display = [
        'name',
        'is_active',
        'created_at',
    ]
    list_filter = [
        'is_active',
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
        ('الحالة', {
            'fields': ('is_active',)
        }),
    )
    ordering = ['name']
