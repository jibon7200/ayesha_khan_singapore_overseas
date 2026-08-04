from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from accounts.permissions import StaffLoginRequiredMixin, DelegateAccessRequiredMixin, AdminRequiredMixin
from .models import Delegate
from .forms import DelegateForm


class DelegateListView(StaffLoginRequiredMixin, ListView):
    model = Delegate
    template_name = "delegates/delegate_list.html"
    context_object_name = "delegates"
    paginate_by = 20

    def get_queryset(self):
        qs = Delegate.objects.all()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(phone__icontains=q)
        status = self.request.GET.get("status")
        if status == "active":
            qs = qs.filter(is_active=True)
        elif status == "inactive":
            qs = qs.filter(is_active=False)
        return qs.order_by("name")


class DelegateDetailView(StaffLoginRequiredMixin, DetailView):
    model = Delegate
    template_name = "delegates/delegate_detail.html"
    context_object_name = "delegate"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["passports"] = self.object.passports.all().order_by("-created_at")
        return ctx


class DelegateCreateView(DelegateAccessRequiredMixin, CreateView):
    model = Delegate
    form_class = DelegateForm
    template_name = "delegates/delegate_form.html"
    success_url = reverse_lazy("delegates:list")

    def form_valid(self, form):
        messages.success(self.request, "নতুন ডেলিগেট যোগ করা হয়েছে।")
        return super().form_valid(form)


class DelegateUpdateView(DelegateAccessRequiredMixin, UpdateView):
    model = Delegate
    form_class = DelegateForm
    template_name = "delegates/delegate_form.html"
    success_url = reverse_lazy("delegates:list")

    def form_valid(self, form):
        messages.success(self.request, "ডেলিগেটের তথ্য আপডেট হয়েছে।")
        return super().form_valid(form)


class DelegateDeleteView(AdminRequiredMixin, DeleteView):
    model = Delegate
    template_name = "delegates/delegate_confirm_delete.html"
    success_url = reverse_lazy("delegates:list")

    def form_valid(self, form):
        messages.success(self.request, "ডেলিগেট ডিলিট করা হয়েছে।")
        return super().form_valid(form)
