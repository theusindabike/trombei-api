from django.urls import path
from . import views

app_name = "places"

urlpatterns = [
    path("", views.PlaceCreate.as_view(), name="place-create"),
    path("list/", views.PlaceList.as_view(), name="place-list"),
    path("<uuid:pk>/", views.PlaceRetrieveUpdateDestroy.as_view(), name="place-detail"),
]
