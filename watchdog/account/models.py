from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, unique=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]

    def __str__(self):
        return str(self.email)


class AuthProvider(models.Model):
    class ProviderType(models.TextChoices):
        EMAIL = "email", "Email"
        GOOGLE = "google", "Google"
        TELEGRAM = "telegram", "Telegram"

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="providers",
    )
    provider = models.CharField(
        max_length=20,
        choices=ProviderType.choices,
        default=ProviderType.EMAIL,
        verbose_name="Провайдер",
        db_index=True,
    )
    provider_user_id = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Провайдер входа"
        verbose_name_plural = "Провайдеры входа"
        indexes = [
            models.Index(
                fields=["user", "provider"],
                name="acct_authprov_user_prov_idx",
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["provider", "provider_user_id"],
                name="unique_provider_user",
            ),
        ]

    def __str__(self):
        return f"{self.get_provider_display()}: {self.provider_user_id}"
