from django.contrib import admin
from django.utils.html import format_html
from django.db import models
from django.forms import TextInput, Textarea
from ..models import CarModel


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['full_name_display', 'brand', 'year_range_display', 'generation', 'body_type', 'compatible_products_count', 'is_active']
    list_filter = ['brand', 'is_active', 'body_type', 'year_from', 'created_at']
    search_fields = ['name', 'brand__name', 'generation', 'body_type', 'engine_types']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'full_name', 'year_range_display']
    autocomplete_fields = ['brand']
    
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('brand', 'name', 'slug')
        }),
        ('السنوات والمواصفات', {
            'fields': ('year_from', 'year_to', 'generation', 'body_type', 'engine_types')
        }),
        ('الوسائط', {
            'fields': ('image',)
        }),
        ('الوصف', {
            'fields': ('description',)
        }),
        ('الإعدادات', {
            'fields': ('is_active',)
        }),
        ('معلومات إضافية', {
            'fields': ('full_name', 'year_range_display'),
            'classes': ('collapse',)
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '40'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 60})},
    }

    def full_name_display(self, obj):
        return obj.full_name
    full_name_display.short_description = "الاسم الكامل"

    def compatible_products_count(self, obj):
        return obj.compatible_products.count()
    compatible_products_count.short_description = "المنتجات المتوافقة"


