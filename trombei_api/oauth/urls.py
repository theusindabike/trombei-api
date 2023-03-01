from django.urls import path
from . import views

app_name = "oauth"

urlpatterns = [
    path("google/", views.GoogleLoginView.as_view(), name="oauth-google"),
    path("google/code/", views.CodeView, name="oauth-google-code"),
]
