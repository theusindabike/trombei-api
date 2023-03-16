from django.urls import path
from . import views

app_name = "feeds"

urlpatterns = [
    path("", views.FeedList.as_view(), name="feed-list"),
    path("past/", views.PastFeedList.as_view(), name="past-feed-list"),
    path("<uuid:pk>/", views.FeedRetrieve.as_view(), name="feed-detail"),
]
