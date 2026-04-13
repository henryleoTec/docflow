# documents/urls.py

from django.urls import path
from .views import (
    DocumentListView,
    DocumentDetailView,
    DocumentCreateView,
    DocumentDeleteView,
    convert_view,
    conversion_status,
    dashboard_view,
)

urlpatterns = [
    path("", DocumentListView.as_view(), name="document-list"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("<int:pk>/", DocumentDetailView.as_view(), name="document-detail"),
    path("upload/", DocumentCreateView.as_view(), name="document-create"),
    path("<int:pk>/delete/", DocumentDeleteView.as_view(), name="document-delete"),
    path("<int:pk>/convert/", convert_view, name="document-convert"),
    path("<int:pk>/status/", conversion_status, name="document-status"),
]
