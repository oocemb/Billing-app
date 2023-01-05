from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/", include(("api.urls", "api"), namespace="api")),
        path("", include(("front_end.urls", "front_end"), namespace="front_end")),
        path("", include("social_django.urls", namespace="social")),
        path("accounts/", include("django.contrib.auth.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
