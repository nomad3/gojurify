from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import DocumentTemplateSerializer
from documents.models import DocumentTemplate

class DocumentTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentTemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DocumentTemplate.objects.filter(owners=self.request.user)
