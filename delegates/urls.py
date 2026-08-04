from django.urls import path
from . import views

app_name = "delegates"

urlpatterns = [
    path("", views.DelegateListView.as_view(), name="list"),
    path("add/", views.DelegateCreateView.as_view(), name="add"),
    path("<int:pk>/", views.DelegateDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.DelegateUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.DelegateDeleteView.as_view(), name="delete"),
]
