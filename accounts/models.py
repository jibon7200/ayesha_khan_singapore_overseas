from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    কাস্টম ইউজার মডেল - Master Developer Bible অধ্যায় ২ অনুযায়ী রোলসমূহ:
    Admin, Office Staff, Data Entry Operator, Visa Processing Officer,
    Delegate Manager, Accounts Staff (ভবিষ্যতে), Super Admin
    """

    class Role(models.TextChoices):
        SUPER_ADMIN = "super_admin", "Super Admin"
        ADMIN = "admin", "Admin"
        OFFICE_STAFF = "office_staff", "Office Staff"
        DATA_ENTRY = "data_entry_operator", "Data Entry Operator"
        VISA_OFFICER = "visa_processing_officer", "Visa Processing Officer"
        DELEGATE_MANAGER = "delegate_manager", "Delegate Manager"
        ACCOUNTS_STAFF = "accounts_staff", "Accounts Staff"

    role = models.CharField(max_length=30, choices=Role.choices, default=Role.OFFICE_STAFF)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_photo = models.ImageField(upload_to="user_photos/", blank=True, null=True)
    is_active_staff = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_super_admin(self):
        return self.role == self.Role.SUPER_ADMIN or self.is_superuser

    @property
    def is_admin_level(self):
        return self.role in (self.Role.SUPER_ADMIN, self.Role.ADMIN) or self.is_superuser

    @property
    def can_manage_visa(self):
        return self.role in (
            self.Role.SUPER_ADMIN, self.Role.ADMIN, self.Role.VISA_OFFICER,
        ) or self.is_superuser

    @property
    def can_manage_delegates(self):
        return self.role in (
            self.Role.SUPER_ADMIN, self.Role.ADMIN, self.Role.DELEGATE_MANAGER,
        ) or self.is_superuser


class ActivityLog(models.Model):
    """
    সিস্টেম-ওয়াইড Audit Log - প্রতিটি গুরুত্বপূর্ণ অ্যাকশন এখানে রেকর্ড হবে।
    (Bible অধ্যায় ৯ ও ১০ - Security ও Access Control Audit Log)
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="activity_logs")
    action = models.CharField(max_length=255)
    module = models.CharField(max_length=100, blank=True)
    object_repr = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    path = models.CharField(max_length=255, blank=True)
    method = models.CharField(max_length=10, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp:%Y-%m-%d %H:%M}"
