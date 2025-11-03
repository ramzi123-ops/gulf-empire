from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.dashboard'
    verbose_name = 'لوحة التحكم'
    icon = 'fa fa-gauge'  # FontAwesome icon
    divider_title = "لوحة التحكم"  # Section divider title
    priority = 200  # Sidebar ordering (higher = top)
    hide = False  # Show in sidebar
