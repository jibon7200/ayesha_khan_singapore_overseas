from django.urls import path
from . import views

app_name = "passports"

urlpatterns = [
    path("", views.PassportListView.as_view(), name="list"),
    path("add/", views.PassportCreateView.as_view(), name="add"),
    path("ocr-upload/", views.PassportOCRUploadView.as_view(), name="ocr_upload"),
    path("<int:pk>/", views.PassportDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.PassportUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.PassportDeleteView.as_view(), name="delete"),
    path("<int:pk>/add-movement/", views.PassportAddMovementView.as_view(), name="add_movement"),
]
