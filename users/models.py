from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=15, verbose_name="Телефон", blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="Город", blank=True, null=True)
    avatar = models.ImageField(
        upload_to="users/", blank=True, null=True, verbose_name="Аватар"
    )
    is_active = models.BooleanField(default=False, verbose_name="Активный")
    token = models.CharField(
        max_length=255, verbose_name="Токен", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


