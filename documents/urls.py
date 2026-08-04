from django.urls import path
from . import views

app_name = "documents"

urlpatterns = [
    path("", views.DocumentListView.as_view(), name="list"),
    path("add/", views.DocumentCreateView.as_view(), name="add"),
    path("<int:pk>/delete/", views.DocumentDeleteView.as_view(), name="delete"),
]
