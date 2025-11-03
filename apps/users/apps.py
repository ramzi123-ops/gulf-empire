from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = 'المستخدمون'
    icon = 'fa fa-users'  # FontAwesome icon
    divider_title = "إدارة النظام"  # Section divider title
    priority = 10  # Sidebar ordering (higher = top)
    hide = False  # Show in sidebar
