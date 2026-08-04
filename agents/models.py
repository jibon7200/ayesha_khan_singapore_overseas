from django.db import models
from django.urls import reverse


class Agent(models.Model):
    """
    Bible অধ্যায় ৩ - Agent Management module:
    add, edit, delete, search, history, agent-wise passport list
    """
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    nid_or_id_number = models.CharField(max_length=100, blank=True, verbose_name="NID / ID Number")
    is_active = models.BooleanField(default=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("agents:detail", args=[self.pk])

    @property
    def total_passports(self):
        return self.passports.count()
