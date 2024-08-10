from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from server.views import ServerListViewSet
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

router = DefaultRouter()
router.register("api/server/select", ServerListViewSet, basename="server-list")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view()),
    path("", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.DEBUG, document_root=settings.MEDIA_ROOT)
