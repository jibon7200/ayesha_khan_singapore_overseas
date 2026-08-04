from django.utils.deprecation import MiddlewareMixin

# যেসব path সাধারণত লগ করার দরকার নেই (static/media/admin jsi18n ইত্যাদি)
SKIP_PREFIXES = ("/static/", "/media/", "/admin/jsi18n/")

WRITE_METHODS = ("POST", "PUT", "PATCH", "DELETE")


class ActivityLogMiddleware(MiddlewareMixin):
    """
    প্রতিটি ডাটা-পরিবর্তনকারী (POST/PUT/PATCH/DELETE) রিকোয়েস্ট স্বয়ংক্রিয়ভাবে
    ActivityLog-এ সংরক্ষণ করে। GET রিকোয়েস্ট (শুধু দেখা) লগ করা হয় না,
    যাতে টেবিল অপ্রয়োজনীয়ভাবে বড় না হয়।
    """

    def process_response(self, request, response):
        try:
            if request.path.startswith(SKIP_PREFIXES):
                return response
            if request.method not in WRITE_METHODS:
                return response
            if not hasattr(request, "user") or not request.user.is_authenticated:
                return response
            if 200 <= response.status_code < 400:
                from .models import ActivityLog
                ActivityLog.objects.create(
                    user=request.user,
                    action=f"{request.method} {request.path}",
                    module=request.path.strip("/").split("/")[0] if request.path.strip("/") else "root",
                    path=request.path,
                    method=request.method,
                    ip_address=self._get_client_ip(request),
                )
        except Exception:
            # লগিং কখনোই মূল রিকোয়েস্ট ব্যর্থ করবে না
            pass
        return response

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
