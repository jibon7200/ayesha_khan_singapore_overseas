from django import forms
from .models import AirTicket


class AirTicketForm(forms.ModelForm):
    class Meta:
        model = AirTicket
        fields = [
            "passport", "passenger_name", "airline_name", "pnr", "flight_number",
            "travel_date", "return_date", "origin", "destination", "status",
            "e_ticket_file", "remark",
        ]
        widgets = {
            "passport": forms.Select(attrs={"class": "form-select"}),
            "passenger_name": forms.TextInput(attrs={"class": "form-control"}),
            "airline_name": forms.TextInput(attrs={"class": "form-control"}),
            "pnr": forms.TextInput(attrs={"class": "form-control"}),
            "flight_number": forms.TextInput(attrs={"class": "form-control"}),
            "travel_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "return_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "origin": forms.TextInput(attrs={"class": "form-control"}),
            "destination": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "e_ticket_file": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "remark": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
