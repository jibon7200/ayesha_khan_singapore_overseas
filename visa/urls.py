from django.urls import path
from . import views

app_name = "visa"

urlpatterns = [
    path("", views.VisaListView.as_view(), name="list"),
    path("add/", views.VisaCreateView.as_view(), name="add"),
    path("check/", views.VisaCheckView.as_view(), name="check"),
    path("<int:pk>/", views.VisaDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.VisaUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.VisaDeleteView.as_view(), name="delete"),
]
