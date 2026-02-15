from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import AuthProvider, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active"]
    search_fields = ["email", "username"]
    ordering = ["email"]


@admin.register(AuthProvider)
class AuthProviderAdmin(admin.ModelAdmin):
    list_display = ["user", "provider", "provider_user_id", "created_at"]
    list_filter = ["provider"]
    search_fields = ["provider_user_id", "user__email"]
    raw_id_fields = ["user"]
