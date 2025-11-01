from django.contrib import admin
from apps.users.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    إدارة الملفات الشخصية
    Profile administration
    """
    list_display = [
        'user',
        'date_of_birth',
        'newsletter_subscribed',
        'created_at',
    ]
    list_filter = [
        'newsletter_subscribed',
        'sms_notifications',
        'email_notifications',
        'created_at',
    ]
    search_fields = [
        'user__username',
        'user__email',
        'bio',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
    ]
    fieldsets = (
        ('المستخدم', {
            'fields': ('user',)
        }),
        ('المعلومات الشخصية', {
            'fields': ('avatar', 'bio', 'date_of_birth')
        }),
        ('التفضيلات', {
            'fields': (
                'newsletter_subscribed',
                'sms_notifications',
                'email_notifications',
            )
        }),
        ('التواريخ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    ordering = ['-created_at']

    def get_queryset(self, request):
        """
        Optimize queryset with select_related
        """
        qs = super().get_queryset(request)
        return qs.select_related('user')
