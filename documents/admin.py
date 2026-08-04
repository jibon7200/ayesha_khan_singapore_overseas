from django.contrib import admin
from .models import Document, DocumentCategory


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "passport", "category", "uploaded_by", "uploaded_at")
    list_filter = ("category",)
    search_fields = ("title", "passport__passport_number", "passport__holder_name")
