from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from accounts.permissions import StaffLoginRequiredMixin, AdminRequiredMixin
from .models import Agent
from .forms import AgentForm


class AgentListView(StaffLoginRequiredMixin, ListView):
    model = Agent
    template_name = "agents/agent_list.html"
    context_object_name = "agents"
    paginate_by = 20

    def get_queryset(self):
        qs = Agent.objects.all()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(phone__icontains=q) | qs.filter(email__icontains=q)
        status = self.request.GET.get("status")
        if status == "active":
            qs = qs.filter(is_active=True)
        elif status == "inactive":
            qs = qs.filter(is_active=False)
        return qs.order_by("name")


class AgentDetailView(StaffLoginRequiredMixin, DetailView):
    model = Agent
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["passports"] = self.object.passports.all().order_by("-created_at")
        return ctx


class AgentCreateView(StaffLoginRequiredMixin, CreateView):
    model = Agent
    form_class = AgentForm
    template_name = "agents/agent_form.html"
    success_url = reverse_lazy("agents:list")

    def form_valid(self, form):
        messages.success(self.request, "নতুন এজেন্ট যোগ করা হয়েছে।")
        return super().form_valid(form)


class AgentUpdateView(StaffLoginRequiredMixin, UpdateView):
    model = Agent
    form_class = AgentForm
    template_name = "agents/agent_form.html"
    success_url = reverse_lazy("agents:list")

    def form_valid(self, form):
        messages.success(self.request, "এজেন্টের তথ্য আপডেট হয়েছে।")
        return super().form_valid(form)


class AgentDeleteView(AdminRequiredMixin, DeleteView):
    model = Agent
    template_name = "agents/agent_confirm_delete.html"
    success_url = reverse_lazy("agents:list")

    def form_valid(self, form):
        messages.success(self.request, "এজেন্ট ডিলিট করা হয়েছে।")
        return super().form_valid(form)
