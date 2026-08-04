from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from accounts.permissions import StaffLoginRequiredMixin
from passports.models import Passport
from visa.models import VisaApplication
from agents.models import Agent
from delegates.models import Delegate


class ReportsHomeView(StaffLoginRequiredMixin, TemplateView):
    template_name = "reports/reports_home.html"


class BaseExcelExportView(StaffLoginRequiredMixin, View):
    """সব Excel export view এই বেস ক্লাস থেকে ইনহেরিট করবে।"""
    filename = "report.xlsx"
    headers = []

    def get_rows(self, request):
        raise NotImplementedError

    def get(self, request):
        import openpyxl
        from openpyxl.styles import Font

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Report"
        ws.append(self.headers)
        for cell in ws[1]:
            cell.font = Font(bold=True)

        for row in self.get_rows(request):
            ws.append(row)

        for col in ws.columns:
            max_len = max((len(str(c.value)) if c.value else 0) for c in col)
            ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 40)

        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = f"attachment; filename={self.filename}"
        wb.save(response)
        return response


class BasePDFExportView(StaffLoginRequiredMixin, View):
    """সব PDF export view এই বেস ক্লাস থেকে ইনহেরিট করবে (reportlab দিয়ে সাধারণ টেবিল রিপোর্ট)।"""
    filename = "report.pdf"
    title = "Report"
    headers = []

    def get_rows(self, request):
        raise NotImplementedError

    def get(self, request):
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import cm

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f"attachment; filename={self.filename}"

        doc = SimpleDocTemplate(response, pagesize=landscape(A4),
                                 leftMargin=1.5 * cm, rightMargin=1.5 * cm)
        styles = getSampleStyleSheet()
        elements = [Paragraph(self.title, styles["Title"]), Spacer(1, 12)]

        data = [self.headers] + list(self.get_rows(request))
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0d3b66")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(table)
        doc.build(elements)
        return response


# ---------------- Passport Report ----------------

class PassportReportExcelView(BaseExcelExportView):
    filename = "passport_report.xlsx"
    headers = ["Holder Name", "Passport Number", "Agent", "Delegate", "Status", "Expiry Date"]

    def get_rows(self, request):
        for p in Passport.objects.select_related("agent", "delegate"):
            yield [p.holder_name, p.passport_number, str(p.agent or ""), str(p.delegate or ""),
                   p.get_status_display(), str(p.expiry_date or "")]


class PassportReportPDFView(BasePDFExportView):
    filename = "passport_report.pdf"
    title = "Passport Report - Ayesha Khan Singapore Overseas"
    headers = ["Holder Name", "Passport No.", "Agent", "Delegate", "Status", "Expiry Date"]

    def get_rows(self, request):
        for p in Passport.objects.select_related("agent", "delegate"):
            yield [p.holder_name, p.passport_number, str(p.agent or ""), str(p.delegate or ""),
                   p.get_status_display(), str(p.expiry_date or "")]


# ---------------- Visa Report ----------------

class VisaReportExcelView(BaseExcelExportView):
    filename = "visa_report.xlsx"
    headers = ["Holder Name", "Country", "Category", "Status", "Submission Date", "Visa Expiry"]

    def get_rows(self, request):
        for v in VisaApplication.objects.select_related("passport"):
            yield [v.passport.holder_name, v.destination_country, v.visa_category,
                   v.get_status_display(), str(v.submission_date or ""), str(v.visa_expiry_date or "")]


class VisaReportPDFView(BasePDFExportView):
    filename = "visa_report.pdf"
    title = "Visa Processing Report - Ayesha Khan Singapore Overseas"
    headers = ["Holder Name", "Country", "Category", "Status", "Submission Date", "Visa Expiry"]

    def get_rows(self, request):
        for v in VisaApplication.objects.select_related("passport"):
            yield [v.passport.holder_name, v.destination_country, v.visa_category,
                   v.get_status_display(), str(v.submission_date or ""), str(v.visa_expiry_date or "")]


# ---------------- Agent-wise Report ----------------

class AgentReportExcelView(BaseExcelExportView):
    filename = "agent_report.xlsx"
    headers = ["Agent Name", "Phone", "Total Passports", "Active"]

    def get_rows(self, request):
        for a in Agent.objects.all():
            yield [a.name, a.phone, a.total_passports, "Yes" if a.is_active else "No"]


# ---------------- Delegate-wise Report ----------------

class DelegateReportExcelView(BaseExcelExportView):
    filename = "delegate_report.xlsx"
    headers = ["Delegate Name", "Phone", "Current Passports", "Total Passports", "Active"]

    def get_rows(self, request):
        for d in Delegate.objects.all():
            yield [d.name, d.phone, d.current_passport_count, d.total_passport_count, "Yes" if d.is_active else "No"]
