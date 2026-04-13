# documents/api_urls.py  (create this file)

from rest_framework.routers import DefaultRouter
from .api_views import DocumentViewSet

router = DefaultRouter()
router.register("documents", DocumentViewSet, basename="api-document")
# register() tells the router:
# - "documents" → use this as the URL prefix
# - DocumentViewSet → this viewset handles all the actions
# - basename="api-document" → used to name the URL patterns
#   e.g. "api-document-list", "api-document-detail"

urlpatterns = router.urls
# router.urls expands to all the URL patterns automatically:
# GET    /api/documents/          → list
# POST   /api/documents/          → create
# GET    /api/documents/{pk}/     → retrieve
# PUT    /api/documents/{pk}/     → update
# DELETE /api/documents/{pk}/     → destroy
# POST   /api/documents/{pk}/convert/ → custom convert action
# GET    /api/documents/stats/    → custom stats action
