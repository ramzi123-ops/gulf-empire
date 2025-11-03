from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.payments'
    verbose_name = 'المدفوعات'
    icon = 'fa fa-credit-card'  # FontAwesome icon
    divider_title = "إدارة المالية"  # Section divider title
    priority = 70  # Sidebar ordering (higher = top)
    hide = False  # Show in sidebar
