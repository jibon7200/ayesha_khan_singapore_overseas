from django import forms
from .models import CompanyInfo


class CompanyInfoForm(forms.ModelForm):
    class Meta:
        model = CompanyInfo
        fields = [
            "company_name", "logo", "address", "phone", "email", "website",
            "auto_backup_enabled", "backup_frequency_days",
            "passport_expiry_alert_days", "visa_expiry_alert_days",
        ]
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "website": forms.URLInput(attrs={"class": "form-control"}),
            "auto_backup_enabled": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "backup_frequency_days": forms.NumberInput(attrs={"class": "form-control"}),
            "passport_expiry_alert_days": forms.NumberInput(attrs={"class": "form-control"}),
            "visa_expiry_alert_days": forms.NumberInput(attrs={"class": "form-control"}),
        }
