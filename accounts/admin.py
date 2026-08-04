from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ActivityLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "get_full_name", "role", "email", "phone_number", "is_active_staff", "is_active")
    list_filter = ("role", "is_active", "is_active_staff")
    search_fields = ("username", "first_name", "last_name", "email", "phone_number")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Role & Contact Info", {"fields": ("role", "phone_number", "profile_photo", "is_active_staff")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Role & Contact Info", {"fields": ("role", "phone_number", "email")}),
    )


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user", "action", "module", "method", "ip_address")
    list_filter = ("module", "method", "timestamp")
    search_fields = ("user__username", "action", "path")
    readonly_fields = [f.name for f in ActivityLog._meta.fields]
    ordering = ("-timestamp",)

    def has_add_permission(self, request):
        return False
