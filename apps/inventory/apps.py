from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.inventory'
    verbose_name = 'المخزون'
    icon = 'fa fa-warehouse'  # FontAwesome icon
    divider_title = "إدارة المتجر"  # Section divider title
    priority = 80  # Sidebar ordering (higher = top)
    hide = False  # Show in sidebar
