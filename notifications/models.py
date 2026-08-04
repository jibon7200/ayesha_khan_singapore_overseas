from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    Bible অধ্যায় ৩ - Notification module:
    expiry reminder, visa ready alert, passport return reminder, pending document alert
    """

    class NotificationType(models.TextChoices):
        PASSPORT_EXPIRY = "passport_expiry", "Passport Expiry Reminder"
        VISA_READY = "visa_ready", "Visa Ready Alert"
        PASSPORT_RETURN = "passport_return", "Passport Return Reminder"
        PENDING_DOCUMENT = "pending_document", "Pending Document Alert"
        TICKET_ISSUED = "ticket_issued", "Ticket Issued"
        SYSTEM = "system", "System Notification"

    notification_type = models.CharField(max_length=30, choices=NotificationType.choices, default=NotificationType.SYSTEM)
    title = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    related_url = models.CharField(max_length=255, blank=True)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True,
        help_text="খালি রাখলে সব ইউজার দেখবে"
    )
    is_read = models.BooleanField(default=False)

    # WhatsApp ভবিষ্যৎ ইন্টিগ্রেশন ট্র্যাকিং
    whatsapp_sent = models.BooleanField(default=False)
    whatsapp_sent_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
