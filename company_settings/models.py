from django.db import models


class CompanyInfo(models.Model):
    """
    সিস্টেম-ওয়াইড কোম্পানি সেটিংস (একটিই রেকর্ড থাকবে - singleton style)
    Bible অধ্যায় ৫.৩ - Settings App: company info, logo, backup settings, general config
    """
    company_name = models.CharField(max_length=255, default="Ayesha Khan Singapore Overseas")
    logo = models.ImageField(upload_to="company/", blank=True, null=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    # Backup settings
    auto_backup_enabled = models.BooleanField(default=False)
    backup_frequency_days = models.PositiveIntegerField(default=7)
    last_backup_at = models.DateTimeField(blank=True, null=True)

    # General config
    passport_expiry_alert_days = models.PositiveIntegerField(
        default=30, help_text="মেয়াদ শেষ হওয়ার কত দিন আগে রিমাইন্ডার দেখাবে")
    visa_expiry_alert_days = models.PositiveIntegerField(default=30)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Setting"
        verbose_name_plural = "Company Settings"

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        self.pk = 1  # সবসময় একটাই রেকর্ড (singleton)
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
