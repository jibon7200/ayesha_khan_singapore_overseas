from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.db.models import Count, Q
from accounts.permissions import StaffLoginRequiredMixin
from passports.models import Passport
from agents.models import Agent
from delegates.models import Delegate
from visa.models import VisaApplication
from airtickets.models import AirTicket
from notifications.models import Notification


class DashboardHomeView(StaffLoginRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["total_passports"] = Passport.objects.count()
        ctx["total_agents"] = Agent.objects.filter(is_active=True).count()
        ctx["total_delegates"] = Delegate.objects.filter(is_active=True).count()
        ctx["visa_processing"] = VisaApplication.objects.filter(
            status=VisaApplication.Status.UNDER_PROCESSING).count()
        ctx["visa_completed"] = VisaApplication.objects.filter(
            status__in=[VisaApplication.Status.APPROVED, VisaApplication.Status.VISA_COLLECTED,
                        VisaApplication.Status.DELIVERED]).count()
        ctx["passport_ready_for_delivery"] = Passport.objects.filter(
            status=Passport.Status.READY_FOR_DELIVERY).count()
        ctx["pending_passport"] = Passport.objects.exclude(
            status__in=[Passport.Status.DELIVERED, Passport.Status.RETURNED]).count()

        # Air ticket / AI OCR stats (অধ্যায় ১০)
        ctx["total_air_tickets"] = AirTicket.objects.count()
        ctx["upcoming_travel"] = AirTicket.objects.filter(status=AirTicket.Status.CONFIRMED).count()
        ctx["tickets_issued"] = AirTicket.objects.filter(status=AirTicket.Status.ISSUED).count()
        ctx["ai_scanned_passports"] = Passport.objects.filter(ocr_processed=True).count()

        # Recent Activity
        ctx["recent_notifications"] = Notification.objects.filter(is_read=False).order_by("-created_at")[:8]

        # Visa status breakdown (চার্টের জন্য)
        visa_breakdown = VisaApplication.objects.values("status").annotate(count=Count("id"))
        ctx["visa_status_labels"] = [dict(VisaApplication.Status.choices).get(v["status"], v["status"]) for v in visa_breakdown]
        ctx["visa_status_counts"] = [v["count"] for v in visa_breakdown]

        return ctx


class SmartSearchView(StaffLoginRequiredMixin, View):
    """ড্যাশবোর্ডের Smart Search Box - পাসপোর্ট নম্বর, হোল্ডার নাম, এজেন্ট বা ডেলিগেট নাম দিয়ে সার্চ।"""
    template_name = "dashboard/smart_search.html"

    def get(self, request):
        query = request.GET.get("q", "").strip()
        passports = agents = delegates = None
        if query:
            passports = Passport.objects.filter(
                Q(holder_name__icontains=query) | Q(passport_number__icontains=query)
            )[:25]
            agents = Agent.objects.filter(name__icontains=query)[:10]
            delegates = Delegate.objects.filter(name__icontains=query)[:10]
        return render(request, self.template_name, {
            "query": query, "passports": passports, "agents": agents, "delegates": delegates,
        })
