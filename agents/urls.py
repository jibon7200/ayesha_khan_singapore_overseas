from django.urls import path
from . import views

app_name = "agents"

urlpatterns = [
    path("", views.AgentListView.as_view(), name="list"),
    path("add/", views.AgentCreateView.as_view(), name="add"),
    path("<int:pk>/", views.AgentDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.AgentUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.AgentDeleteView.as_view(), name="delete"),
]
