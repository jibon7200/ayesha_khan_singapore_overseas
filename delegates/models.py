from django.db import models
from django.urls import reverse


class Delegate(models.Model):
    """
    Bible অধ্যায় ৩ ও ৮ - Delegate Management module:
    add, edit, delete, search, delegate-wise passport list,
    active-inactive, movement history
    """
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    designation = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("delegates:detail", args=[self.pk])

    @property
    def current_passport_count(self):
        return self.passports.exclude(status="delivered").count()

    @property
    def total_passport_count(self):
        return self.passports.count()
