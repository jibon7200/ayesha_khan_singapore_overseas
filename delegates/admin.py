from django.contrib import admin
from .models import Delegate


@admin.register(Delegate)
class DelegateAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "designation", "is_active", "current_passport_count", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "phone", "email")
