from django.urls import path
from . import views

app_name = "places"

urlpatterns = [
    path("", views.PlaceList.as_view(), name="place-list"),
    path("<uuid:pk>/", views.PlaceDetail.as_view(), name="place-detail"),
]
