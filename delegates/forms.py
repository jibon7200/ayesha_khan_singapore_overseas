from django import forms
from .models import Delegate


class DelegateForm(forms.ModelForm):
    class Meta:
        model = Delegate
        fields = ["name", "phone", "email", "address", "designation", "is_active", "remarks"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "designation": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }
