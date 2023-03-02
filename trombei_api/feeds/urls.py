from django.urls import path
from . import views

app_name = "feeds"

urlpatterns = [
    path("", views.FeedList.as_view(), name="feed-list"),
]
