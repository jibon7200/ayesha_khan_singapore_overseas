"""
Role-based access control mixins - প্রতিটি App-এর views.py এখান থেকে import করবে।
Bible-এর নিরাপত্তা নীতি: "শুধু অনুমোদিত ইউজাররাই তথ্য দেখতে/পরিবর্তন করতে পারবে।"
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """শুধু Admin / Super Admin অ্যাক্সেস পাবে (যেমন: Agent/Delegate ডিলিট, ইউজার ম্যানেজমেন্ট)।"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin_level


class VisaAccessRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Visa মডিউল অ্যাক্সেসের জন্য।"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.can_manage_visa


class DelegateAccessRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Delegate মডিউল অ্যাক্সেসের জন্য।"""
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.can_manage_delegates or self.request.user.is_admin_level
        )


class StaffLoginRequiredMixin(LoginRequiredMixin):
    """সাধারণ লগইন-প্রয়োজনীয় ভিউয়ের জন্য (সব রোল অ্যাক্সেস পায়)।"""
    login_url = "accounts:login"
