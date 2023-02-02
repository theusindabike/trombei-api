from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static

BASE_PATH = "trombei_api"

schema_view = get_schema_view(
    openapi.Info(
        title="Trombei API",
        default_version="v1",
        description="Trombei project API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mlopes.matheus@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.IsAdminUser],
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("admin/", admin.site.urls),
    re_path(r"api/(?P<version>[v1|v2]+)/oauth/", include(f"{BASE_PATH}.oauth.urls")),
    re_path(r"api/(?P<version>[v1|v2]+)/users/", include(f"{BASE_PATH}.core.urls")),
    re_path(r"api/(?P<version>[v1|v2]+)/events/", include(f"{BASE_PATH}.events.urls")),
    re_path(
        r"api/(?P<version>[v1|v2]+)/places/",
        include(f"{BASE_PATH}.places.urls"),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
