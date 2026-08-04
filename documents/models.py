from django.db import models
from django.conf import settings
from passports.models import Passport


class DocumentCategory(models.Model):
    """Bible অধ্যায় ৩ - Documents module: document upload, categorize"""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Document Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Document(models.Model):
    passport = models.ForeignKey(Passport, on_delete=models.CASCADE, related_name="documents", null=True, blank=True)
    category = models.ForeignKey(DocumentCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="documents")
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="documents/")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    # OCR ভবিষ্যৎ ফিচার
    ocr_text = models.TextField(blank=True, help_text="ভবিষ্যৎ OCR ফলাফল")
    ocr_processed = models.BooleanField(default=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title
