from django import forms
from .models import Agent


class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ["name", "phone", "email", "address", "nid_or_id_number", "is_active", "remarks"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Agent Name"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "nid_or_id_number": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }
