# documents/api_views.py  (create this new file)

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Document
from .serializers import DocumentSerializer
from .utils import convert_document


class DocumentViewSet(viewsets.ModelViewSet):
    # ModelViewSet automatically provides these actions:
    # list()    → GET  /api/documents/
    # create()  → POST /api/documents/
    # retrieve()→ GET  /api/documents/3/
    # update()  → PUT  /api/documents/3/
    # destroy() → DELETE /api/documents/3/

    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes overrides the global default for this viewset
    # Every action in this viewset requires authentication

    def get_queryset(self):
        # Only return documents belonging to the logged-in user
        # self.request.user is set by JWTAuthentication
        return Document.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Called when POST /api/documents/ succeeds validation
        # serializer.save() writes to the database
        # We pass owner=request.user so it's set automatically
        serializer.save(owner=self.request.user)

        # Check file limit — SaaS business logic
        # Count how many documents this user already has
        user_doc_count = Document.objects.filter(
            owner=self.request.user
        ).count()

        if user_doc_count > 5:
            # Delete the file we just saved and raise an error
            serializer.instance.delete()
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "Free tier limit reached. You can only upload 5 documents."
            )
            # PermissionDenied returns HTTP 403 Forbidden automatically

    @action(detail=True, methods=["post"])
    # @action creates a CUSTOM endpoint on the viewset
    # detail=True means it works on a single object: /api/documents/3/convert/
    # detail=False would mean it works on the list: /api/documents/convert/
    # methods=["post"] means only POST requests are allowed here
    def convert(self, request, pk=None):
        # This creates: POST /api/documents/3/convert/
        document = self.get_object()
        # get_object() fetches the document by pk AND checks permissions
        # It uses get_queryset() so users can only access their own docs

        if document.converted:
            return Response(
                {"detail": "Already converted."},
                status=status.HTTP_400_BAD_REQUEST
                # status codes are constants in DRF — much cleaner than
                # writing the raw number 400 everywhere
            )

        success, message = convert_document(document)

        if success:
            serializer = self.get_serializer(document)
            # Serialize the updated document to return in the response
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": message},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["get"])
    def stats(self, request):
        # GET /api/documents/stats/
        # detail=False means it's not tied to a specific document
        queryset = self.get_queryset()
        total = queryset.count()
        converted = queryset.filter(converted=True).count()
        pending = total - converted

        return Response({
            "total_documents": total,
            "converted": converted,
            "pending": pending,
            "limit": 5,
            "remaining_uploads": max(0, 5 - total),
        })
