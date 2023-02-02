from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    path("", views.EventList.as_view(), name="event-list"),
    path("<uuid:pk>/", views.EventDetail.as_view(), name="event-detail"),
]
