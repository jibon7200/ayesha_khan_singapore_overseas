from django.contrib import admin
from .models import Agent


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "is_active", "total_passports", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "phone", "email", "nid_or_id_number")
