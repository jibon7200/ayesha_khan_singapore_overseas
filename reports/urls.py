from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("", views.ReportsHomeView.as_view(), name="home"),

    path("passports/excel/", views.PassportReportExcelView.as_view(), name="passport_excel"),
    path("passports/pdf/", views.PassportReportPDFView.as_view(), name="passport_pdf"),

    path("visa/excel/", views.VisaReportExcelView.as_view(), name="visa_excel"),
    path("visa/pdf/", views.VisaReportPDFView.as_view(), name="visa_pdf"),

    path("agents/excel/", views.AgentReportExcelView.as_view(), name="agent_excel"),
    path("delegates/excel/", views.DelegateReportExcelView.as_view(), name="delegate_excel"),
]
