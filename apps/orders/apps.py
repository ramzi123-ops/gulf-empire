from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.orders'
    verbose_name = 'الطلبات'
    icon = 'fa fa-shopping-cart'  # FontAwesome icon
    divider_title = "إدارة المتجر"  # Section divider title
    priority = 90  # Sidebar ordering (higher = top)
    hide = False  # Show in sidebar
