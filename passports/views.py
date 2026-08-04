from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from accounts.permissions import StaffLoginRequiredMixin, AdminRequiredMixin
from .models import Passport
from .forms import PassportForm, PassportOCRUploadForm, PassportMovementForm
from .ocr import extract_passport_data


class PassportListView(StaffLoginRequiredMixin, ListView):
    model = Passport
    template_name = "passports/passport_list.html"
    context_object_name = "passports"
    paginate_by = 25

    def get_queryset(self):
        qs = Passport.objects.select_related("agent", "delegate")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(holder_name__icontains=q) | qs.filter(passport_number__icontains=q)
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        agent_id = self.request.GET.get("agent")
        if agent_id:
            qs = qs.filter(agent_id=agent_id)
        delegate_id = self.request.GET.get("delegate")
        if delegate_id:
            qs = qs.filter(delegate_id=delegate_id)
        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["status_choices"] = Passport.Status.choices
        return ctx


class PassportDetailView(StaffLoginRequiredMixin, DetailView):
    model = Passport
    template_name = "passports/passport_detail.html"
    context_object_name = "passport"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["movements"] = self.object.movements.all()
        ctx["movement_form"] = PassportMovementForm()
        return ctx


class PassportCreateView(StaffLoginRequiredMixin, CreateView):
    model = Passport
    form_class = PassportForm
    template_name = "passports/passport_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        self.object.log_movement("Passport Received / Created", handled_by=self.request.user)
        messages.success(self.request, "নতুন পাসপোর্ট যোগ করা হয়েছে।")
        return response

    def get_success_url(self):
        return reverse_lazy("passports:detail", args=[self.object.pk])


class PassportUpdateView(StaffLoginRequiredMixin, UpdateView):
    model = Passport
    form_class = PassportForm
    template_name = "passports/passport_form.html"

    def form_valid(self, form):
        old_status = Passport.objects.get(pk=self.object.pk).status
        response = super().form_valid(form)
        if old_status != self.object.status:
            self.object.log_movement(
                f"Status changed: {old_status} → {self.object.status}", handled_by=self.request.user)
        messages.success(self.request, "পাসপোর্টের তথ্য আপডেট হয়েছে।")
        return response

    def get_success_url(self):
        return reverse_lazy("passports:detail", args=[self.object.pk])


class PassportDeleteView(AdminRequiredMixin, DeleteView):
    model = Passport
    template_name = "passports/passport_confirm_delete.html"
    success_url = reverse_lazy("passports:list")

    def form_valid(self, form):
        messages.success(self.request, "পাসপোর্ট ডিলিট করা হয়েছে।")
        return super().form_valid(form)


class PassportAddMovementView(StaffLoginRequiredMixin, View):
    def post(self, request, pk):
        passport = get_object_or_404(Passport, pk=pk)
        form = PassportMovementForm(request.POST)
        if form.is_valid():
            passport.log_movement(
                action=form.cleaned_data["action"],
                location=form.cleaned_data["location"],
                handled_by=request.user,
                note=form.cleaned_data["note"],
            )
            messages.success(request, "মুভমেন্ট হিস্ট্রি যোগ করা হয়েছে।")
        return redirect("passports:detail", pk=pk)


class PassportOCRUploadView(StaffLoginRequiredMixin, View):
    """AI Passport Scan & OCR Automation (ভবিষ্যৎ ফিচার - অধ্যায় ১০)"""
    template_name = "passports/passport_ocr_upload.html"

    def get(self, request):
        form = PassportOCRUploadForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = PassportOCRUploadForm(request.POST, request.FILES)
        extracted = None
        if form.is_valid():
            uploaded_image = request.FILES["passport_image"]
            import tempfile, os
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                for chunk in uploaded_image.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name
            extracted = extract_passport_data(tmp_path)
            os.unlink(tmp_path)
        return render(request, self.template_name, {"form": form, "extracted": extracted})
