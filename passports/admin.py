from django.contrib import admin
from .models import Passport, PassportMovement


class PassportMovementInline(admin.TabularInline):
    model = PassportMovement
    extra = 0
    readonly_fields = ("action", "location", "handled_by", "note", "timestamp")
    can_delete = False


@admin.register(Passport)
class PassportAdmin(admin.ModelAdmin):
    list_display = ("passport_number", "holder_name", "agent", "delegate", "status", "expiry_date", "created_at")
    list_filter = ("status", "gender", "nationality")
    search_fields = ("passport_number", "holder_name", "agent__name", "delegate__name")
    date_hierarchy = "created_at"
    inlines = [PassportMovementInline]


@admin.register(PassportMovement)
class PassportMovementAdmin(admin.ModelAdmin):
    list_display = ("passport", "action", "location", "handled_by", "timestamp")
    list_filter = ("timestamp",)
    search_fields = ("passport__passport_number", "action")
