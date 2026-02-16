from django.conf import settings
from django.db import models


class Marketplace(models.Model):
    class MarketplaceType(models.TextChoices):
        OZON = "ozon", "OZON"
        WILDBERRIES = "wildberries", "Wildberries"

    name = models.CharField(
        max_length=255,
        choices=MarketplaceType.choices,
        verbose_name="Название",
    )
    slug = models.SlugField(verbose_name="Slug", unique=True)
    base_url = models.URLField(
        verbose_name="Базовый URL",
    )

    class Meta:
        verbose_name = "Маркетплейс"
        verbose_name_plural = "Маркетплейсы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(verbose_name="Slug", unique=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    image_url = models.URLField(verbose_name="Картинка", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "created_at"]

    def __str__(self):
        return self.name


class ProductOffer(models.Model):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="offers",
        verbose_name="Продукт",
    )
    marketplace = models.ForeignKey(
        to=Marketplace,
        on_delete=models.CASCADE,
        related_name="offers",
        verbose_name="Маркетплейс",
    )
    url = models.URLField(verbose_name="Ссылка на товар")
    external_id = models.CharField(
        max_length=255,
        verbose_name="Артикул на товар",
        db_index=True,
    )
    current_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Текущая цена",
    )
    last_checked_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Предложение"
        verbose_name_plural = "Предложения"
        ordering = ["current_price", "created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "marketplace"],
                name="unique_product_marketplace",
            )
        ]

    def __str__(self):
        return f"{self.marketplace} - {self.product}"


class PriceHistory(models.Model):
    offer = models.ForeignKey(
        to=ProductOffer,
        on_delete=models.CASCADE,
        related_name="history",
        verbose_name="Предложение",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
    )
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "История цены"
        verbose_name_plural = "История цен"
        ordering = ["-recorded_at"]
        indexes = [
            models.Index(
                fields=["offer", "recorded_at"],
                name="product_pricehist_offer_dt",
            ),
        ]


class ProductSubscription(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="product_subscriptions",
        verbose_name="Пользователь",
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Продукт",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    notify_at = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Пороговая цена",
        help_text="Уведомление будет отправлено, если цена продукта упадет ниже этого значения",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
    )
    last_notified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Последнее уведомление",
    )
    notify_cooldown_hours = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Минимум часов между уведомлениями",
    )

    def __str__(self):
        return f"{self.user.email} — {self.product.name}"

    class Meta:
        verbose_name = "Подписка на продукт"
        verbose_name_plural = "Подписки на продукты"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_product",
            )
        ]
