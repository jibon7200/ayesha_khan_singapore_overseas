from django.db import models
from django.urls import reverse
from django.conf import settings
from agents.models import Agent
from delegates.models import Delegate


class Passport(models.Model):
    """
    Bible অধ্যায় ৩, ৪ ও ৭ - Passport Management Module
    """

    class Status(models.TextChoices):
        RECEIVED = "received", "Received"
        IN_PROCESS = "in_process", "In Process"
        VISA_APPROVED = "visa_approved", "Visa Approved"
        READY_FOR_DELIVERY = "ready_for_delivery", "Ready for Delivery"
        DELIVERED = "delivered", "Delivered"
        RETURNED = "returned", "Returned"

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    holder_name = models.CharField(max_length=150)
    passport_number = models.CharField(max_length=50, unique=True)
    nationality = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    mrz_data = models.TextField(blank=True, help_text="AI/OCR MRZ raw text (ভবিষ্যৎ ফিচার)")

    signature_scan = models.ImageField(upload_to="signatures/", blank=True, null=True)
    passport_scan = models.ImageField(upload_to="passports/", blank=True, null=True)
    holder_photo = models.ImageField(upload_to="photos/", blank=True, null=True)

    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name="passports")
    delegate = models.ForeignKey(Delegate, on_delete=models.SET_NULL, null=True, blank=True, related_name="passports")

    status = models.CharField(max_length=25, choices=Status.choices, default=Status.RECEIVED)
    remark = models.TextField(blank=True)

    # AI/OCR ভবিষ্যৎ ফিচার-সম্পর্কিত ফিল্ড
    ocr_processed = models.BooleanField(default=False)
    ai_visa_detected = models.BooleanField(null=True, blank=True, help_text="AI Visa Detection ফলাফল (ভবিষ্যৎ)")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="passports_created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["passport_number"]),
            models.Index(fields=["status"]),
            models.Index(fields=["expiry_date"]),
        ]

    def __str__(self):
        return f"{self.holder_name} ({self.passport_number})"

    def get_absolute_url(self):
        return reverse("passports:detail", args=[self.pk])

    def log_movement(self, action, location="", handled_by=None, note=""):
        PassportMovement.objects.create(
            passport=self, action=action, location=location, handled_by=handled_by, note=note,
        )


class PassportMovement(models.Model):
    """প্রতিটি পাসপোর্টের সম্পূর্ণ movement history (কবে, কোথায়, কার কাছে ছিল)।"""
    passport = models.ForeignKey(Passport, on_delete=models.CASCADE, related_name="movements")
    action = models.CharField(max_length=255)
    location = models.CharField(max_length=150, blank=True)
    handled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.passport.passport_number} - {self.action} @ {self.timestamp:%Y-%m-%d %H:%M}"
