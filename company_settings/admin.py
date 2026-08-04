from django.contrib import admin
from .models import CompanyInfo


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ("company_name", "phone", "email", "auto_backup_enabled", "updated_at")

    def has_add_permission(self, request):
        # Singleton - একবারের বেশি নতুন রেকর্ড তৈরি করতে দেওয়া হবে না
        return not CompanyInfo.objects.exists()
