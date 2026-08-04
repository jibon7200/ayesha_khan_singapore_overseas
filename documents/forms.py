from django import forms
from .models import Document, DocumentCategory


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["passport", "category", "title", "file"]
        widgets = {
            "passport": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class DocumentCategoryForm(forms.ModelForm):
    class Meta:
        model = DocumentCategory
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}
