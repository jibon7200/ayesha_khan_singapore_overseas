"""
Root URL configuration - Ayesha Khan Singapore Overseas
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("accounts/", include("accounts.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path("agents/", include("agents.urls")),
    path("delegates/", include("delegates.urls")),
    path("passports/", include("passports.urls")),
    path("visa/", include("visa.urls")),
    path("air-tickets/", include("airtickets.urls")),
    path("documents/", include("documents.urls")),
    path("reports/", include("reports.urls")),
    path("notifications/", include("notifications.urls")),
    path("settings/", include("company_settings.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

admin.site.site_header = "Ayesha Khan Singapore Overseas - Admin"
admin.site.site_title = "AKSO Admin Portal"
admin.site.index_title = "Visa, Passport & Document Management System"
