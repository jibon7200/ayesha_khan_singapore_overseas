from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, View
from accounts.permissions import StaffLoginRequiredMixin
from .models import Notification


class NotificationListView(StaffLoginRequiredMixin, ListView):
    model = Notification
    template_name = "notifications/notification_list.html"
    context_object_name = "notifications"
    paginate_by = 30

    def get_queryset(self):
        from django.db.models import Q
        return Notification.objects.filter(
            Q(recipient=self.request.user) | Q(recipient__isnull=True)
        ).order_by("-created_at")


class NotificationMarkReadView(StaffLoginRequiredMixin, View):
    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk)
        notification.is_read = True
        notification.save(update_fields=["is_read"])
        return redirect(request.META.get("HTTP_REFERER", "notifications:list"))
