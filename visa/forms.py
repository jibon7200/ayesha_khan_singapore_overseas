from django import forms
from .models import VisaApplication


class VisaApplicationForm(forms.ModelForm):
    class Meta:
        model = VisaApplication
        fields = [
            "passport", "agent", "delegate", "destination_country", "visa_category",
            "application_number", "submission_date", "processing_officer", "status",
            "approval_date", "visa_issue_date", "visa_expiry_date", "attachment", "remark",
        ]
        widgets = {
            "passport": forms.Select(attrs={"class": "form-select"}),
            "agent": forms.Select(attrs={"class": "form-select"}),
            "delegate": forms.Select(attrs={"class": "form-select"}),
            "destination_country": forms.TextInput(attrs={"class": "form-control"}),
            "visa_category": forms.TextInput(attrs={"class": "form-control"}),
            "application_number": forms.TextInput(attrs={"class": "form-control"}),
            "submission_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "processing_officer": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "approval_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "visa_issue_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "visa_expiry_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "attachment": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "remark": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class VisaCheckForm(forms.Form):
    """Bible ৯.৪ - Visa Check module: quick search"""
    passport_number = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Passport Number"}))
    application_number = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Application Number"}))
    applicant_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Applicant Name"}))
    country = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Country"}))
