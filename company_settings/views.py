from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.permissions import AdminRequiredMixin
from django.views.generic import View
from .models import CompanyInfo
from .forms import CompanyInfoForm


class CompanySettingsView(AdminRequiredMixin, View):
    template_name = "company_settings/settings_form.html"

    def get(self, request):
        instance = CompanyInfo.load()
        form = CompanyInfoForm(instance=instance)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        instance = CompanyInfo.load()
        form = CompanyInfoForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "কোম্পানি সেটিংস সংরক্ষণ করা হয়েছে।")
            return redirect("company_settings:settings")
        return render(request, self.template_name, {"form": form})
