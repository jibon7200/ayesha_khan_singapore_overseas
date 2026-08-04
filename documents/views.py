from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, DeleteView
from accounts.permissions import StaffLoginRequiredMixin, AdminRequiredMixin
from .models import Document
from .forms import DocumentForm


class DocumentListView(StaffLoginRequiredMixin, ListView):
    model = Document
    template_name = "documents/document_list.html"
    context_object_name = "documents"
    paginate_by = 25

    def get_queryset(self):
        qs = Document.objects.select_related("passport", "category")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(title__icontains=q) | qs.filter(passport__passport_number__icontains=q)
        category = self.request.GET.get("category")
        if category:
            qs = qs.filter(category_id=category)
        return qs.order_by("-uploaded_at")


class DocumentCreateView(StaffLoginRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = "documents/document_form.html"
    success_url = reverse_lazy("documents:list")

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, "নতুন ডকুমেন্ট আপলোড করা হয়েছে।")
        return super().form_valid(form)


class DocumentDeleteView(AdminRequiredMixin, DeleteView):
    model = Document
    template_name = "documents/document_confirm_delete.html"
    success_url = reverse_lazy("documents:list")

    def form_valid(self, form):
        messages.success(self.request, "ডকুমেন্ট ডিলিট করা হয়েছে।")
        return super().form_valid(form)
