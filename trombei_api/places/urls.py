from django.urls import path
from . import views

app_name = "places"

urlpatterns = [
    path("", views.PlaceListCreate.as_view(), name="place-list-create"),
    path(
        "<uuid:pk>/",
        views.PlaceRetrieveUpdateDestroy.as_view(),
        name="place-rud",
    ),
]
