from django.urls import path
from . import views

app_name = "company_settings"

urlpatterns = [
    path("", views.CompanySettingsView.as_view(), name="settings"),
]
