from django.contrib import admin

from .models import Marketplace, PriceHistory, Product, ProductOffer


@admin.register(Marketplace)
class MarketplaceAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "base_url"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


class PriceHistoryInline(admin.TabularInline):
    model = PriceHistory
    extra = 0
    readonly_fields = ["price", "recorded_at"]
    can_delete = True
    show_change_link = True


@admin.register(ProductOffer)
class ProductOfferAdmin(admin.ModelAdmin):
    list_display = [
        "product",
        "marketplace",
        "current_price",
        "last_checked_at",
        "created_at",
    ]
    list_filter = ["marketplace"]
    search_fields = ["product__name", "external_id", "url"]
    autocomplete_fields = ["product", "marketplace"]
    inlines = [PriceHistoryInline]
    readonly_fields = ["created_at"]


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ["offer", "price", "recorded_at"]
    list_filter = ["recorded_at"]
    search_fields = ["offer__product__name", "offer__external_id"]
    autocomplete_fields = ["offer"]
    readonly_fields = ["recorded_at"]
