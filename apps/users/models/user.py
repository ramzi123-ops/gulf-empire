from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    نموذج المستخدم المخصص
    Custom User model extending Django's AbstractUser
    """
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="رقم الهاتف",
        help_text="رقم الهاتف مع رمز الدولة"
    )
    
    class Meta:
        verbose_name = "مستخدم"
        verbose_name_plural = "المستخدمون"
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        """Return full name or username if not set"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
