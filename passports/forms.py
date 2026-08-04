from django import forms
from .models import Passport


class PassportForm(forms.ModelForm):
    class Meta:
        model = Passport
        fields = [
            "holder_name", "passport_number", "nationality", "gender", "date_of_birth",
            "issue_date", "expiry_date", "signature_scan", "passport_scan", "holder_photo",
            "agent", "delegate", "status", "remark",
        ]
        widgets = {
            "holder_name": forms.TextInput(attrs={"class": "form-control"}),
            "passport_number": forms.TextInput(attrs={"class": "form-control"}),
            "nationality": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "date_of_birth": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "issue_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "expiry_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "signature_scan": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "passport_scan": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "holder_photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "agent": forms.Select(attrs={"class": "form-select"}),
            "delegate": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "remark": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class PassportOCRUploadForm(forms.Form):
    """AI Passport Scan & OCR Automation (ভবিষ্যৎ ফিচার - অধ্যায় ১০)"""
    passport_image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"})
    )


class PassportMovementForm(forms.Form):
    action = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "যেমন: Delegate-কে হস্তান্তর করা হলো"}))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control", "rows": 2}))
