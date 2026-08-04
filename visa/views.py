from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from accounts.permissions import VisaAccessRequiredMixin, StaffLoginRequiredMixin, AdminRequiredMixin
from .models import VisaApplication, VisaStatusHistory
from .forms import VisaApplicationForm, VisaCheckForm


class VisaListView(StaffLoginRequiredMixin, ListView):
    model = VisaApplication
    template_name = "visa/visa_list.html"
    context_object_name = "visas"
    paginate_by = 25

    def get_queryset(self):
        qs = VisaApplication.objects.select_related("passport", "agent", "delegate")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(passport__holder_name__icontains=q) | qs.filter(application_number__icontains=q) \
                 | qs.filter(passport__passport_number__icontains=q)
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        country = self.request.GET.get("country")
        if country:
            qs = qs.filter(destination_country__icontains=country)
        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["status_choices"] = VisaApplication.Status.choices
        return ctx


class VisaDetailView(StaffLoginRequiredMixin, DetailView):
    model = VisaApplication
    template_name = "visa/visa_detail.html"
    context_object_name = "visa"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["history"] = self.object.status_history.all()
        return ctx


class VisaCreateView(VisaAccessRequiredMixin, CreateView):
    model = VisaApplication
    form_class = VisaApplicationForm
    template_name = "visa/visa_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        VisaStatusHistory.objects.create(
            visa_application=self.object, old_status="", new_status=self.object.status,
            changed_by=self.request.user, note="Application created",
        )
        messages.success(self.request, "নতুন ভিসা অ্যাপ্লিকেশন যোগ করা হয়েছে।")
        return response

    def get_success_url(self):
        return reverse_lazy("visa:detail", args=[self.object.pk])


class VisaUpdateView(VisaAccessRequiredMixin, UpdateView):
    model = VisaApplication
    form_class = VisaApplicationForm
    template_name = "visa/visa_form.html"

    def form_valid(self, form):
        old_status = VisaApplication.objects.get(pk=self.object.pk).status
        response = super().form_valid(form)
        if old_status != self.object.status:
            VisaStatusHistory.objects.create(
                visa_application=self.object, old_status=old_status, new_status=self.object.status,
                changed_by=self.request.user,
            )
        messages.success(self.request, "ভিসা অ্যাপ্লিকেশন আপডেট হয়েছে।")
        return response

    def get_success_url(self):
        return reverse_lazy("visa:detail", args=[self.object.pk])


class VisaDeleteView(AdminRequiredMixin, DeleteView):
    model = VisaApplication
    template_name = "visa/visa_confirm_delete.html"
    success_url = reverse_lazy("visa:list")

    def form_valid(self, form):
        messages.success(self.request, "ভিসা অ্যাপ্লিকেশন ডিলিট করা হয়েছে।")
        return super().form_valid(form)


class VisaCheckView(StaffLoginRequiredMixin, View):
    """Bible ৯.৪ - Visa Check module: ড্যাশবোর্ড থেকে country/agent সিলেক্ট করে দ্রুত চেক।"""
    template_name = "visa/visa_check.html"

    def get(self, request):
        form = VisaCheckForm(request.GET or None)
        results = None
        if request.GET:
            qs = VisaApplication.objects.select_related("passport", "agent")
            if form.is_valid():
                data = form.cleaned_data
                if data.get("passport_number"):
                    qs = qs.filter(passport__passport_number__icontains=data["passport_number"])
                if data.get("application_number"):
                    qs = qs.filter(application_number__icontains=data["application_number"])
                if data.get("applicant_name"):
                    qs = qs.filter(passport__holder_name__icontains=data["applicant_name"])
                if data.get("country"):
                    qs = qs.filter(destination_country__icontains=data["country"])
            results = qs.order_by("-created_at")[:100]
        return render(request, self.template_name, {"form": form, "results": results})
