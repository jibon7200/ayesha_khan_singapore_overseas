from django.urls import path
from . import views

app_name = "airtickets"

urlpatterns = [
    path("", views.AirTicketListView.as_view(), name="list"),
    path("add/", views.AirTicketCreateView.as_view(), name="add"),
    path("<int:pk>/", views.AirTicketDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.AirTicketUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.AirTicketDeleteView.as_view(), name="delete"),
]
