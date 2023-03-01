from django.urls import path
from . import views

app_name = "oauth"

urlpatterns = [
    path("token/", views.GoogleLoginView.as_view(), name="oauth-google"),
    path("code/", views.CodeView, name="code"),
]
