from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.store'
    verbose_name = 'المتجر'
    icon = 'fa fa-store'  # FontAwesome icon
    divider_title = "إدارة المتجر"  # Section divider title
    priority = 100  # Sidebar ordering (higher = top)
    hide = False  # Show in sidebar
