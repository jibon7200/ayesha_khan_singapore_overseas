from django.contrib.auth import views as auth_views
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User, ActivityLog
from .forms import StyledAuthenticationForm, UserCreateForm, UserUpdateForm, StyledPasswordChangeForm
from .permissions import AdminRequiredMixin


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    authentication_form = StyledAuthenticationForm
    redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    next_page = "accounts:login"


class PasswordChangeView(LoginRequiredMixin, View):
    template_name = "accounts/password_change.html"

    def get(self, request):
        form = StyledPasswordChangeForm(user=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = StyledPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "পাসওয়ার্ড সফলভাবে পরিবর্তন হয়েছে।")
            return redirect("dashboard:home")
        return render(request, self.template_name, {"form": form})


# ---------------- User / Role Management (শুধু Admin) ----------------

class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = "accounts/user_list.html"
    context_object_name = "users"
    paginate_by = 20

    def get_queryset(self):
        qs = User.objects.all().order_by("username")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(username__icontains=q) | qs.filter(email__icontains=q)
        return qs


class UserCreateView(AdminRequiredMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("accounts:user_list")

    def form_valid(self, form):
        messages.success(self.request, "নতুন ইউজার তৈরি হয়েছে।")
        return super().form_valid(form)


class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy("accounts:user_list")

    def form_valid(self, form):
        messages.success(self.request, "ইউজার তথ্য আপডেট হয়েছে।")
        return super().form_valid(form)


class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = "accounts/user_confirm_delete.html"
    success_url = reverse_lazy("accounts:user_list")

    def form_valid(self, form):
        messages.success(self.request, "ইউজার ডিলিট করা হয়েছে।")
        return super().form_valid(form)


class ActivityLogListView(AdminRequiredMixin, ListView):
    model = ActivityLog
    template_name = "accounts/activity_log_list.html"
    context_object_name = "logs"
    paginate_by = 40

    def get_queryset(self):
        return ActivityLog.objects.select_related("user").order_by("-timestamp")
