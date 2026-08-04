from django.db import models
from django.urls import reverse
from django.conf import settings
from passports.models import Passport
from agents.models import Agent
from delegates.models import Delegate


class VisaApplication(models.Model):
    """
    Bible অধ্যায় ৯ - Visa Processing & Visa Check Module (Final Edition)
    """

    class Status(models.TextChoices):
        APPLICATION_RECEIVED = "application_received", "Application Received"
        DOCUMENT_VERIFIED = "document_verified", "Document Verified"
        SUBMITTED = "submitted", "Submitted"
        UNDER_PROCESSING = "under_processing", "Under Processing"
        ADDITIONAL_DOCUMENT_REQUIRED = "additional_document_required", "Additional Document Required"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        VISA_COLLECTED = "visa_collected", "Visa Collected"
        READY_FOR_DELIVERY = "ready_for_delivery", "Ready for Delivery"
        DELIVERED = "delivered", "Delivered"
        CLOSED = "closed", "Closed"

    passport = models.ForeignKey(Passport, on_delete=models.CASCADE, related_name="visa_applications")
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name="visa_applications")
    delegate = models.ForeignKey(Delegate, on_delete=models.SET_NULL, null=True, blank=True, related_name="visa_applications")

    destination_country = models.CharField(max_length=100)
    visa_category = models.CharField(max_length=100, blank=True)
    application_number = models.CharField(max_length=100, blank=True)
    submission_date = models.DateField(null=True, blank=True)
    processing_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="visa_processed"
    )
    status = models.CharField(max_length=35, choices=Status.choices, default=Status.APPLICATION_RECEIVED)
    approval_date = models.DateField(null=True, blank=True)
    visa_issue_date = models.DateField(null=True, blank=True)
    visa_expiry_date = models.DateField(null=True, blank=True)
    attachment = models.FileField(upload_to="visa_docs/", blank=True, null=True, help_text="Visa PDF/Image copy")
    remark = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["destination_country"]),
        ]

    def __str__(self):
        return f"{self.passport.holder_name} - {self.destination_country} ({self.get_status_display()})"

    def get_absolute_url(self):
        return reverse("visa:detail", args=[self.pk])


class VisaStatusHistory(models.Model):
    """প্রতিটি স্ট্যাটাস পরিবর্তনের audit trail।"""
    visa_application = models.ForeignKey(VisaApplication, on_delete=models.CASCADE, related_name="status_history")
    old_status = models.CharField(max_length=35, blank=True)
    new_status = models.CharField(max_length=35)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.visa_application} : {self.old_status} → {self.new_status}"
