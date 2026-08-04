from .models import Notification


def notification_summary(request):
    """সব টেমপ্লেটে টপ-বার নোটিফিকেশন বেল আইকনের জন্য গ্লোবাল কনটেক্সট।"""
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return {"unread_notifications": [], "unread_notification_count": 0}
    base_qs = Notification.objects.filter(is_read=False).filter(
        models_q_recipient(request.user)
    ).order_by("-created_at")
    count = base_qs.count()
    return {"unread_notifications": base_qs[:10], "unread_notification_count": count}


def models_q_recipient(user):
    from django.db.models import Q
    return Q(recipient=user) | Q(recipient__isnull=True)
