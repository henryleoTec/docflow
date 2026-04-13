"""
URL configuration for docflow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# docflow/urls.py

# docflow/urls.py  (full updated file)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("documents/", include("documents.urls")),

    # API routes
    path("api/", include("documents.api_urls")),
    # All ViewSet routes live under /api/

    # JWT token endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # POST here with username+password → get access + refresh tokens back

    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # POST here with refresh token → get a new access token back

    # API documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Returns the raw OpenAPI JSON schema

    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # Renders the interactive Swagger UI at /api/docs/

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
