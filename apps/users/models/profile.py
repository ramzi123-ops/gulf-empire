from django.db import models
from django.conf import settings


class Profile(models.Model):
    """
    الملف الشخصي للمستخدم
    User Profile model
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="المستخدم"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name="الصورة الشخصية"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="نبذة عني",
        help_text="معلومات إضافية عن المستخدم"
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاريخ الميلاد"
    )
    
    # Customer preferences
    newsletter_subscribed = models.BooleanField(
        default=False,
        verbose_name="الاشتراك في النشرة الإخبارية"
    )
    sms_notifications = models.BooleanField(
        default=True,
        verbose_name="إشعارات الرسائل النصية"
    )
    email_notifications = models.BooleanField(
        default=True,
        verbose_name="إشعارات البريد الإلكتروني"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاريخ التحديث"
    )

    class Meta:
        verbose_name = "ملف شخصي"
        verbose_name_plural = "الملفات الشخصية"

    def __str__(self):
        return f"ملف {self.user.username}"
