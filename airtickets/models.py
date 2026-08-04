from django.db import models
from django.urls import reverse
from passports.models import Passport


class AirTicket(models.Model):
    """
    Bible অধ্যায় ৩ ও ১০ - Air Ticket Checking module
    """

    class Status(models.TextChoices):
        REQUESTED = "requested", "Ticket Requested"
        BOOKING_IN_PROGRESS = "booking_in_progress", "Booking in Progress"
        CONFIRMED = "confirmed", "Ticket Confirmed"
        ISSUED = "issued", "Ticket Issued"
        TRAVEL_COMPLETED = "travel_completed", "Travel Completed"
        CANCELLED = "cancelled", "Ticket Cancelled"
        REFUNDED = "refunded", "Ticket Refunded"

    passport = models.ForeignKey(Passport, on_delete=models.CASCADE, related_name="air_tickets")
    passenger_name = models.CharField(max_length=150)
    airline_name = models.CharField(max_length=150)
    pnr = models.CharField(max_length=50, verbose_name="PNR")
    flight_number = models.CharField(max_length=50)
    travel_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    origin = models.CharField(max_length=100, blank=True)
    destination = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=25, choices=Status.choices, default=Status.REQUESTED)
    e_ticket_file = models.FileField(upload_to="tickets/", blank=True, null=True)
    remark = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.passenger_name} - {self.airline_name} ({self.pnr})"

    def get_absolute_url(self):
        return reverse("airtickets:detail", args=[self.pk])
