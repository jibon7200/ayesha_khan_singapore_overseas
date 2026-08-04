from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from accounts.permissions import StaffLoginRequiredMixin, AdminRequiredMixin
from .models import AirTicket
from .forms import AirTicketForm


class AirTicketListView(StaffLoginRequiredMixin, ListView):
    model = AirTicket
    template_name = "airtickets/airticket_list.html"
    context_object_name = "tickets"
    paginate_by = 25

    def get_queryset(self):
        qs = AirTicket.objects.select_related("passport")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(passenger_name__icontains=q) | qs.filter(pnr__icontains=q) | qs.filter(flight_number__icontains=q)
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["status_choices"] = AirTicket.Status.choices
        return ctx


class AirTicketDetailView(StaffLoginRequiredMixin, DetailView):
    model = AirTicket
    template_name = "airtickets/airticket_detail.html"
    context_object_name = "ticket"


class AirTicketCreateView(StaffLoginRequiredMixin, CreateView):
    model = AirTicket
    form_class = AirTicketForm
    template_name = "airtickets/airticket_form.html"
    success_url = reverse_lazy("airtickets:list")

    def form_valid(self, form):
        messages.success(self.request, "নতুন এয়ার টিকিট যোগ করা হয়েছে।")
        return super().form_valid(form)


class AirTicketUpdateView(StaffLoginRequiredMixin, UpdateView):
    model = AirTicket
    form_class = AirTicketForm
    template_name = "airtickets/airticket_form.html"
    success_url = reverse_lazy("airtickets:list")

    def form_valid(self, form):
        messages.success(self.request, "টিকিটের তথ্য আপডেট হয়েছে।")
        return super().form_valid(form)


class AirTicketDeleteView(AdminRequiredMixin, DeleteView):
    model = AirTicket
    template_name = "airtickets/airticket_confirm_delete.html"
    success_url = reverse_lazy("airtickets:list")

    def form_valid(self, form):
        messages.success(self.request, "টিকিট ডিলিট করা হয়েছে।")
        return super().form_valid(form)
