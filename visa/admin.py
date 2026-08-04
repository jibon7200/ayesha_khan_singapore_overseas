from django.contrib import admin
from .models import VisaApplication, VisaStatusHistory


class VisaStatusHistoryInline(admin.TabularInline):
    model = VisaStatusHistory
    extra = 0
    readonly_fields = ("old_status", "new_status", "changed_by", "changed_at", "note")
    can_delete = False


@admin.register(VisaApplication)
class VisaApplicationAdmin(admin.ModelAdmin):
    list_display = ("passport", "destination_country", "visa_category", "status", "submission_date", "visa_expiry_date")
    list_filter = ("status", "destination_country")
    search_fields = ("passport__holder_name", "passport__passport_number", "application_number")
    date_hierarchy = "submission_date"
    inlines = [VisaStatusHistoryInline]


@admin.register(VisaStatusHistory)
class VisaStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("visa_application", "old_status", "new_status", "changed_by", "changed_at")
