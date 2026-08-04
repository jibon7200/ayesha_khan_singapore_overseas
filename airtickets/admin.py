from django.contrib import admin
from .models import AirTicket


@admin.register(AirTicket)
class AirTicketAdmin(admin.ModelAdmin):
    list_display = ("passenger_name", "airline_name", "pnr", "flight_number", "travel_date", "status")
    list_filter = ("status", "airline_name")
    search_fields = ("passenger_name", "pnr", "flight_number", "passport__passport_number")
    date_hierarchy = "travel_date"
