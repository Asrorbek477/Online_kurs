from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User modeli.
    AbstractUser'dan meros olamiz – username, password, email
    maydonlari tayyor keladi, biz faqat is_instructor qo'shamiz.
    """
    email = models.EmailField(unique=True)  # Email noyob bo'lsin

    is_instructor = models.BooleanField(
        default=False,
        help_text="True = Instruktor, False = Student"
    )

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        role = 'Instruktor' if self.is_instructor else 'Student'
        return f"{self.username} ({role})"